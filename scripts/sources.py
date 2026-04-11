"""
수집 소스 정의.
- RSS_FEEDS: (카테고리, 이름, URL)
- YOUTUBE_CHANNELS: 공신력 있는 해외 채널 핸들 또는 채널 ID
- YOUTUBE_SEARCH_QUERIES: 추가 검색 쿼리
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
    # 국내
    ("startup", "Platum", "https://platum.kr/feed"),
    ("startup", "ByLine Network", "https://byline.network/feed/"),
    ("startup", "EO", "https://eopla.net/feed"),
]

# YouTube: (카테고리, 채널명, channelId 또는 핸들)
# channelId가 없으면 핸들로 검색해 ID를 얻는다.
YOUTUBE_CHANNELS = [
    ("world",   "Bloomberg Television", "UCIALMKvObZNtJ6AmdCLP7Lg"),
    ("world",   "Reuters",              "UChqUTb7kYRX8-EiaN3XFrSQ"),
    ("world",   "BBC News",             "UC16niRr50-MSBwiO3YDb3RA"),
    ("world",   "DW News",              "UCknLrEdhRCp1aegoMqRaCZg"),
    ("world",   "Wall Street Journal",  "UCK7tptUDHh-RYDsdxO1-5QQ"),
    ("world",   "Financial Times",      "UCNjsbTY6cJqB1FGYzMYR4iQ"),

    ("tech",    "Y Combinator",         "UCcefcZRL2oaA_uBNeo5UOWg"),
    ("tech",    "a16z",                 "UC9cn0TuPq4dnbTY-CBsm8XA"),
    ("tech",    "Lex Fridman",          "UCSHZKyawb77ixDdsGog4iWA"),
    ("tech",    "TED",                  "UCAuUUnT6oDeKwE6v1NGQxug"),
    ("tech",    "MIT Technology Review","UCT7uV-LjMSWtP6_uMlSc-aQ"),

    ("startup", "How I Built This",     "UCzQUP1qoWDoEbmsQxvdjxgQ"),
    ("startup", "Startup Grind",        "UC0CRYvGlWGlsGxBNgvkUbAg"),
]

# 검색어 기반 추가 수집 (테마 보강)
YOUTUBE_SEARCH_QUERIES = [
    ("tech",    "AI startup case study"),
    ("tech",    "tech innovation 2026"),
    ("startup", "founder interview"),
    ("world",   "geopolitics analysis"),
]
