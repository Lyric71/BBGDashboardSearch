"""
Create all BBG Google Ads campaigns, ad groups, keywords and RSA ads.
Account : 557-577-6523
Status  : All PAUSED — review before enabling
Budget  : HKD 5/day per campaign
Match   : EXACT only
URL     : https://beyondbordergroup.com
"""
import yaml, warnings
warnings.filterwarnings('ignore')
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# ── Config ────────────────────────────────────────────────────────────────────
CUSTOMER_ID = '5575776523'
FINAL_URL   = 'https://beyondbordergroup.com'
BUDGET_MICROS = 5_000_000   # HKD 5 / day
CPC_MICROS    = 10_000_000  # HKD 10 default CPC

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
lang_svc     = client.get_service('CampaignCriterionService')
ag_svc       = client.get_service('AdGroupService')
kw_svc       = client.get_service('AdGroupCriterionService')
ad_svc       = client.get_service('AdGroupAdService')

# ── Campaign / ad-group data ───────────────────────────────────────────────────
CAMPAIGNS = [
    {
        'name': 'BBG CBEC EN',
        'budget': 'BBG CBEC Budget',
        'ad_groups': [
            {
                'name': '1A - CBEC Generic',
                'keywords': [
                    'cross border ecommerce china',
                    'china cross border ecommerce consulting',
                    'cbec consulting china',
                    'cbec agency',
                    'cross border ecommerce agency china',
                    'cross border ecommerce agency',
                    'china cbec strategy',
                    'china cbec solutions',
                    'cross border commerce china consultant',
                ],
                'headlines': [
                    ('Cross-Border eCommerce China', None),
                    ('China CBEC Experts',           None),
                    ('Sell in China via CBEC',        None),
                    ('Cross-Border Strategy China',   None),
                    ('CBEC Done Right',               None),
                    ('Your China CBEC Partner',       None),
                    ('Launch via Cross-Border',        None),
                    ('China Cross-Border Agency',     None),
                    ('CBEC Strategy & Execution',     None),
                    ('Skip the Red Tape',             None),
                    ('Beyond Border Group',           1),
                    ('Book a Free Consultation',      3),
                ],
                'descriptions': [
                    ('We build cross-border ecommerce operations that actually sell. Strategy to execution.', None),
                    ('Launch on Tmall Global or JD Worldwide without a Chinese entity. Full setup handled.',  None),
                    ('From platform selection to daily ops. Brands trust us to run their China CBEC business.', None),
                    ('Cross-border is the fastest route into China. Right model, right execution.',            None),
                ],
            },
            {
                'name': '1B - Sell Without Entity',
                'keywords': [
                    'china ecommerce without entity',
                    'sell in china without chinese company',
                    'china cross border ecommerce without entity',
                ],
                'headlines': [
                    ('Sell in China, No Entity',    None),
                    ('No Chinese Company Needed',    None),
                    ('China Sales Without Entity',   None),
                    ('Skip the Entity Setup',        None),
                    ('Go Live in China Faster',      None),
                    ('No Local Entity Required',     None),
                    ('Start Selling in 8 Weeks',     None),
                    ('China Revenue, No Red Tape',   None),
                    ('Cross-Border = No Entity',     None),
                    ('Sell in China Tomorrow',       None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('No Chinese entity? No problem. CBEC lets you sell directly to Chinese consumers.',        None),
                    ('Skip the 12-month entity setup. We launch your brand on Tmall Global via CBEC.',         None),
                    ('Brands sell millions in China without a local company. We show you how.',                None),
                    ('No entity, no local bank, no CFDA registration for most SKUs via cross-border.',        None),
                ],
            },
            {
                'name': '1C - CBEC Market Entry',
                'keywords': [
                    'china market entry consulting',
                    'china market entry agency',
                    'china market entry strategy',
                    'china market entry services',
                    'enter chinese market',
                    'entering the china market',
                    'how to enter china market',
                    'china market entry for brands',
                    'launch brand in china',
                    'china brand launch consulting',
                    'china business entry consulting',
                ],
                'headlines': [
                    ('Enter China via CBEC',         None),
                    ('China Market Entry, Fast',      None),
                    ('Launch Your Brand in China',    None),
                    ('CBEC Market Entry Experts',     None),
                    ('Your First China Sales',        None),
                    ('From Zero to China Revenue',    None),
                    ('China Launch via CBEC',         None),
                    ('Market Entry Made Simple',      None),
                    ('Go Live on Tmall Global',       None),
                    ('We Launch Brands in China',     None),
                    ('Beyond Border Group',           1),
                    ('Book a Free Consultation',      3),
                ],
                'descriptions': [
                    ('Market entry via cross-border is faster and cheaper than general trade. We execute it.', None),
                    ("We've launched 40+ brands into China via CBEC. Feasibility to first sale in 90 days.",   None),
                    ('Your China market entry, handled. Platform setup, listing, logistics, marketing.',       None),
                    ('Not sure if China fits your brand? We run feasibility assessments before you commit.',   None),
                ],
            },
            {
                'name': '1D - CBEC vs General Trade',
                'keywords': [
                    'cbec vs general trade china',
                    'tmall global vs jd worldwide',
                    'tmall global vs jd worldwide which is better',
                ],
                'headlines': [
                    ('CBEC or General Trade?',       None),
                    ('Which China Model Fits You',   None),
                    ('CBEC vs General Trade',        None),
                    ('Pick the Right China Route',   None),
                    ('Cross-Border or Local?',       None),
                    ('We Help You Decide',           None),
                    ('China Entry: Two Routes',      None),
                    ('Compare CBEC & Local Trade',   None),
                    ('Smart China Market Entry',     None),
                    ("Don't Guess, Get Advice",      None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('CBEC or general trade? Wrong choice costs years and millions. We help you pick right.',   None),
                    ('Cross-border is faster but limited. General trade costs more. We advise on the fit.',    None),
                    ("Most brands don't know which China entry model fits. We've helped 40+ brands decide.",   None),
                    ('Clear comparison of CBEC vs general trade for your category and growth ambitions.',      None),
                ],
            },
            {
                'name': '1E - CBEC Platforms',
                'keywords': [
                    'tmall global consulting',
                    'tmall global agency',
                    'sell on tmall',
                    'how to sell on tmall',
                    'how to list products on tmall global',
                    'how to open tmall global store',
                    'jd worldwide consulting',
                    'china ecommerce platform consulting',
                ],
                'headlines': [
                    ('Tmall Global Experts',         None),
                    ('JD Worldwide Partner',         None),
                    ('Launch on Tmall Global',       None),
                    ('Sell on JD Worldwide',         None),
                    ('Tmall or JD? We Advise',       None),
                    ('CBEC Platform Setup China',    None),
                    ('Your Tmall Global Partner',    None),
                    ('Go Live on JD Worldwide',      None),
                    ('Platform Experts China',       None),
                    ('We Run Your China Store',      None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('Tmall Global or JD Worldwide? We pick the right platform and manage your store end to end.', None),
                    ('From store setup to daily operations. We run your Tmall Global or JD Worldwide business.', None),
                    ("Platform selection is the first critical decision. We've operated every major marketplace.", None),
                    ('Bonded warehouse, listing, pricing, store design. We handle the full CBEC stack.',         None),
                ],
            },
            {
                'name': '1F - CBEC by Industry',
                'keywords': [
                    'sell beauty products in china',
                    'sell cosmetics in china',
                    'sell health products in china',
                    'sell supplements in china ecommerce',
                    'sell food in china ecommerce',
                    'sell luxury brands in china',
                    'sell fashion in china',
                    'foreign brand china ecommerce',
                    'international brand china market',
                    'european brand china market entry',
                ],
                'headlines': [
                    ('Sell Beauty in China',         None),
                    ('Cosmetics CBEC China',         None),
                    ('Health Brands Enter China',    None),
                    ('Luxury Brands in China',       None),
                    ('Fashion Brands in China',      None),
                    ('Food & Supplements China',     None),
                    ('European Brands in China',     None),
                    ('Foreign Brands Sell China',    None),
                    ('Your Category, Our China',     None),
                    ('We Know Your Sector',          None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ("Beauty, health, food, fashion. We've launched brands in your category into China via CBEC.", None),
                    ('Regulatory needs vary by industry. We know which products work via CBEC vs local trade.',  None),
                    ('European and international brands trust us for China market entry. Niche to scale.',       None),
                    ('Your category shapes your China strategy. We tailor platform, pricing and content.',       None),
                ],
            },
        ],
    },
    {
        'name': 'BBG China Consulting EN',
        'budget': 'BBG Consulting Budget',
        'ad_groups': [
            {
                'name': '2A - Consulting Generic',
                'keywords': [
                    'china ecommerce consulting',
                    'china ecommerce consultant',
                    'ecommerce consulting china',
                    'china ecommerce strategy',
                    'china ecommerce strategy consulting',
                    'china ecommerce solutions',
                    'china ecommerce experts',
                    'china ecommerce advisor',
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
                'name': '2B - Market Entry Strategy',
                'keywords': [
                    'china market entry consulting',
                    'china market entry strategy',
                    'china market entry services',
                    'enter chinese market',
                    'how to enter china market',
                    'china market entry for brands',
                    'china market expansion consulting',
                    'china brand launch consulting',
                    'go to market strategy china',
                    'market entry strategy china consulting',
                    'china business entry consulting',
                ],
                'headlines': [
                    ('China Market Entry Strategy',  None),
                    ('Enter the China Market',       None),
                    ('Launch Your Brand in China',   None),
                    ('China Market Entry Experts',   None),
                    ('How to Enter China Market',    None),
                    ('China Go-to-Market Plan',      None),
                    ('Your China Launch Partner',    None),
                    ('Plan Your China Entry',        None),
                    ('Brand Launch China',           None),
                    ('China Expansion Consulting',   None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('Thinking about China? We plan realistic market entry strategies that lead to real sales.',  None),
                    ('Market entry is more than a platform. Distribution, pricing, regulatory. We plan it all.', None),
                    ("We've launched 40+ international brands into China. Strategy, setup, ongoing operations.", None),
                    ('China market entry done properly. Feasibility first, then a phased executable plan.',      None),
                ],
            },
            {
                'name': '2C - Feasibility & Cost',
                'keywords': [
                    'china ecommerce cost how much',
                    'china market entry cost consulting',
                    'is china ecommerce worth it for my brand',
                    'china market feasibility study',
                    'china market opportunity assessment',
                    'china ecommerce consulting for small brands',
                    'china market entry consulting for startups',
                ],
                'headlines': [
                    ('China Market Feasibility',     None),
                    ('How Much Does China Cost?',    None),
                    ('Is China Right for You?',      None),
                    ('China eCommerce ROI Check',    None),
                    ('China Budget Assessment',      None),
                    ('Before You Invest in China',   None),
                    ('China Market Readiness',       None),
                    ('Realistic China Budget Plan',  None),
                    ('China Entry Cost Analysis',    None),
                    ('Small Brand? Start Smart',     None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ("Not sure China is worth it? We run honest feasibility assessments. Just numbers.",        None),
                    ('We help brands understand the real cost of selling in China before committing budget.',   None),
                    ('Small brand, big China ambitions? We build lean entry strategies for your resources.',    None),
                    ('China entry costs vary wildly by model. Clear breakdown for your specific category.',     None),
                ],
            },
            {
                'name': '2D - Research & Positioning',
                'keywords': [
                    'china market research consulting',
                    'china consumer insights agency',
                    'china competitive analysis',
                    'china market feasibility study',
                    'china ecommerce market research',
                    'china brand positioning consulting',
                    'china market opportunity assessment',
                    'china retail consulting',
                    'china localization consulting',
                    'china product localization',
                ],
                'headlines': [
                    ('China Consumer Research',      None),
                    ('China Brand Positioning',      None),
                    ('China Market Intelligence',    None),
                    ('China Competitive Analysis',   None),
                    ('Know Your China Audience',     None),
                    ('China Localization Experts',   None),
                    ('China Product Localization',   None),
                    ('China Market Deep Dive',       None),
                    ('Understand Chinese Buyers',    None),
                    ('China Insight, Not Guesswork', None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('China strategy starts with consumer insight. We research your category and competition.', None),
                    ('China brand positioning is not translation. We build messaging that resonates locally.', None),
                    ('We analyze your China competitive landscape so you enter with a defensible position.',      None),
                    ('Product localization, naming, messaging, visual identity. Adapted for Chinese consumers.',  None),
                ],
            },
            {
                'name': '2E - Platform Comparison',
                'keywords': [
                    'china ecommerce platform consulting',
                    'tmall global vs jd worldwide which is better',
                ],
                'headlines': [
                    ('Tmall vs JD: Which One?',      None),
                    ('China Platform Comparison',    None),
                    ('Pick the Right Platform',      None),
                    ('Tmall Global or JD?',          None),
                    ('Which China Platform Fits?',   None),
                    ('Platform Strategy China',      None),
                    ("Don't Pick the Wrong One",     None),
                    ('Expert Platform Advice',       None),
                    ('Compare China Marketplaces',   None),
                    ('Douyin, Tmall, JD, RED?',      None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('Tmall, JD, Douyin, RED. Each platform serves a different purpose. We pick the right mix.', None),
                    ('Platform selection shapes margins, audience, trajectory. Get it right the first time.',   None),
                    ('Most brands pick their China platform on hearsay. We advise based on category data.',     None),
                    ("We've operated on every major Chinese marketplace. Advice from daily platform experience.", None),
                ],
            },
        ],
    },
    {
        'name': 'BBG China Agency EN',
        'budget': 'BBG Agency Budget',
        'ad_groups': [
            {
                'name': '3A - Agency Generic',
                'keywords': [
                    'china ecommerce agency',
                    'china ecommerce services',
                    'china ecommerce management',
                    'best agency to sell in china',
                    'china ecommerce agency for western brands',
                    'how to sell products in china online',
                    'western brand sell in china',
                    'canadian brand china market',
                    'australian brand china market',
                ],
                'headlines': [
                    ('China eCommerce Agency',       None),
                    ('Your China Sales Team',        None),
                    ('We Run Your China Store',      None),
                    ('China eCommerce, Managed',     None),
                    ('Best China eCommerce Agency',  None),
                    ('Sell More in China',           None),
                    ('China Revenue, Delivered',     None),
                    ('Full Service China Agency',    None),
                    ('We Grow China Sales',          None),
                    ('China Operations Handled',     None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ("We don't just advise. We run your China ecommerce business day to day. Full execution.",  None),
                    ('Store management, content, marketing, logistics. One team for your entire China operation.', None),
                    ("China ecommerce agency that actually runs stores. We manage 40+ brands across platforms.", None),
                    ("Senior practitioners, not junior consultants. We operate your China business like our own.", None),
                ],
            },
            {
                'name': '3B - Tmall',
                'keywords': [
                    'tmall consulting',
                    'tmall agency',
                    'tmall partner agency',
                    'tmall setup consulting',
                    'tmall store management',
                    'tmall for foreign brands',
                    'tmall market entry',
                    'tmall partner',
                    'tmall tp agency',
                    'open store tmall',
                ],
                'headlines': [
                    ('Tmall Agency',                 None),
                    ('Tmall Global Partner',         None),
                    ('Sell on Tmall Global',         None),
                    ('Tmall Store Management',       None),
                    ('Open Your Tmall Store',        None),
                    ('Tmall Global Experts',         None),
                    ('Tmall TP Agency',              None),
                    ('Launch on Tmall Global',       None),
                    ('Tmall for Foreign Brands',     None),
                    ('Your Tmall Partner Agency',    None),
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
                'name': '3C - JD.com',
                'keywords': [
                    'jd.com consulting',
                    'jd.com agency',
                    'sell on jd.com',
                    'jd worldwide consulting',
                    'jd.com partner agency',
                    'how to sell on jd china',
                    'jd.com store management',
                ],
                'headlines': [
                    ('JD.com Agency',                None),
                    ('Sell on JD.com',               None),
                    ('JD Worldwide Partner',         None),
                    ('JD.com Store Management',      None),
                    ('Launch on JD Worldwide',       None),
                    ('Your JD.com Partner',          None),
                    ('JD China Experts',             None),
                    ('JD Store Setup & Ops',         None),
                    ('JD Worldwide for Brands',      None),
                    ('Grow Sales on JD.com',         None),
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
                'name': '3D - Douyin',
                'keywords': [
                    'douyin ecommerce consulting',
                    'douyin agency',
                    'douyin for brands',
                    'douyin live commerce consulting',
                    'douyin shop setup',
                    'tiktok china ecommerce',
                    'douyin marketing agency',
                    'live commerce china consulting',
                    'china live streaming marketing',
                ],
                'headlines': [
                    ('Douyin eCommerce Agency',      None),
                    ('Douyin for Brands',            None),
                    ('China Live Commerce Experts',  None),
                    ('Sell on Douyin',               None),
                    ('Douyin Shop Setup',            None),
                    ('Live Selling in China',        None),
                    ('Douyin Marketing Agency',      None),
                    ('TikTok China eCommerce',       None),
                    ('Douyin Store Management',      None),
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
                'name': '3E - Xiaohongshu RED',
                'keywords': [
                    'xiaohongshu agency',
                    'little red book agency',
                    'red china marketing',
                    'xiaohongshu marketing consulting',
                    'little red book marketing consulting',
                    'xiaohongshu for brands',
                    'red ecommerce consulting',
                ],
                'headlines': [
                    ('Xiaohongshu Agency',           None),
                    ('Little Red Book Experts',      None),
                    ('RED China Marketing',          None),
                    ('Sell on Xiaohongshu',          None),
                    ('RED for Beauty Brands',        None),
                    ('Xiaohongshu for Brands',       None),
                    ('Little Red Book Agency',       None),
                    ('RED Content & Commerce',       None),
                    ('Grow on Xiaohongshu',          None),
                    ('Your RED China Partner',       None),
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
                'name': '3F - WeChat Social',
                'keywords': [
                    'wechat marketing agency',
                    'wechat consulting',
                    'wechat store setup',
                    'weibo marketing agency',
                    'wechat mini program agency',
                    'wechat ecommerce consulting',
                    'china social media agency',
                    'china social commerce consulting',
                ],
                'headlines': [
                    ('WeChat Marketing Agency',      None),
                    ('WeChat Store Setup',           None),
                    ('WeChat Mini Program Agency',   None),
                    ('China Social Commerce',        None),
                    ('WeChat eCommerce Experts',     None),
                    ('Sell via WeChat',              None),
                    ('WeChat for Brands',            None),
                    ('Build Your WeChat Store',      None),
                    ('China Social Media Agency',    None),
                    ('WeChat CRM & Commerce',        None),
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
            {
                'name': '3G - Digital Marketing KOL',
                'keywords': [
                    'china digital marketing agency',
                    'china digital marketing consulting',
                    'china digital marketing services',
                    'china online marketing agency',
                    'china seo agency',
                    'china sem agency',
                    'china ppc agency',
                    'china kol marketing',
                    'china influencer marketing agency',
                    'china content marketing agency',
                    'chinese digital strategy consulting',
                    'china social media marketing agency',
                    'china brand awareness consulting',
                    'china performance marketing agency',
                ],
                'headlines': [
                    ('China Digital Marketing',      None),
                    ('China KOL Marketing',          None),
                    ('China Influencer Agency',      None),
                    ('China Content Marketing',      None),
                    ('China Performance Marketing',  None),
                    ('KOL Campaigns That Convert',   None),
                    ('China Media Buying Agency',    None),
                    ('Reach Chinese Consumers',      None),
                    ('China Brand Awareness',        None),
                    ('Drive Sales in China',         None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('KOL campaigns, paid media, content production. Digital marketing that drives China sales.', None),
                    ("We don't just pick influencers. Full-funnel campaigns connecting awareness to purchases.", None),
                    ('China digital marketing needs local expertise. Campaigns across all major platforms.',    None),
                    ('Brand awareness to conversion. China marketing campaigns built around your sales targets.', None),
                ],
            },
        ],
    },
    {
        'name': 'BBG China Distribution EN',
        'budget': 'BBG Distribution Budget',
        'ad_groups': [
            {
                'name': '4A - Distributor Search',
                'keywords': [
                    'find distributor in china',
                    'how to find chinese distributor',
                    'china distributor consulting',
                    'china distribution strategy',
                ],
                'headlines': [
                    ('Find a Distributor China',     None),
                    ('China Distributor Search',     None),
                    ('Chinese Distributor Partner',  None),
                    ('Find Your China Partner',      None),
                    ('China Import Partner',         None),
                    ('Distributor Sourcing China',   None),
                    ('The Right China Distributor',  None),
                    ('We Find Your Distributor',     None),
                    ('China Partner Selection',      None),
                    ('Vetted China Distributors',    None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('Finding the right Chinese distributor is hardest. We source, vet and negotiate for you.', None),
                    ('Wrong distributor kills your brand in China. We find one that fits your category.',       None),
                    ("We've helped 40+ brands find distribution partnerships in China. Sourcing to contract.",  None),
                    ("Don't pick a China distributor blind. We assess fit, negotiate terms, monitor performance.", None),
                ],
            },
            {
                'name': '4B - Distribution Strategy',
                'keywords': [
                    'china distribution strategy',
                    'china distribution network',
                    'china retail distribution',
                    'china general trade',
                    'china omnichannel distribution',
                    'china channel strategy',
                ],
                'headlines': [
                    ('China Distribution Strategy',  None),
                    ('China Distribution Planning',  None),
                    ('Build Your China Network',     None),
                    ('China Retail Distribution',    None),
                    ('Omnichannel China Strategy',   None),
                    ('Offline Distribution China',   None),
                    ('China General Trade Setup',    None),
                    ('Distribution Architecture',    None),
                    ('China Channel Strategy',       None),
                    ('Scale Your China Network',     None),
                    ('Beyond Border Group',          1),
                    ('Book a Free Consultation',     3),
                ],
                'descriptions': [
                    ('Distribution in China is not one channel. Multi-channel architectures that reach buyers.', None),
                    ('Online, offline, general trade, CBEC. Distribution strategies matching your growth stage.', None),
                    ('Brands get China distribution wrong starting with one channel. We plan the full picture.', None),
                    ('General trade, key accounts, regional distributors. China distribution done properly.', None),
                ],
            },
        ],
    },
]

NEGATIVE_KEYWORDS = [
    'jobs','salary','career','internship','intern','course','training','free','pdf',
    'download','template','wikipedia','what is','definition','meaning','tutorial',
    'example','sample','case study','book','certification','degree','masters','mba',
    'reddit','quora','blog','news','amazon','alibaba','aliexpress','wish','shein','temu',
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def lookup(query):
    return list(ga_svc.search(customer_id=CUSTOMER_ID, query=query))

def get_or_create_budget(name):
    rows = lookup(f"SELECT campaign_budget.resource_name FROM campaign_budget WHERE campaign_budget.name = '{name}'")
    if rows:
        r = rows[0].campaign_budget.resource_name
        print(f'  budget reused: {name}')
        return r
    op = client.get_type('CampaignBudgetOperation')
    b = op.create
    b.name = name
    b.amount_micros = BUDGET_MICROS
    b.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    res = budget_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[op])
    r = res.results[0].resource_name
    print(f'  budget created: {name}')
    return r

def get_or_create_campaign(name, budget_resource):
    rows = lookup(f"SELECT campaign.resource_name FROM campaign WHERE campaign.name = '{name}' AND campaign.status != 'REMOVED'")
    if rows:
        r = rows[0].campaign.resource_name
        print(f'  campaign reused: {name}')
        return r
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
        lang_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=[op])
    except Exception:
        pass  # already set

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
    lang_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f'  {len(ops)} negative keywords added')

def get_or_create_adgroup(name, camp_resource):
    rows = lookup(f"SELECT ad_group.resource_name FROM ad_group WHERE ad_group.name = '{name}' AND ad_group.campaign = '{camp_resource}' AND ad_group.status != 'REMOVED'")
    if rows:
        r = rows[0].ad_group.resource_name
        print(f'    ag reused: {name}')
        return r
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
        kw.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
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
    print(f'    RSA created: {res.results[0].resource_name}')

# ── Main ──────────────────────────────────────────────────────────────────────
total_ag = sum(len(c['ad_groups']) for c in CAMPAIGNS)
print(f'\nCreating {len(CAMPAIGNS)} campaigns / {total_ag} ad groups in account {CUSTOMER_ID}')
print('All PAUSED — will not spend until manually enabled.\n')

for camp_data in CAMPAIGNS:
    print(f'\n[{camp_data["name"]}]')
    budget_r  = get_or_create_budget(camp_data['budget'])
    camp_r    = get_or_create_campaign(camp_data['name'], budget_r)
    add_language(camp_r)
    add_negatives(camp_r)

    for ag_data in camp_data['ad_groups']:
        print(f'\n  [{ag_data["name"]}]')
        ag_r = get_or_create_adgroup(ag_data['name'], camp_r)
        add_keywords(ag_r, ag_data['keywords'])
        add_rsa(ag_r, ag_data['headlines'], ag_data['descriptions'])

print('\n\nDone.')
print(f'Campaigns : {len(CAMPAIGNS)} (all PAUSED)')
print(f'Ad groups : {total_ag} (all PAUSED)')
print(f'Final URL : {FINAL_URL}')
print(f'Match type: EXACT')
print(f'Budget    : HKD 5/day per campaign')
print('\nReview in Google Ads UI, update final URLs per ad group, then enable when ready.')
