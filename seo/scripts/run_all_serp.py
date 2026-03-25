"""
Run all SERP group reports sequentially.
Usage: python seo/scripts/run_all_serp.py
       (run from any directory)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from serp_utils import build_report

GROUPS = [
    {
        "group_name":    "01-china-ecommerce-agency",
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
        "group_name":    "02-cross-border-ecommerce",
        "location_code": 2840,
        "language_code": "en",
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
    },
    {
        "group_name":    "03-market-entry",
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
]

if __name__ == "__main__":
    for g in GROUPS:
        build_report(
            group_name    = g["group_name"],
            keywords      = g["keywords"],
            location_code = g["location_code"],
            language_code = g["language_code"],
        )
    print("\n\nAll groups done.")
