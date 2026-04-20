"""
매일 아침 브리핑 데이터 생성기.

흐름:
  1) RSS 피드 수집 → 카테고리별 후보 기사
  2) YouTube Data API 수집 → 영상 후보
  3) Claude API로 관심사 기반 큐레이션 (각 카테고리 상위 N개 선별)
  4) data.json 으로 저장

환경 변수 (없으면 해당 단계 스킵):
  ANTHROPIC_API_KEY  : AI 큐레이션
  YOUTUBE_API_KEY    : YouTube 수집

로컬에서 직접 실행:
  python scripts/build.py
"""
from __future__ import annotations

import io
import json
import os
import sys
import time

# Windows 콘솔에서 UTF-8 출력 보장
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import feedparser
import requests
from dateutil import parser as dateparser

# ── 사용자 관심사 (큐레이션 프롬프트에 그대로 사용) ─────────────
INTERESTS = """
- 국제 정세를 파악할 수 있는 해외 뉴스
- 공신력 있는 해외 매체의 분석/해설 영상
- 혁신적인 사업, 새로운 기술 아이디어
- 실제 혁신 기업의 케이스 스터디
- 글로벌 테크 트렌드
- 해외 스타트업의 기술혁신 트렌드
- 국내 스타트업 기업 트렌드
""".strip()

EXCLUDE = """
- 단순 연예/가십, 국내 정치 가십, 스포츠 결과
- 광고성/홍보성 보도자료
- 클릭베이트성 제목
""".strip()

# 카테고리별 최종 노출 개수
TARGET_COUNTS = {
    "world": 8,
    "tech": 8,
    "startup": 8,
    "videos": 10,
}

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import RSS_FEEDS, YOUTUBE_CHANNELS, YOUTUBE_SEARCH_QUERIES  # noqa: E402


@dataclass
class Item:
    category: str       # world / tech / startup / videos
    kind: str           # "article" or "video"
    title: str
    url: str
    source: str
    published: str = ""  # ISO8601
    summary: str = ""
    thumbnail: str = ""
    extras: dict = field(default_factory=dict)


# ──────────────────────────────────────────────────────────────
# 1) RSS 수집
# ──────────────────────────────────────────────────────────────
def fetch_rss() -> list[Item]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)
    items: list[Item] = []
    for category, name, url in RSS_FEEDS:
        try:
            parsed = feedparser.parse(url, request_headers={"User-Agent": "morning-brief/1.0"})
        except Exception as e:
            print(f"[rss] {name} 실패: {e}", file=sys.stderr)
            continue
        for entry in parsed.entries[:25]:
            published = ""
            try:
                if getattr(entry, "published", None):
                    dt = dateparser.parse(entry.published)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    if dt < cutoff:
                        continue
                    published = dt.astimezone(timezone.utc).isoformat()
            except Exception:
                pass
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            if not title or not link:
                continue
            summary = (entry.get("summary") or "").strip()
            # HTML 태그 거칠게 제거
            summary = _strip_html(summary)[:400]
            items.append(
                Item(
                    category=category,
                    kind="article",
                    title=title,
                    url=link,
                    source=name,
                    published=published,
                    summary=summary,
                )
            )
        time.sleep(0.1)
    print(f"[rss] 수집된 항목: {len(items)}")
    return items


def _strip_html(text: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", text or "").strip()


# ──────────────────────────────────────────────────────────────
# 2) YouTube 수집 — 공개 RSS 우선, 실패 시 Data API fallback
# ──────────────────────────────────────────────────────────────
YT_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id={}"
YT_API = "https://www.googleapis.com/youtube/v3"
UA_BROWSER = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def _fetch_from_rss(channel_id: str, name: str, category: str, cutoff) -> list[Item]:
    """RSS 피드에서 최근 영상 수집. 404나 빈 피드면 빈 리스트 반환."""
    try:
        parsed = feedparser.parse(
            YT_RSS.format(channel_id),
            request_headers={"User-Agent": UA_BROWSER},
        )
    except Exception as e:
        print(f"[yt][rss] {name} 예외: {e}", file=sys.stderr)
        return []

    items: list[Item] = []
    for entry in parsed.entries[:5]:
        video_id = entry.get("yt_videoid") or entry.get("id", "").split(":")[-1]
        if not video_id:
            continue
        published = ""
        try:
            if getattr(entry, "published", None):
                dt = dateparser.parse(entry.published)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt < cutoff:
                    continue
                published = dt.astimezone(timezone.utc).isoformat()
        except Exception:
            pass

        thumb = ""
        thumbs = entry.get("media_thumbnail") or []
        if thumbs:
            thumb = thumbs[0].get("url", "")
        if not thumb:
            thumb = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"

        media_desc = entry.get("media_description") or entry.get("summary") or ""
        summary = _strip_html(media_desc)[:300]

        items.append(
            Item(
                category="videos",
                kind="video",
                title=(entry.get("title") or "").strip(),
                url=entry.get("link") or f"https://www.youtube.com/watch?v={video_id}",
                source=name,
                published=published,
                summary=summary,
                thumbnail=thumb,
                extras={"theme": category, "videoId": video_id, "via": "rss"},
            )
        )
    return items


def _fetch_from_api(channel_id: str, name: str, category: str, cutoff, api_key: str) -> list[Item]:
    """YouTube Data API v3 fallback. RSS가 실패했을 때만 호출."""
    try:
        published_after = cutoff.isoformat().replace("+00:00", "Z")
        r = requests.get(
            f"{YT_API}/search",
            params={
                "key": api_key,
                "channelId": channel_id,
                "part": "snippet",
                "order": "date",
                "type": "video",
                "maxResults": 5,
                "publishedAfter": published_after,
            },
            timeout=15,
        )
        r.raise_for_status()
    except Exception as e:
        print(f"[yt][api] {name} 실패: {e}", file=sys.stderr)
        return []

    items: list[Item] = []
    for it in r.json().get("items", []):
        vid = it["id"].get("videoId")
        if not vid:
            continue
        sn = it["snippet"]
        thumb = (sn.get("thumbnails", {}).get("medium", {}) or {}).get("url", "")
        if not thumb:
            thumb = f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg"
        items.append(
            Item(
                category="videos",
                kind="video",
                title=sn.get("title", "").strip(),
                url=f"https://www.youtube.com/watch?v={vid}",
                source=name,
                published=sn.get("publishedAt", ""),
                summary=(sn.get("description") or "")[:300],
                thumbnail=thumb,
                extras={"theme": category, "videoId": vid, "via": "api"},
            )
        )
    return items


def fetch_youtube() -> list[Item]:
    """고정 채널의 최신 영상을 수집. 채널별로 RSS 시도 후 비면 Data API로 재시도."""
    items: list[Item] = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=21)
    api_key = os.environ.get("YOUTUBE_API_KEY", "")

    for category, name, channel_id in YOUTUBE_CHANNELS:
        ch_items = _fetch_from_rss(channel_id, name, category, cutoff)
        if not ch_items and api_key:
            ch_items = _fetch_from_api(channel_id, name, category, cutoff, api_key)
        if not ch_items:
            print(f"[yt] {name}: 수집 실패 (RSS/API 모두)", file=sys.stderr)
        items.extend(ch_items)
        time.sleep(0.2)

    # 중복 제거
    seen = set()
    unique: list[Item] = []
    for it in items:
        if it.url in seen:
            continue
        seen.add(it.url)
        unique.append(it)
    print(f"[yt] 수집된 영상: {len(unique)}")
    return unique


# ──────────────────────────────────────────────────────────────
# 3) Claude 큐레이션
# ──────────────────────────────────────────────────────────────
CURATION_PROMPT = """당신은 매일 아침 사용자에게 브리핑을 제공하는 큐레이터입니다.

# 사용자 관심사
{interests}

# 제외 기준
{exclude}

# 작업
아래 후보 목록에서 "{category}" 카테고리의 가장 중요하고 흥미로운 항목 {n}개를 골라주세요.
- 사용자 관심사와 직접 관련된 것을 우선
- 단순 발표보다는 인사이트/분석/케이스가 있는 것을 우선
- 같은 사건을 다룬 중복은 1개만
- 클릭베이트, 가십, 광고성은 제외

# 후보 (id, source, title, summary)
{candidates}

# 출력 형식
선택한 항목의 id만 JSON 배열로 출력하세요. 다른 텍스트 없이 JSON만:
[12, 5, 7, ...]
"""


def curate(items: list[Item], category: str, n: int) -> list[Item]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    candidates = [it for it in items if it.category == category]
    if not candidates:
        return []
    if not api_key:
        # API 키가 없으면 발행시간 기준 최신순 fallback
        print(f"[curate] ANTHROPIC_API_KEY 없음 → '{category}' 최신순 fallback")
        return sorted(candidates, key=lambda x: x.published or "", reverse=True)[:n]

    # Claude에게 보낼 후보 목록 (id 부여)
    formatted = []
    for idx, it in enumerate(candidates):
        formatted.append(
            f"[{idx}] ({it.source}) {it.title}\n    {it.summary[:200]}"
        )
    prompt = CURATION_PROMPT.format(
        interests=INTERESTS,
        exclude=EXCLUDE,
        category=category,
        n=n,
        candidates="\n".join(formatted),
    )

    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        # JSON 추출
        start = text.find("[")
        end = text.rfind("]")
        if start == -1 or end == -1:
            raise ValueError(f"JSON 배열 못 찾음: {text[:200]}")
        ids = json.loads(text[start : end + 1])
        picked = [candidates[i] for i in ids if 0 <= i < len(candidates)]
        if not picked:
            raise ValueError("선택된 항목 없음")
        return picked[:n]
    except Exception as e:
        print(f"[curate] '{category}' 실패 → fallback: {e}", file=sys.stderr)
        return sorted(candidates, key=lambda x: x.published or "", reverse=True)[:n]


# ──────────────────────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────────────────────
def main() -> None:
    print(f"=== build start: {datetime.now(timezone.utc).isoformat()} ===")
    rss_items = fetch_rss()
    yt_items = fetch_youtube()
    all_items = rss_items + yt_items

    sections = {}
    # 기사 카테고리: AI 큐레이션 사용 (키 없으면 최신순 fallback)
    for cat in ("world", "tech", "startup"):
        picked = curate(all_items, cat, TARGET_COUNTS[cat])
        sections[cat] = [asdict(p) for p in picked]
        print(f"[final] {cat}: {len(picked)}개")

    # 비디오: 고정 채널의 최신 영상을 채널 다양성 유지하며 선택
    # - 채널당 상한을 2부터 시작해 점진적으로 올려가며 목표 개수를 채움
    # - 한 채널이 전체를 독점하는 것을 방지
    video_candidates = sorted(
        [it for it in all_items if it.category == "videos"],
        key=lambda x: x.published or "",
        reverse=True,
    )
    target = TARGET_COUNTS["videos"]
    picked: list = []
    for cap in range(2, 6):
        picked = []
        counts: dict = {}
        for it in video_candidates:
            if counts.get(it.source, 0) >= cap:
                continue
            picked.append(it)
            counts[it.source] = counts.get(it.source, 0) + 1
            if len(picked) >= target:
                break
        if len(picked) >= target:
            break
    sections["videos"] = [asdict(p) for p in picked]
    unique_channels = len({p.source for p in picked})
    print(f"[final] videos: {len(picked)}개 ({unique_channels}개 채널, 채널당 최대 {cap}개)")

    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "interests": INTERESTS,
        "sections": sections,
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"=== wrote {OUT_PATH} ===")


if __name__ == "__main__":
    main()
