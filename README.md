Below is a refined and categorized GitHub README in English, incorporating your request for a project status announcement.

---

# Datalix Server Status Monitor

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Project Status](#project-status)
- [Contributing](#contributing)

## Overview

This Python script is designed for monitoring the status of servers managed by Datalix. It conducts periodic checks on server health, including DDoS attack logs, service status, and other critical metrics, and reports these statuses via Discord notifications. The script leverages the Datalix backend API for data retrieval and Discord webhooks for alert dispatching.

## Features

- **Service Status Monitoring**: Checks and alerts for any changes in the operational status of servers.
- **DDoS Attack Detection**: Monitors for DDoS attacks and provides detailed incident reports.
- **Dynamic Delay Management**: Adjusts request intervals to comply with rate limits.
- **Logging**: Maintains detailed logs of requests and responses for debugging and auditing.
- **Customizable Notifications**: Sends tailored Discord notifications containing server status and DDoS attack details.

## Requirements

- Python 3.x
- The `requests` library for API requests
- The `json` library for parsing and handling JSON data

## Setup

1. **Install Dependencies**: Ensure Python 3.x is installed on your system. Then, use pip to install the required Python packages:

   ```bash
   pip3 install requests json datetime random
   ```

2. **Configuration**: Modify the `data` list within the script to include your server details, such as server name, API token, service ID, and Discord webhook URLs for status changes and DDoS logs.

## Usage

Execute the script with Python:

```bash
python3 main.py
```

## How It Works

The script iterates over each server defined in the `data` list, making API calls to the Datalix backend to fetch the current status and DDoS logs. Based on the responses, it processes the information, updates the last known status, and determines if there are any new DDoS attacks. Detected status changes or new attacks trigger Discord notifications. All requests and responses are logged.

## Customization

- **Request Interval**: Modify the `rqDelay` variable to change the delay between API requests, accommodating different rate limit requirements.
- **Notification Colors**: Adjust the `colors` dictionary to alter the color scheme of Discord notifications.
- **User Agents**: Update the `user_agents_list` to use different User-Agent headers in requests.

## Troubleshooting

Ensure your API tokens and service IDs are correctly configured, check the Discord webhook URLs for accuracy and permissions, and review the `debug.log` file for error messages and request/response details.

## Project Status

This project is no longer maintained by me and represents the last update. The community is warmly invited to take over the project and further develop it. Forks can be created, and Pull Requests submitted for those interested.

## Contributing

Contributions to improve the project are always welcome, even though it is not actively maintained by the original author. Feel free to fork the project and submit your contributions through Pull Requests.
