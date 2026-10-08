"""
Helper script to detect the Telegram Chat ID from @shiv_laptop_sniper_bot,
save it to .env, and fire a confirmation message.
"""
import os
import sys
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path

BOT_TOKEN = "8682779333:AAFTFEiqTlIqQCqtBUBkaI54ztsemoxiNS8"
ENV_PATH = Path(__file__).parent / ".env"

def check_updates():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    req = urllib.request.Request(url, headers={"User-Agent": "TelegramSetup/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("result", [])

def send_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"User-Agent": "TelegramSetup/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status == 200

def update_env(chat_id):
    if not ENV_PATH.exists():
        return
    content = ENV_PATH.read_text(encoding="utf-8")
    new_lines = []
    found_chat_id = False
    for line in content.splitlines():
        if line.startswith("TELEGRAM_CHAT_ID="):
            new_lines.append(f"TELEGRAM_CHAT_ID={chat_id}")
            found_chat_id = True
        else:
            new_lines.append(line)
    if not found_chat_id:
        new_lines.append(f"TELEGRAM_CHAT_ID={chat_id}")
    ENV_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"[OK] Saved TELEGRAM_CHAT_ID={chat_id} to .env")

def main():
    print(f"Checking for messages to @shiv_laptop_sniper_bot...")
    updates = check_updates()
    if not updates:
        print("NO_UPDATES_YET")
        return False

    # Get the latest message
    latest = updates[-1]
    chat = latest.get("message", {}).get("chat", {}) or latest.get("my_chat_member", {}).get("chat", {})
    chat_id = chat.get("id")
    username = chat.get("username", "") or chat.get("first_name", "User")

    if not chat_id:
        print("[ERROR] Could not extract chat_id from updates.")
        return False

    print(f"[FOUND] Detected user: {username} (Chat ID: {chat_id})")
    update_env(chat_id)

    # Send confirmation test message
    msg = (
        f"🤖 <b>Telegram Alerts Connected!</b>\n\n"
        f"Hello <b>{username}</b>! Your 24/7 Acer Predator Stock Sniper is now directly linked to your Telegram.\n\n"
        f"🎯 <b>Tracking:</b> Acer Predator Helios Neo 16S AI (RTX 5060, Intel Core Ultra 7)\n"
        f"📍 <b>Pincode:</b> 360005 (Rajkot, Gujarat)\n"
        f"⚡ <b>Coverage:</b> Reliance Digital, Flipkart, Vijay Sales, Acer Store\n\n"
        f"As soon as stock is detected, you will receive an instant notification here with a direct Buy Now link!"
    )
    send_telegram(chat_id, msg)
    print(f"[SUCCESS] Sent confirmation alert to Telegram Chat ID: {chat_id}")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
