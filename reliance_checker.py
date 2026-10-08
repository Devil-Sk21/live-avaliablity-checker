#!/usr/bin/env python3
"""
Reliance Digital Delivery & Pincode Availability Checker
Checks delivery serviceability for a specific product across cities in every state/UT in India.
"""

import argparse
import concurrent.futures
import csv
import json
import os
import re
import sys
import time
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple

from pincodes_india import INDIA_PINCODES
from reliance_client import RelianceClient

# ANSI colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def format_status(status: str) -> str:
    if status == "AVAILABLE":
        return f"{GREEN}{BOLD}AVAILABLE{RESET}"
    elif status == "OUT_OF_STOCK":
        return f"{YELLOW}OUT OF STOCK{RESET}"
    elif status == "UNSERVICEABLE":
        return f"{RED}UNSERVICEABLE{RESET}"
    else:
        return f"{RED}ERROR{RESET}"


def extract_slug(input_str: str) -> str:
    """
    Extracts the product slug from a full URL, or returns the string if already a slug.
    """
    input_str = input_str.strip()
    # Check if URL
    if input_str.startswith("http://") or input_str.startswith("https://"):
        # Pattern 1: /product/<slug>
        match = re.search(r"/product/([a-zA-Z0-9_\-]+)", input_str)
        if match:
            return match.group(1)
        # Pattern 2: /<slug>/p/<id>
        match2 = re.search(r"reliancedigital\.in/([a-zA-Z0-9_\-]+)/p/", input_str)
        if match2:
            return match2.group(1)
        # Fallback: last segment of URL path
        path = urllib.parse.urlparse(input_str).path.strip("/")
        segments = [s for s in path.split("/") if s]
        if segments:
            return segments[-1]
    return input_str


def resolve_product(
    client: RelianceClient, query_or_url: str
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Resolves product slug, title, and default size.
    Returns (slug, title, default_size).
    """
    slug = extract_slug(query_or_url)

    # First, test if it directly resolves as a product slug
    sizes = client.get_product_sizes(slug)
    if sizes:
        detail = client.get_product_detail(slug)
        title = detail.get("name", slug) if detail else slug
        first_size = sizes[0].get("value")
        return slug, title, first_size

    # Otherwise, treat input as a search query
    print(f"{CYAN}Searching Reliance Digital for: '{query_or_url}'...{RESET}")
    results = client.search_products(query_or_url, limit=5)
    if not results:
        return None, None, None

    # Found search results
    print(f"\n{BOLD}Matching Products Found:{RESET}")
    for idx, item in enumerate(results, 1):
        print(f"  [{idx}] {item.get('name')} (Brand: {item.get('brand', {}).get('name', 'N/A')})")

    chosen = results[0]
    chosen_slug = chosen.get("slug")
    chosen_name = chosen.get("name")
    sizes = client.get_product_sizes(chosen_slug)
    chosen_size = sizes[0].get("value") if sizes else "OS"

    print(f"\n{BOLD}Selected:{RESET} {chosen_name}")
    print(f"{BOLD}Slug:{RESET} {chosen_slug}")
    return chosen_slug, chosen_name, chosen_size


def load_pincodes(
    custom_file: Optional[str] = None,
    filter_states: Optional[List[str]] = None,
) -> List[Dict[str, str]]:
    """
    Loads pincodes from the default list or a custom JSON/CSV file.
    Optionally filters by state names.
    """
    pincodes: List[Dict[str, str]] = []

    if custom_file and os.path.exists(custom_file):
        if custom_file.endswith(".json"):
            with open(custom_file, "r", encoding="utf-8") as f:
                pincodes = json.load(f)
        elif custom_file.endswith(".csv"):
            with open(custom_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pincodes.append(
                        {
                            "state": row.get("state", "").strip(),
                            "city": row.get("city", "").strip(),
                            "pincode": row.get("pincode", "").strip(),
                        }
                    )
    else:
        pincodes = list(INDIA_PINCODES)

    if filter_states:
        filter_states_lower = [s.strip().lower() for s in filter_states]
        filtered = []
        for p in pincodes:
            st = p.get("state", "").lower()
            if any(fs in st for fs in filter_states_lower):
                filtered.append(p)
        return filtered

    return pincodes


def check_single_location(
    client: RelianceClient,
    slug: str,
    size: str,
    loc: Dict[str, str],
    delay: float = 0.05,
) -> Dict[str, Any]:
    """
    Worker function to check delivery for a single pincode.
    """
    time.sleep(delay)
    pincode = loc["pincode"]
    res = client.check_delivery(slug, size, pincode)
    return {
        "state": loc["state"],
        "city": loc["city"],
        **res,
    }


def export_results(results: List[Dict[str, Any]], export_path: str) -> None:
    """
    Exports check results to CSV or JSON format.
    """
    if export_path.endswith(".json"):
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    else:
        fields = [
            "state",
            "city",
            "pincode",
            "status",
            "stock",
            "effective_price",
            "marked_price",
            "delivery_min",
            "delivery_max",
            "cod_available",
            "store_name",
            "message",
        ]
        with open(export_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for r in results:
                writer.writerow(r)
    print(f"\n{GREEN}Results successfully exported to: {export_path}{RESET}")


def print_table(results: List[Dict[str, Any]], available_only: bool = False) -> None:
    """
    Prints a nicely formatted console table of delivery availability results.
    """
    display_list = [r for r in results if not available_only or r["status"] == "AVAILABLE"]

    if not display_list:
        print(f"\n{YELLOW}No matching locations found to display.{RESET}")
        return

    # Table headers
    headers = ["State", "City", "PIN", "Status", "Stock", "Price (INR)", "Est. Delivery", "COD", "Notes"]
    col_widths = [18, 16, 8, 15, 7, 13, 14, 6, 26]

    def make_row(cols: List[str]) -> str:
        row_str = " | ".join(f"{c:<{w}}" for c, w in zip(cols, col_widths))
        return f"| {row_str} |"

    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

    print("\n" + separator)
    print(make_row(headers))
    print(separator)

    current_state = None
    for r in display_list:
        state_str = r["state"]
        # Group by state visually
        if state_str != current_state:
            current_state = state_str
            state_display = state_str[: col_widths[0]]
        else:
            state_display = ""

        city_display = r["city"][: col_widths[1]]
        pin_display = str(r["pincode"])[: col_widths[2]]
        status_raw = r["status"]
        status_display = format_status(status_raw)
        # Raw width for padding
        padding = " " * (col_widths[3] - len(status_raw))
        status_padded = f"{status_display}{padding}"

        stock_display = str(r["stock"]) if r["stock"] > 0 else "-"
        price_display = f"Rs. {r['effective_price']:,.0f}" if r["effective_price"] else "-"
        del_display = r["delivery_max"] or r["delivery_min"] or "-"
        cod_display = "Yes" if r["cod_available"] else "No"
        notes_display = r["message"][: col_widths[8]]

        cols = [
            f"{state_display:<{col_widths[0]}}",
            f"{city_display:<{col_widths[1]}}",
            f"{pin_display:<{col_widths[2]}}",
            status_padded,
            f"{stock_display:>{col_widths[4]}}",
            f"{price_display:>{col_widths[5]}}",
            f"{del_display:<{col_widths[6]}}",
            f"{cod_display:<{col_widths[7]}}",
            f"{notes_display:<{col_widths[8]}}",
        ]
        print("| " + " | ".join(cols) + " |")

    print(separator)


def run_checker(
    product_input: str,
    size_input: Optional[str] = None,
    filter_states: Optional[List[str]] = None,
    available_only: bool = False,
    workers: int = 5,
    export_path: Optional[str] = None,
    custom_pincodes_file: Optional[str] = None,
) -> None:
    client = RelianceClient()

    # 1. Resolve product
    slug, title, default_size = resolve_product(client, product_input)
    if not slug:
        print(f"{RED}Error: Could not resolve product for '{product_input}'. Please check the URL or search query.{RESET}")
        return

    selected_size = size_input or default_size or "OS"

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}Product:{RESET} {title}")
    print(f"{BOLD}Slug:{RESET}    {slug}")
    print(f"{BOLD}Variant:{RESET} {selected_size}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    # 2. Load locations
    locations = load_pincodes(custom_pincodes_file, filter_states)
    total_locs = len(locations)
    print(f"Loaded {BOLD}{total_locs}{RESET} locations to check across {len(set(loc['state'] for loc in locations))} states/UTs.")
    print(f"Checking delivery serviceability using {workers} concurrent workers...\n")

    results: List[Dict[str, Any]] = []
    completed_count = 0

    # 3. Check delivery concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_loc = {
            executor.submit(
                check_single_location, client, slug, selected_size, loc
            ): loc
            for loc in locations
        }

        for future in concurrent.futures.as_completed(future_to_loc):
            completed_count += 1
            loc = future_to_loc[future]
            try:
                res = future.result()
                results.append(res)
                status_colored = format_status(res["status"])
                sys.stdout.write(
                    f"\r[{completed_count:3d}/{total_locs:3d}] "
                    f"Checked {loc['city']:<18} ({loc['pincode']}) -> {status_colored:<25}"
                )
                sys.stdout.flush()
            except Exception as e:
                results.append(
                    {
                        "state": loc["state"],
                        "city": loc["city"],
                        "pincode": loc["pincode"],
                        "status": "ERROR",
                        "stock": 0,
                        "effective_price": None,
                        "marked_price": None,
                        "cod_available": False,
                        "delivery_min": None,
                        "delivery_max": None,
                        "store_name": None,
                        "courier_partners": [],
                        "message": str(e),
                    }
                )

    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

    # Sort results by State and City
    results.sort(key=lambda x: (x["state"], x["city"]))

    # 4. Display Results Table
    print_table(results, available_only=available_only)

    # 5. Summary Statistics
    total = len(results)
    avail = sum(1 for r in results if r["status"] == "AVAILABLE")
    oos = sum(1 for r in results if r["status"] == "OUT_OF_STOCK")
    unserv = sum(1 for r in results if r["status"] == "UNSERVICEABLE")
    err = sum(1 for r in results if r["status"] == "ERROR")

    print(f"\n{BOLD}=== Availability Summary ==={RESET}")
    print(f"  • Total Locations Checked: {BOLD}{total}{RESET}")
    print(f"  • Available for Delivery:  {GREEN}{BOLD}{avail}{RESET} ({avail*100/total:.1f}%)")
    print(f"  • Out of Stock:            {YELLOW}{BOLD}{oos}{RESET} ({oos*100/total:.1f}%)")
    print(f"  • Unserviceable:           {RED}{BOLD}{unserv}{RESET} ({unserv*100/total:.1f}%)")
    if err > 0:
        print(f"  • Errors encountered:      {RED}{BOLD}{err}{RESET}")

    # 6. Export if requested
    if export_path:
        export_results(results, export_path)


def main():
    parser = argparse.ArgumentParser(
        description="Check product delivery availability on Reliance Digital across cities in all Indian states."
    )
    parser.add_argument(
        "-p",
        "--product",
        type=str,
        help="Product URL, slug, or search term (e.g. 'iphone 15' or 'https://www.reliancedigital.in/product/...')",
    )
    parser.add_argument(
        "--size",
        type=str,
        default=None,
        help="Product size/variant value (defaults to first available size)",
    )
    parser.add_argument(
        "-s",
        "--states",
        type=str,
        default=None,
        help="Comma-separated list of states to check (e.g. 'Maharashtra,Karnataka,Delhi'). Defaults to all 36 States/UTs.",
    )
    parser.add_argument(
        "--available-only",
        action="store_true",
        help="Only display cities/pincodes where the product is in stock and available for delivery.",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=5,
        help="Number of concurrent workers (default: 5).",
    )
    parser.add_argument(
        "-e",
        "--export",
        type=str,
        default=None,
        help="Path to export results (supports .csv or .json, e.g. results.csv).",
    )
    parser.add_argument(
        "--pincodes-file",
        type=str,
        default=None,
        help="Path to custom CSV/JSON file of pincodes to check.",
    )

    args = parser.parse_args()

    product_input = args.product
    if not product_input:
        print(f"{BOLD}=== Reliance Digital India-wide Delivery Checker ==={RESET}")
        product_input = input("Enter Reliance Digital Product URL or Name to search: ").strip()
        if not product_input:
            print("No product provided. Exiting.")
            sys.exit(1)

    filter_states = [s.strip() for s in args.states.split(",")] if args.states else None

    run_checker(
        product_input=product_input,
        size_input=args.size,
        filter_states=filter_states,
        available_only=args.available_only,
        workers=args.workers,
        export_path=args.export,
        custom_pincodes_file=args.pincodes_file,
    )


if __name__ == "__main__":
    main()
