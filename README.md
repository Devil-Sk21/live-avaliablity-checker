# Reliance Digital Delivery & Pincode Availability Checker

A high-performance Python script to check product delivery serviceability across major cities in **every State and Union Territory in India** on **Reliance Digital** (`reliancedigital.in`).

---

## 🌟 Key Features

- **Live Reliance Digital Integration**: Uses Reliance Digital's actual FDK HMAC-SHA256 authenticated API for accurate, real-time stock and delivery serviceability checks.
- **Pan-India Coverage**: Pre-loaded with over 120+ cities across all **28 States and 8 Union Territories**.
- **Flexible Product Input**:
  - Direct Reliance Digital product URLs (e.g. `https://www.reliancedigital.in/product/apple-iphone-15-...`)
  - Product slugs
  - Product search keywords (e.g. `Sony WH-1000XM5`, `MacBook Air M3`, `Samsung S24`)
- **Rich Delivery Information**:
  - Availability status (`AVAILABLE`, `OUT OF STOCK`, `UNSERVICEABLE`)
  - Live stock quantity
  - Effective selling price & MRP
  - Estimated delivery date (min/max delivery promise)
  - Cash on Delivery (COD) eligibility
  - Fulfillment store / distribution center name
- **High Performance & Multi-threaded**: Uses concurrent worker threads to quickly check all locations without getting blocked.
- **Export Options**: Export full results to CSV or JSON.

---

## 📁 Project Structure

```text
reliance_digital_checker/
├── stock_sniper.py       # Multi-platform 24/7 automated stock sniper & alert bot
├── reliance_checker.py   # Main CLI tool & nationwide delivery scanner
├── reliance_client.py    # Reliance Digital signed API client
├── pincodes_india.py     # Database of 120+ cities & PIN codes across all 36 States/UTs
└── README.md             # Documentation & usage guide
```

---

## 🎯 24/7 Automated Stock Sniper (`stock_sniper.py`)

Monitors **Reliance Digital**, **Flipkart**, **Vijay Sales**, and the **Acer Official Online Store** in a continuous loop:
- **Audible Beep Alarm**: Plays a loud, continuous audio chime on your computer the second stock appears.
- **Auto-Opens Browser**: Immediately pops open the exact checkout/purchase page in your default browser.
- **System Notification Popup**: Displays a Windows alert dialog.

### To start monitoring:
```bash
python stock_sniper.py
```

### Options:
* Change check interval (e.g. every 60 seconds):
  ```bash
  python stock_sniper.py --interval 60
  ```
* Specify your personal pincode:
  ```bash
  python stock_sniper.py --pincode 560001
  ```
* Test the alarm, popup, and browser opening mechanism:
  ```bash
  python stock_sniper.py --test-alert
  ```

---

## 🚀 How to Use

### 1. Interactive Mode
Run the script without arguments and it will prompt you for the product name or URL:
```bash
python reliance_checker.py
```

### 2. Check by Product URL (Entire India)
Check availability across all states and union territories in India:
```bash
python reliance_checker.py --product "https://www.reliancedigital.in/product/apple-iphone-fine-woven-magsafe-mobile-wallet-burgundy-mtveiu-10611105"
```

### 3. Check by Search Keyword & Export to CSV
Search for any product and export the results to CSV:
```bash
python reliance_checker.py --product "Sony WH-1000XM5" --export delivery_status.csv
```

### 4. Filter by Specific States
Check delivery only in chosen states (comma-separated):
```bash
python reliance_checker.py --product "iPhone 15" --states "Maharashtra,Karnataka,Delhi,Tamil Nadu"
```

### 5. Show Only Available Locations
Hide out-of-stock and unserviceable areas:
```bash
python reliance_checker.py --product "Sony WH-1000XM5" --available-only
```

### 6. Adjust Worker Threads
Speed up or slow down checks using `--workers`:
```bash
python reliance_checker.py --product "Sony WH-1000XM5" --workers 8
```

### 7. Use a Custom Pincodes File
Pass your own list of pincodes in CSV or JSON format:
```bash
python reliance_checker.py --product "Sony WH-1000XM5" --pincodes-file custom_pins.csv
```

*(Custom CSV format: `state,city,pincode`)*

---

## 📊 Sample Output

```text
============================================================
Product: Apple iPhone Fine Woven MagSafe Mobile Wallet, Burgundy
Slug:    apple-iphone-fine-woven-magsafe-mobile-wallet-burgundy-mtveiu-10611105
Variant: OS
============================================================

Loaded 12 locations to check across 3 states/UTs.
Checking delivery serviceability using 5 concurrent workers...

+--------------------+------------------+----------+-----------------+---------+---------------+----------------+--------+----------------------------+
| State              | City             | PIN      | Status          | Stock   | Price (INR)   | Est. Delivery  | COD    | Notes                      |
+--------------------+------------------+----------+-----------------+---------+---------------+----------------+--------+----------------------------+
| Assam              | Dibrugarh        | 786001   | AVAILABLE       |       2 |     Rs. 6,900 | 2026-10-10     | Yes    | In Stock & Serviceable     |
|                    | Guwahati         | 781001   | AVAILABLE       |       2 |     Rs. 6,900 | 2026-10-10     | Yes    | In Stock & Serviceable     |
|                    | Jorhat           | 785001   | AVAILABLE       |       2 |     Rs. 6,900 | 2026-10-10     | Yes    | In Stock & Serviceable     |
|                    | Silchar          | 788001   | AVAILABLE       |       2 |     Rs. 6,900 | 2026-10-10     | Yes    | In Stock & Serviceable     |
|                    | Tezpur           | 784001   | AVAILABLE       |       2 |     Rs. 6,900 | 2026-10-10     | Yes    | In Stock & Serviceable     |
| Goa                | Mapusa           | 403507   | OUT OF STOCK    |       - |             - | -              | No     | Out of Stock               |
|                    | Margao           | 403601   | AVAILABLE       |       2 |     Rs. 6,900 | 2026-10-10     | Yes    | In Stock & Serviceable     |
|                    | Panaji           | 403001   | OUT OF STOCK    |       - |             - | -              | No     | Out of Stock               |
|                    | Vasco da Gama    | 403802   | OUT OF STOCK    |       - |             - | -              | No     | Out of Stock               |
| Jammu and Kashmir  | Anantnag         | 192101   | OUT OF STOCK    |       - |             - | -              | No     | Out of Stock               |
|                    | Jammu            | 180001   | AVAILABLE       |       2 |     Rs. 6,900 | 2026-10-10     | Yes    | In Stock & Serviceable     |
|                    | Srinagar         | 190001   | OUT OF STOCK    |       - |             - | -              | No     | Out of Stock               |
+--------------------+------------------+----------+-----------------+---------+---------------+----------------+--------+----------------------------+

=== Availability Summary ===
  • Total Locations Checked: 12
  • Available for Delivery:  7 (58.3%)
  • Out of Stock:            5 (41.7%)
  • Unserviceable:           0 (0.0%)
```

---

## ⚙️ Dependencies

Only uses Python standard library modules (`urllib`, `hashlib`, `hmac`, `concurrent.futures`, `json`, `csv`, `argparse`). No third-party packages required!
