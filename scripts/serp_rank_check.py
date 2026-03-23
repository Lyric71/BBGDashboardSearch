import http.client
import json
import base64
import time

# Credentials
LOGIN = "cyril.drouin@beyondbordergroup.com"
PASSWORD = "9e6796d9d94cf3e3"
CREDENTIALS = base64.b64encode(f"{LOGIN}:{PASSWORD}".encode()).decode()

# Domains to track
DOMAINS = [
    "beyondbordergroup.com",
    "wpic.co",
    "genuine-asia.com",
    "ecommercetochina.com",
    "web2asia.com",
    "azoyagroup.com",
    "agencychina.com",
    "daxueconsulting.com",
    "marketingtochina.com",
    "ecommercechinaagency.com",
    "tmogroup.asia",
    "eggsist.com",
]

# Keywords — China Ecommerce Consulting category
KEYWORDS = [
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
]

def get_serp(keyword, language_code="en"):
    """Call DataForSEO SERP Live Regular endpoint. google.com = global English."""
    conn = http.client.HTTPSConnection("api.dataforseo.com")
    payload = json.dumps([{
        "keyword": keyword,
        "location_code": 2840,
        "language_code": language_code,
        "device": "desktop",
        "depth": 100
    }])
    headers = {
        "Authorization": f"Basic {CREDENTIALS}",
        "Content-Type": "application/json"
    }
    conn.request("POST", "/v3/serp/google/organic/live/regular", payload, headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    conn.close()
    return data

def extract_ranks(serp_data, domains):
    """Extract rank for each domain from SERP results. Also returns the #1 domain."""
    ranks = {d: None for d in domains}
    top_domain = None
    try:
        items = serp_data["tasks"][0]["result"][0]["items"]
        organic_items = [i for i in items if i.get("type") == "organic"]
        # Get domain at position 1
        if organic_items:
            top_url = organic_items[0].get("url", "")
            # Extract root domain from URL
            top_domain = top_url.split("/")[2].replace("www.", "") if "/" in top_url else top_url
        for item in organic_items:
            url = item.get("url", "")
            rank = item.get("rank_absolute")
            for domain in domains:
                if domain in url and ranks[domain] is None:
                    ranks[domain] = rank
    except (KeyError, IndexError, TypeError):
        pass
    return ranks, top_domain

def main():
    results = {}

    print(f"Checking {len(KEYWORDS)} keywords x {len(DOMAINS)} domains...\n")

    for kw in KEYWORDS:
        print(f"  > {kw}")
        data = get_serp(kw)
        ranks, top_domain = extract_ranks(data, DOMAINS)
        results[kw] = {"ranks": ranks, "top_domain": top_domain}
        time.sleep(0.5)  # be nice to the API

    # Build markdown table
    all_cols = ["#1 Domain"] + DOMAINS
    header = "| Keyword | " + " | ".join(all_cols) + " |"
    separator = "|---------|" + "|".join(["------" for _ in all_cols]) + "|"

    lines = [
        "# SERP Rank Check - China Ecommerce Consulting Keywords",
        "Date: 2026-03-23",
        "Search Engine: google.com | Language: English (Global) | Depth: 100",
        "",
        header,
        separator
    ]

    for kw, data in results.items():
        ranks = data["ranks"]
        top_domain = data["top_domain"] or "-"
        row_values = [top_domain]
        for domain in DOMAINS:
            r = ranks[domain]
            if r is None:
                row_values.append("-")
            elif r <= 3:
                row_values.append(f"**{r}**")
            elif r <= 10:
                row_values.append(str(r))
            else:
                row_values.append(f"*{r}*")
        lines.append(f"| {kw} | " + " | ".join(row_values) + " |")

    output = "\n".join(lines)
    print("\n" + output)

    # Save to file
    with open("c:/Users/cyril/Project/GoogleSearch/reports/competitors/serp_ranks_china-ecommerce-consulting.md", "w") as f:
        f.write(output)

    print("\n\nSaved to reports/competitors/serp_ranks_china-ecommerce-consulting.md")

if __name__ == "__main__":
    main()
