# Server Status Monitor with Discord Notifications

This Python script allows you to monitor the status of a server and receive updates through Discord webhooks. It utilizes the AIOHTTP library for asynchronous HTTP requests, providing an easy way to keep track of important server information.

---

## Table of Contents

1. [**Overview**](#overview)
2. [**Installation**](#installation)
3. [**Configuration**](#configuration)
4. [**Usage**](#usage)
5. [**Customization**](#customization)
6. [**License**](#license)
7. [**Disclaimer**](#disclaimer)

---

## Overview

This script is designed to monitor server status and send notifications via Discord webhooks. It is particularly useful for administrators who need real-time information about their server.

## Installation

1. **Install Python and Pip**:

   Ensure that Python and Pip are installed on your system.

2. **Install Dependencies**:

   Open the command line and enter the following command:

   ```
   pip install aiohttp
   ```

## Configuration

- Open the `main.py` file.

- Replace the following placeholders with your own information:

  - `webhook`: The Discord webhook where notifications should be sent.
  - `service_id`, `callcenter`: Your specific service ID and callcenter ID (Datalix API Token).
  - Additional configurable variables and messages can be customized.

## Usage

Run the script, for example, with the command:

```
python main.py
```

The script will now start monitoring the server status and send notifications when changes are detected.

## Customization

You can customize the script to fit your specific requirements by editing the functions in the `main.py` file.

## License

This project is licensed under the MIT License. For more information about the MIT License, see [here](https://opensource.org/licenses/MIT).

## Disclaimer

Disclaimer and Legal Notices:

The use of this script is solely at the user's own risk and is strictly on an "as is" basis. Any liability of the author for direct or indirect damages, including but not limited to loss of profits, data loss, or business interruptions that may arise from the use of this script, is hereby rigorously excluded.

The script is provided to the user with no express or implied warranties of any kind. The author expressly disclaims any warranty, whether express or implied, including but not limited to merchantability or fitness for a particular purpose.

It is solely the responsibility of the user to ensure that the use of this script complies with all applicable laws and regulations. The author assumes no responsibility for any legal consequences that may arise from the use of this script, including potential violations of copyrights, privacy policies, or other legal provisions.

The author of this script accepts no liability for legal violations that may result from the use of this script.

The author reserves the right, at their discretion, to make changes to the script or terminate support, should it be deemed necessary for legal, technical, or other compelling reasons.

---

## Developer

- [AsylantenCeo](https://github.com/asylceo)

## Contributors

- FlorianGH Datalix Owner

## Thanks

Thanks to everyone who contributed to this project.
