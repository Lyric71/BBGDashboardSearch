"""
Set max CPC = HKD 10 and match type = PHRASE on every keyword in all BBG campaigns.
Match type is immutable in Google Ads API, so we remove the old keyword and create
a new one with PHRASE match type and updated CPC.
Account: 557-577-6523
"""
import yaml, warnings
warnings.filterwarnings('ignore')
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = '5575776523'
CPC_MICROS  = 10_000_000  # HKD 10

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
        ad_group_criterion.keyword.match_type,
        ad_group_criterion.cpc_bid_micros,
        ad_group_criterion.status,
        ad_group.resource_name,
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

# Collect keywords to recreate
keywords = []
for batch in stream:
    for row in batch.results:
        crit = row.ad_group_criterion
        match_name = crit.keyword.match_type.name if crit.keyword.match_type else 'UNKNOWN'
        keywords.append({
            'resource_name': crit.resource_name,
            'text': crit.keyword.text,
            'match_type': match_name,
            'status': crit.status.name,
            'ag_resource': row.ad_group.resource_name,
            'ag_name': row.ad_group.name,
            'campaign_name': row.campaign.name,
        })

if not keywords:
    print("No keywords found.")
else:
    # Step 1: Remove old keywords
    print(f"Removing {len(keywords)} old keywords...")
    remove_ops = []
    for kw in keywords:
        op = client.get_type('AdGroupCriterionOperation')
        op.remove = kw['resource_name']
        remove_ops.append(op)

    for i in range(0, len(remove_ops), 1000):
        batch_ops = remove_ops[i:i+1000]
        kw_svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=batch_ops)
        print(f"  Removed {len(batch_ops)} keywords (batch {i//1000 + 1})")

    # Step 2: Create new keywords with PHRASE match type and HKD 10 CPC
    print(f"\nCreating {len(keywords)} keywords as PHRASE / HKD 10...")
    create_ops = []
    for kw in keywords:
        print(f"  [{kw['campaign_name']}] [{kw['ag_name']}] {kw['text']}  "
              f"{kw['match_type']} -> PHRASE / {CPC_MICROS}")
        op = client.get_type('AdGroupCriterionOperation')
        criterion = op.create
        criterion.ad_group = kw['ag_resource']
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = kw['text']
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        criterion.cpc_bid_micros = CPC_MICROS
        create_ops.append(op)

    for i in range(0, len(create_ops), 1000):
        batch_ops = create_ops[i:i+1000]
        kw_svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=batch_ops)
        print(f"  Created {len(batch_ops)} keywords (batch {i//1000 + 1})")

    print(f"\nDone. {len(keywords)} keywords recreated as PHRASE match / HKD 10 max CPC.")
