"""
SERP report — Group 03: Market Entry (EN)
Usage: python seo/scripts/serp_03_market_entry.py
"""
from serp_utils import build_report

KEYWORDS = [
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
]

if __name__ == "__main__":
    build_report(
        group_name     = "03-market-entry",
        keywords       = KEYWORDS,
        location_code  = 2840,
        language_code  = "en",
    )
    print("\nDone.")
