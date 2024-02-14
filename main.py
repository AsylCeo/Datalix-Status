import datetime
import time
import requests
import json
from time import sleep
from datetime import datetime
import random

useIPv4AsName = True

data = [{
    "name": "KVM-01",
    "token": "YOUR API TOKEN",
    "service": "YOUR SERVICE ID",
    "webhook": "YOUR DISCORD WEBHOOK FÜR STAUTS CHANGES",
    "alerts": "YOUR DISCORD API FOR DDOS LOGS",
    "lastState": "",  # placeholder, will get filled by the script
    "ipv4": None,
}]

rqDelay = len(data) + 2 or 2  # default 2 sec per service 2 sec delay (ratelimit is 30rq/60sec)

colors = {
    "green": 0x00FF00,
    "yellow": 0xFFFF00,
    "orange": 0xFFAA00,
    "red": 0xFF0000,
    "gray": 0x696969,
    "blue": 0x0000FF,
    "lightblue": 0x00ffff,
    "violet": 0x6900FF,
}

api_state_desc = {
    "stopping": {"desc": "Stopping.", "color": colors["orange"]},
    "shutdown": {"desc": "Shutting down", "color": colors["yellow"]},
    "starting": {"desc": "Starting...", "color": colors["lightblue"]},
    "running": {"desc": "Online", "color": colors["green"]},
    "stopped": {"desc": "Offline", "color": colors["red"]},
    "installing": {"desc": "Service is installing", "color": colors["lightblue"]},
    "backupplanned": {"desc": "Backup planned", "color": colors["violet"]},
    "restorebackup": {"desc": "Backup is being imported. (Layer8)", "color": colors["violet"]},
    "createbackup": {"desc": "Creating Backup", "color": colors["violet"]},
    "restoreplanned": {"desc": "Has a restore planned.", "color": colors["violet"]},
    "preorder": {"desc": "Preorded", "color": colors["blue"]},
    "deletedService": {"desc": "Service got permanently deleted", "color": colors["red"]},
    "error": {"desc": "API responded with an 'error'", "color": colors["red"]},
    "unk": {"desc": "No data", "color": colors["gray"]},
}

# Sleeps for the specified number of milliseconds
def sleep_ms(ms):
    sleep(ms / 1000.0)


user_agents_list = [
    "Datalix Status",
]

# Funktion zum zufälligen Auswählen eines User Agents aus der Liste
def get_random_user_agent():
    return random.choice(user_agents_list)

# Funktion zum Senden von API-Anfragen mit einem zufälligen User-Agent
def send_request(url):
    userAgent = get_random_user_agent()  # Setze den zufälligen User-Agent für diese Anfrage
    headers = {'User-Agent': userAgent}
    response = requests.get(url, headers=headers)
    request_id(response, url)  # Hier wird die Funktion request_id mit der aktuellen response aufgerufen
    return response

def get_random_user_agent():
    return random.choice(user_agents_list)


def request_id(response, endpoint):
    request_id = response.headers.get('x-request-id', 'N/A')
    timestamp = datetime.utcnow().isoformat()

    separator = "#" * 60
    log_entry = (
        f"\n{separator}\n"
        f"Timestamp: {timestamp}\n"
        f"Endpoint: {endpoint}\n"
        f"x-request-id: {request_id}\n"
        f"HTTP Status Code: {response.status_code}\n"
        f"User Agent: {response.request.headers['User-Agent']}\n"
    )

    # Nur den Textformat der API-Antwort protokollieren, nicht das JSON-Format
    response_text = response.text.encode('utf-8').decode('utf-8')
    log_entry += f"Response (Text):\n{response_text}\n{separator}\n"

    with open('./debug.log', 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)





# Sends an embed message to a Discord webhook with specified details
def send_embed(title, details, index, color, webhook, request_id=None):
    out = {
        "author": {
            "name": "Datalix",
            "icon_url": "https://cdn.discordapp.com/emojis/1176196317781966920.gif?size=96&quality=lossless",
            "url": f"https://datalix.de/cp/service/{data[index]['service']}",
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/emojis/1176196317781966920.gif?size=96&quality=lossless",
        },
        "title": title or "Server Status Update",
        "url": f"https://datalix.de/cp/service/{data[index]['service']}",
        "color": color,
        "fields": details,
        "timestamp": datetime.utcnow().isoformat(),
    }

    headers = {"Content-type": "application/json"}

    payload = {
        "content": "",
        "username": "Datalix",
        "avatar_url": "https://cdn.discordapp.com/emojis/1176196317781966920.gif?size=96&quality=lossless",
        "embeds": [out],
    }

    response = requests.post(webhook, json=payload, headers=headers)

    print(f"Status update for {data[index]['name']} | DDoS or Status")

# Constructs the URL for making API requests based on the specified index and optional URL path

def sex_url(index, url=None):
    endpoint = f"https://backend.datalix.de/v1/service/{data[index]['service']}"
    if url:
        endpoint += f"/{url}?token={data[index]['token']}"
    else:
        endpoint += f"?token={data[index]['token']}"
    return endpoint


# Retrieves the IPv4 address for a service and updates the corresponding data entry
def le_get_ip(index):
    userAgent = get_random_user_agent()  # Setze den zufälligen User-Agent für diese Anfrage
    headers = {'User-Agent': userAgent}

    response = requests.get(sex_url(index, "ip"), headers=headers)
    request_id(response, sex_url(index, "ip"))
    response_data = response.json()

    if not response_data or response.status_code != 200 or (not response_data["ipv4"][0] or not response_data["ipv4"][0]["ip"]):
        if data[index]["ipv4"] is None:
            data[index]["ipv4"] = "Error getting IPv4."
        data[index]["name"] = "Error getting IPv4."
        return

    data[index]["ipv4"] = response_data["ipv4"][0]["ip"]
    data[index]["name"] = data[index]["ipv4"]


most_occuring_method = {}
most_occuring_method_sent = False

# Processes DDoS logs for a specified service index and sends a Discord embed if there's a new DDoS attack
def ddos_logs(index):
    global last_sent_creation_time

    userAgent = get_random_user_agent()  # Setze den zufälligen User-Agent für diese Anfrage
    headers = {'User-Agent': userAgent}

    response = requests.get(sex_url(index, "incidents"), headers=headers)
    request_id(response, sex_url(index, "incidents"))
    response_data = response.json()
    
    try:
        if response.status_code == 429:
            print(f"Ratelimited, new delay: {rqDelay} | {response.text}")
            return
        if response.status_code == 403:
            if "Ihre Dienstleistung wurde unwiederruflich" not in json.dumps(response.text):
                print(f"Forbidden: {response.status_code} | {response.text}")
                return
        if response.status_code != 200:
            print(f"HTTP error: {response.status_code}")
            print(response.text)
            return response.status_code
        if not response_data:
            print("No data returned")
            return

        if response_data and response_data["data"] and len(response_data["data"]) > 0:
            latest_creation_time = response_data["data"][0]["created_on"]
            global most_occuring_method_sent  
            if last_sent_creation_time != latest_creation_time:
                embed_details = [
                    f"**IP Address:** {response_data['data'][0]['ip']}",
                    f"**Mbps:** {response_data['data'][0]['mbps']}",
                    f"**PPS:** {response_data['data'][0]['pps']}",
                    f"**Mode:** {response_data['data'][0]['mode']}",
                    f"**Attack Method:** {response_data['data'][0]['method']}",
                    f"**Most Occurring Attack Method:** {find_most_occuring_method(response_data['data'])}",
                    f"**Total Attacks:** {len(response_data['data'])}",
                    f"**Created On:** {latest_creation_time}",
                ]

                
                latest_attack_method = response_data["data"][0]["method"]
                if latest_attack_method not in most_occuring_method:
                    most_occuring_method[latest_attack_method] = 1
                else:
                    most_occuring_method[latest_attack_method] += 1

                send_embed("DDoS Attack alert", [{"name": f"Service: {data[index]['name']}", "value": "\n".join(embed_details)}], index, 0x00FF69, data[index]["alerts"])
                last_sent_creation_time = latest_creation_time
                most_occuring_method_sent = True
    except Exception as e:
        print(e)

last_sent_creation_time = ""

# Processes status logs for a specified service index and sends a Discord embed if there's a status update
def ddos_logs(index, headers):
    global last_sent_creation_time

    response = requests.get(sex_url(index, "incidents"), headers=headers)
    request_id(response, sex_url(index, "incidents"))
    response_data = response.json()
    try:
        if response.status_code == 429:
            print(f"Ratelimited, new delay: {rqDelay} | {response.text}")
            return
        if response.status_code == 403:
            if "Ihre Dienstleistung wurde unwiederruflich" not in json.dumps(response.text):
                print(f"Forbidden: {response.status_code} | {response.text}")
                return
        if response.status_code != 200:
            print(f"HTTP error: {response.status_code}")
            print(response.text)
            return response.status_code
        if not response_data:
            print("No data returned")
            return

        if response_data and response_data["data"] and len(response_data["data"]) > 0:
            latest_creation_time = response_data["data"][0]["created_on"]
            global most_occuring_method_sent  
            if last_sent_creation_time != latest_creation_time:
                embed_details = [
                    f"**IP Address:** {response_data['data'][0]['ip']}",
                    f"**Mbps:** {response_data['data'][0]['mbps']}",
                    f"**PPS:** {response_data['data'][0]['pps']}",
                    f"**Mode:** {response_data['data'][0]['mode']}",
                    f"**Attack Method:** {response_data['data'][0]['method']}",
                    f"**Most Occurring Attack Method:** {find_most_occuring_method(response_data['data'])}",
                    f"**Total Attacks:** {len(response_data['data'])}",
                    f"**Created On:** {latest_creation_time}",
                ]

                
                latest_attack_method = response_data["data"][0]["method"]
                if latest_attack_method not in most_occuring_method:
                    most_occuring_method[latest_attack_method] = 1
                else:
                    most_occuring_method[latest_attack_method] += 1

                send_embed("DDoS Attack alert", [{"name": f"Service: {data[index]['name']}", "value": "\n".join(embed_details)}], index, 0x00FF69, data[index]["alerts"])
                last_sent_creation_time = latest_creation_time
                most_occuring_method_sent = True
    except Exception as e:
        print(e)


def status_logs(index, headers):
    try:
        start_time = time.time() 
        response = requests.get(sex_url(index), headers=headers)
        request_id(response, sex_url(index))
        response_data = response.json() 
        end_time = time.time() 

       
        traffic_limit = "No"

        if response.status_code == 429:
            print(f"Ratelimited, new delay: {rqDelay} | {response.text}")
            return
        if response.status_code == 403:
            if "Ihre Dienstleistung wurde unwiederruflich" not in json.dumps(response.text):
                print(f"Forbidden: {response.status_code} | {response.text}")
                return
            if data[index]["lastState"] == "deleted":
                return
            embed_data = [
                {"name": "Service", "value": data[index]["name"]},
                {"name": "Status", "value": api_state_desc["deletedService"]["desc"]},
            ]
            send_embed("Server Status Update", embed_data, index, api_state_desc["deletedService"]["color"], data[index]["webhook"])
            data[index]["lastState"] = "deleted"
            return
        if response.status_code != 200:
            print(f"HTTP error: {response.status_code}")
            print(response.text)
            return response.status_code
        if not response_data:
            print("No data returned")
            return

        api_response_time = round((end_time - start_time) * 1000)
        
        additional_details = ""
        locked = "No"
        state = {"name": response_data["product"]["status"], "color": api_state_desc["unk"]["color"]}
        if response_data["service"]["daysleft"] < 1:
            response_data["service"]["daysleft"] = "none"
        if response_data["service"]["locked"] != 0:
            locked = f"Yes, {response_data['service']['lockreason']}" or "no info"
        if response_data["product"]["trafficlimitreached"] != 0:
            traffic_limit = "Yes" 

        if response_data["product"]["status"] not in api_state_desc:
            state["name"] = f"{api_state_desc['unk']['desc']} ({response_data['product']['status']})"
        else:
            if response_data["product"]["status"] == "uselast":
                return 
            state["name"] = api_state_desc[response_data["product"]["status"]]["desc"]
            state["color"] = api_state_desc[response_data["product"]["status"]]["color"]
        if data[index]["lastState"] == response_data["product"]["status"]:
            return

        data[index]["lastState"] = response_data["product"]["status"]

       
        if "node" in response_data["product"]:
            additional_details += f"> **node**: {response_data['product']['node']}\n"
        if "location" in response_data["product"]:
            additional_details += f"> **datacenter**: {response_data['product']['location']}\n"
        if "cluster" in response_data["product"]:
            additional_details += f"> **cluster**: {response_data['product']['cluster']}\n"
        if "trafficlimitreached" in response_data["product"]:
            additional_details += f"> **Traffic Limit Reached**: {traffic_limit}\n" or "No\n"
        additional_details += f"> **Locked**: {locked}\n"
        additional_details += f"> **Days left**: {response_data['service']['daysleft'] or 'No data'} | **Price**: {response_data['service']['price']}€\n"
        additional_details += f"> **API-Time**: {api_response_time:.5f}ms\n"

        details = [
            {"name": "Service", "value": data[index]["name"] or "No data"},
            {"name": "Status", "value": state["name"]},
            {"name": f"{response_data['service']['productdisplay']} informations", "value": additional_details},
        ]

        send_embed("Server Status Update", details, index, state["color"], data[index]["webhook"])
    except Exception as e:
        print(e)


# Finds the most occurring attack method from a list of DDoS incidents
def get_server_status(index):
    try:
        userAgent = get_random_user_agent()  # Setze den zufälligen User-Agent für diese Anfrage
        headers = {'User-Agent': userAgent}

        if useIPv4AsName and (data[index]["ipv4"] is None or data[index]["ipv4"] == "Error getting IPv4 address."):
            le_get_ip(index)
            sleep_ms(269) 
        ddos_logs(index, headers)
        status_logs(index, headers)
    except Exception as e:
        print(e)


def find_most_occuring_method(api_data):
    method_counts = {}

    for entry in api_data:
        method = entry["method"]
        if method not in method_counts:
            method_counts[method] = 1
        else:
            method_counts[method] += 1

    most_occuring_method = max(method_counts, key=method_counts.get)

    print(f"Most Occurring Attack Method: {most_occuring_method}")

    return most_occuring_method

# Main function that runs an infinite loop to periodically check and update server status
def main():
    try:
        while True:
            for i in range(len(data)):
                request_id(requests.get(sex_url(i)), sex_url(i))
                get_server_status(i)
            sleep_ms(rqDelay * 4000)
    except Exception as e:
        print(e)

# Entry point of the script

if __name__ == "__main__":
    main()
