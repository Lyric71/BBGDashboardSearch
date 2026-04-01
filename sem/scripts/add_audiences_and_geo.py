"""
Add audience segments and positive geo targeting to enabled BBG campaigns.
- Positive geo targets: US, UK, AU, CA, FR, DE, Scandinavia, Benelux, CH, NZ, IT, ES, SG, HK, MY
- In-market audiences (observation mode): Business Services, Import & Export, Retail Trade
- Custom audience: search intent + competitor URLs
Account: 557-577-6523
"""
import yaml, warnings
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

ga_svc   = client.get_service('GoogleAdsService')
crit_svc = client.get_service('CampaignCriterionService')
ca_svc   = client.get_service('CustomAudienceService')

# ── Target campaigns (enabled only) ─────────────────────────────────────────
CAMPAIGN_RESOURCES = {
    'BBG CBEC EN':             'customers/5575776523/campaigns/23684716995',
    'BBG China Consulting EN': 'customers/5575776523/campaigns/23694745882',
}

# ── 1. POSITIVE GEO TARGETING ───────────────────────────────────────────────
GEO_TARGETS = {
    # Tier 1
    'United States':  2840,
    'United Kingdom': 2826,
    'Australia':      2036,
    'Canada':         2124,
    'France':         2250,
    'Germany':        2276,
    # Tier 2 - Scandinavia
    'Sweden':         2752,
    'Norway':         2578,
    'Denmark':        2208,
    'Finland':        2246,
    # Tier 2 - Benelux
    'Netherlands':    2528,
    'Belgium':        2056,
    'Luxembourg':     2442,
    # Tier 2 - Other
    'Switzerland':    2756,
    'New Zealand':    2554,
    'Italy':          2380,
    'Spain':          2724,
    # Asia
    'Singapore':      2702,
    'Hong Kong':      2344,
    'Malaysia':       2458,
}

print('=== ADDING POSITIVE GEO TARGETS ===\n')
for camp_name, camp_resource in CAMPAIGN_RESOURCES.items():
    print(f'[{camp_name}]')
    ops = []
    for country, geo_id in GEO_TARGETS.items():
        op = client.get_type('CampaignCriterionOperation')
        c = op.create
        c.campaign = camp_resource
        c.negative = False
        c.location.geo_target_constant = f'geoTargetConstants/{geo_id}'
        ops.append(op)

    try:
        res = crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
        for country in GEO_TARGETS:
            print(f'  + {country}')
        print(f'  {len(res.results)} locations added')
    except GoogleAdsException as e:
        print(f'  Error: {e.failure.errors[0].message}')

# ── 2. IN-MARKET AUDIENCES (observation mode) ───────────────────────────────
# Observation mode = OBSERVATION (bid-only), not TARGETING (restricts reach)
IN_MARKET_AUDIENCES = {
    'Business Services':  80463,
    'Import & Export':    354,
    'Retail Trade':       841,
}

print('\n=== ADDING IN-MARKET AUDIENCES (observation mode) ===\n')
for camp_name, camp_resource in CAMPAIGN_RESOURCES.items():
    print(f'[{camp_name}]')
    ops = []
    for audience_name, interest_id in IN_MARKET_AUDIENCES.items():
        op = client.get_type('CampaignCriterionOperation')
        c = op.create
        c.campaign = camp_resource
        c.user_interest.user_interest_category = f'customers/{CUSTOMER_ID}/userInterests/{interest_id}'
        ops.append(op)

    try:
        res = crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
        for name in IN_MARKET_AUDIENCES:
            print(f'  + {name}')
        print(f'  {len(res.results)} audiences added')
    except GoogleAdsException as e:
        print(f'  Error: {e.failure.errors[0].message}')

# ── 3. CUSTOM AUDIENCE (search intent + competitor URLs) ─────────────────────
print('\n=== CREATING CUSTOM AUDIENCE ===\n')

SEARCH_TERMS = [
    'sell in China',
    'China market entry',
    'Tmall Global',
    'cross-border ecommerce',
    'China ecommerce agency',
    'China consulting',
]

COMPETITOR_URLS = [
    'azoya.com',
    'tmogroup.com',
    'walkthechat.com',
    'hylink.com',
    'wpic.co',
]

try:
    op = client.get_type('CustomAudienceOperation')
    ca = op.create
    ca.name = 'BBG - China Ecommerce Intent + Competitors'
    ca.type_ = client.enums.CustomAudienceTypeEnum.AUTO
    ca.status = client.enums.CustomAudienceStatusEnum.ENABLED

    for term in SEARCH_TERMS:
        member = client.get_type('CustomAudienceMember')
        member.member_type = client.enums.CustomAudienceMemberTypeEnum.KEYWORD
        member.keyword = term
        ca.members.append(member)

    for url in COMPETITOR_URLS:
        member = client.get_type('CustomAudienceMember')
        member.member_type = client.enums.CustomAudienceMemberTypeEnum.URL
        member.url = url
        ca.members.append(member)

    res = ca_svc.mutate_custom_audiences(customer_id=CUSTOMER_ID, operations=[op])
    custom_audience_resource = res.results[0].resource_name
    print(f'  Created: {custom_audience_resource}')

    # Attach custom audience to campaigns (observation mode)
    print('\n  Attaching to campaigns...')
    for camp_name, camp_resource in CAMPAIGN_RESOURCES.items():
        op = client.get_type('CampaignCriterionOperation')
        c = op.create
        c.campaign = camp_resource
        c.custom_audience.custom_audience = custom_audience_resource
        try:
            crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=[op])
            print(f'  + [{camp_name}] attached')
        except GoogleAdsException as e:
            print(f'  [{camp_name}] Error: {e.failure.errors[0].message}')

except GoogleAdsException as e:
    print(f'  Error creating custom audience: {e.failure.errors[0].message}')

print('\nDone. Geo targets, in-market audiences, and custom audience applied.')
