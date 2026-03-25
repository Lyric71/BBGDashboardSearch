"""
SERP report — Group 01: China Ecommerce Agency (EN)
Usage: python seo/scripts/serp_01_china_ecommerce_agency.py
"""
from serp_utils import build_report

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

if __name__ == "__main__":
    build_report(
        group_name     = "01-china-ecommerce-agency",
        keywords       = KEYWORDS,
        location_code  = 2840,   # USA / Global EN
        language_code  = "en",
    )
    print("\nDone.")
