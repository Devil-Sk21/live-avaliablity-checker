#!/usr/bin/env python3
"""
24/7 Cloud Stock Sniper & Phone Alert Bot
Monitors Acer Predator Helios Neo 16S AI (NH.QX9SI.001 / PHN16S-71)
Across Reliance Digital (Pincode: 360005), Flipkart, Vijay Sales, and Acer Store.

Sends instant high-priority alerts to your phone via Telegram and/or Email.
Runs 24/7 in the cloud without requiring your personal computer to be on.
"""

import argparse
import datetime
import gzip
import io
import os
import smtplib
import sys
import time
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Tuple

from reliance_client import RelianceClient


def load_dotenv():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ and v.strip():
                        os.environ[k.strip()] = v.strip()


load_dotenv()

# Target Specs
TARGET_NAME = "Acer Predator Helios Neo 16S AI"
TARGET_MPN = "NH.QX9SI.001"
TARGET_MODEL = "PHN16S-71"
DEFAULT_PINCODE = "360005"

RELIANCE_SLUG = "acer-phn16s-71-nhqx9si001-gaming-laptop-intel-core-ultra-7-255hx16-gb1-tb8-gb-nvidia-geforce-rtx-5050windows-11-homewqxga-4064-cm-16-inch-abyssal-black-mhnbsm-9568670"
RELIANCE_URL = f"https://www.reliancedigital.in/product/{RELIANCE_SLUG}"
FLIPKART_URL = "https://www.flipkart.com/search?q=NH.QX9SI.001"
VIJAY_SALES_URL = "https://www.vijaysales.com/search/NH.QX9SI.001"
ACER_STORE_URL = "https://store.acer.com/en-in/catalogsearch/result/?q=NH.QX9SI.001"

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
}


NTFY_TOPIC = "acer_predator_rajkot_360005"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"


def send_ntfy_alert(platform: str, buy_url: str, details: str = ""):
    """
    Sends an instant high-priority push notification to your phone via ntfy.sh.
    Zero configuration required.
    """
    try:
        data = f"Laptop in stock on {platform}!\nStatus: {details}\nDelivery: Serviceable to {DEFAULT_PINCODE}".encode("utf-8")
        req = urllib.request.Request(
            NTFY_URL,
            data=data,
            headers={
                "Title": f"STOCK ALERT: {platform.upper()}!",
                "Priority": "urgent",
                "Tags": "fire,laptop,moneybag",
                "Click": buy_url,
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print(f"[SUCCESS] Instant Phone Push Alert dispatched to {NTFY_URL}!")
    except Exception as e:
        print(f"[ERROR] Failed to send ntfy phone push: {e}")


def send_telegram_alert(bot_token: str, chat_id: str, platform: str, buy_url: str, details: str = ""):
    """
    Sends an instant push notification message to your Telegram app.
    """
    if not bot_token or not chat_id:
        return

    message = (
        f"🚨 <b>STOCK ALERT: LAPTOP IN STOCK!</b> 🚨\n\n"
        f"💻 <b>Model:</b> {TARGET_NAME}\n"
        f"🏷️ <b>Part Number:</b> <code>{TARGET_MPN}</code>\n"
        f"🏬 <b>Platform:</b> <b>{platform}</b>\n"
        f"📍 <b>Delivery:</b> Serviceable to <b>{DEFAULT_PINCODE}</b>\n"
        f"📝 <b>Status:</b> {details}\n\n"
        f"⚡ <b><a href='{buy_url}'>CLICK HERE TO BUY NOW</a></b> ⚡\n\n"
        f"<i>Order immediately before stock runs out!</i>"
    )

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "false",
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers={"User-Agent": "StockSniperBot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print(f"[SUCCESS] Telegram alert sent to your phone for {platform}!")
    except Exception as e:
        print(f"[ERROR] Failed to send Telegram alert: {e}")


def send_email_alert(
    gmail_user: str,
    gmail_pass: str,
    recipient_email: str,
    platform: str,
    buy_url: str,
    details: str = "",
):
    """
    Sends an email alert directly to your inbox.
    """
    if not gmail_user or not gmail_pass or not recipient_email:
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚨 URGENT: {TARGET_NAME} is IN STOCK on {platform}!"
    msg["From"] = gmail_user
    msg["To"] = recipient_email

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="background: #e63946; color: white; padding: 15px; border-radius: 8px 8px 0 0; text-align: center;">
          <h2>🔥 URGENT STOCK ALERT! 🔥</h2>
        </div>
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 0 0 8px 8px;">
          <p>The laptop you are tracking is <b>now available for purchase</b>!</p>
          <ul>
            <li><b>Laptop:</b> {TARGET_NAME}</li>
            <li><b>Part Number:</b> {TARGET_MPN} ({TARGET_MODEL})</li>
            <li><b>Platform:</b> {platform}</li>
            <li><b>Status:</b> {details}</li>
            <li><b>Delivery Pincode:</b> {DEFAULT_PINCODE} (Rajkot)</li>
          </ul>
          <div style="text-align: center; margin: 30px 0;">
            <a href="{buy_url}" style="background: #2a9d8f; color: white; padding: 15px 30px; text-decoration: none; font-size: 18px; font-weight: bold; border-radius: 6px;">👉 BUY NOW ON {platform.upper()}</a>
          </div>
          <p style="color: #666; font-size: 12px;">This is an automated notification from your 24/7 Cloud Stock Sniper.</p>
        </div>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, recipient_email, msg.as_string())
        print(f"[SUCCESS] Email alert sent to {recipient_email}!")
    except Exception as e:
        print(f"[ERROR] Failed to send Email alert: {e}")


def check_reliance_digital(client: RelianceClient, pincode: str) -> Tuple[bool, str]:
    try:
        sizes = client.get_product_sizes(RELIANCE_SLUG)
        if sizes:
            qty = sizes[0].get("quantity", 0)
            avail = sizes[0].get("is_available", False)
            if avail and qty > 0:
                deliv = client.check_delivery(RELIANCE_SLUG, "OS", pincode)
                if deliv.get("status") == "AVAILABLE":
                    return True, f"IN STOCK ({qty} units available for PIN {pincode})"
                return True, f"IN STOCK ({qty} units in central warehouse)"
            return False, f"Out of Stock (Quantity: {qty})"
        return False, "Out of Stock"
    except Exception as e:
        return False, f"Check error ({e})"


def check_flipkart() -> Tuple[bool, str]:
    try:
        req = urllib.request.Request(FLIPKART_URL, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as res:
            raw = res.read()
            if res.info().get("Content-Encoding") == "gzip":
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            html = raw.decode("utf-8", errors="ignore")

            has_model = TARGET_MPN in html or TARGET_MODEL in html
            if has_model:
                is_oos = any(s in html for s in ["Currently unavailable", "Out of Stock", "Sold Out", "Coming Soon"])
                if not is_oos:
                    return True, "IN STOCK / Buyable listing active on Flipkart!"
                return False, "Listed but Currently Unavailable / Out of Stock"
            return False, "Not listed in active catalog"
    except Exception as e:
        return False, f"Check error ({e})"


def check_vijay_sales() -> Tuple[bool, str]:
    try:
        req = urllib.request.Request(VIJAY_SALES_URL, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as res:
            raw = res.read()
            if res.info().get("Content-Encoding") == "gzip":
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            html = raw.decode("utf-8", errors="ignore")

            if TARGET_MPN in html or TARGET_MODEL in html:
                if "Add to Cart" in html or "Buy Now" in html:
                    return True, "IN STOCK on Vijay Sales!"
                return False, "Out of Stock / In-store only"
            return False, "Not listed online"
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "Page 404 (No active listing)"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"Check error ({e})"


def check_acer_store() -> Tuple[bool, str]:
    try:
        req = urllib.request.Request(ACER_STORE_URL, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as res:
            raw = res.read()
            if res.info().get("Content-Encoding") == "gzip":
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            html = raw.decode("utf-8", errors="ignore")

            if TARGET_MPN in html or TARGET_MODEL in html:
                if "Add to Cart" in html or "In stock" in html:
                    return True, "IN STOCK on official Acer Store!"
                return False, "Out of Stock"
            return False, "Not currently in online inventory"
    except Exception as e:
        return False, f"Check error ({e})"


def scan_once(
    bot_token: Optional[str] = None,
    chat_id: Optional[str] = None,
    gmail_user: Optional[str] = None,
    gmail_pass: Optional[str] = None,
    recipient_email: Optional[str] = None,
    pincode: str = DEFAULT_PINCODE,
) -> bool:
    """
    Performs a single complete scan across all platforms and fires alerts if found.
    Returns True if stock was detected on any platform.
    """
    client = RelianceClient()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Checking stock for PIN {pincode}...")

    platforms = [
        ("Reliance Digital", lambda: check_reliance_digital(client, pincode), RELIANCE_URL),
        ("Flipkart", check_flipkart, FLIPKART_URL),
        ("Vijay Sales", check_vijay_sales, VIJAY_SALES_URL),
        ("Acer Store", check_acer_store, ACER_STORE_URL),
    ]

    any_stock = False

    for name, check_fn, url in platforms:
        is_in_stock, msg = check_fn()
        status_marker = "[IN STOCK]" if is_in_stock else "[OUT OF STOCK]"
        print(f"  * {name:<18}: {status_marker} - {msg}")

        if is_in_stock:
            any_stock = True
            # 1. Instant Phone Push Notification (Zero setup)
            send_ntfy_alert(name, url, msg)
            
            # 2. Telegram Alert (if configured)
            if bot_token and chat_id:
                send_telegram_alert(bot_token, chat_id, name, url, msg)
                
            # 3. Email Alert (if configured)
            if gmail_user and gmail_pass and recipient_email:
                send_email_alert(gmail_user, gmail_pass, recipient_email, name, url, msg)

    return any_stock


def main():
    parser = argparse.ArgumentParser(description="24/7 Cloud Stock Sniper for Acer Predator Helios Neo 16S AI")
    parser.add_argument("--once", action="store_true", help="Run once and exit (for GitHub Actions / Cron jobs)")
    parser.add_argument("--interval", type=int, default=180, help="Check interval in seconds (default: 180s = 3 mins)")
    parser.add_argument("--pincode", type=str, default=DEFAULT_PINCODE, help="Delivery pincode (default: 360005)")
    parser.add_argument("--telegram-token", type=str, default=os.getenv("TELEGRAM_BOT_TOKEN"))
    parser.add_argument("--telegram-chat-id", type=str, default=os.getenv("TELEGRAM_CHAT_ID"))
    parser.add_argument("--gmail-user", type=str, default=os.getenv("GMAIL_USER"))
    parser.add_argument("--gmail-pass", type=str, default=os.getenv("GMAIL_APP_PASSWORD"))
    parser.add_argument("--recipient-email", type=str, default=os.getenv("ALERT_EMAIL"))
    parser.add_argument("--test-notify", action="store_true", help="Send a test notification to verify Telegram/Email")

    args = parser.parse_args()

    if args.test_notify:
        print("[TEST] Sending test notifications to phone...")
        send_ntfy_alert("TEST PLATFORM", RELIANCE_URL, "Test Notification - System is working perfectly!")
        if args.telegram_token and args.telegram_chat_id:
            send_telegram_alert(args.telegram_token, args.telegram_chat_id, "TEST PLATFORM", RELIANCE_URL, "Test Notification")
        if args.gmail_user and args.gmail_pass and args.recipient_email:
            send_email_alert(args.gmail_user, args.gmail_pass, args.recipient_email, "TEST PLATFORM", RELIANCE_URL, "Test Notification")
        print("[TEST] Done. Open https://ntfy.sh/acer_predator_rajkot_360005 on your phone to verify!")
        sys.exit(0)

    if args.once:
        scan_once(
            bot_token=args.telegram_token,
            chat_id=args.telegram_chat_id,
            gmail_user=args.gmail_user,
            gmail_pass=args.gmail_pass,
            recipient_email=args.recipient_email,
            pincode=args.pincode,
        )
        sys.exit(0)

    # 24/7 Loop
    print(f"=== 24/7 Cloud Sniper Active (Pincode: {args.pincode}, Interval: {args.interval}s) ===")
    while True:
        try:
            scan_once(
                bot_token=args.telegram_token,
                chat_id=args.telegram_chat_id,
                gmail_user=args.gmail_user,
                gmail_pass=args.gmail_pass,
                recipient_email=args.recipient_email,
                pincode=args.pincode,
            )
            print(f"Waiting {args.interval} seconds for next cycle...\n")
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("Stopped.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()
