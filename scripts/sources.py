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
    # ── 해외 7 : 산업·기술 트렌드 분석 + 창업자 인사이트 ─────
    ("innovation", "Y Combinator",      "UCcefcZRL2oaA_uBNeo5UOWg"),  # 스타트업 실전 트렌드
    ("innovation", "a16z",              "UC9cn0TuPq4dnbTY-CBsm8XA"),  # 벤처·기술 산업 분석
    ("deep_dive",  "Acquired",          "UCyFqFYfTW2VoIQKylJ04Rtw"),  # 기업 케이스 스터디
    ("analysis",   "All-In Podcast",    "UCESLZhusAkFfsNsApnjF_Cg"),  # 비즈니스·VC·뉴스 분석
    ("interview",  "Lex Fridman",       "UCSHZKyawb77ixDdsGog4iWA"),  # 창업자·석학 롱폼 인터뷰
    ("news",       "TLDR News Global",  "UC-uhvujip5deVcEtLxnW8qg"),  # 국제 뉴스 분석 요약
    ("trend",      "Cleo Abram",        "UC415bOPUcGSamy543abLmRA"),  # 신기술 트렌드 해설

    # ── 국내 3 : 슈카월드·EO 스타일의 다양한 비즈니스 큐레이션 ─
    ("kr",         "슈카월드",          "UCsJ6RuBiTVWRX156FVbeaGg"),  # 경제·산업 이슈 분석
    ("kr",         "EO 이오",           "UCQ2DWm5Md16Dc3xRwwhVE7Q"),  # 스타트업·창업자 스토리
    ("kr",         "티타임즈TV",        "UCelFN6fJ6OY6v8pbc_SLiXA"),  # 비즈니스 트렌드 해설
]

# (더 이상 필요 없음 — 고정 채널 방식으로 통일)
YOUTUBE_SEARCH_QUERIES: list = []
