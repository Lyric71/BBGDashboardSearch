"""
Shared utilities for DataForSEO SERP reports.
"""
import http.client, json, base64, re, time
from collections import defaultdict
from datetime import date
from pathlib import Path

# ── Credentials ───────────────────────────────────────────────────────────────
LOGIN    = "cyril.drouin@beyondbordergroup.com"
PASSWORD = "9e6796d9d94cf3e3"
CREDENTIALS = base64.b64encode(f"{LOGIN}:{PASSWORD}".encode()).decode()
BBG = "beyondbordergroup.com"

REPORTS_DIR = Path(__file__).parent.parent / "reports"

SKIP_DOMAINS = {
    "google.com", "google.co", "youtube.com", "linkedin.com", "facebook.com",
    "wikipedia.org", "reddit.com", "quora.com", "amazon.com", "yelp.com",
    "sortlist.com", "clutch.co", "goodfirms.co", "designrush.com",
    "forbes.com", "medium.com", "hubspot.com",
}

# ── API ───────────────────────────────────────────────────────────────────────
def api_post(endpoint, payload):
    conn = http.client.HTTPSConnection("api.dataforseo.com", timeout=60)
    conn.request("POST", endpoint, json.dumps(payload), {
        "Authorization": f"Basic {CREDENTIALS}",
        "Content-Type": "application/json",
    })
    data = json.loads(conn.getresponse().read().decode())
    conn.close()
    return data

def check_task(data, keyword=""):
    """Return (ok, items_or_error)."""
    try:
        task = data["tasks"][0]
        code = task.get("status_code")
        if code == 20000:
            items = task["result"][0].get("items", [])
            return True, items
        msg = task.get("status_message", "unknown error")
        print(f"  ! API error [{code}] {msg}  kw={keyword!r}")
        return False, []
    except Exception as e:
        print(f"  ! Parse error: {e}")
        return False, []

def get_serp(keyword, location_code=2840, language_code="en"):
    data = api_post("/v3/serp/google/organic/live/regular", [{
        "keyword": keyword,
        "location_code": location_code,
        "language_code": language_code,
        "device": "desktop",
        "depth": 100,
    }])
    ok, items = check_task(data, keyword)
    return ok, [i for i in items if i.get("type") == "organic"]

def get_volumes(keywords, location_code=2840, language_code="en"):
    data = api_post("/v3/keywords_data/google_ads/search_volume/live", [{
        "keywords": keywords,
        "location_code": location_code,
        "language_code": language_code,
    }])
    volumes = {}
    try:
        task = data["tasks"][0]
        if task.get("status_code") != 20000:
            print(f"  ! Volume API error [{task.get('status_code')}] {task.get('status_message')}")
            return volumes
        for item in (task["result"][0].get("result") or task["result"]):
            kw   = item.get("keyword", "").lower()
            volumes[kw] = {
                "volume":      item.get("search_volume") or 0,
                "cpc":         round(item.get("cpc") or 0, 2),
                "competition": item.get("competition_index") or 0,
            }
    except Exception as e:
        print(f"  ! Volume parse error: {e}")
    return volumes

# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_domain(url):
    try:
        d = url.split("/")[2].lower()
        return re.sub(r'^www\.', '', d)
    except Exception:
        return ""

def is_skip(domain):
    return any(s in domain for s in SKIP_DOMAINS)

def discover_top_competitors(organic_lists, top_n=10):
    appearances = defaultdict(int)
    rank_sum    = defaultdict(int)
    for items in organic_lists:
        seen = set()
        for item in items:
            d    = extract_domain(item.get("url", ""))
            rank = item.get("rank_absolute", 999)
            if not d or d == BBG or is_skip(d):
                continue
            if d not in seen:
                appearances[d] += 1
                rank_sum[d]    += rank
                seen.add(d)
    scored = []
    for d, count in appearances.items():
        avg   = rank_sum[d] / count
        score = count * 100 - avg
        scored.append((d, count, round(avg, 1), round(score, 1)))
    scored.sort(key=lambda x: -x[3])
    return [d for d, *_ in scored[:top_n]], appearances, rank_sum

def fmt(r):
    if r is None: return "—"
    if r <= 3:    return f"**{r}**"
    if r <= 10:   return str(r)
    return f"*{r}*"

# ── Report builder ────────────────────────────────────────────────────────────
def build_report(group_name, keywords, location_code, language_code):
    print(f"\n{'='*60}")
    print(f"GROUP: {group_name}  ({len(keywords)} kw) [{language_code.upper()}]")
    print('='*60)

    # 1. Fetch SERP
    organic_cache = {}
    failed = []
    for kw in keywords:
        print(f"  SERP -> {kw}")
        ok, items = get_serp(kw, location_code, language_code)
        organic_cache[kw] = items
        if not ok:
            failed.append(kw)
        time.sleep(0.5)

    if failed:
        print(f"\n  WARNING: {len(failed)} keywords failed: {failed}")
        if len(failed) == len(keywords):
            print("  All keywords failed — check DataForSEO credits. Aborting.")
            return None

    # 2. Discover competitors
    print(f"\n  Discovering top competitors...")
    top10, appearances, rank_sum = discover_top_competitors(
        list(organic_cache.values()), top_n=10
    )
    print(f"  Top 10: {', '.join(top10) or '(none found)'}")

    # 3. Search volumes
    print(f"  Fetching search volumes...")
    volumes = get_volumes(keywords, location_code, language_code)

    # 4. Extract ranks
    tracked = [BBG] + top10
    results = {}
    for kw in keywords:
        items = organic_cache[kw]
        ranks     = {d: None for d in tracked}
        top_domain = extract_domain(items[0].get("url", "")) if items else "—"
        for item in items:
            url  = item.get("url", "")
            rank = item.get("rank_absolute")
            for d in tracked:
                if d in url and ranks[d] is None:
                    ranks[d] = rank
        results[kw] = {"ranks": ranks, "top_domain": top_domain}

    # 5. Build markdown
    today     = date.today().strftime("%Y-%m-%d")
    loc_label = "France (FR)" if location_code == 2250 else "Global (EN)"
    cols      = ["Volume", "CPC", "Comp.", "#1 Domain", BBG] + top10
    header    = "| Keyword | " + " | ".join(cols) + " |"
    sep       = "|---------|" + "|".join(["---"] * len(cols)) + "|"

    lines = [
        f"# SERP Report — {group_name.replace('-', ' ').title()}",
        f"Date: {today} | google.com | {loc_label} | Depth: 100",
        "",
        "**Bold** = top 3 · plain = top 10 · *italic* = 11–100 · — = not ranked",
        "",
        header, sep,
    ]
    for kw in keywords:
        v   = volumes.get(kw.lower(), {})
        row = [
            f"{v.get('volume', 0):,}" if v.get("volume") else "—",
            f"${v.get('cpc', 0):.2f}" if v.get("cpc") else "—",
            str(v.get("competition", "—")),
            results[kw]["top_domain"] or "—",
        ]
        for d in tracked:
            row.append(fmt(results[kw]["ranks"][d]))
        lines.append("| " + kw + " | " + " | ".join(row) + " |")

    lines += [
        "",
        "## Top 10 Competitors (auto-discovered)",
        "",
        "| Rank | Domain | Appearances | Avg Position |",
        "|------|--------|-------------|--------------|",
    ]
    for i, d in enumerate(top10, 1):
        c   = appearances[d]
        avg = round(rank_sum[d] / c, 1) if c else "—"
        lines.append(f"| {i} | {d} | {c}/{len(keywords)} | {avg} |")

    report = "\n".join(lines)

    # Save
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORTS_DIR / f"serp_ranks_{group_name}.md"
    out.write_text(report, encoding="utf-8")
    print(f"\n  Saved -> {out}")
    return report
