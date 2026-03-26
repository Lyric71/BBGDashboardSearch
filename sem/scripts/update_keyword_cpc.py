"""
Set max CPC = HKD 5 on every keyword in all BBG campaigns.
Account: 557-577-6523
"""
import yaml, warnings
warnings.filterwarnings('ignore')
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = '5575776523'
CPC_MICROS  = 5_000_000  # HKD 5

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

ga_svc  = client.get_service('GoogleAdsService')
kw_svc  = client.get_service('AdGroupCriterionService')

# Fetch all non-removed keywords in BBG campaigns
query = """
    SELECT
        ad_group_criterion.resource_name,
        ad_group_criterion.keyword.text,
        ad_group_criterion.cpc_bid_micros,
        ad_group.name,
        campaign.name
    FROM ad_group_criterion
    WHERE
        ad_group_criterion.type = 'KEYWORD'
        AND ad_group_criterion.status != 'REMOVED'
        AND campaign.name IN ('BBG CBEC EN', 'BBG China Consulting EN', 'BBG China Agency EN', 'BBG China Distribution EN')
        AND campaign.status != 'REMOVED'
        AND ad_group.status != 'REMOVED'
"""

stream = ga_svc.search_stream(customer_id=CUSTOMER_ID, query=query)

ops = []
count = 0
for batch in stream:
    for row in batch.results:
        crit = row.ad_group_criterion
        print(f"  [{row.campaign.name}] [{row.ad_group.name}] {crit.keyword.text}  "
              f"current={crit.cpc_bid_micros} -> {CPC_MICROS}")
        op = client.get_type('AdGroupCriterionOperation')
        op.update.resource_name = crit.resource_name
        op.update.cpc_bid_micros = CPC_MICROS
        op.update_mask.paths.append('cpc_bid_micros')
        ops.append(op)
        count += 1

if not ops:
    print("No keywords found.")
else:
    # Send in batches of 1000 (API limit)
    for i in range(0, len(ops), 1000):
        batch_ops = ops[i:i+1000]
        kw_svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=batch_ops)
        print(f"  Updated {len(batch_ops)} keywords (batch {i//1000 + 1})")

print(f"\nDone. {count} keywords set to HKD 5 max CPC.")
