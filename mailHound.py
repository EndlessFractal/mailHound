import argparse
import re
from email import message_from_binary_file, policy, utils


def extract_urls_from_part(part):
    """Extracts URLs from a text/html or text/plain email part."""
    content_type = part.get_content_type()
    if content_type in ("text/html", "text/plain"):
        content = part.get_content()
        return re.findall(r"(?P<url>https?://[^\s\">\]\']+)", content)
    return []


def extract_recipients(header_value):
    """Extracts recipients' names and email addresses from the email header."""
    recipients = []
    if header_value:
        recipient_list = header_value.split(",")
        for recipient in recipient_list:
            recipient_name, recipient_email = utils.getaddresses([recipient.strip()])[0]
            # Decode non-ASCII names in the recipient field
            recipient_name = recipient_name.encode('latin-1').decode('utf-8')
            recipients.append(f"{recipient_name} <{recipient_email}>")
    return recipients


def decode_attachment(part):
    """Extracts information about an attachment from an email part."""
    content_disposition = part.get_content_disposition()
    content_id = part.get("Content-ID")

    if content_id:
        attachment_name = content_id.strip("<>").split("@")[0]
    elif content_disposition and "attachment" in content_disposition.lower():
        attachment_name = part.get_filename()
    else:
        return None

    return {"Name": attachment_name, "Size": len(part.get_content())}


def analyze_email_headers(file_path, email_policy):
    """Analyzes the email headers and content from the specified file."""
    with open(file_path, "rb") as file:
        email_message = message_from_binary_file(file, policy=email_policy)

    # Extract sender's name and email address
    sender_name, sender_email = utils.getaddresses([email_message["From"]])[0]

    # Extract recipients
    recipients = {
        "TO": extract_recipients(email_message["To"]),
        "CC": extract_recipients(email_message["Cc"]),
        "BCC": extract_recipients(email_message["Bcc"]),
    }

    # Extract other headers
    headers = ["Reply-To", "Subject", "Date", "Message-ID", "Received"]
    header_data = {header: email_message.get(header, None) for header in headers}

    # Extract authentication results
    authentication_results = email_message.get_all("Authentication-Results", [])

    # Extract URLs and attachments from the email content
    urls = []
    attachments = []
    for part in email_message.walk():
        urls += extract_urls_from_part(part)
        attachment = decode_attachment(part)
        if attachment:
            attachments.append(attachment)

    # Prepare results dictionary
    results = {
        "Sender Name": sender_name,
        "Sender Email": sender_email,
        **header_data,
        **recipients,
        "Authentication Results": authentication_results,
        "# of URLs": len(urls),
        "URLs": urls,
        "# of Attachments & Files": len(attachments),
        "Attachments & Files": attachments,
    }

    return results


def format_size(size_in_bytes):
    """Formats the size in bytes to a human-readable format (e.g., KB, MB)."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.0f} {unit}" if size_in_bytes == int(size_in_bytes) else f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024


def generate_report(results):
    """Generates a report based on the analysis results."""
    report = """
                 _ _ _   _                       _
                (_) | | | |                     | |
 _ __ ___   __ _ _| | |_| | ___  _   _ _ __   __| |
| '_ ` _ \ / _` | | |  _  |/ _ \| | | | '_ \ / _` |
| | | | | | (_| | | | | | | (_) | |_| | | | | (_| |
|_| |_| |_|\__,_|_|_\_| |_/\___/ \__,_|_| |_|\__,_|

by Endless Fractal\n\n"""
    if results:
        for key, value in results.items():
            if value:  # Check if the value is not empty
                if isinstance(value, list):
                    report += f"{key}:\n"
                    for item in value:
                        if isinstance(item, dict):
                            name = item.get('Name', 'N/A')
                            size = item.get('Size', 'N/A')
                            size_formatted = format_size(size)
                            report += f"  - Name: {name}, Size: {size_formatted}\n"
                        else:
                            report += f"  - {item}\n"
                else:
                    report += f"{key}: {value}\n"
    else:
        report += "No warnings found in the email headers."

    return report


def main():
    """Main entry point for the email header analysis script."""
    parser = argparse.ArgumentParser(description="Analyze email headers")
    parser.add_argument("file_path", type=str, help="Path to the email file")
    args = parser.parse_args()

    file_path = args.file_path

    # Determine the policy based on the file extension
    if file_path.lower().endswith(".eml"):
        email_policy = policy.default
    elif file_path.lower().endswith(".msg"):
        email_policy = policy.SMTP
    else:
        print("Unsupported email file format.")
        return

    try:
        results = analyze_email_headers(file_path, email_policy)
        report = generate_report(results)
        print(report)
    except FileNotFoundError:
        print("Error: The specified email file was not found.")
    except Exception as e:
        print(f"An error occurred during email analysis: {str(e)}")


if __name__ == "__main__":
    main()
