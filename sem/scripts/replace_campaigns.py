"""
Replace all BBG Google Ads campaigns with new service-intent keyword structure.
Step 1: Remove all existing campaigns
Step 2: Create 3 new campaigns (all PAUSED)

Account : 557-577-6523
Manager : 572-730-1811
Status  : All PAUSED — review before enabling
Budget  : HKD 100/day per campaign
Match   : PHRASE
URL     : https://beyondbordergroup.com
"""
import yaml, warnings
warnings.filterwarnings('ignore')
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# ── Config ────────────────────────────────────────────────────────────────────
CUSTOMER_ID   = '5575776523'
FINAL_URL     = 'https://beyondbordergroup.com'
BUDGET_MICROS = 100_000_000   # HKD 100 / day
CPC_MICROS    = 10_000_000    # HKD 10 default CPC

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

ga_svc       = client.get_service('GoogleAdsService')
budget_svc   = client.get_service('CampaignBudgetService')
campaign_svc = client.get_service('CampaignService')
crit_svc     = client.get_service('CampaignCriterionService')
ag_svc       = client.get_service('AdGroupService')
kw_svc       = client.get_service('AdGroupCriterionService')
ad_svc       = client.get_service('AdGroupAdService')

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Remove all existing campaigns
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("STEP 1: Removing all existing campaigns")
print("=" * 60)

query = """
    SELECT campaign.resource_name, campaign.name
    FROM campaign
    WHERE campaign.status != 'REMOVED'
"""
rows = list(ga_svc.search(customer_id=CUSTOMER_ID, query=query))

if rows:
    ops = []
    for row in rows:
        print(f"  Removing: {row.campaign.name}")
        op = client.get_type('CampaignOperation')
        op.remove = row.campaign.resource_name
        ops.append(op)
    campaign_svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=ops)
    print(f"\n  {len(ops)} campaigns removed.\n")
else:
    print("  No campaigns to remove.\n")

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Create new campaigns
# ══════════════════════════════════════════════════════════════════════════════

CAMPAIGNS = [
    {
        'name': 'BBG Ecommerce Consulting EN',
        'budget': 'BBG Ecom Consulting Budget',
        'ad_groups': [
            {
                'name': '1A - China Ecommerce Consulting',
                'keywords': [
                    'china ecommerce consulting',
                    'china ecommerce consultant',
                    'china ecommerce agency',
                    'china ecommerce strategy consulting',
                    'china ecommerce advisor',
                    'china ecommerce experts',
                    'ecommerce consulting china',
                    'china ecommerce services',
                    'china ecommerce firm',
                    'china ecommerce specialist',
                    'china ecommerce solutions',
                    'china ecommerce advisory',
                    'china ecommerce provider',
                    'hire china ecommerce expert',
                    'china ecommerce managed services',
                    'outsource china ecommerce',
                ],
                'headlines': [
                    ('China eCommerce Consulting',   None),
                    ('China eCommerce Strategy',     None),
                    ('China eCommerce Experts',      None),
                    ('Your China eCommerce Advisor', None),
                    ('Smart China eCommerce Plan',   None),
                    ('Get China Right First Time',   None),
                    ('China eCommerce, Sorted',      None),
                    ('Grow Your China Sales',        None),
                    ('China Strategy That Works',    None),
                    ('Stop Guessing About China',    None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('We help brands build China ecommerce strategies that translate into actual revenue.',     None),
                    ('Platform, pricing, logistics, marketing plan. Every angle of your China strategy covered.', None),
                    ('Our consultants have operated in China 10+ years. Strategy from daily platform experience.', None),
                    ('Get a clear China ecommerce roadmap before you spend a dollar. Assess, plan, execute.',  None),
                ],
            },
            {
                'name': '1B - Cross-Border Ecommerce Services',
                'keywords': [
                    'cross border ecommerce agency',
                    'cross border ecommerce agency china',
                    'cbec agency',
                    'cbec consulting china',
                    'china cross border ecommerce consulting',
                    'cross border commerce china consultant',
                    'cbec specialist',
                    'cbec solutions',
                    'cbec managed services',
                    'cross border ecommerce consultant china',
                    'cross border ecommerce firm',
                    'china cbec provider',
                    'china cbec advisory',
                    'outsource cross border ecommerce china',
                ],
                'headlines': [
                    ('Cross-Border eCommerce China', None),
                    ('China CBEC Experts',           None),
                    ('Cross-Border Strategy China',  None),
                    ('CBEC Done Right',              None),
                    ('Your China CBEC Partner',      None),
                    ('Launch via Cross-Border',      None),
                    ('China Cross-Border Agency',    None),
                    ('CBEC Strategy & Execution',    None),
                    ('Skip the Red Tape',            None),
                    ('Sell in China via CBEC',       None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('We build cross-border ecommerce operations that actually sell. Strategy to execution.', None),
                    ('Launch on Tmall Global or JD Worldwide without a Chinese entity. Full setup handled.',  None),
                    ('From platform selection to daily ops. Brands trust us to run their China CBEC business.', None),
                    ('Cross-border is the fastest route into China. Right model, right execution.',            None),
                ],
            },
            {
                'name': '1C - Market Entry Consulting',
                'keywords': [
                    'china market entry consulting',
                    'china market entry agency',
                    'china market entry services',
                    'china market entry strategy',
                    'china brand launch consulting',
                    'china business entry consulting',
                    'china market expansion consulting',
                    'market entry strategy china consulting',
                    'china market entry firm',
                    'china market entry specialist',
                    'china market entry advisor',
                    'china market entry solutions',
                    'china market entry provider',
                    'hire china market entry consultant',
                    'china go to market agency',
                ],
                'headlines': [
                    ('China Market Entry Strategy',  None),
                    ('Launch Your Brand in China',   None),
                    ('China Market Entry Experts',   None),
                    ('Your China Launch Partner',    None),
                    ('Plan Your China Entry',        None),
                    ('China Expansion Consulting',   None),
                    ('China Go-to-Market Plan',      None),
                    ('CBEC Market Entry Experts',    None),
                    ('From Zero to China Revenue',   None),
                    ('We Launch Brands in China',    None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('Market entry via cross-border is faster and cheaper than general trade. We execute it.', None),
                    ("We've launched 40+ brands into China via CBEC. Feasibility to first sale in 90 days.",   None),
                    ('Your China market entry, handled. Platform setup, listing, logistics, marketing.',       None),
                    ('Not sure if China fits your brand? We run feasibility assessments before you commit.',   None),
                ],
            },
            {
                'name': '1D - Feasibility & Research Consulting',
                'keywords': [
                    'china market research consulting',
                    'china market feasibility study',
                    'china market opportunity assessment',
                    'china ecommerce market research',
                    'china consumer insights agency',
                    'china brand positioning consulting',
                    'china localization consulting',
                    'china retail consulting',
                    'china market entry cost consulting',
                    'china market research firm',
                    'china market research agency',
                    'china consumer research specialist',
                    'china brand strategy consulting',
                    'china market due diligence consulting',
                ],
                'headlines': [
                    ('China Consumer Research',      None),
                    ('China Brand Positioning',      None),
                    ('China Market Intelligence',    None),
                    ('Know Your China Audience',     None),
                    ('China Localization Experts',   None),
                    ('China Market Deep Dive',       None),
                    ('Understand Chinese Buyers',    None),
                    ('China Insight, Not Guesswork', None),
                    ('China Market Feasibility',     None),
                    ('China Entry Cost Analysis',    None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('China strategy starts with consumer insight. We research your category and competition.', None),
                    ('China brand positioning is not translation. We build messaging that resonates locally.', None),
                    ('We analyze your China competitive landscape so you enter with a defensible position.',      None),
                    ('We help brands understand the real cost of selling in China before committing budget.',   None),
                ],
            },
        ],
    },
    {
        'name': 'BBG Platform Agency EN',
        'budget': 'BBG Platform Agency Budget',
        'ad_groups': [
            {
                'name': '2A - Tmall Agency',
                'keywords': [
                    'tmall agency',
                    'tmall consulting',
                    'tmall partner agency',
                    'tmall tp agency',
                    'tmall global agency',
                    'tmall global consulting',
                    'tmall setup consulting',
                    'tmall store management',
                    'tmall specialist',
                    'tmall managed services',
                    'tmall solutions',
                    'tmall expert agency',
                    'tmall global partner',
                    'tmall global management',
                    'hire tmall agency',
                ],
                'headlines': [
                    ('Tmall Agency',                 None),
                    ('Tmall Global Partner',         None),
                    ('Tmall Store Management',       None),
                    ('Tmall Global Experts',         None),
                    ('Tmall TP Agency',              None),
                    ('Launch on Tmall Global',       None),
                    ('Your Tmall Partner Agency',    None),
                    ('Tmall Setup & Operations',     None),
                    ('Tmall Managed Services',       None),
                    ('Full Service Tmall Agency',    None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('We set up and manage Tmall Global stores for international brands. Listing to daily ops.', None),
                    ("Tmall Global is China's top cross-border platform. We get you listed and selling fast.",  None),
                    ('Store design, listing, pricing, promotions, customer service. Your Tmall, fully managed.', None),
                    ('Underperforming on Tmall? We take over operations and turn around your China sales.',     None),
                ],
            },
            {
                'name': '2B - JD.com Agency',
                'keywords': [
                    'jd.com agency',
                    'jd.com consulting',
                    'jd.com partner agency',
                    'jd.com store management',
                    'jd worldwide consulting',
                    'jd.com specialist',
                    'jd.com managed services',
                    'jd.com solutions',
                    'jd worldwide agency',
                    'hire jd.com agency',
                ],
                'headlines': [
                    ('JD.com Agency',                None),
                    ('JD Worldwide Partner',         None),
                    ('JD.com Store Management',      None),
                    ('Launch on JD Worldwide',       None),
                    ('Your JD.com Partner',          None),
                    ('JD China Experts',             None),
                    ('JD Store Setup & Ops',         None),
                    ('JD Worldwide for Brands',      None),
                    ('Grow Sales on JD.com',         None),
                    ('JD Managed Services',          None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('JD.com reaches 600M+ users with best-in-class logistics. We manage your store end to end.', None),
                    ('JD Worldwide is ideal for health, electronics, premium brands. Setup and operations.',    None),
                    ('From store opening to daily order management. We run JD so you focus on product.',       None),
                    ('Not sure about JD? We advise on fit and manage your store if JD is right for you.',     None),
                ],
            },
            {
                'name': '2C - Douyin Agency',
                'keywords': [
                    'douyin agency',
                    'douyin marketing agency',
                    'douyin ecommerce consulting',
                    'douyin live commerce consulting',
                    'douyin shop setup',
                    'live commerce china consulting',
                    'douyin specialist',
                    'douyin managed services',
                    'douyin advertising agency',
                    'douyin commerce agency',
                    'hire douyin agency',
                    'douyin full service agency',
                ],
                'headlines': [
                    ('Douyin eCommerce Agency',      None),
                    ('China Live Commerce Experts',  None),
                    ('Douyin Shop Setup',            None),
                    ('Live Selling in China',        None),
                    ('Douyin Marketing Agency',      None),
                    ('Douyin Store Management',      None),
                    ('Douyin Managed Services',      None),
                    ('Full Service Douyin Agency',   None),
                    ('Douyin Specialist Agency',     None),
                    ('Go Live, Sell More',           None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ("Douyin is China's fastest-growing commerce channel. We set up shops and sell via live.",  None),
                    ('Douyin ecommerce is not hype. We build shops, run live sessions, and scale your sales.', None),
                    ('Live commerce in China works. We set up your Douyin presence and manage content.',       None),
                    ('Douyin shop setup to livestream ops. We handle the full Douyin commerce stack for brands.', None),
                ],
            },
            {
                'name': '2D - Xiaohongshu RED Agency',
                'keywords': [
                    'xiaohongshu agency',
                    'xiaohongshu marketing consulting',
                    'little red book agency',
                    'little red book marketing consulting',
                    'red ecommerce consulting',
                    'red china marketing',
                    'xiaohongshu specialist',
                    'xiaohongshu managed services',
                    'little red book specialist',
                    'hire xiaohongshu agency',
                    'xiaohongshu advertising agency',
                ],
                'headlines': [
                    ('Xiaohongshu Agency',           None),
                    ('Little Red Book Experts',      None),
                    ('RED China Marketing',          None),
                    ('Xiaohongshu for Brands',       None),
                    ('Little Red Book Agency',       None),
                    ('RED Content & Commerce',       None),
                    ('Grow on Xiaohongshu',          None),
                    ('Your RED China Partner',       None),
                    ('Xiaohongshu Specialist',       None),
                    ('RED Managed Services',         None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('Xiaohongshu is where Chinese consumers discover brands. We build your RED presence.',    None),
                    ("RED is not just social. It's a search engine and a store. We manage content and commerce.", None),
                    ('Beauty, fashion, lifestyle brands perform best on RED. Content that converts.',           None),
                    ('KOL seeding to Xiaohongshu shop management. RED strategy and daily operations.',         None),
                ],
            },
            {
                'name': '2E - WeChat & Social Agency',
                'keywords': [
                    'wechat marketing agency',
                    'wechat consulting',
                    'wechat ecommerce consulting',
                    'wechat mini program agency',
                    'wechat store setup',
                    'weibo marketing agency',
                    'china social media agency',
                    'china social commerce consulting',
                    'wechat specialist',
                    'wechat managed services',
                    'wechat solutions',
                    'china social media consulting firm',
                    'hire wechat agency',
                    'weibo consulting',
                ],
                'headlines': [
                    ('WeChat Marketing Agency',      None),
                    ('WeChat Store Setup',           None),
                    ('WeChat Mini Program Agency',   None),
                    ('China Social Commerce',        None),
                    ('WeChat eCommerce Experts',     None),
                    ('WeChat for Brands',            None),
                    ('Build Your WeChat Store',      None),
                    ('China Social Media Agency',    None),
                    ('WeChat CRM & Commerce',        None),
                    ('WeChat Managed Services',      None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ("WeChat is China's everything app. Mini programs, stores, CRM that drive repeat sales.",  None),
                    ('WeChat is where Chinese customers live. Content, commerce, and CRM in one ecosystem.',   None),
                    ('Mini programs, official accounts, WeChat stores. Full WeChat ecosystem, fully managed.', None),
                    ('Social commerce starts with WeChat. We build the infrastructure for follower-to-buyer.', None),
                ],
            },
        ],
    },
    {
        'name': 'BBG Digital Marketing Agency EN',
        'budget': 'BBG Digital Marketing Budget',
        'ad_groups': [
            {
                'name': '3A - Digital Marketing Agency',
                'keywords': [
                    'china digital marketing agency',
                    'china digital marketing consulting',
                    'china digital marketing services',
                    'china online marketing agency',
                    'chinese digital strategy consulting',
                    'china digital marketing firm',
                    'china digital marketing specialist',
                    'china digital marketing provider',
                    'hire china digital marketing agency',
                    'china digital marketing solutions',
                ],
                'headlines': [
                    ('China Digital Marketing',      None),
                    ('China Marketing Agency',       None),
                    ('China Digital Strategy',       None),
                    ('China Marketing Experts',      None),
                    ('China Marketing Consulting',   None),
                    ('Digital Strategy for China',   None),
                    ('Reach Chinese Consumers',      None),
                    ('Drive Sales in China',         None),
                    ('China Marketing Solutions',    None),
                    ('Full Service China Marketing', None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('China digital marketing needs local expertise. Campaigns across all major platforms.',    None),
                    ('We plan and execute digital marketing strategies that drive real China revenue.',         None),
                    ('From search to social to ecommerce marketing. Full-funnel China digital strategy.',      None),
                    ('Brand awareness to conversion. China marketing campaigns built around your sales targets.', None),
                ],
            },
            {
                'name': '3B - Performance & Paid Agency',
                'keywords': [
                    'china performance marketing agency',
                    'china sem agency',
                    'china ppc agency',
                    'china seo agency',
                    'china paid media agency',
                    'china search marketing agency',
                    'china paid advertising agency',
                    'china search engine marketing consulting',
                ],
                'headlines': [
                    ('China SEM Agency',             None),
                    ('China PPC Agency',             None),
                    ('China SEO Agency',             None),
                    ('China Paid Media Experts',     None),
                    ('China Performance Marketing',  None),
                    ('China Search Marketing',       None),
                    ('Baidu & Beyond',               None),
                    ('China Paid Advertising',       None),
                    ('China Media Buying Agency',    None),
                    ('Results-Driven China Ads',     None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('Baidu, Douyin, WeChat, RED. We run paid campaigns across every major Chinese platform.',  None),
                    ('China performance marketing that delivers measurable ROI. From setup to optimization.',   None),
                    ('Search, social, display. China media buying from practitioners who know the platforms.',   None),
                    ('China SEM and paid social managed by native speakers with platform-specific expertise.',   None),
                ],
            },
            {
                'name': '3C - Influencer & Content Agency',
                'keywords': [
                    'china influencer marketing agency',
                    'china content marketing agency',
                    'china social media marketing agency',
                    'china brand awareness consulting',
                    'china kol agency',
                    'china kol consulting',
                    'china influencer consulting',
                    'china content strategy consulting',
                    'hire china influencer agency',
                    'china influencer management agency',
                ],
                'headlines': [
                    ('China KOL Agency',             None),
                    ('China Influencer Marketing',   None),
                    ('China Content Marketing',      None),
                    ('KOL Campaigns That Convert',   None),
                    ('China Brand Awareness',        None),
                    ('China Influencer Agency',      None),
                    ('China KOL Management',         None),
                    ('China Content Strategy',       None),
                    ('Influencer Campaigns China',   None),
                    ('KOL Seeding & Campaigns',      None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('KOL campaigns, paid media, content production. Digital marketing that drives China sales.', None),
                    ("We don't just pick influencers. Full-funnel campaigns connecting awareness to purchases.", None),
                    ('China KOL sourcing, briefing, management and reporting. Campaigns that move product.',    None),
                    ('Content that resonates with Chinese consumers. Strategy, production, distribution.',      None),
                ],
            },
        ],
    },
]

NEGATIVE_KEYWORDS = [
    'jobs', 'salary', 'career', 'internship', 'intern',
    'course', 'training', 'free', 'pdf', 'download',
    'template', 'wikipedia', 'what is', 'definition', 'meaning',
    'tutorial', 'example', 'sample', 'case study',
    'book', 'certification', 'degree', 'masters', 'mba',
    'reddit', 'quora', 'blog', 'news',
    'amazon', 'alibaba', 'aliexpress', 'wish', 'shein', 'temu',
    'how to', 'diy', 'guide', 'tips', 'checklist',
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def lookup(query):
    return list(ga_svc.search(customer_id=CUSTOMER_ID, query=query))

def create_budget(name):
    op = client.get_type('CampaignBudgetOperation')
    b = op.create
    b.name = name
    b.amount_micros = BUDGET_MICROS
    b.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    res = budget_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[op])
    r = res.results[0].resource_name
    print(f'  budget created: {name}')
    return r

def create_campaign(name, budget_resource):
    op = client.get_type('CampaignOperation')
    c = op.create
    c.name = name
    c.status = client.enums.CampaignStatusEnum.PAUSED
    c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    c.campaign_budget = budget_resource
    c.network_settings.target_google_search = True
    c.network_settings.target_search_network = False
    c.network_settings.target_content_network = False
    op._pb.create.manual_cpc.SetInParent()
    op._pb.create.contains_eu_political_advertising = 3
    res = campaign_svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    r = res.results[0].resource_name
    print(f'  campaign created: {name}')
    return r

def add_language(camp_resource):
    try:
        op = client.get_type('CampaignCriterionOperation')
        l = op.create
        l.campaign = camp_resource
        l.language.language_constant = 'languageConstants/1000'  # English
        crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=[op])
    except Exception:
        pass

def add_negatives(camp_resource):
    ops = []
    for kw in NEGATIVE_KEYWORDS:
        op = client.get_type('CampaignCriterionOperation')
        n = op.create
        n.campaign = camp_resource
        n.negative = True
        n.keyword.text = kw
        n.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        ops.append(op)
    crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f'  {len(ops)} negative keywords added')

def create_adgroup(name, camp_resource):
    op = client.get_type('AdGroupOperation')
    ag = op.create
    ag.name = name
    ag.campaign = camp_resource
    ag.status = client.enums.AdGroupStatusEnum.PAUSED
    ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag.cpc_bid_micros = CPC_MICROS
    res = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
    r = res.results[0].resource_name
    print(f'    ag created: {name}')
    return r

def add_keywords(ag_resource, keywords):
    ops = []
    for text in keywords:
        op = client.get_type('AdGroupCriterionOperation')
        kw = op.create
        kw.ad_group = ag_resource
        kw.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        kw.keyword.text = text
        kw.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
    res = kw_svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f'    {len(res.results)} keywords added')

def add_rsa(ag_resource, headlines, descriptions):
    op = client.get_type('AdGroupAdOperation')
    ad = op.create
    ad.ad_group = ag_resource
    ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    rsa = ad.ad.responsive_search_ad
    ad.ad.final_urls.append(FINAL_URL)
    for text, pin in headlines:
        h = client.get_type('AdTextAsset')
        h.text = text
        if pin:
            h.pinned_field = getattr(client.enums.ServedAssetFieldTypeEnum, f'HEADLINE_{pin}')
        rsa.headlines.append(h)
    for text, pin in descriptions:
        d = client.get_type('AdTextAsset')
        d.text = text
        if pin:
            d.pinned_field = getattr(client.enums.ServedAssetFieldTypeEnum, f'DESCRIPTION_{pin}')
        rsa.descriptions.append(d)
    res = ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[op])
    print(f'    RSA created')

# ── Main ──────────────────────────────────────────────────────────────────────
total_ag = sum(len(c['ad_groups']) for c in CAMPAIGNS)
total_kw = sum(len(ag['keywords']) for c in CAMPAIGNS for ag in c['ad_groups'])

print("=" * 60)
print("STEP 2: Creating new campaigns")
print("=" * 60)
print(f'\nCreating {len(CAMPAIGNS)} campaigns / {total_ag} ad groups / {total_kw} keywords')
print('All PAUSED — will not spend until manually enabled.\n')

for camp_data in CAMPAIGNS:
    print(f'\n[{camp_data["name"]}]')
    budget_r = create_budget(camp_data['budget'])
    camp_r   = create_campaign(camp_data['name'], budget_r)
    add_language(camp_r)
    add_negatives(camp_r)

    for ag_data in camp_data['ad_groups']:
        print(f'\n  [{ag_data["name"]}]')
        ag_r = create_adgroup(ag_data['name'], camp_r)
        add_keywords(ag_r, ag_data['keywords'])
        add_rsa(ag_r, ag_data['headlines'], ag_data['descriptions'])

print('\n' + '=' * 60)
print('DONE')
print('=' * 60)
print(f'Campaigns  : {len(CAMPAIGNS)} (all PAUSED)')
print(f'Ad groups  : {total_ag} (all PAUSED)')
print(f'Keywords   : {total_kw} (PHRASE match)')
print(f'Negatives  : {len(NEGATIVE_KEYWORDS)} per campaign')
print(f'CPC        : HKD 10')
print(f'Budget     : HKD 100/day per campaign')
print(f'Final URL  : {FINAL_URL}')
print('\nReview in Google Ads UI, then enable when ready.')
