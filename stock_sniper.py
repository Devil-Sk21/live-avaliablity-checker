#!/usr/bin/env python3
"""
Multi-Platform Automated Stock Sniper & Alert Bot
Monitors Acer Predator Helios Neo 16S AI (NH.QX9SI.001 / PHN16S-71)
Across Reliance Digital, Flipkart, Vijay Sales, and Acer Store.

Triggers an audible alarm and automatically opens the purchase page
the second stock is detected on any platform.
"""

import argparse
import ctypes
import datetime
import gzip
import io
import json
import os
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from typing import Dict, Tuple

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

from reliance_client import RelianceClient

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Product Details
TARGET_NAME = "Acer Predator Helios Neo 16S AI"
TARGET_MPN = "NH.QX9SI.001"
TARGET_MODEL = "PHN16S-71"
RELIANCE_SLUG = "acer-phn16s-71-nhqx9si001-gaming-laptop-intel-core-ultra-7-255hx16-gb1-tb8-gb-nvidia-geforce-rtx-5050windows-11-homewqxga-4064-cm-16-inch-abyssal-black-mhnbsm-9568670"
RELIANCE_URL = f"https://www.reliancedigital.in/product/{RELIANCE_SLUG}"
FLIPKART_URL = "https://www.flipkart.com/search?q=NH.QX9SI.001"
VIJAY_SALES_URL = "https://www.vijaysales.com/search/NH.QX9SI.001"
ACER_STORE_URL = "https://store.acer.com/en-in/catalogsearch/result/?q=NH.QX9SI.001"

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
}


def trigger_alarm(platform: str, buy_url: str, enable_sound: bool = True):
    """
    Sounds an alarm, shows a Windows popup, and automatically opens the buy page in browser.
    """
    print(f"\n{GREEN}{BOLD}{'='*70}{RESET}")
    print(f"{GREEN}{BOLD}🔥 STOCK DETECTED ON {platform.upper()}! 🔥{RESET}")
    print(f"{BOLD}URL:{RESET} {buy_url}")
    print(f"{GREEN}{BOLD}{'='*70}{RESET}\n")

    # 1. Automatically launch the checkout / product page in the default web browser
    try:
        webbrowser.open(buy_url)
    except Exception as e:
        print(f"Failed to open browser automatically: {e}")

    # 2. Windows popup in a background thread (so it doesn't block the audio loop)
    def show_popup():
        try:
            ctypes.windll.user32.MessageBoxW(
                0,
                f"STOCK DETECTED ON {platform}!\n\nProduct: {TARGET_NAME}\nPart No: {TARGET_MPN}\n\nBrowser opened to checkout page!",
                f"🔥 STOCK ALERT - {platform} 🔥",
                0x1000 | 0x40,  # MB_SYSTEMMODAL | MB_ICONINFORMATION
            )
        except Exception:
            pass

    threading.Thread(target=show_popup, daemon=True).start()

    # 3. Continuous sound alert
    if enable_sound and HAS_WINSOUND:
        for _ in range(10):
            try:
                winsound.Beep(1200, 350)
                time.sleep(0.1)
                winsound.Beep(1600, 450)
                time.sleep(0.1)
            except Exception:
                break


def check_reliance_digital(client: RelianceClient, pincode: str) -> Tuple[bool, str]:
    """
    Checks Reliance Digital's live inventory API directly.
    Returns (is_in_stock, message).
    """
    try:
        sizes = client.get_product_sizes(RELIANCE_SLUG)
        if sizes:
            qty = sizes[0].get("quantity", 0)
            avail = sizes[0].get("is_available", False)
            if avail and qty > 0:
                # Also verify delivery for this specific pincode
                deliv = client.check_delivery(RELIANCE_SLUG, "OS", pincode)
                if deliv.get("status") == "AVAILABLE":
                    return True, f"IN STOCK ({qty} units available for PIN {pincode})"
                return True, f"IN STOCK ({qty} units in central warehouse)"
            return False, f"Out of Stock (Quantity: {qty})"
        return False, "Out of Stock (No active listings)"
    except Exception as e:
        return False, f"Check error ({e})"


def check_flipkart() -> Tuple[bool, str]:
    """
    Checks Flipkart for live, buyable listings of the target model.
    """
    try:
        req = urllib.request.Request(FLIPKART_URL, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as res:
            raw = res.read()
            if res.info().get("Content-Encoding") == "gzip":
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            html = raw.decode("utf-8", errors="ignore")

            # Check if this exact product is listed
            has_model = TARGET_MPN in html or TARGET_MODEL in html
            if has_model:
                # Check for out of stock signals
                is_oos = (
                    "Currently unavailable" in html
                    or "Out of Stock" in html
                    or "Sold Out" in html
                    or "Coming Soon" in html
                )
                if not is_oos:
                    return True, "IN STOCK / Buyable listing found!"
                return False, "Listed but Currently Unavailable / Out of Stock"
            return False, "Not currently listed in active catalog"
    except Exception as e:
        return False, f"Check error ({e})"


def check_vijay_sales() -> Tuple[bool, str]:
    """
    Checks Vijay Sales catalog for active buy status.
    """
    try:
        req = urllib.request.Request(VIJAY_SALES_URL, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as res:
            raw = res.read()
            if res.info().get("Content-Encoding") == "gzip":
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
            html = raw.decode("utf-8", errors="ignore")

            if TARGET_MPN in html or TARGET_MODEL in html:
                if "Add to Cart" in html or "Buy Now" in html:
                    return True, "IN STOCK / Buy button active!"
                return False, "Listed but Out of Stock / In-store only"
            return False, "Not listed online"
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "Page 404 (No active listing)"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"Check error ({e})"


def check_acer_store() -> Tuple[bool, str]:
    """
    Checks the official Acer India Online Store for catalog presence and stock.
    """
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
                return False, "Listed but Out of Stock"
            return False, "Not currently in online inventory"
    except Exception as e:
        return False, f"Check error ({e})"


def run_sniper(interval_seconds: int = 180, pincode: str = "360005", enable_sound: bool = True):
    client = RelianceClient()
    cycle = 0

    print(f"{BOLD}{'='*70}{RESET}")
    print(f"{CYAN}{BOLD}🎯 MULTI-PLATFORM STOCK SNIPER STARTED{RESET}")
    print(f"{BOLD}Target Laptop:{RESET} {TARGET_NAME}")
    print(f"{BOLD}Part Number:{RESET}   {TARGET_MPN} (Model: {TARGET_MODEL})")
    print(f"{BOLD}Specs:{RESET}         Intel Core Ultra 7 255HX | RTX 5060 | 16 GB | 1 TB SSD")
    print(f"{BOLD}Check Interval:{RESET}{interval_seconds} seconds")
    print(f"{BOLD}Target PIN:{RESET}    {pincode}")
    print(f"{BOLD}Platforms:{RESET}     Reliance Digital, Flipkart, Vijay Sales, Acer Store")
    print(f"{BOLD}{'='*70}{RESET}\n")
    print(f"{YELLOW}Bot is actively monitoring in the background. Press Ctrl+C to stop.{RESET}\n")

    while True:
        cycle += 1
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{now_str}] Cycle #{cycle} | Scanning all platforms...")

        # 1. Reliance Digital
        rd_stock, rd_msg = check_reliance_digital(client, pincode)
        rd_color = GREEN if rd_stock else RED
        print(f"  • Reliance Digital: {rd_color}{rd_msg}{RESET}")
        if rd_stock:
            trigger_alarm("Reliance Digital", RELIANCE_URL, enable_sound)
            time.sleep(60)

        # 2. Flipkart
        fk_stock, fk_msg = check_flipkart()
        fk_color = GREEN if fk_stock else RED
        print(f"  • Flipkart:         {fk_color}{fk_msg}{RESET}")
        if fk_stock:
            trigger_alarm("Flipkart", FLIPKART_URL, enable_sound)
            time.sleep(60)

        # 3. Vijay Sales
        vs_stock, vs_msg = check_vijay_sales()
        vs_color = GREEN if vs_stock else RED
        print(f"  • Vijay Sales:      {vs_color}{vs_msg}{RESET}")
        if vs_stock:
            trigger_alarm("Vijay Sales", VIJAY_SALES_URL, enable_sound)
            time.sleep(60)

        # 4. Acer Store
        ac_stock, ac_msg = check_acer_store()
        ac_color = GREEN if ac_stock else RED
        print(f"  • Acer India Store: {ac_color}{ac_msg}{RESET}")
        if ac_stock:
            trigger_alarm("Acer Official Store", ACER_STORE_URL, enable_sound)
            time.sleep(60)

        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Next check in {interval_seconds}s...\n")
        try:
            time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Sniper stopped by user. Goodbye!{RESET}")
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="Automated multi-platform stock sniper for Acer Predator Helios Neo 16S AI."
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=180,
        help="Interval between stock scans in seconds (default: 180s = 3 minutes).",
    )
    parser.add_argument(
        "-p",
        "--pincode",
        type=str,
        default="360005",
        help="Pincode to check serviceability for (default: 360005).",
    )
    parser.add_argument(
        "--no-sound",
        action="store_true",
        help="Disable audible beeping alarm when stock is detected.",
    )
    parser.add_argument(
        "--test-alert",
        action="store_true",
        help="Test the audio alarm, popup, and browser opening mechanism immediately.",
    )

    args = parser.parse_args()

    if args.test_alert:
        print(f"{CYAN}Testing alert mechanisms (audio, browser open, popup)...{RESET}")
        trigger_alarm("TEST SIMULATION", RELIANCE_URL, enable_sound=not args.no_sound)
        sys.exit(0)

    run_sniper(
        interval_seconds=args.interval,
        pincode=args.pincode,
        enable_sound=not args.no_sound,
    )


if __name__ == "__main__":
    main()
