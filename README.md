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
- `.eml` files only

## Sample Report 📄
```text
Email Analysis Report
==================================================
Sender: Ripple <xrpl@isarops.com>
Subject: Good news and rewards for the XRP Community
Date: Thu, 27 Jul 2023 08:23:11 +0000
Message-ID: <20230727082311.9d0b426cad4b843b@isarops.com>

Recipients:
  TO:
    - phishing@pot <phishing@pot>
  CC: N/A
  BCC: N/A

Authentication Results:
  - spf=pass (sender IP is 198.61.254.42) smtp.mailfrom=isarops.com
  - dkim=pass (signature was verified) header.d=isarops.com
  - dmarc=pass action=none header.from=isarops.com
  - compauth=pass reason=100

Server Information:
  First Server: From: <unknown>, By: 58e756f13322, Timestamp: Thu, 27 Jul 2023 08:23:11 GMT
  Intermediate Servers:
    1. From: so254-42.mailgun.net, By: BN1NAM02FT029.mail.protection.outlook.com, Timestamp: Thu, 27 Jul 2023 08:23:11 +0000
    2. From: BN1NAM02FT029.eop-nam02.prod.protection.outlook.com, By: BN9PR03CA0370.outlook.office365.com, Timestamp: Thu, 27 Jul 2023 08:23:11 +0000
    3. From: BN9PR03CA0370.namprd03.prod.outlook.com, By: LV3PR19MB8443.namprd19.prod.outlook.com, Timestamp: Thu, 27 Jul 2023 08:23:11 +0000
  Final Server: From: LV3PR19MB8443.namprd19.prod.outlook.com, By: MN0PR19MB6312.namprd19.prod.outlook.com, Timestamp: Thu, 27 Jul 2023 08:23:12 +0000

URLs:
  - http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd
  - http://www.w3.org/1999/xhtml
  - https://i.imgur.com/T2B3JTm.png
  - https://mail122-ripple.net/726f647269676f2d662d7040686f746d61696c2e636f6d?c_id=r25j-9d981df1-f2da-41f0-99da-41da09f42b72
  - https://mail122-ripple.net/726f647269676f2d662d7040686f746d61696c2e636f6d.gif?c_id=r25j-9d981df1-f2da-41f0-99da-41da09f42b72

Attachments & Files (0):
  None
```

## Contributing 🤝
Found an issue or have an enhancement idea?
- Open an issue for bug reports or feature requests
- Submit pull requests for improvements
