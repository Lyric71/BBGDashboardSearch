"""
Update campaign budgets to HKD 100/day and ad group CPC bids to HKD 5
for all 4 BBG campaigns.
Account: 557-577-6523
"""
import yaml, warnings
warnings.filterwarnings('ignore')
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID    = '5575776523'
BUDGET_MICROS  = 100_000_000  # HKD 100 / day per campaign
CPC_MICROS     =   5_000_000  # HKD 5 / ad group default CPC

CAMPAIGN_NAMES = [
    'BBG CBEC EN',
    'BBG China Consulting EN',
    'BBG China Agency EN',
    'BBG China Distribution EN',
]

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

ga_svc      = client.get_service('GoogleAdsService')
budget_svc  = client.get_service('CampaignBudgetService')
ag_svc      = client.get_service('AdGroupService')

names_sql = ', '.join(f"'{n}'" for n in CAMPAIGN_NAMES)

# ── 1. Update campaign budgets ─────────────────────────────────────────────────
print("=== Updating campaign budgets to HKD 100/day ===")
budget_query = f"""
    SELECT campaign.name, campaign_budget.resource_name, campaign_budget.amount_micros
    FROM campaign
    WHERE campaign.name IN ({names_sql})
      AND campaign.status != 'REMOVED'
"""
stream = ga_svc.search_stream(customer_id=CUSTOMER_ID, query=budget_query)
budget_ops = []
for batch in stream:
    for row in batch.results:
        budget_rn = row.campaign_budget.resource_name
        current   = row.campaign_budget.amount_micros
        print(f"  {row.campaign.name}: {current} -> {BUDGET_MICROS}")
        op = client.get_type('CampaignBudgetOperation')
        op.update.resource_name  = budget_rn
        op.update.amount_micros  = BUDGET_MICROS
        op.update_mask.paths.append('amount_micros')
        budget_ops.append(op)

if budget_ops:
    budget_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=budget_ops)
    print(f"  Updated {len(budget_ops)} campaign budgets.\n")

# ── 2. Update ad group CPC bids ────────────────────────────────────────────────
print("=== Updating ad group CPC bids to HKD 5 ===")
ag_query = f"""
    SELECT ad_group.resource_name, ad_group.name, ad_group.cpc_bid_micros, campaign.name
    FROM ad_group
    WHERE campaign.name IN ({names_sql})
      AND campaign.status != 'REMOVED'
      AND ad_group.status != 'REMOVED'
"""
stream = ga_svc.search_stream(customer_id=CUSTOMER_ID, query=ag_query)
ag_ops = []
for batch in stream:
    for row in batch.results:
        ag  = row.ad_group
        print(f"  [{row.campaign.name}] {ag.name}: {ag.cpc_bid_micros} -> {CPC_MICROS}")
        op = client.get_type('AdGroupOperation')
        op.update.resource_name  = ag.resource_name
        op.update.cpc_bid_micros = CPC_MICROS
        op.update_mask.paths.append('cpc_bid_micros')
        ag_ops.append(op)

if ag_ops:
    ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=ag_ops)
    print(f"  Updated {len(ag_ops)} ad groups.\n")

print("Done.")
