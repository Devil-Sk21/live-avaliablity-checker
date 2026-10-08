"""
Reliance Digital API Client
Handles FDK request authentication (HMAC-SHA256 signing),
product search, product detail retrieval, variant resolution,
and pincode-level delivery availability checking.
"""

import base64
import datetime
import hashlib
import hmac
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


class RelianceClient:
    APP_ID = "645a057875d8c4882b096f7e"
    APP_TOKEN = "__-O44-4i"
    SECRET = "1234567"
    HOST = "www.reliancedigital.in"

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.auth_token = base64.b64encode(
            f"{self.APP_ID}:{self.APP_TOKEN}".encode("utf-8")
        ).decode("utf-8")

    def _sign_request(
        self,
        method: str,
        path: str,
        query_params: Optional[Dict[str, Any]] = None,
        body: str = "",
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[Dict[str, str], str]:
        """
        Signs the request following Reliance Digital's FDK HMAC-SHA256 protocol.
        """
        if extra_headers is None:
            extra_headers = {}

        now = datetime.datetime.now(datetime.timezone.utc)
        fp_date = now.strftime("%Y%m%dT%H%M%SZ")

        # Canonical query string
        query_str = ""
        if query_params:
            sorted_keys = sorted(query_params.keys())
            parts = []
            for k in sorted_keys:
                val = query_params[k]
                if isinstance(val, list):
                    for item in sorted(val):
                        parts.append(f"{k}={urllib.parse.quote(str(item), safe='')}")
                else:
                    parts.append(f"{k}={urllib.parse.quote(str(val), safe='')}")
            query_str = "&".join(parts)

        # Body hash
        body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

        # Headers to sign: 'host' and any 'x-fp-.*' headers
        headers_to_sign = {
            "host": self.HOST,
            "x-fp-date": fp_date,
            **{
                k.lower(): v
                for k, v in extra_headers.items()
                if k.lower().startswith("x-fp-")
            },
        }

        included_header_keys = sorted(headers_to_sign.keys())
        canonical_headers = (
            "\n".join(
                f"{h}:{headers_to_sign[h].strip()}" for h in included_header_keys
            )
            + "\n"
        )
        signed_headers = ";".join(included_header_keys)

        canonical_request = "\n".join(
            [
                method.upper(),
                path,
                query_str,
                canonical_headers,
                signed_headers,
                body_hash,
            ]
        )

        string_to_sign = f"{fp_date}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
        signature = f"v1:{hmac.new(self.SECRET.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()}"

        request_headers = {
            "Host": self.HOST,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "x-application-id": self.APP_ID,
            "x-application-token": self.APP_TOKEN,
            "x-fp-date": fp_date,
            "x-fp-signature": signature,
            "Authorization": f"Bearer {self.auth_token}",
            **extra_headers,
        }

        return request_headers, query_str

    def _make_request(
        self,
        method: str,
        path: str,
        query_params: Optional[Dict[str, Any]] = None,
        body: str = "",
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Executes an HTTP request and returns (status_code, json_response).
        """
        headers, query_str = self._sign_request(
            method, path, query_params, body, extra_headers
        )
        url = f"https://{self.HOST}{path}"
        if query_str:
            url = f"{url}?{query_str}"

        req_body = body.encode("utf-8") if body else None
        req = urllib.request.Request(
            url, data=req_body, headers=headers, method=method
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                content = response.read().decode("utf-8", errors="ignore")
                data = json.loads(content) if content else {}
                return response.status, data
        except urllib.error.HTTPError as e:
            content = e.read().decode("utf-8", errors="ignore")
            try:
                data = json.loads(content)
            except Exception:
                data = {"message": content or str(e)}
            return e.code, data
        except Exception as e:
            return 500, {"message": str(e)}

    def search_products(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for products on Reliance Digital matching a keyword or phrase.
        """
        path = "/api/service/application/catalog/v1.0/products"
        status, data = self._make_request("GET", path, query_params={"q": query})
        if status == 200:
            items = data.get("items", [])
            return items[:limit]
        return []

    def get_product_detail(self, slug: str) -> Optional[Dict[str, Any]]:
        """
        Fetches detailed product metadata by slug.
        """
        path = f"/api/service/application/catalog/v1.0/products/{slug}"
        status, data = self._make_request("GET", path)
        if status == 200:
            return data
        return None

    def get_product_sizes(self, slug: str) -> List[Dict[str, Any]]:
        """
        Fetches available sizes/variants for a product slug.
        """
        path = f"/api/service/application/catalog/v1.0/products/{slug}/sizes/"
        status, data = self._make_request("GET", path)
        if status == 200:
            return data.get("sizes", [])
        return []

    def check_delivery(
        self, slug: str, size: str, pincode: str
    ) -> Dict[str, Any]:
        """
        Checks delivery availability, stock, and turnaround time for a specific pincode.
        """
        pincode = str(pincode).strip()
        loc_header = json.dumps({"country_iso_code": "IN", "pincode": pincode})
        path = f"/api/service/application/catalog/v3.0/products/{slug}/sizes/{size}/price/"

        status, data = self._make_request(
            "GET", path, extra_headers={"x-location-detail": loc_header}
        )

        result = {
            "pincode": pincode,
            "is_serviceable": False,
            "status": "UNSERVICEABLE",
            "stock": 0,
            "effective_price": None,
            "marked_price": None,
            "cod_available": False,
            "delivery_min": None,
            "delivery_max": None,
            "store_name": None,
            "courier_partners": [],
            "message": "",
        }

        if status == 200:
            is_serv = data.get("is_serviceable", False)
            qty = data.get("quantity", 0)
            price_info = data.get("price") if isinstance(data.get("price"), dict) else {}
            promise = data.get("delivery_promise") if isinstance(data.get("delivery_promise"), dict) else {}
            store = data.get("store") if isinstance(data.get("store"), dict) else {}
            
            couriers = []
            for c in data.get("courier_partners", []):
                if isinstance(c, dict) and c.get("name"):
                    couriers.append(c["name"])
                elif isinstance(c, str):
                    couriers.append(c)

            min_dt = promise.get("min") if isinstance(promise, dict) else None
            max_dt = promise.get("max") if isinstance(promise, dict) else None

            result.update(
                {
                    "is_serviceable": is_serv,
                    "status": "AVAILABLE" if (is_serv and qty > 0) else "OUT_OF_STOCK",
                    "stock": qty,
                    "effective_price": price_info.get("effective"),
                    "marked_price": price_info.get("marked"),
                    "cod_available": data.get("is_cod", False),
                    "delivery_min": min_dt[:10] if isinstance(min_dt, str) else None,
                    "delivery_max": max_dt[:10] if isinstance(max_dt, str) else None,
                    "store_name": store.get("name") if isinstance(store, dict) else str(store or ""),
                    "courier_partners": couriers,
                    "message": "In Stock & Serviceable" if qty > 0 else "Out of Stock",
                }
            )
        elif status == 400:
            msg = data.get("message", "Not serviceable at given locality")
            if "out of stock" in msg.lower():
                result["status"] = "OUT_OF_STOCK"
                result["message"] = "Out of Stock"
            else:
                result["status"] = "UNSERVICEABLE"
                result["message"] = msg
        else:
            result["status"] = "ERROR"
            result["message"] = data.get("message", f"HTTP {status}")

        return result
