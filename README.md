# Server Status Monitoring Script


This script enables continuous monitoring of your remote server's status through the Datalix API. In case of status changes, instant notifications are sent via a Discord webhook, ensuring you're always kept informed.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [Customization](#customization)
- [Example Notification](#example-notification)
- [Why This Script?](#why-this-script)
- [How It Works](#how-it-works)
- [Example Use Case](#example-use-case)
- [Error Handling](#error-handling)
- [Notes](#notes)
- [License](#license)

## Prerequisites

- **Python 3.x**
- Required Python libraries: `json`, `requests`, `discord`, `asyncio`
- Product hosted at https://datalix.de/a/asylceo/

## Setup

1. Clone or download this repository.
2. Install the required libraries using the command:
   ```bash
   pip3 install discord requests
   ```
3. Open the script (`main.py`) in a text editor like Visual Studio Code (VSC).
4. Customize the configuration variables by replacing the following placeholders:
   - `webhook_url`: Your Discord webhook URL.
   - `service_id`: Your Datalix service ID, also replace it in line 96.
   - `api_token`: Your Datalix API token, also replace it in line 96.
   - Customize `status_descriptions` to tailor status descriptions.

## Configuration

Within the script, you'll find various configuration options:

- `webhook_url`: The Discord webhook URL for sending notifications.
- `service_id`: Your Datalix service ID.
- `api_token`: Your Datalix API token.
- `base_url`: The base URL for the Datalix API.
- `status_descriptions`: A list containing status descriptions for different server statuses.

## Usage

Here's the updated usage guide with the usage of the `screen` service for Linux:

## Usage

1. Open a terminal or command prompt on your Linux server.
2. Navigate to the directory containing the script.
3. Start a `screen` session to run the script in the background:
   ```bash
   screen -S monitoring
   ```
4. Execute the script using the following command:
   ```bash
   python3 main.py
   ```
5. The script will start monitoring the server status continuously and send notifications through the Discord webhook on changes.
6. Press `Ctrl + A` and then `D` to detach from the `screen` session and leave the script running in the background.

To later return to view the status of the script or to stop it, use the following command:

```bash
screen -r monitoring
```

If you want to stop the script while within the `screen` session, press `Ctrl + C` to terminate the script and then `Ctrl + D` to exit the `screen` session.

Using `screen` allows you to run the script in the background and later reattach to the `screen` session to view the status or stop the script without keeping an active terminal session open.

## Features

The script includes the following functions:

- `get_server_status`: Retrieves the server status from the Datalix API.
- `get_server_ip`: Retrieves the server IP address from the Datalix API.
- `send_discord_embed`: Sends a Discord webhook with status information.
- `main`: The main asynchronous function that performs monitoring.

## Customization

You can customize the script to fit your needs, such as adjusting the frequency of checks or displaying additional information in the notifications.

Feel free to create a pull request if you encounter any issues.

## Example Notification

![Example Notification](https://cdn.discordapp.com/attachments/1139948214120886292/1140386807809331200/VXxeBu6UzgqO.png)

## Why This Script?

Monitoring server status is crucial to ensuring smooth server operations. By using this script, you can react to issues early on. Notifications allow you to promptly address potential problems and maintain server availability.

## How It Works

The script utilizes the Datalix API to check your server's status. It regularly fetches the current status and IP address, comparing them to the previous status. On changes, a Discord webhook message with relevant information is sent. Information includes the IP address, timestamp, status, and any error messages if applicable.

## Example Use Case

Here's an example of how you could use the script:

1. Start the script on a server or a device that runs continuously.
2. Customize the configuration variables to input your API credentials and Discord webhook URL.
3. Execute the script.
4. Monitor the Discord channel where notifications are sent. You'll receive notifications on status changes.

## Error Handling

The script incorporates error-handling mechanisms. If the Datalix API is unreachable or a request fails, it will be logged. Regularly check the console output to ensure everything is functioning correctly.

## Notes

- Ensure that you keep your Datalix API token and Discord webhook URL secure and private.
- This script is provided "as is" and can be adapted based on your specific use case.

*coded with ❤️ by AsylantenCeo*
```
