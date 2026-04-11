# Morning Brief

매일 아침 자동으로 갱신되는 개인용 브리핑 페이지.
국제 뉴스 / 테크 트렌드 / 스타트업 / 볼만한 영상을 한 화면에서 본다.

## 구조

```
morning-brief/
├── index.html / app.js     # 정적 프론트엔드 (Tailwind CDN)
├── data.json               # 매일 자동 갱신
├── scripts/
│   ├── build.py            # 수집 + 큐레이션
│   └── sources.py          # RSS / YouTube 소스 목록
├── .github/workflows/daily.yml  # 매일 KST 06:00 실행
└── requirements.txt
```

## 동작
1. GitHub Actions 가 매일 새벽 `build.py` 실행
2. RSS 피드 + YouTube Data API 로 후보 수집
3. Claude API 가 관심사 기반으로 상위 N개 큐레이션 (키 없으면 최신순 fallback)
4. `data.json` 커밋 → GitHub Pages 자동 배포

## 로컬에서 실행
```bash
pip install -r requirements.txt

# (선택) 키 설정 — 없어도 RSS만 수집해서 동작
export ANTHROPIC_API_KEY=sk-ant-...
export YOUTUBE_API_KEY=AIza...

python scripts/build.py
# → data.json 생성됨
# index.html 을 브라우저로 열거나 간단한 정적 서버 띄우기
python -m http.server 8000
# http://localhost:8000
```

## 배포 (GitHub Pages)
1. 새 GitHub 레포 만들고 이 폴더 push
2. Settings → Pages → Source = "GitHub Actions"
3. Settings → Secrets and variables → Actions 에서 등록:
   - `ANTHROPIC_API_KEY`
   - `YOUTUBE_API_KEY` (Google Cloud Console → YouTube Data API v3 활성화 후 키 발급)
4. Actions 탭 → `daily-build` → Run workflow 로 첫 빌드 수동 실행

## 커스터마이징
- **관심사 / 제외 조건**: `scripts/build.py` 상단의 `INTERESTS`, `EXCLUDE` 수정
- **소스 추가/제거**: `scripts/sources.py`
- **카테고리별 노출 개수**: `scripts/build.py` 의 `TARGET_COUNTS`
- **디자인**: `index.html` (Tailwind 클래스)
