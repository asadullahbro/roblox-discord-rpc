import time
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from pypresence import Presence

# ================= CONFIG =================
load_dotenv()
DISCORD_CLIENT_ID = "1464954943080497174"
ROBLOX_USER_ID = os.getenv("ROBLOX_USER_ID")
RAW_COOKIE = os.getenv("ROBLOSECURITY")
CHECK_INTERVAL = 15 

# Fallback image if game icon fails
SILVER_LOGO = "https://cdn.discordapp.com/app-icons/363445589247131668/f2b60e350a2097289b3b0b877495e55f.webp?size=512"

# ---------- Cookie Cleaner ----------
def get_clean_cookie(cookie_str):
    if not cookie_str:
        return None
    return cookie_str.strip()

CLEANED_COOKIE = get_clean_cookie(RAW_COOKIE)
COOKIES = {".ROBLOSECURITY": CLEANED_COOKIE}
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ---------- Console Logging ----------
def log(label, value):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {label:<16}: {value}")

# ---------- Roblox Helpers ----------
def get_presence():
    try:
        url = "https://presence.roblox.com/v1/presence/users"
        payload = {"userIds": [ROBLOX_USER_ID]}
        r = requests.post(url, json=payload, cookies=COOKIES, headers=HEADERS, timeout=10)
        
        if r.status_code == 401:
            log("SECURITY", "Cookie Expired! Update your .env file.")
            return "EXPIRED"
            
        data = r.json()
        if data.get("userPresences"):
            return data["userPresences"][0]
        return None
    except Exception as e:
        log("Presence Error", e)
        return None

def get_game_info(place_id):
    try:
        # Get Universe ID
        u_url = f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
        u_resp = requests.get(u_url, timeout=10)
        universe_id = u_resp.json().get("universeId")
        
        # Get Game Name
        g_url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
        g_resp = requests.get(g_url, cookies=COOKIES, timeout=10)
        data = g_resp.json()
        
        if data and "data" in data and len(data["data"]) > 0:
            return {"name": data["data"][0].get("name")}
        return None
    except:
        return None

def get_game_icon(place_id):
    try:
        url = "https://thumbnails.roblox.com/v1/places/gameicons"
        params = {"placeIds": place_id, "size": "512x512", "format": "Png"}
        r = requests.get(url, params=params, timeout=10)
        return r.json()["data"][0]["imageUrl"]
    except:
        return SILVER_LOGO

# ---------- Main Loop ----------
def main():
    rpc = Presence(DISCORD_CLIENT_ID)
    try:
        rpc.connect()
        log("System", "Connected to Discord")
    except:
        log("System", "Discord not found. Open Discord first!")
        return

    start_time = int(time.time())
    rpc_active = False 

    while True:
        try:
            presence = get_presence()

            if presence == "EXPIRED":
                break # Exit script if cookie is dead

            # Type 2 = In Game
            if presence and presence.get("userPresenceType") == 2:
                place_id = presence.get("placeId")
                game = get_game_info(place_id)
                game_name = game["name"] if game else "Unknown Game"
                icon_url = get_game_icon(place_id)

                log("Status", f"Playing: {game_name}")
                rpc.update(
                    state="In Game",
                    details=game_name,
                    large_image=icon_url,
                    large_text=game_name,
                    start=start_time,
                    buttons=[{"label": "Join Game", "url": f"https://www.roblox.com/games/{place_id}"}]
                )
                rpc_active = True
            
            else:
                # If in Menu/Offline, clear the status
                if rpc_active:
                    log("Status", "Cleared (Not playing)")
                    rpc.clear()
                    rpc_active = False
                else:
                    print(".", end="", flush=True)

        except Exception as e:
            log("Loop Error", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()