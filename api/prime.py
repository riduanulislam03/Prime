
import os, json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

UPSTREAM = os.getenv("FREEFIRE_API_URL", "http://siambhau69.eu.cc/freefireinfo/bhau")
API_KEY = os.getenv("FREEFIRE_API_KEY", "")

REGIONS = {
    "BD":"Bangladesh", "IND":"India", "PK":"Pakistan", "SG":"Singapore",
    "ID":"Indonesia", "TH":"Thailand", "VN":"Vietnam", "TW":"Taiwan",
    "BR":"Brazil", "SAC":"South America", "US":"United States",
    "NA":"North America", "ME":"Middle East", "RU":"Russia",
    "CIS":"CIS", "EUROPE":"Europe"
}

def json_response(status, payload):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Cache-Control": "no-store, max-age=0"
        },
        "body": json.dumps(payload, ensure_ascii=False)
    }

def handler(request):
    # Vercel Python handler shape
    try:
        if getattr(request, "method", "GET") == "OPTIONS":
            return json_response(204, {})

        query = getattr(request, "args", {}) or {}
        uid = str(query.get("uid", "")).strip()
        region = str(query.get("region", "BD")).strip().upper()

        if not uid.isdigit() or not (5 <= len(uid) <= 15):
            return json_response(400, {
                "success": False,
                "error": "Valid Free Fire UID is required (5-15 digits)."
            })

        if region not in REGIONS:
            return json_response(400, {
                "success": False,
                "error": "Unsupported region.",
                "supported_regions": REGIONS
            })

        if not API_KEY:
            return json_response(500, {
                "success": False,
                "error": "Server API key is not configured.",
                "hint": "Set FREEFIRE_API_KEY in Vercel Environment Variables."
            })

        qs = urlencode({"uid": uid, "region": region, "key": API_KEY})
        req = Request(
            f"{UPSTREAM}?{qs}",
            headers={"User-Agent": "FreeFire-Prime-Checker/1.0", "Accept": "application/json"}
        )

        with urlopen(req, timeout=15) as response:
            raw = response.read().decode("utf-8", errors="replace")
            upstream = json.loads(raw)

        # The upstream documentation exposes primeInfo.primeLevel.
        basic = upstream.get("basicInfo") or {}
        prime_info = basic.get("primeInfo") or basic.get("prime_level") or {}
        prime_level = (
            prime_info.get("primeLevel")
            if isinstance(prime_info, dict)
            else prime_info
        )

        if prime_level is None:
            # Some APIs use snake_case.
            prime_level = basic.get("primeLevel")

        nickname = basic.get("nickname") or upstream.get("nickname")
        account_id = basic.get("accountId") or upstream.get("uid") or uid
        actual_region = basic.get("region") or upstream.get("region") or region

        return json_response(200, {
            "success": True,
            "uid": str(account_id),
            "requested_region": region,
            "region": actual_region,
            "region_name": REGIONS.get(actual_region, REGIONS[region]),
            "nickname": nickname,
            "prime_level": prime_level,
            "checked_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "source": "Free Fire player-data API",
            "raw_available": False
        })

    except HTTPError as e:
        return json_response(502, {
            "success": False,
            "error": "Upstream API returned an error.",
            "upstream_status": e.code
        })
    except (URLError, TimeoutError) as e:
        return json_response(504, {
            "success": False,
            "error": "Upstream API request timed out or failed."
        })
    except Exception as e:
        return json_response(502, {
            "success": False,
            "error": "Could not retrieve Prime Level.",
            "details": str(e)
        })

app = handler
          
