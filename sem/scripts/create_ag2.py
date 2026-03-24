"""
Create Campaign 1 + AG2 (Consulting & Advisory) in Google Ads account 557-577-6523
Campaign status: PAUSED (review before enabling)
"""
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import yaml, warnings
warnings.filterwarnings('ignore')

CUSTOMER_ID = '5575776523'
FINAL_URL   = 'https://beyondbordergroup.com/china-ecommerce-consulting/'

with open('config/credentials.yml') as f:
    creds = yaml.safe_load(f)['google_ads']

client = GoogleAdsClient.load_from_dict({
    'developer_token': creds['developer_token'],
    'client_id':       creds['client_id'],
    'client_secret':   creds['client_secret'],
    'refresh_token':   creds['refresh_token'],
    'login_customer_id': str(creds['customer_id']),
    'use_proto_plus':  True,
})

# ── Services ──────────────────────────────────────────────────────
budget_svc   = client.get_service('CampaignBudgetService')
campaign_svc = client.get_service('CampaignService')
ag_svc       = client.get_service('AdGroupService')
kw_svc       = client.get_service('AdGroupCriterionService')
ad_svc       = client.get_service('AdGroupAdService')

# ── 1. Get or create campaign budget ─────────────────────────────
print('Looking up campaign budget...')
ga_svc = client.get_service('GoogleAdsService')
budget_rows = list(ga_svc.search(
    customer_id=CUSTOMER_ID,
    query="SELECT campaign_budget.id, campaign_budget.resource_name FROM campaign_budget WHERE campaign_budget.name = 'China Ecommerce Services Budget'"
))
if budget_rows:
    budget_resource = budget_rows[0].campaign_budget.resource_name
    print(f'  Reusing existing budget: {budget_resource}')
else:
    print('Creating campaign budget...')
    budget_op = client.get_type('CampaignBudgetOperation')
    budget = budget_op.create
    budget.name = 'China Ecommerce Services Budget'
    budget.amount_micros = 10_000_000  # HKD 10/day
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    budget_response = budget_svc.mutate_campaign_budgets(
        customer_id=CUSTOMER_ID, operations=[budget_op]
    )
    budget_resource = budget_response.results[0].resource_name
    print(f'  Budget: {budget_resource}')

# ── 2. Get or create campaign ─────────────────────────────────────
print('Looking up campaign...')
ga_svc2 = client.get_service('GoogleAdsService')
camp_rows = list(ga_svc2.search(
    customer_id=CUSTOMER_ID,
    query="SELECT campaign.id, campaign.resource_name FROM campaign WHERE campaign.name = 'BBG China Ecommerce EN' AND campaign.status != 'REMOVED'"
))
if camp_rows:
    camp_resource = camp_rows[0].campaign.resource_name
    print(f'  Reusing existing campaign: {camp_resource}')
else:
    print('Creating campaign...')
    camp_op = client.get_type('CampaignOperation')
    camp = camp_op.create
    camp.name = 'BBG China Ecommerce EN'
    camp.status = client.enums.CampaignStatusEnum.PAUSED
    camp.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    camp.campaign_budget = budget_resource
    camp.network_settings.target_google_search = True
    camp.network_settings.target_search_network = False
    camp.network_settings.target_content_network = False
    camp_op._pb.create.manual_cpc.SetInParent()
    camp_op._pb.create.contains_eu_political_advertising = 3
    camp.geo_target_type_setting.positive_geo_target_type = (
        client.enums.PositiveGeoTargetTypeEnum.PRESENCE_OR_INTEREST
    )
    camp_response = campaign_svc.mutate_campaigns(
        customer_id=CUSTOMER_ID, operations=[camp_op]
    )
    camp_resource = camp_response.results[0].resource_name
    print(f'  Campaign: {camp_resource}')

# ── 3. Add English language targeting ─────────────────────────────
print('Adding language targeting (English)...')
from google.ads.googleads.client import GoogleAdsClient as _C
camp_lang_svc = client.get_service('CampaignCriterionService')
lang_op = client.get_type('CampaignCriterionOperation')
lang = lang_op.create
lang.campaign = camp_resource
lang.language.language_constant = 'languageConstants/1000'  # English
camp_lang_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=[lang_op])
print('  Language: English added')

# ── 4. Get or create ad group ─────────────────────────────────────
print('Looking up ad group...')
ag_rows = list(ga_svc2.search(
    customer_id=CUSTOMER_ID,
    query=f"SELECT ad_group.id, ad_group.resource_name FROM ad_group WHERE ad_group.name = 'AG2 - Consulting & Advisory' AND ad_group.campaign = '{camp_resource}' AND ad_group.status != 'REMOVED'"
))
if ag_rows:
    ag_resource = ag_rows[0].ad_group.resource_name
    print(f'  Reusing existing ad group: {ag_resource}')
else:
    print('Creating ad group...')
    ag_op = client.get_type('AdGroupOperation')
    ag = ag_op.create
    ag.name = 'AG2 - Consulting & Advisory'
    ag.campaign = camp_resource
    ag.status = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag.cpc_bid_micros = 15_000_000  # HKD 15 default CPC
    ag_response = ag_svc.mutate_ad_groups(
        customer_id=CUSTOMER_ID, operations=[ag_op]
    )
    ag_resource = ag_response.results[0].resource_name
    print(f'  Ad Group: {ag_resource}')

# ── 5. Add keywords ───────────────────────────────────────────────
print('Adding keywords...')
KEYWORDS = [
    ('china ecommerce consulting',    'PHRASE'),
    ('china ecommerce consulting',    'EXACT'),
    ('china market advisor',          'PHRASE'),
    ('china ecommerce experts',       'PHRASE'),
    ('china ecommerce experts',       'EXACT'),
    ('trusted china consultants',     'PHRASE'),
    ('china business advisory',       'PHRASE'),
    ('expert china market advice',    'PHRASE'),
    ('china market intelligence',     'PHRASE'),
    ('independent china advisors',    'PHRASE'),
    ('unbiased china consulting',     'PHRASE'),
    ('data-driven china strategy',    'PHRASE'),
    ('china expert consultation',     'PHRASE'),
    ('china ecommerce advisor',       'PHRASE'),
    ('china ecommerce consulting',    'BROAD'),
]

kw_ops = []
for text, match in KEYWORDS:
    op = client.get_type('AdGroupCriterionOperation')
    kw = op.create
    kw.ad_group = ag_resource
    kw.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    kw.keyword.text = text
    kw.keyword.match_type = getattr(
        client.enums.KeywordMatchTypeEnum, match
    )
    kw_ops.append(op)

kw_response = kw_svc.mutate_ad_group_criteria(
    customer_id=CUSTOMER_ID, operations=kw_ops
)
print(f'  {len(kw_response.results)} keywords added')

# ── 6. Create RSA ─────────────────────────────────────────────────
print('Creating RSA...')

HEADLINES = [
    ('China Ecommerce Consulting',  None),
    ('China Market Advisor',        None),
    ('China Ecommerce Experts',     None),
    ('Trusted China Consultants',   None),
    ('China Business Advisory',     None),
    ('Expert China Market Advice',  None),
    ('10+ Years in China Market',   None),
    ('Proven China Ecommerce ROI',  None),
    ('China Market Intelligence',   None),
    ('Independent China Advisors',  None),
    ('Beyond Border Group',         1),    # Pinned position 1
    ('Unbiased China Consulting',   None),
    ('Data-Driven China Strategy',  None),
    ('China Expert Consultation',   None),
    ('Book a Free China Consult',   3),    # Pinned position 3
]

DESCRIPTIONS = [
    ('Independent consultants helping brands make the right China ecommerce decisions.',  1),
    ('China market expertise: platforms, regulations, consumer insights & growth strategy.', 1),
    ('BBG provides honest, data-driven advice on entering and scaling in the Chinese market.', None),
    ('From feasibility to full launch — BBG guides every step of your China journey.',       None),
]

ad_op = client.get_type('AdGroupAdOperation')
ad = ad_op.create
ad.ad_group = ag_resource
ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

rsa = ad.ad.responsive_search_ad
ad.ad.final_urls.append(FINAL_URL)

for text, pin in HEADLINES:
    h = client.get_type('AdTextAsset')
    h.text = text
    if pin:
        h.pinned_field = getattr(
            client.enums.ServedAssetFieldTypeEnum,
            f'HEADLINE_{pin}'
        )
    rsa.headlines.append(h)

for text, pin in DESCRIPTIONS:
    d = client.get_type('AdTextAsset')
    d.text = text
    if pin:
        d.pinned_field = getattr(
            client.enums.ServedAssetFieldTypeEnum,
            f'DESCRIPTION_{pin}'
        )
    rsa.descriptions.append(d)

ad_response = ad_svc.mutate_ad_group_ads(
    customer_id=CUSTOMER_ID, operations=[ad_op]
)
print(f'  RSA: {ad_response.results[0].resource_name}')

print('\nDone.')
print(f'Campaign:  China Ecommerce Services - EN  [PAUSED]')
print(f'Ad Group:  AG2 - Consulting & Advisory')
print(f'Keywords:  {len(kw_response.results)}')
print(f'Final URL: {FINAL_URL}')
print('\nReview in Google Ads, then enable the campaign when ready.')
