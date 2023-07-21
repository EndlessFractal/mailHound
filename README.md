# mailHound

This tool is designed to analyze the headers and content of email files and provide valuable information. It can extract sender and recipient information, important header details, URLs, and attachments from an email file in `.eml` or `.msg` format.

## Installation

To use the mailHound, follow these steps:

1. Clone the repository using the following command:

```bash
git clone https://github.com/your-username/email-header-analysis.git
```

2. Navigate to the cloned directory:

```bash
cd mailHound
```

## Usage

To analyze an email file, simply run the `mailHound.py` script with the path to the email file as an argument:

```bash
python mailHound.py path/to/email_file.eml
```

Replace `path/to/email_file.eml` with the actual path to your email file.

### Supported Formats

The tool supports two email file formats: `.eml` and `.msg`. If your email file has a different extension or is in another format, the tool will raise an error.

### Analysis Report

After running the script, the tool will generate a detailed analysis report for the provided email file. The report will include the following information:

- Sender Name and Email
- Recipients (TO, CC, BCC)
- Reply-To
- Subject
- Date
- Message-ID
- Received
- Authentication Results
- URLs found in the email content
- Attachments & Files and their respective sizes

Note: If the email file does not contain any URLs or attachments, the report will indicate this accordingly.

### Example

```bash

                 _ _ _   _                       _
                (_) | | | |                     | |
 _ __ ___   __ _ _| | |_| | ___  _   _ _ __   __| |
| '_ ` _ \ / _` | | |  _  |/ _ \| | | | '_ \ / _` |
| | | | | | (_| | | | | | | (_) | |_| | | | | (_| |
|_| |_| |_|\__,_|_|_\_| |_/\___/ \__,_|_| |_|\__,_|

by Endless Fractal

Sender Name: Group Marketing Online Accounts Payable
Sender Email: Accounts.Payable@groupmarketingonline.icu
Subject: Group Marketing Online Direct Credit Advice - michael.ascot@swiftspend.finance
Date: Sun, 28 Jun 2020 17:01:33 -0500
Received: from SG2PR01MB4517.apcprd01.prod.exchangelabs.com(YYYY:YYYY:YYYY:YYYY:YYYY:YYYY) by SG2PR01MB3173.apcprd01.prod.exchangelabs.com withHTTPS; Sun, 28 Jun 2020 22:01:56 +0000
TO:
  - Michael Ascot <michael.ascot@swiftspend.finance>
Authentication Results:
  - spf=pass (sender IP is X.X.X.X)smtp.mailfrom=BRAEMARHOWELLS.COM
  - dkim=none (message not signed)header.d=none
  - dmarc=none action=noneheader.from=groupmarketingonline.icu
  - compauth=softpass reason=202
# of URLs: 14
URLs:
  - https://www.facebook.com/GroupMarketingOnline
  - https://www.youtube.com/user/GroupMarketingOnline
  - https://www.linkedin.com/company/GroupMarketingOnline
  - https://twitter.com/GroupMarketingOnline
  - https://www.instagram.com/GroupMarketingOnline/
  - https://pinterest.com/GroupMarketingOnline/
  - http://schemas.microsoft.com/office/2004/12/omml
  - http://www.w3.org/TR/REC-html40
  - https://www.facebook.com/GroupMarketingOnline
  - https://www.youtube.com/user/GroupMarketingOnline
  - https://www.linkedin.com/company/GroupMarketingOnline
  - https://twitter.com/GroupMarketingOnline
  - https://www.instagram.com/GroupMarketingOnline/
  - https://pinterest.com/GroupMarketingOnline/
# of Attachments & Files: 9
Attachments & Files:
  - Name: image001.png, Size: 25.88 KB
  - Name: image003.png, Size: 794 B
  - Name: image004.png, Size: 984 B
  - Name: image005.png, Size: 921 B
  - Name: image006.png, Size: 756 B
  - Name: image007.png, Size: 819 B
  - Name: image008.png, Size: 776 B
  - Name: image009.png, Size: 21.19 KB
  - Name: Direct Credit Advice.html, Size: 515 B
```

## Contributing

If you find any issues with this tool or have suggestions for improvements, feel free to open an issue or submit a pull request on!
