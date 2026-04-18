"""
수집 소스 정의.
- RSS_FEEDS: (카테고리, 이름, URL) — 기사용
- YOUTUBE_CHANNELS: 고정 채널 리스트 — 신기술·신사업·국제 비즈니스·경영자 인사이트 중심
"""

RSS_FEEDS = [
    # ── 국제 정세 / 해외 종합 ────────────────────────────────
    ("world", "BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("world", "Reuters World", "https://feeds.reuters.com/Reuters/worldNews"),
    ("world", "Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
    ("world", "The Guardian World", "https://www.theguardian.com/world/rss"),
    ("world", "NYT World", "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"),
    ("world", "AP Top News", "https://feeds.apnews.com/rss/apf-topnews"),

    # ── 테크 트렌드 / 혁신 ──────────────────────────────────
    ("tech", "TechCrunch", "https://techcrunch.com/feed/"),
    ("tech", "The Verge", "https://www.theverge.com/rss/index.xml"),
    ("tech", "Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("tech", "MIT Technology Review", "https://www.technologyreview.com/feed/"),
    ("tech", "Wired", "https://www.wired.com/feed/rss"),
    ("tech", "Hacker News Front", "https://hnrss.org/frontpage"),

    # ── 스타트업 / 사업 / 케이스 스터디 ──────────────────────
    ("startup", "Crunchbase News", "https://news.crunchbase.com/feed/"),
    ("startup", "Sifted (EU startups)", "https://sifted.eu/feed"),
    ("startup", "First Round Review", "https://review.firstround.com/feed"),
    ("startup", "Y Combinator Blog", "https://www.ycombinator.com/blog/rss"),
    ("startup", "a16z", "https://a16z.com/feed/"),
    ("startup", "Platum", "https://platum.kr/feed"),
    ("startup", "ByLine Network", "https://byline.network/feed/"),
    ("startup", "EO", "https://eopla.net/feed"),
]

# ──────────────────────────────────────────────────────────────
# YouTube: 테마별 고정 채널. (카테고리 이름은 UI 필터용 tag, 실제 섹션은 "videos" 하나로 합쳐짐)
# ──────────────────────────────────────────────────────────────
YOUTUBE_CHANNELS = [
    # 🚀 신기술 / 혁신 / 스타트업 이너 서클
    ("innovation", "Y Combinator",          "UCcefcZRL2oaA_uBNeo5UOWg"),
    ("innovation", "a16z",                   "UC9cn0TuPq4dnbTY-CBsm8XA"),
    ("innovation", "MIT Technology Review",  "UCT7uV-LjMSWtP6_uMlSc-aQ"),
    ("innovation", "TED",                    "UCAuUUnT6oDeKwE6v1NGQxug"),
    ("innovation", "Startup Grind",          "UC0CRYvGlWGlsGxBNgvkUbAg"),

    # 🎙 경영자·창업자 인사이트 / 마인드
    ("founder",    "Lex Fridman",            "UCSHZKyawb77ixDdsGog4iWA"),
    ("founder",    "How I Built This (NPR)", "UCzQUP1qoWDoEbmsQxvdjxgQ"),

    # 🌐 국제 사업·경제 동향
    ("business",   "Bloomberg Television",   "UCIALMKvObZNtJ6AmdCLP7Lg"),
    ("business",   "Wall Street Journal",    "UCK7tptUDHh-RYDsdxO1-5QQ"),
    ("business",   "Financial Times",        "UCNjsbTY6cJqB1FGYzMYR4iQ"),
    ("business",   "CNBC International",     "UCo7a6riBFJ3tkeHjvkXPn1g"),
]

# (더 이상 필요 없음 — 고정 채널 방식으로 통일)
YOUTUBE_SEARCH_QUERIES: list = []
