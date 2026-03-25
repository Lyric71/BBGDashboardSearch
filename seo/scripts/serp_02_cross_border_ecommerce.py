"""
SERP report — Group 02: Cross-Border Ecommerce (EN)
Usage: python seo/scripts/serp_02_cross_border_ecommerce.py
"""
from serp_utils import build_report

KEYWORDS = [
    "china cross border ecommerce consulting",
    "cross border ecommerce china",
    "CBEC consulting china",
    "CBEC agency",
    "cross border ecommerce agency china",
    "cross border ecommerce agency",
    "china CBEC strategy",
    "china CBEC solutions",
    "cross border commerce china consultant",
]

if __name__ == "__main__":
    build_report(
        group_name     = "02-cross-border-ecommerce",
        keywords       = KEYWORDS,
        location_code  = 2840,
        language_code  = "en",
    )
    print("\nDone.")
