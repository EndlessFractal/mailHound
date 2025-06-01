import argparse
from email import message_from_binary_file, policy, utils
from email.errors import MessageError
from email.message import Message
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple, Union

# Improved URL regex pattern.
URL_REGEX = (
    r"https?://(?:[a-zA-Z0-9]|[$-_@.&+]|[!*\\(\\),]|"
    r"(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)

# Extract URLs from text parts (HTML/plain) using regex.
def extract_urls_from_part(part: Message) -> List[str]:
    if part.get_content_type() in ("text/html", "text/plain"):
        try:
            content = part.get_content()
        except Exception as e:
            print(f"Failed to get content from part: {e}")
            return []
        if isinstance(content, str):
            return re.findall(URL_REGEX, content)
    return []

# Get recipient strings from header.
def extract_recipients(header_value: Optional[str]) -> List[str]:
    if not header_value:
        return []
    addresses = utils.getaddresses([header_value])
    return [f"{name or email} <{email}>" for name, email in addresses if email and email.lower() != "none"]

# Get first sender address from header.
def extract_first_address(header_value: Optional[str]) -> Tuple[str, str]:
    if not header_value:
        return ("Unknown", "Unknown")
    addresses = utils.getaddresses([header_value])
    return addresses[0] if addresses else ("Unknown", "Unknown")

# Decode attachment; return its name and size.
def decode_attachment(part: Message) -> Optional[Dict[str, Union[str, int]]]:
    content_disposition = part.get_content_disposition()
    content_id = part.get("Content-ID")

    attachment_name = None
    if content_id:
        # Use Content-ID (without angle brackets) as name.
        attachment_name = content_id.strip("<>").split("@")[0]
    elif content_disposition and "attachment" in content_disposition.lower():
        attachment_name = part.get_filename()

    if not attachment_name:
        return None

    try:
        payload = part.get_payload(decode=True)
        attachment_size = len(payload) if payload is not None else 0
    except Exception as e:
        print(f"Failed to decode attachment: {e}")
        attachment_size = 0

    return {"Name": attachment_name, "Size": attachment_size}

# Parse Received headers for server info.
def extract_server_info(received_headers: List[str]) -> Dict[str, Any]:
    servers = []
    pattern = re.compile(r"from\s+(.*?)\s+.*?by\s+(.*?)\s+.*?;\s+(.*)", re.IGNORECASE)
    for header in received_headers:
        match = pattern.search(header)
        if match:
            servers.append({
                "From": match.group(1).strip(),
                "By": match.group(2).strip(),
                "Timestamp": match.group(3).strip(),
            })
    servers.reverse()  # Reverse order to match sending order.
    first_server = servers[0] if servers else None
    final_server = servers[-1] if len(servers) > 1 else None
    intermediate_servers = servers[1:-1] if len(servers) > 2 else []

    return {
        "First Server": first_server,
        "Intermediate Servers": intermediate_servers,
        "Final Server": final_server,
    }

# Combine Authentication-Results headers.
def parse_authentication_results(headers: List[str]) -> List[str]:
    if headers:
        combined = "; ".join(headers)
        return [part.strip() for part in combined.split(";") if part.strip()]
    return ["N/A"]

# Analyze the email file; extract headers, URLs, and attachments.
def analyze_email_headers(file_path: str, email_policy: Any) -> Optional[Dict[str, Any]]:
    try:
        with open(file_path, "rb") as file:
            email_message = message_from_binary_file(file, policy=email_policy)
    except MessageError as e:
        print(f"Failed to parse email: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error reading file '{file_path}': {e}")
        return None

    # Get sender info.
    from_header = email_message.get("From")
    sender_name, sender_email = extract_first_address(from_header)
    if sender_name == "Unknown" and sender_email == "Unknown":
        print("Warning: Missing 'From' header in email.")

    # Get recipients (To, Cc, Bcc).
    recipients = {
        "TO": extract_recipients(email_message.get("To")),
        "CC": extract_recipients(email_message.get("Cc")),
        "BCC": extract_recipients(email_message.get("Bcc")),
    }

    # Get basic headers.
    header_data = {header: email_message.get(header, "N/A") for header in ["Reply-To", "Subject", "Date", "Message-ID"]}

    # Parse Authentication-Results.
    auth_headers = email_message.get_all("Authentication-Results", [])
    authentication_results_split = parse_authentication_results(auth_headers)

    # Get server info.
    server_info = extract_server_info(email_message.get_all("Received", []))

    # Collect URLs and attachments.
    urls: List[str] = []
    attachments: List[Dict[str, Union[str, int]]] = []
    for part in email_message.walk():
        urls.extend(extract_urls_from_part(part))
        attachment = decode_attachment(part)
        if attachment:
            attachments.append(attachment)
    # Remove duplicate URLs while preserving order.
    urls = list(dict.fromkeys(urls))

    return {
        "Sender Name": sender_name,
        "Sender Email": sender_email,
        **header_data,
        **recipients,
        "Authentication Results": authentication_results_split,
        "Server Information": server_info,
        "URLs": urls,
        "# of Attachments & Files": len(attachments),
        "Attachments & Files": attachments,
    }

# Format byte size into a human-readable string.
def format_size(size_in_bytes: Union[int, float]) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size_in_bytes < 1024:
            if size_in_bytes == int(size_in_bytes):
                return f"{size_in_bytes:.0f} {unit}"
            else:
                return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"

# Create a plain-text report from the analysis results.
def generate_report(results: Dict[str, Any]) -> str:
    lines = []
    lines.append("Email Analysis Report")
    lines.append("=" * 50)
    lines.append(f"Sender: {results.get('Sender Name', 'N/A')} <{results.get('Sender Email', 'N/A')}>")
    lines.append(f"Subject: {results.get('Subject', 'N/A')}")
    lines.append(f"Date: {results.get('Date', 'N/A')}")
    lines.append(f"Message-ID: {results.get('Message-ID', 'N/A')}")
    if results.get("Reply-To") not in (None, "N/A"):
        lines.append(f"Reply-To: {results.get('Reply-To')}")
    lines.append("")

    # Recipients.
    lines.append("Recipients:")
    for key in ("TO", "CC", "BCC"):
        recipients_list = results.get(key, [])
        if recipients_list:
            lines.append(f"  {key}:")
            for recipient in recipients_list:
                lines.append(f"    - {recipient}")
        else:
            lines.append(f"  {key}: N/A")
    lines.append("")

    # Authentication Results.
    lines.append("Authentication Results:")
    for result in results.get("Authentication Results", []):
        lines.append(f"  - {result}")
    lines.append("")

    # Server Information.
    server_info = results.get("Server Information", {})
    if server_info:
        lines.append("Server Information:")
        if server_info.get("First Server"):
            fs = server_info.get("First Server")
            lines.append(f"  First Server: From: {fs.get('From')}, By: {fs.get('By')}, Timestamp: {fs.get('Timestamp')}")
        if server_info.get("Intermediate Servers"):
            lines.append("  Intermediate Servers:")
            for idx, server in enumerate(server_info.get("Intermediate Servers", []), start=1):
                lines.append(f"    {idx}. From: {server.get('From')}, By: {server.get('By')}, Timestamp: {server.get('Timestamp')}")
        if server_info.get("Final Server"):
            fs = server_info.get("Final Server")
            lines.append(f"  Final Server: From: {fs.get('From')}, By: {fs.get('By')}, Timestamp: {fs.get('Timestamp')}")
    lines.append("")

    # URLs.
    urls = results.get("URLs", [])
    lines.append("URLs:")
    if urls:
        for url in urls:
            lines.append(f"  - {url}")
    else:
        lines.append("  None")
    lines.append("")

    # Attachments.
    attachments = results.get("Attachments & Files", [])
    lines.append(f"Attachments & Files ({results.get('# of Attachments & Files', 0)}):")
    if attachments:
        for attachment in attachments:
            size_str = format_size(attachment.get("Size", 0))
            lines.append(f"  - Name: {attachment.get('Name')}, Size: {size_str}")
    else:
        lines.append("  None")

    return "\n".join(lines)

# Main entry point; parses args and outputs analysis.
def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze email headers")
    parser.add_argument("file_path", type=str, help="Path to the email file")
    parser.add_argument("--json", action="store_true", help="Output the results as JSON")
    args = parser.parse_args()

    file_path = args.file_path
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Only .eml files supported.
    if file_path.lower().endswith(".eml"):
        email_policy = policy.default
    else:
        print("Error: Unsupported email file format. Only .eml files are supported.")
        return

    results = analyze_email_headers(file_path, email_policy)
    if results is None:
        print("Error: Failed to analyze email.")
        return

    if args.json:
        print(json.dumps(results, indent=4))
    else:
        report = generate_report(results)
        print(report)

if __name__ == "__main__":
    main()
