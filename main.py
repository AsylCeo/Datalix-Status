import json
import requests
import discord
import asyncio
import time

webhook_url = 'https://canary.discord.com/api/webhooks/2222222222222222222/xxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Discord Webhook
service_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Service-id 
api_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # API token
base_url = 'https://backend.datalix.de/v1/service/' # API URL
status_descriptions = {
    "stopping": "Der Server wird unter Anwendung drakonischer Maßnahmen zwangsweise zur Vernunft gebracht werden.", # english: The server will be forcibly brought to its senses using draconian measures.
    "shutdown": "The server will be shut down.",
    "starting": "Service is starting...",
    "running": "Server Online.",
    "stopped": "Server offline.",
    "installing": "Service is installing.",
    "restorebackup": "Backup is being imported.",
    "backupplanned": "Backup planned.",
    "restoreplanned": "Service has a restore planned.",
}

# Function get server status
async def get_server_status():
    url = f'{base_url}{service_id}/status?token={api_token}'
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Failed to fetch server status: {e}')
        return None

# Function get server IP
async def get_server_ip():
    ip_url = f'{base_url}{service_id}/ip?token={api_token}'
    try:
        response = requests.get(ip_url)
        response.raise_for_status()  
        ip_data = response.json()
        ipv4 = ip_data.get("ipv4", [])
        if ipv4:
            return ipv4[0].get("ip", "IP not available")
        return "IP not available"
    except requests.exceptions.RequestException as e:
        print(f'Failed to fetch server IP: {e}')
        return "IP not available"

# Function to send Discord webhook with embed
async def send_discord_embed(status, ip, current_time, color, error_message=None, duration=None, service_info=None):
    status_description = status_descriptions.get(status, "Status unknown")
    
    embed = discord.Embed(title='Server Status Update', description=f'Serverstatus is: {status_description}', color=color)
    embed.add_field(name='IP-Address', value=ip, inline=False)
    embed.add_field(name='Statuscode', value=status, inline=False)
    embed.add_field(name='Current time', value=current_time, inline=False)
    
    if error_message:
        embed.add_field(name='Error message', value=error_message, inline=False)
    
    if duration:
        embed.add_field(name='Response API', value=f'{duration:.2f} ms', inline=False)
    
    if service_info:
        service_info_text = '\n'.join([f"{key}: {value}" for key, value in service_info.items()])
        embed.add_field(name='More information', value=service_info_text, inline=False)
    
    data = {
        "embeds": [embed.to_dict()]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code != 204:
        print(f'Webhook seizured: {response.text}')

# Main asynchronous function
async def main():
    previous_status = None
    
    while True:
        start_time = time.time()
        server_status = await get_server_status()
        server_ip = await get_server_ip()
        end_time = time.time()
        
        if server_status:
            current_status = server_status['status']
            ip_address = server_ip
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Service Info API                               -service id                         -     - API token                          -
            api_url = "https://backend.datalix.de/v1/service/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # <------------------------- 
            response = requests.get(api_url, headers={"accept": "application/json"})
            data = response.json()
            product_data = data.get("product", {})
            service_data = data.get("service", {})
            # service info (kvm/dedi)
            service_info = {
                "Service Locked": service_data.get("locked", "Nicht verfügbar"),
                "Lock Reason": service_data.get("lockreason", "Nicht verfügbar"),
                "nodeid": product_data.get("nodeid", "Nicht verfügbar"),
                "mac": product_data.get("mac", "Nicht verfügbar"),
                "Uplink": product_data.get("uplink", "Nicht verfügbar"),
                "cputype": product_data.get("cputype", "Nicht verfügbar"),
                "Hostname": product_data.get("hostname", "Nicht verfügbar"),
                "node": product_data.get("node", "Nicht verfügbar"),
                "Datacenter (Rechenzentrum)": product_data.get("location", "Nicht verfügbar"),
                "Cluster": product_data.get("cluster", "Nicht verfügbar"),
                "Service ID": product_data.get("serviceid", "Nicht verfügbar"),
                "Proxmox ID": product_data.get("proxmoxid", "Nicht verfügbar"),
            }
            
            if current_status != previous_status:
                color = 0x00FF00  # green color for normal status
                
                if current_status == 'error':
                    color = 0xFF0000  # Red color for error status
                    error_message = "Fehler erkannt. Proxmox retarded"
                    await send_discord_embed(current_status, ip_address, current_time, color, error_message, duration, service_info)
                else:
                    await send_discord_embed(current_status, ip_address, current_time, color, duration=duration, service_info=service_info)
                
                previous_status = current_status
        else:
            print('Failed to fetch server status.')
        
        await asyncio.sleep(2) # check all 2 sec

######################################################################

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
