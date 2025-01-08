import time
import socket
import requests

# Server details
SERVER_IP = "play.adventurecraft.uk"  # Your Minecraft server domain
SERVER_PORT = 25565                   # Minecraft server port
CHECK_INTERVAL = 60                   # Time (in seconds) between checks
ALERT_INTERVAL = 300                  # Time (in seconds) before alerting if server is down
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1326562942581211197/IFl_yca5lNJM-2gQQCXw8-W1clbE1uwXGi9WnkOdKja3AILn4J7sGgEueTi-Frwp4LJW"
DISCORD_USER_IDS = ["441213776461692931", "553254039224320011"]  # AidenMouse and matkis IDs

def is_server_online(ip, port):
    """Check if the Minecraft server is online."""
    try:
        with socket.create_connection((ip, port), timeout=10):
            return True
    except Exception:
        return False

def send_discord_message(message):
    """Send a message to Discord."""
    mentions = " ".join([f"<@{user_id}>" for user_id in DISCORD_USER_IDS])  # Tag users
    payload = {
        "content": f"{mentions} {message}"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord message: {e}")

def main():
    """Main monitoring loop."""
    down_start_time = None

    # Send initial message when script starts
    send_discord_message("🔍 The monitoring script is up and running. Watching the server now!")

    while True:
        if is_server_online(SERVER_IP, SERVER_PORT):
            if down_start_time:
                down_duration = time.time() - down_start_time
                send_discord_message(f"🎉 Server is back online after being down for {int(down_duration / 60)} minutes!")
                down_start_time = None
            else:
                print("Server is online.")
        else:
            print("Server is offline.")
            if down_start_time is None:
                down_start_time = time.time()
            elif time.time() - down_start_time >= ALERT_INTERVAL:
                send_discord_message("⚠️ Server has been offline for over 5 minutes! Please check it immediately!")
                time.sleep(60)  # Prevent spamming Discord too frequently

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()