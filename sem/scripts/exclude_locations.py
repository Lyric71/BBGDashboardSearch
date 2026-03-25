"""
Add negative location targeting to all BBG campaigns.
Excludes: Africa (continent), Russia, India
Account: 557-577-6523
"""
import yaml, warnings
warnings.filterwarnings('ignore')
from google.ads.googleads.client import GoogleAdsClient

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

# ── Geo target constant IDs ───────────────────────────────────────────────────
EXCLUDE_GEO = {
    # Russia & India
    'Russia':                       2643,
    'India':                        2356,
    # Africa — all 54 countries
    'Algeria':                      2012,
    'Angola':                       2024,
    'Benin':                        2204,
    'Botswana':                     2072,
    'Burkina Faso':                 2854,
    'Burundi':                      2108,
    'Cabo Verde':                   2132,
    'Cameroon':                     2120,
    'Central African Republic':     2140,
    'Chad':                         2148,
    'Comoros':                      2174,
    'Cote d\'Ivoire':               2384,
    'Democratic Republic of Congo': 2180,
    'Djibouti':                     2262,
    'Egypt':                        2818,
    'Equatorial Guinea':            2226,
    'Eritrea':                      2232,
    'Eswatini':                     2748,
    'Ethiopia':                     2231,
    'Gabon':                        2266,
    'Ghana':                        2288,
    'Guinea':                       2324,
    'Guinea-Bissau':                2624,
    'Kenya':                        2404,
    'Lesotho':                      2426,
    'Liberia':                      2430,
    'Libya':                        2434,
    'Madagascar':                   2450,
    'Malawi':                       2454,
    'Mali':                         2466,
    'Mauritania':                   2478,
    'Mauritius':                    2480,
    'Morocco':                      2504,
    'Mozambique':                   2508,
    'Namibia':                      2516,
    'Niger':                        2562,
    'Nigeria':                      2566,
    'Republic of the Congo':        2178,
    'Rwanda':                       2646,
    'Sao Tome and Principe':        2678,
    'Senegal':                      2686,
    'Seychelles':                   2690,
    'Sierra Leone':                 2694,
    'Somalia':                      2706,
    'South Africa':                 2710,
    'South Sudan':                  2728,
    'Sudan':                        2736,
    'Tanzania':                     2834,
    'The Gambia':                   2270,
    'Togo':                         2768,
    'Tunisia':                      2788,
    'Uganda':                       2800,
    'Zambia':                       2894,
    'Zimbabwe':                     2716,
}

# ── Get all BBG campaigns ─────────────────────────────────────────────────────
CAMPAIGN_NAMES = [
    'BBG CBEC EN',
    'BBG China Consulting EN',
    'BBG China Agency EN',
    'BBG China Distribution EN',
]

rows = list(ga_svc.search(
    customer_id=CUSTOMER_ID,
    query="""
        SELECT campaign.id, campaign.name, campaign.resource_name
        FROM campaign
        WHERE campaign.status != 'REMOVED'
    """
))

campaigns = {
    r.campaign.name: r.campaign.resource_name
    for r in rows
    if r.campaign.name in CAMPAIGN_NAMES
}

print(f'Found {len(campaigns)} campaigns to update:\n')
for name in campaigns:
    print(f'  - {name}')

if len(campaigns) != len(CAMPAIGN_NAMES):
    missing = set(CAMPAIGN_NAMES) - set(campaigns.keys())
    print(f'\nWARNING: missing campaigns: {missing}')

# ── Add exclusions to each campaign ──────────────────────────────────────────
print()
for camp_name, camp_resource in campaigns.items():
    print(f'[{camp_name}]')
    ops = []
    for label, geo_id in EXCLUDE_GEO.items():
        op = client.get_type('CampaignCriterionOperation')
        c = op.create
        c.campaign = camp_resource
        c.negative = True
        c.location.geo_target_constant = f'geoTargetConstants/{geo_id}'
        ops.append(op)

    res = crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    for r, (label, _) in zip(res.results, EXCLUDE_GEO.items()):
        print(f'  excluded: {label}')

print('\nDone. Location exclusions applied to all campaigns.')
