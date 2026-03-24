"""
SERP rank tracker — all keyword groups
For each group:
  1. Fetches top 100 SERP results for every keyword
  2. Scores all domains (higher score = more visible = higher positions)
  3. Picks top 10 competitors + always includes BBG
  4. Saves a rank report to reports/competitors/
"""

import http.client
import json
import base64
import time
import os
from collections import defaultdict

# --- Config ---
LOGIN = "cyril.drouin@beyondbordergroup.com"
PASSWORD = "9e6796d9d94cf3e3"
CREDENTIALS = base64.b64encode(f"{LOGIN}:{PASSWORD}".encode()).decode()
BBG = "beyondbordergroup.com"
REPORTS_DIR = "c:/Users/cyril/Project/GoogleSearch/reports/competitors"
DATE = "2026-03-23"

# --- Keyword groups ---
GROUPS = [
    {
        "id": "01-core-ecommerce-consulting",
        "label": "Core Ecommerce Consulting",
        "location_code": 2840,
        "language_code": "en",
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
    },
    {
        "id": "02-cbec-cross-border",
        "label": "Cross-Border Ecommerce (CBEC)",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "china cross border ecommerce consulting",
            "cross border ecommerce china",
            "CBEC consulting china",
            "CBEC agency",
            "cross border ecommerce agency china",
            "china CBEC strategy",
            "china CBEC solutions",
            "cross border commerce china consultant",
            "bonded warehouse china ecommerce",
            "direct mail ecommerce china",
        ],
    },
    {
        "id": "03-market-entry",
        "label": "Market Entry",
        "location_code": 2840,
        "language_code": "en",
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
    },
    {
        "id": "04-tmall",
        "label": "Tmall",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "tmall consulting",
            "tmall agency",
            "tmall partner agency",
            "sell on tmall",
            "tmall global consulting",
            "tmall setup consulting",
            "tmall store management",
            "tmall global agency",
            "how to sell on tmall",
            "tmall for foreign brands",
            "tmall market entry",
            "tmall partner",
            "tmall TP agency",
            "open store tmall",
        ],
    },
    {
        "id": "05-jd-com",
        "label": "JD.com",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "jd.com consulting",
            "jd.com agency",
            "sell on jd.com",
            "jd worldwide consulting",
            "jd.com partner agency",
            "how to sell on jd china",
            "jd.com store management",
        ],
    },
    {
        "id": "06-douyin",
        "label": "Douyin",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "douyin ecommerce consulting",
            "douyin agency",
            "douyin for brands",
            "douyin live commerce consulting",
            "douyin shop setup",
            "tiktok china ecommerce",
            "douyin marketing agency",
            "live commerce china consulting",
        ],
    },
    {
        "id": "07-xiaohongshu-red",
        "label": "Xiaohongshu / RED",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "xiaohongshu agency",
            "little red book agency",
            "RED china marketing",
            "xiaohongshu marketing consulting",
            "little red book marketing consulting",
            "xiaohongshu for brands",
            "RED ecommerce consulting",
        ],
    },
    {
        "id": "08-wechat-weibo",
        "label": "WeChat / Weibo",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "wechat marketing agency",
            "wechat consulting",
            "wechat store setup",
            "weibo marketing agency",
            "wechat mini program agency",
            "wechat ecommerce consulting",
            "china social media agency",
            "china social commerce consulting",
        ],
    },
    {
        "id": "09-pinduoduo-other",
        "label": "Pinduoduo & Other Platforms",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "pinduoduo consulting",
            "kaola consulting",
            "tmall global vs jd worldwide",
            "china ecommerce platform consulting",
        ],
    },
    {
        "id": "10-digital-marketing",
        "label": "Digital Marketing",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "china digital marketing agency",
            "china digital marketing consulting",
            "china digital marketing services",
            "china online marketing agency",
            "china seo agency",
            "china sem agency",
            "china ppc agency",
            "china kol marketing",
            "china influencer marketing agency",
            "china live streaming marketing",
            "china content marketing agency",
            "chinese digital strategy consulting",
            "china social media marketing agency",
            "china brand awareness consulting",
            "china performance marketing agency",
        ],
    },
    {
        "id": "11-distribution-ops",
        "label": "Distribution & Operations",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "china distributor consulting",
            "china distribution strategy",
            "find distributor in china",
            "china 3pl consulting",
            "china logistics consulting",
            "china warehousing consulting",
            "bonded warehouse china",
            "china fulfillment consulting",
            "china supply chain consulting",
            "china import consulting",
            "daigou china consulting",
        ],
    },
    {
        "id": "12-industry-audience",
        "label": "Industry & Audience",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "sell luxury brands in china",
            "sell beauty products in china",
            "sell fashion in china",
            "sell food in china ecommerce",
            "sell health products in china",
            "sell supplements in china ecommerce",
            "sell cosmetics in china",
            "foreign brand china ecommerce",
            "international brand china market",
            "western brand sell in china",
            "european brand china market entry",
            "canadian brand china market",
            "australian brand china market",
        ],
    },
    {
        "id": "13-research-strategy",
        "label": "Research & Strategy",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "china market research consulting",
            "china consumer insights agency",
            "china competitive analysis",
            "china market feasibility study",
            "china ecommerce market research",
            "china brand positioning consulting",
            "china market opportunity assessment",
            "china retail consulting",
            "china localization consulting",
            "china product localization",
        ],
    },
    {
        "id": "14-long-tail",
        "label": "Long-tail / High-Intent",
        "location_code": 2840,
        "language_code": "en",
        "keywords": [
            "how to sell products in china online",
            "how to list products on tmall global",
            "how to open tmall global store",
            "china ecommerce consulting for small brands",
            "china market entry consulting for startups",
            "best agency to sell in china",
            "china ecommerce agency for western brands",
            "how to find chinese distributor",
            "china ecommerce without entity",
            "sell in china without chinese company",
            "china cross border ecommerce without entity",
            "cbec vs general trade china",
            "tmall global vs jd worldwide which is better",
            "china ecommerce cost how much",
            "china market entry cost consulting",
            "is china ecommerce worth it for my brand",
        ],
    },
    {
        "id": "15-french",
        "label": "French (FR)",
        "location_code": 2250,  # France
        "language_code": "fr",
        "keywords": [
            "consulting ecommerce chine",
            "agence ecommerce chine",
            "entrer sur le marche chinois",
            "vendre en chine en ligne",
            "strategie marche chinois",
            "agence marketing chine",
            "consultant chine ecommerce",
            "vendre sur tmall",
            "agence tmall",
            "commerce transfrontalier chine",
            "lancer une marque en chine",
            "ecommerce chine pour les marques europeennes",
            "marketing digital chine",
            "agence digitale chine",
            "reseaux sociaux chinois marketing",
            "wechat marketing agence",
            "douyin agence france",
            "xiaohongshu agence",
            "marche chinois consulting",
            "entrer en chine sans entite juridique",
        ],
    },
]

# --- Helpers ---

def get_serp(keyword, location_code, language_code):
    conn = http.client.HTTPSConnection("api.dataforseo.com")
    payload = json.dumps([{
        "keyword": keyword,
        "location_code": location_code,
        "language_code": language_code,
        "device": "desktop",
        "depth": 100,
    }])
    headers = {
        "Authorization": f"Basic {CREDENTIALS}",
        "Content-Type": "application/json",
    }
    conn.request("POST", "/v3/serp/google/organic/live/regular", payload, headers)
    resp = conn.getresponse()
    data = json.loads(resp.read().decode())
    conn.close()
    return data


def extract_domain(url):
    try:
        d = url.split("/")[2].lower()
        return d.replace("www.", "")
    except Exception:
        return ""


def parse_serp(data):
    """Returns (top1_domain, {domain: rank}) for organic items only."""
    ranks = {}
    top1 = None
    try:
        items = data["tasks"][0]["result"][0]["items"]
        organic = [i for i in items if i.get("type") == "organic"]
        if organic:
            top1 = extract_domain(organic[0].get("url", ""))
        for item in organic:
            domain = extract_domain(item.get("url", ""))
            rank = item.get("rank_absolute")
            if domain and rank and domain not in ranks:
                ranks[domain] = rank
    except (KeyError, IndexError, TypeError):
        pass
    return top1, ranks


def score_domains(all_keyword_ranks):
    """Score each domain across all keywords in a group. Higher = more visible."""
    scores = defaultdict(int)
    appearances = defaultdict(int)
    for kw_ranks in all_keyword_ranks:
        for domain, rank in kw_ranks.items():
            if rank <= 100:
                scores[domain] += (101 - rank)
                appearances[domain] += 1
    return scores, appearances


def render_rank(r):
    if r is None:
        return "-"
    elif r <= 3:
        return f"**{r}**"
    elif r <= 10:
        return str(r)
    else:
        return f"*{r}*"


def build_report(group, keywords, top1s, keyword_ranks_list, top_domains):
    label = group["label"]
    lang = group["language_code"].upper()
    loc = "France" if group["location_code"] == 2250 else "Global English"

    cols = [BBG] + [d for d in top_domains if d != BBG]
    header = "| Keyword | #1 Domain | " + " | ".join(cols) + " |"
    sep = "|---------|-----------|" + "|".join(["------"] * len(cols)) + "|"

    lines = [
        f"# SERP Rank Report — {label}",
        f"Date: {DATE} | Language: {lang} | Location: {loc} | Depth: 100",
        "",
        header,
        sep,
    ]

    for kw, top1, ranks in zip(keywords, top1s, keyword_ranks_list):
        row = [render_rank(ranks.get(d)) for d in cols]
        lines.append(f"| {kw} | {top1 or '-'} | " + " | ".join(row) + " |")

    lines += [
        "",
        "---",
        "",
        "## Top Competitor Visibility Score",
        "",
        "| Domain | Score | Keywords Present |",
        "|--------|-------|-----------------|",
    ]

    scores, appearances = score_domains(keyword_ranks_list)
    sorted_domains = sorted(scores.items(), key=lambda x: -x[1])
    for domain, score in sorted_domains[:15]:
        lines.append(f"| {domain} | {score} | {appearances[domain]}/{len(keywords)} |")

    return "\n".join(lines)


# --- Main ---

total_kws = sum(len(g["keywords"]) for g in GROUPS)
print(f"Running {len(GROUPS)} groups, {total_kws} keywords total...\n")

for group in GROUPS:
    gid = group["id"]
    label = group["label"]
    keywords = group["keywords"]
    loc = group["location_code"]
    lang = group["language_code"]

    print(f"\n[{gid}] {label} ({len(keywords)} keywords)")

    top1s = []
    keyword_ranks_list = []
    domain_scores = defaultdict(int)
    domain_appearances = defaultdict(int)

    for kw in keywords:
        print(f"  > {kw}")
        data = get_serp(kw, loc, lang)
        top1, ranks = parse_serp(data)
        top1s.append(top1)
        keyword_ranks_list.append(ranks)

        for domain, rank in ranks.items():
            if rank <= 100:
                domain_scores[domain] += (101 - rank)
                domain_appearances[domain] += 1

        time.sleep(0.3)

    # Pick top 10 competitors by score (excluding BBG, will be added first)
    sorted_domains = sorted(
        [(d, s) for d, s in domain_scores.items() if d != BBG],
        key=lambda x: -x[1]
    )
    top_competitors = [d for d, _ in sorted_domains[:10]]

    # Build final domain list: BBG first, then top 10
    tracking_domains = [BBG] + top_competitors

    # Build report
    report = build_report(group, keywords, top1s, keyword_ranks_list, tracking_domains)

    filename = f"serp_ranks_{gid}.md"
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    bbg_ranks = [r.get(BBG) for r in keyword_ranks_list if r.get(BBG)]
    best = min(bbg_ranks) if bbg_ranks else None
    visible = len(bbg_ranks)
    print(f"  -> BBG visible on {visible}/{len(keywords)} keywords, best rank: {best}")
    print(f"  -> Saved: {filename}")

print(f"\nDone. {len(GROUPS)} reports saved to reports/competitors/")
