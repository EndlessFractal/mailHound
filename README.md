# mailHound 🐾

**Enhanced Email Header & Content Analyzer**

mailHound extracts valuable information from email files, providing insights into sender/receiver details, server paths, URLs, attachments, and security headers. Ideal for security analysis, phishing investigations, and email forensics.

## Features ✨

- **Comprehensive Email Analysis**:
  - Sender/Recipient identification
  - Server path tracing (first/intermediate/final servers)
  - Authentication results (SPF, DKIM, DMARC)
  - URL extraction with deduplication
  - Attachment analysis with accurate size reporting
- **Multiple Output Formats**:
  - Human-readable text reports
  - JSON output for programmatic use (`--json` flag)
- **Enhanced Security**:
  - Resilient error handling
  - Malformed email recovery
  - Safe header parsing

## Installation 📦

```bash
git clone https://github.com/EndlessFractal/mailHound.git
cd mailHound
```

## Usage 🚀

### Basic Analysis
```bash
python mailHound.py path/to/email_file.eml
```

### JSON Output
```bash
python mailHound.py path/to/email_file.eml --json
```

### Supported Formats
- `.eml` files only (RFC 822 compliant)

## Sample Report 📄
```text
Email Analysis Report
==================================================
Sender: Group Marketing <accounts@example.com>
Subject: Payment Advice - michael@swiftspend.finance
Date: Sun, 28 Jun 2020 17:01:33 -0500
Message-ID: <12345@example.com>
Reply-To: noreply@example.com

Recipients:
  TO:
    - Michael Ascot <michael.ascot@swiftspend.finance>
  CC: N/A
  BCC: N/A

Authentication Results:
  - spf=pass (sender IP is X.X.X.X)
  - dkim=none (message not signed)
  - dmarc=none action=none

Server Information:
  First Server: From: mail.example.com, By: server1.example.com, Timestamp: Sun, 28 Jun 2020 17:01:22 -0500
  Intermediate Servers:
    1. From: server1.example.com, By: server2.example.com, Timestamp: Sun, 28 Jun 2020 17:01:25 -0500
  Final Server: From: server2.example.com, By: mx.destination.com, Timestamp: Sun, 28 Jun 2020 17:01:33 -0500

URLs:
  - https://www.facebook.com/GroupMarketing
  - https://twitter.com/GroupMarketing

Attachments & Files (3):
  - Name: payment_advice.pdf, Size: 256 KB
  - Name: logo.png, Size: 24.8 KB
  - Name: details.html, Size: 1.2 KB
```

## Contributing 🤝
Found an issue or have an enhancement idea?
- Open an issue for bug reports or feature requests
- Submit pull requests for improvements
