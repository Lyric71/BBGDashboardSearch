"""
DataForSEO diagnostic script.
Makes one SERP call + one volume call and prints the full raw JSON response.
Usage: python seo/scripts/test_dataforseo.py
"""
import http.client, json, base64, time, sys
from pathlib import Path

LOGIN    = "cyril.drouin@beyondbordergroup.com"
PASSWORD = "9e6796d9d94cf3e3"
CREDENTIALS = base64.b64encode(f"{LOGIN}:{PASSWORD}".encode()).decode()

TEST_KEYWORD = "china ecommerce agency"
LOCATION_CODE = 2840
LANGUAGE_CODE = "en"

def api_post(endpoint, payload):
    print(f"\n  --> POST {endpoint}")
    print(f"      payload: {json.dumps(payload)[:200]}")
    t0 = time.time()
    try:
        conn = http.client.HTTPSConnection("api.dataforseo.com", timeout=30)
        conn.request("POST", endpoint, json.dumps(payload), {
            "Authorization": f"Basic {CREDENTIALS}",
            "Content-Type": "application/json",
        })
        resp = conn.getresponse()
        elapsed = time.time() - t0
        raw = resp.read().decode()
        conn.close()
        print(f"      HTTP {resp.status} in {elapsed:.2f}s  ({len(raw)} bytes)")
        return json.loads(raw), elapsed
    except Exception as e:
        elapsed = time.time() - t0
        print(f"      EXCEPTION after {elapsed:.2f}s: {e}")
        return None, elapsed

def dump(data, label):
    print(f"\n{'='*60}")
    print(f"  RAW RESPONSE: {label}")
    print('='*60)
    if data is None:
        print("  (no data — request failed)")
        return
    # Top-level keys
    print(f"  top-level keys: {list(data.keys())}")
    print(f"  status_code:    {data.get('status_code')}")
    print(f"  status_message: {data.get('status_message')}")
    print(f"  cost:           {data.get('cost')}")
    print(f"  tasks_count:    {data.get('tasks_count')}")
    tasks = data.get("tasks", [])
    print(f"  tasks count:    {len(tasks)}")
    for i, task in enumerate(tasks):
        print(f"\n  -- task[{i}] --")
        print(f"     status_code:    {task.get('status_code')}")
        print(f"     status_message: {task.get('status_message')}")
        print(f"     cost:           {task.get('cost')}")
        result = task.get("result")
        if result is None:
            print("     result: None")
        elif isinstance(result, list):
            print(f"     result: list of {len(result)}")
            if result:
                r0 = result[0]
                print(f"       result[0] keys: {list(r0.keys()) if isinstance(r0, dict) else type(r0)}")
                items = r0.get("items", []) if isinstance(r0, dict) else []
                print(f"       items count: {len(items)}")
                if items:
                    print(f"       items[0]: {json.dumps(items[0])[:300]}")
        else:
            print(f"     result type: {type(result)}")

# ── 1. SERP call ──────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  TEST 1: SERP organic live/regular")
print("="*60)
serp_payload = [{
    "keyword": TEST_KEYWORD,
    "location_code": LOCATION_CODE,
    "language_code": LANGUAGE_CODE,
    "device": "desktop",
    "depth": 100,
}]
serp_data, serp_time = api_post("/v3/serp/google/organic/live/regular", serp_payload)
dump(serp_data, "SERP")

# ── 2. Volume call ────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  TEST 2: Keywords search volume")
print("="*60)
vol_payload = [{
    "keywords": [TEST_KEYWORD],
    "location_code": LOCATION_CODE,
    "language_code": LANGUAGE_CODE,
}]
vol_data, vol_time = api_post("/v3/keywords_data/google_ads/search_volume/live", vol_payload)
dump(vol_data, "VOLUME")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  SUMMARY")
print("="*60)
print(f"  SERP call:   {serp_time:.2f}s")
print(f"  Volume call: {vol_time:.2f}s")
print(f"  Total:       {serp_time + vol_time:.2f}s")
