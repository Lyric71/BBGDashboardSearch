"""
Export all active keywords from Google Ads to the master keyword list.
Account: 557-577-6523 (BBG client account)
Manager: 572-730-1811
"""
import yaml, warnings, os
from collections import defaultdict
from datetime import date

warnings.filterwarnings('ignore')
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = '5575776523'

with open('config/credentials.yml') as f:
    creds = yaml.safe_load(f)['google_ads']

client = GoogleAdsClient.load_from_dict({
    'developer_token':   creds['developer_token'],
    'client_id':         creds['client_id'],
    'client_secret':     creds['client_secret'],
    'refresh_token':     creds['refresh_token'],
    'login_customer_id': str(creds['customer_id']),
    'use_proto_plus':    True,
})

ga_svc = client.get_service('GoogleAdsService')

# Fetch all non-removed keywords with campaign/ad group info and metrics
query = """
    SELECT
        campaign.name,
        campaign.status,
        ad_group.name,
        ad_group.status,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.cpc_bid_micros,
        ad_group_criterion.status
    FROM ad_group_criterion
    WHERE
        ad_group_criterion.type = 'KEYWORD'
        AND ad_group_criterion.status != 'REMOVED'
        AND campaign.status != 'REMOVED'
        AND ad_group.status != 'REMOVED'
    ORDER BY campaign.name, ad_group.name, ad_group_criterion.keyword.text
"""

print("Fetching keywords from Google Ads...")
stream = ga_svc.search_stream(customer_id=CUSTOMER_ID, query=query)

# Organize by campaign > ad group
campaigns = defaultdict(lambda: defaultdict(list))
total = 0

for batch in stream:
    for row in batch.results:
        campaign_name = row.campaign.name
        campaign_status = row.campaign.status.name
        ag_name = row.ad_group.name
        ag_status = row.ad_group.status.name
        kw_text = row.ad_group_criterion.keyword.text
        match_type = row.ad_group_criterion.keyword.match_type.name
        cpc = row.ad_group_criterion.cpc_bid_micros / 1_000_000 if row.ad_group_criterion.cpc_bid_micros else 0
        kw_status = row.ad_group_criterion.status.name

        campaigns[f"{campaign_name} [{campaign_status}]"][f"{ag_name} [{ag_status}]"].append({
            'text': kw_text,
            'match_type': match_type,
            'cpc': cpc,
            'status': kw_status,
        })
        total += 1

print(f"Found {total} keywords across {len(campaigns)} campaigns.\n")

# Print summary to console
for campaign, ad_groups in sorted(campaigns.items()):
    print(f"Campaign: {campaign}")
    for ag, keywords in sorted(ad_groups.items()):
        print(f"  Ad Group: {ag} ({len(keywords)} keywords)")
        for kw in keywords:
            print(f"    - {kw['text']}  [{kw['match_type']}]  CPC: {kw['cpc']:.2f}  ({kw['status']})")
    print()

# Write to markdown file
output_path = 'data/google_ads_keywords.md'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"# Google Ads Keywords Export\n")
    f.write(f"Date: {date.today()}\n")
    f.write(f"Account: 557-577-6523\n")
    f.write(f"Total keywords: {total}\n\n---\n\n")

    for campaign, ad_groups in sorted(campaigns.items()):
        f.write(f"## {campaign}\n\n")
        for ag, keywords in sorted(ad_groups.items()):
            f.write(f"### {ag}\n\n")
            f.write(f"| Keyword | Match Type | Max CPC | Status |\n")
            f.write(f"|---------|-----------|---------|--------|\n")
            for kw in keywords:
                f.write(f"| {kw['text']} | {kw['match_type']} | {kw['cpc']:.2f} | {kw['status']} |\n")
            f.write(f"\n")

print(f"Keywords exported to {output_path}")
