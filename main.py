import json
import aiohttp
import asyncio
import time
import subprocess
import datetime

webhook = 'https://canary.discord.com/api/webhooks/xxxxxxxxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
service_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
callcenter = 'xxxxxxxxxxxxxxxxxxxxxxxxxx' # API token
kadse = 'https://backend.datalix.de/v1/service/'
breached_vc = 'https://backend.datalix.de/v1/user/apikey/'

status_eisen_stange_zerschlagen = {
    "stopping": "Der Server wird mit einer Eisenstange gewaltsam zur Vernunft gebracht.",
    "shutdown": "The server is shut down.",
    "starting": "Server is starting...",
    "running": "Server Online.",
    "stopped": "Server offline.",
    "installing": "Service is installing.",
    "restorebackup": "Backup is being imported. (Layer8)",
    "backupplanned": "Backup planned.",
    "restoreplanned": "Service has a restore planned.",
    "createbackup": "Service create a backup",
    "error": "Proxmox skill issue",
}

def get_lefishe(endpoint):
    if endpoint:
        return f'{kadse}{service_id}/{endpoint}?token={callcenter}'
    else:
        return f'{kadse}{service_id}?token={callcenter}'

async def send_discord_embed_aiohttp(embed_data):
    if embed_data:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook, json={"embeds": [embed_data]}) as response:
                if response.status != 200:
                    print(f"Fehler beim Senden: {response.status}")
    else:
        print("Embed-Daten sind leer, Nachricht kann nicht gesendet werden.")

async def skid_api_response(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientResponseError as http_error:
        print("API-Anfragefehler:", http_error)
        print(f"Statuscode: {http_error.status}")
        return None

async def sex_with_server_status(session):
    headers = {
        "user-agent": "Mozilla/5.0 domis router lass mich durch asyl holt daten ab"
    }
    url = get_lefishe('status')
    return await skid_api_response(session, url)

cached_ip = None
last_ip_fetch_time = None

async def get_ip(session):
    global cached_ip, last_ip_fetch_time

    if cached_ip is None or (last_ip_fetch_time is not None and (datetime.datetime.now() - last_ip_fetch_time).total_seconds() >= 12 * 3600):
        headers = {
            "user-agent": "Mozilla/5.0 domis router lass mich durch asyl holt daten ab"
        }
        url = get_lefishe('ip')
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                ip_data = await response.json()
                ipv4 = ip_data.get("ipv4", [])
                if ipv4:
                    cached_ip = ipv4[0].get("ip", "IP nicht verfügbar")
                    last_ip_fetch_time = datetime.datetime.now()
                    return cached_ip
                else:
                    return "IP nicht verfügbar"
        except aiohttp.ClientResponseError as e:
            print(f"Fehler beim Abrufen der Server-IP: {e}")
            if cached_ip is not None:
                return cached_ip

    return cached_ip

async def get_api_key_data(session):
    url = f'{breached_vc}{callcenter}?token={callcenter}'
    data = await skid_api_response(session, url)

    if data:
        user_info = data.get("userInfo", {})
        credit_str = user_info.get("credit", "0").replace(',', '.')
        credit_in_euro = round(float(credit_str), 2) 
        
        expire_at_unix = data.get("expire_at", 0)
        expire_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_at_unix))
        
        created_on_unix = user_info.get("created_on", 0)
        created_on = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created_on_unix))
        
        email = user_info.get("email", "")
        email_parts = email.split("@")
        email_hidden = email_parts[0][:3] + "###" + "@" + email_parts[1]
        
        return {
            "username": user_info.get("username", "failed gived"),
            "email": email_hidden,
            "credit": f"{credit_in_euro} €",
            "created_on": created_on,
            "expire_at": expire_at
        }

previous_status = None

async def main(): 
    global previous_status 

    async with aiohttp.ClientSession() as session:
        while True:
            start_time = time.time()

            server_status = await sex_with_server_status(session)
            ip_address = await get_ip(session)
            api_key_data = await get_api_key_data(session)

            end_time = time.time()

            if server_status:
                current_status = server_status['status']
                ip_address = await get_ip(session)
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                duration = (end_time - start_time) * 1000

                headers = {
                    "user-agent": "Mozilla/5.0 domis router lass mich durch asyl holt daten ab",
                    "accept": "application/json"
                }
                response = await session.get(get_lefishe(''), headers=headers)
                data = await response.json()
                product_data = data.get("product", {})
                service_data = data.get("service", {})

                service_info = {
                    "Lock Reason": service_data.get("lockreason", "Nicht verfügbar"),
                    "node": product_data.get("node", "Nicht verfügbar"),
                    "Datacenter": product_data.get("location", "Nicht verfügbar"),
                    "Cluster": product_data.get("cluster", "Nicht verfügbar"),
                }

                customer_info_embed = {
                    "title": "Server Status Update",
                    "description": status_eisen_stange_zerschlagen.get(current_status, "Unbekannter Status"),
                    "color": 0x00FF00,  
                    "thumbnail": {
                        "url": "https://cdn.discordapp.com/emojis/1155264718408265838.gif?size=96&quality=lossless"
                    },
                    "fields": [
                        {"name": "IP Address", "value": ip_address, "inline": False},
                        {"name": "Status Code", "value": current_status, "inline": False},
                        {"name": "Current Time", "value": current_time, "inline": False}
                    ]
                }

                customer_info_embed["author"] = {
                    "name": "AsylantenCeo",
                    "url": "https://asyloperations.xyz",
                    "icon_url": "https://cdn.discordapp.com/emojis/943540250133811241.webp?size=96&quality=lossless"
                }

                if duration:
                    customer_info_embed["fields"].append({"name": "Response Time API", "value": f"{duration:.2f} ms", "inline": False})
                
                service_info_text = "\n".join([f"**{key}:** {value}" for key, value in service_info.items()])
                customer_info_embed["fields"].append({"name": "Service Information", "value": service_info_text, "inline": False})
                customer_info_embed["footer"] = {"text": "Powered by Asyloperations"}
                customer_info_embed["fields"].extend([
                    {"name": "Customer Information", "value": f"Username: {api_key_data['username']}\n"
                                                              f"Email: {api_key_data['email']}\n"
                                                              f"Credit: {api_key_data['credit']}\n"
                                                              f"Created On: {api_key_data['created_on']}\n"
                                                              f"Expire At: {api_key_data['expire_at']}",
                     "inline": False}
                ])

                if current_status != previous_status:
                    await send_discord_embed_aiohttp(customer_info_embed)

                previous_status = current_status            
            else:
                print('Fehler beim Abrufen des Serverstatus.')

            await asyncio.sleep(2)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
