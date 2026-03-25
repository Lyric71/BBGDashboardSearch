"""
Group Report — Auto-discover top 10 competitors + search volumes
Usage: python seo/scripts/group_report.py
"""

import http.client, json, base64, time, re
from collections import defaultdict
from datetime import date

# Credentials
LOGIN    = "cyril.drouin@beyondbordergroup.com"
PASSWORD = "9e6796d9d94cf3e3"
CREDENTIALS = base64.b64encode(f"{LOGIN}:{PASSWORD}".encode()).decode()
BBG = "beyondbordergroup.com"

# ── Keyword Groups ────────────────────────────────────────────────
# Format: { "slug": {"keywords": [...], "location_code": int, "language_code": str} }
GROUPS = {
    "01-china-ecommerce-agency": {
        "keywords": [
            "china ecommerce consulting",
            "china ecommerce agency",
            "china ecommerce consultant",
            "ecommerce consulting china",
            "china ecommerce services",
            "china ecommerce strategy",
            "china ecommerce strategy consulting",
            "china ecommerce management",
            "china ecommerce solutions",
            "china ecommerce experts",
            "china ecommerce advisor",
        ],
        "location_code": 2840,   # USA / Global EN
        "language_code": "en",
    },
    "02-cross-border-ecommerce": {
        "keywords": [
            "china cross border ecommerce consulting",
            "cross border ecommerce china",
            "CBEC consulting china",
            "CBEC agency",
            "cross border ecommerce agency china",
            "cross border ecommerce agency",
            "china CBEC strategy",
            "china CBEC solutions",
            "cross border commerce china consultant",
        ],
        "location_code": 2840,
        "language_code": "en",
    },
    "03-market-entry": {
        "keywords": [
            "china market entry consulting",
            "china market entry agency",
            "china market entry strategy",
            "china market entry services",
            "enter chinese market",
            "entering the china market",
            "how to enter china market",
            "china market entry for brands",
            "china market expansion consulting",
            "launch brand in china",
            "china brand launch consulting",
            "market entry strategy china consulting",
            "china business entry consulting",
            "go to market strategy china",
        ],
        "location_code": 2840,
        "language_code": "en",
    },
}

SKIP_DOMAINS = {
    "google.com", "google.co", "youtube.com", "linkedin.com", "facebook.com",
    "wikipedia.org", "reddit.com", "quora.com", "amazon.com", "yelp.com",
    "sortlist.com", "clutch.co", "goodfirms.co", "designrush.com",
    "forbes.com", "medium.com", "hubspot.com",
}

# ── API helpers ───────────────────────────────────────────────────
def api_post(endpoint, payload):
    conn = http.client.HTTPSConnection("api.dataforseo.com")
    conn.request("POST", endpoint, json.dumps(payload), {
        "Authorization": f"Basic {CREDENTIALS}",
        "Content-Type": "application/json"
    })
    data = json.loads(conn.getresponse().read().decode())
    conn.close()
    return data

def get_serp(keyword, location_code=2840, language_code="en"):
    return api_post("/v3/serp/google/organic/live/regular", [{
        "keyword": keyword,
        "location_code": location_code,
        "language_code": language_code,
        "device": "desktop",
        "depth": 100,
    }])

def get_volumes(keywords, location_code=2840, language_code="en"):
    """Batch search volume lookup."""
    data = api_post("/v3/keywords_data/google_ads/search_volume/live", [{
        "keywords": keywords,
        "location_code": location_code,
        "language_code": language_code,
    }])
    volumes = {}
    try:
        for item in data["tasks"][0]["result"]:
            kw   = item.get("keyword", "")
            vol  = item.get("search_volume") or 0
            cpc  = item.get("cpc") or 0
            comp = item.get("competition_index") or 0
            volumes[kw.lower()] = {"volume": vol, "cpc": round(cpc, 2), "competition": comp}
    except Exception:
        pass
    return volumes

def extract_domain(url):
    try:
        d = url.split("/")[2].lower()
        d = re.sub(r'^www\.', '', d)
        return d
    except Exception:
        return ""

def extract_ranks(serp_data, domains):
    ranks = {d: None for d in domains}
    top_domain = None
    all_organic = []
    try:
        items = serp_data["tasks"][0]["result"][0]["items"]
        all_organic = [i for i in items if i.get("type") == "organic"]
        if all_organic:
            top_domain = extract_domain(all_organic[0].get("url", ""))
        for item in all_organic:
            url  = item.get("url", "")
            rank = item.get("rank_absolute")
            for d in domains:
                if d in url and ranks[d] is None:
                    ranks[d] = rank
    except Exception:
        pass
    return ranks, top_domain, all_organic

# ── Score domains to find top 10 ─────────────────────────────────
def discover_top_competitors(serp_results_list, top_n=10):
    """
    Score each domain by: appearances across keywords + position quality.
    Lower avg rank = better.
    """
    appearances = defaultdict(int)
    rank_sum    = defaultdict(int)

    for organic_items in serp_results_list:
        seen = set()
        for item in organic_items:
            url  = item.get("url", "")
            rank = item.get("rank_absolute", 999)
            d    = extract_domain(url)
            if not d or d == BBG:
                continue
            if any(skip in d for skip in SKIP_DOMAINS):
                continue
            if d not in seen:
                appearances[d] += 1
                rank_sum[d] += rank
                seen.add(d)

    # Score: appearances * 100 - avg_rank
    scored = []
    for d, count in appearances.items():
        avg_rank = rank_sum[d] / count
        score    = count * 100 - avg_rank
        scored.append((d, count, round(avg_rank, 1), round(score, 1)))

    scored.sort(key=lambda x: -x[2+1])  # sort by score desc
    return [d for d, *_ in scored[:top_n]]

# ── Format rank cell ──────────────────────────────────────────────
def fmt(r):
    if r is None:   return "—"
    if r <= 3:      return f"**{r}**"
    if r <= 10:     return str(r)
    return f"*{r}*"

# ── Main ──────────────────────────────────────────────────────────
def run_group(group_name, keywords, location_code=2840, language_code="en"):
    print(f"\n{'='*60}")
    print(f"GROUP: {group_name}  ({len(keywords)} keywords) [{language_code.upper()}]")
    print('='*60)

    # 1. SERP for every keyword
    serp_cache    = {}
    organic_cache = {}
    for kw in keywords:
        print(f"  SERP -> {kw}")
        data = get_serp(kw, location_code=location_code, language_code=language_code)
        serp_cache[kw] = data
        _, _, organic = extract_ranks(data, [])
        organic_cache[kw] = organic
        time.sleep(0.4)

    # 2. Discover top 10 competitors
    print(f"\n  Discovering top competitors...")
    top10 = discover_top_competitors(list(organic_cache.values()), top_n=10)
    print(f"  Top 10: {', '.join(top10)}")

    # 3. Search volumes (batch)
    print(f"  Fetching search volumes...")
    volumes = get_volumes(keywords, location_code=location_code, language_code=language_code)

    # 4. Extract ranks for BBG + top10
    tracked = [BBG] + top10
    results = {}
    for kw in keywords:
        ranks, top_domain, _ = extract_ranks(serp_cache[kw], tracked)
        results[kw] = {"ranks": ranks, "top_domain": top_domain}

    # 5. Build report
    today    = date.today().strftime("%Y-%m-%d")
    loc_label = "France (FR)" if location_code == 2250 else "Global (EN)"
    cols   = ["Volume", "CPC", "Comp.", "#1 Domain", BBG] + top10
    header = "| Keyword | " + " | ".join(cols) + " |"
    sep    = "|---------|" + "|".join(["---" for _ in cols]) + "|"

    lines = [
        f"# SERP Report — {group_name.replace('-', ' ').title()}",
        f"Date: {today} | google.com | {loc_label} | Depth: 100",
        "",
        "**Bold** = top 3 · plain = top 10 · *italic* = 11-100 · — = not ranked",
        "",
        header, sep
    ]

    for kw in keywords:
        v    = volumes.get(kw.lower(), {})
        vol  = f"{v.get('volume', 0):,}" if v.get('volume') else "—"
        cpc  = f"${v.get('cpc', 0):.2f}" if v.get('cpc') else "—"
        comp = str(v.get('competition', "—"))
        top  = results[kw]["top_domain"] or "—"
        row  = [vol, cpc, comp, top]
        for d in tracked:
            row.append(fmt(results[kw]["ranks"][d]))
        lines.append(f"| {kw} | " + " | ".join(row) + " |")

    # Competitor summary
    lines += [
        "",
        "## Top 10 Competitors (auto-discovered)",
        "",
        "| Rank | Domain | Appearances | Avg Position |",
        "|------|--------|-------------|--------------|",
    ]
    all_organic = list(organic_cache.values())
    scored_full = []
    appearances = defaultdict(int)
    rank_sum    = defaultdict(int)
    for organic_items in all_organic:
        seen = set()
        for item in organic_items:
            url  = item.get("url", "")
            rank = item.get("rank_absolute", 999)
            d    = extract_domain(url)
            if not d or any(skip in d for skip in SKIP_DOMAINS):
                continue
            if d not in seen:
                appearances[d] += 1
                rank_sum[d] += rank
                seen.add(d)
    for d in top10:
        c   = appearances[d]
        avg = round(rank_sum[d] / c, 1) if c else "—"
        scored_full.append((d, c, avg))
    for i, (d, c, avg) in enumerate(scored_full, 1):
        bbg_marker = " ← BBG" if d == BBG else ""
        lines.append(f"| {i} | {d}{bbg_marker} | {c}/{len(keywords)} | {avg} |")

    report = "\n".join(lines)

    # Save
    out_path = f"c:/Users/cyril/Project/GoogleSearch/seo/reports/serp_ranks_{group_name}.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n  Saved -> seo/reports/serp_ranks_{group_name}.md")
    return report

def main():
    for group_name, cfg in GROUPS.items():
        run_group(
            group_name,
            cfg["keywords"],
            location_code=cfg.get("location_code", 2840),
            language_code=cfg.get("language_code", "en"),
        )
    print("\n\nAll groups done.")

if __name__ == "__main__":
    main()
