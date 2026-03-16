# Design Styles Expansion + HTML Preview System

## Overview

기존 10종의 디자인 스타일을 산업/용도별 15종 추가하여 총 25종으로 확장하고, 각 스타일을 브라우저에서 시각적으로 비교할 수 있는 HTML 프리뷰 시스템을 구축한다. `/typst` 스킬의 Phase 2(디자인 선택)에 통합하여 사용자가 스타일을 선택할 때 자동으로 웹서버를 띄워 비교 후 선택할 수 있도록 한다.

## 1. NLM 리서치 전략

### 노트북 구성
- 노트북 1개 생성: `"PPT Design Trends by Industry"`

### 전체 NLM 워크플로우

```bash
# 1. 인증 확인
nlm login --check
# 실패 시: nlm login

# 2. 노트북 생성
nlm notebook create "PPT Design Trends by Industry"
# → 출력에서 NOTEBOOK_ID 캡처

# 3. 도메인별 리서치 실행 (8건, 각 ~30초)
nlm research start "presentation design trends healthcare medical 2024 2025" --notebook-id $NOTEBOOK_ID --mode fast
nlm research start "education academic slide deck design best practices" --notebook-id $NOTEBOOK_ID --mode fast
nlm research start "startup pitch deck design trends modern" --notebook-id $NOTEBOOK_ID --mode fast
nlm research start "marketing agency presentation design visual trends" --notebook-id $NOTEBOOK_ID --mode fast
nlm research start "finance banking corporate presentation style" --notebook-id $NOTEBOOK_ID --mode fast
nlm research start "creative agency portfolio presentation design" --notebook-id $NOTEBOOK_ID --mode fast
nlm research start "government public sector presentation accessibility" --notebook-id $NOTEBOOK_ID --mode fast
nlm research start "technology AI SaaS product presentation design" --notebook-id $NOTEBOOK_ID --mode fast

# 4. 각 리서치 완료 대기 및 소스 임포트
nlm research status $NOTEBOOK_ID --max-wait 120
# 각 task-id에 대해:
nlm research import $NOTEBOOK_ID $TASK_ID

# 5. 종합 분석 쿼리
nlm notebook query $NOTEBOOK_ID "For each industry domain (healthcare, education, startup, marketing, finance, creative, government, technology), summarize: (1) dominant color palettes with hex codes, (2) typography trends (serif vs sans, weight preferences), (3) layout patterns, (4) mood/tone adjectives, (5) common visual elements"
```

### 리서치-스타일 매핑

| 리서치 도메인 | → 생성할 스타일 |
|--------------|----------------|
| 의료 | medical-clinical, pharma-biotech |
| 교육 | edu-classroom, edu-research |
| 스타트업 | startup-pitch |
| 마케팅 | marketing-campaign, brand-storytelling |
| 금융 | finance-trust, consulting-strategy |
| 크리에이티브 | creative-portfolio |
| 공공 | gov-accessible, ngo-impact |
| 테크 | saas-product, retail-lifestyle, ai-futuristic |

### 산출물 형식

각 도메인별 리서치 결과를 다음 구조로 정리:
```markdown
### [도메인명]
- **색상**: primary hex, secondary hex, accent hex
- **타이포그래피**: 추천 폰트 패밀리, 웨이트
- **레이아웃**: 주요 패턴 (grid/cards/full-bleed 등)
- **분위기**: 형용사 3-5개
- **비주얼 요소**: 아이콘 스타일, 장식 패턴 등
```

리서치 결과가 특정 도메인에서 부실할 경우, 해당 도메인은 기존 디자인 지식 기반으로 보완한다.

## 2. 신규 디자인 스타일 (15종)

기존 10종에 추가:

| # | ID | 이름 | 타겟 도메인 |
|---|-----|------|------------|
| 11 | `medical-clinical` | 메디컬 클리니컬 / Medical Clinical | 의료/헬스케어 |
| 12 | `pharma-biotech` | 파마 바이오텍 / Pharma Biotech | 제약/바이오 |
| 13 | `edu-classroom` | 에듀 클래스룸 / Edu Classroom | 초중고 교육 |
| 14 | `edu-research` | 에듀 리서치 / Edu Research | 대학/연구기관 |
| 15 | `startup-pitch` | 스타트업 피치 / Startup Pitch | 스타트업 IR/피치덱 |
| 16 | `saas-product` | SaaS 프로덕트 / SaaS Product | B2B SaaS/테크 |
| 17 | `marketing-campaign` | 마케팅 캠페인 / Marketing Campaign | 광고/마케팅 에이전시 |
| 18 | `brand-storytelling` | 브랜드 스토리텔링 / Brand Storytelling | 브랜딩/크리에이티브 |
| 19 | `finance-trust` | 파이낸스 트러스트 / Finance Trust | 은행/금융/보험 |
| 20 | `consulting-strategy` | 컨설팅 스트래터지 / Consulting Strategy | 컨설팅/전략 |
| 21 | `gov-accessible` | 거버먼트 액세서블 / Gov Accessible | 공공기관/정부 |
| 22 | `ngo-impact` | NGO 임팩트 / NGO Impact | 비영리/사회적기업 |
| 23 | `creative-portfolio` | 크리에이티브 포트폴리오 / Creative Portfolio | 디자이너/포트폴리오 |
| 24 | `retail-lifestyle` | 리테일 라이프스타일 / Retail Lifestyle | 유통/라이프스타일 |
| 25 | `ai-futuristic` | AI 퓨처리스틱 / AI Futuristic | AI/딥테크/로보틱스 |

### 각 스타일 데이터 구조

`design-vocabulary.json` 엔트리:
```json
{
  "id": "medical-clinical",
  "name": "메디컬 클리니컬 / Medical Clinical",
  "description": "English description of the visual style...",
  "keywords": ["healthcare", "clinical", ...],
  "mood": "Mood phrase in English"
}
```

`color-themes.json` 엔트리 (9 필드):
```json
{
  "id": "medical-clinical",
  "primary": "#hex",
  "secondary": "#hex",
  "accent": "#hex",
  "background": "#hex",
  "surface": "#hex",
  "text": "#hex",
  "textLight": "#hex",
  "heading": "#hex",
  "border": "#hex"
}
```

### 참고 기준 컬러 (NLM 리서치 결과로 보정)

| ID | primary | secondary | accent | background | mood |
|----|---------|-----------|--------|------------|------|
| medical-clinical | #0077B6 | #48CAE4 | #00B4D8 | #F8FDFF | Clean trust |
| pharma-biotech | #2D6A4F | #40916C | #95D5B2 | #F0FFF4 | Scientific precision |
| edu-classroom | #FF6B35 | #FFB563 | #004E89 | #FFFBF5 | Energetic learning |
| edu-research | #1B4965 | #5FA8D3 | #CAE9FF | #F5F9FC | Scholarly depth |
| startup-pitch | #7209B7 | #F72585 | #4CC9F0 | #FFFFFF | Bold disruption |
| saas-product | #3A0CA3 | #4361EE | #4CC9F0 | #F8F9FF | Techy clarity |
| marketing-campaign | #FF006E | #FB5607 | #FFBE0B | #FFF8F0 | Vibrant energy |
| brand-storytelling | #2B2D42 | #8D99AE | #EF233C | #EDF2F4 | Editorial elegance |
| finance-trust | #003049 | #023E7D | #0077B6 | #F5F7FA | Institutional trust |
| consulting-strategy | #14213D | #FCA311 | #E5E5E5 | #FFFFFF | Strategic clarity |
| gov-accessible | #1B3A4B | #455A64 | #0288D1 | #FAFAFA | WCAG-compliant |
| ngo-impact | #606C38 | #DDA15E | #BC6C25 | #FEFAE0 | Earnest warmth |
| creative-portfolio | #0D0D0D | #FF4500 | #FFD700 | #FFFFFF | Avant-garde edge |
| retail-lifestyle | #E07A5F | #F2CC8F | #81B29A | #F4F1DE | Lifestyle warmth |
| ai-futuristic | #0A0E27 | #6C63FF | #00F5D4 | #0A0E27 | Cosmic intelligence |

**ai-futuristic vs tech-neon 차별화**: tech-neon은 회로 기판/네온 라인 미학(사이버펑크). ai-futuristic는 우주적/신경망 시각화 미학(딥스페이스 + 뉴럴넷 노드). tech-neon은 밝은 네온 그린(#00FF9C), ai-futuristic는 보라+민트(#6C63FF + #00F5D4).

### 스타일 이름 규칙
- 기존 10종과 동일: `"한글 이름 / English Name"` 형식
- description은 영어 (기존 패턴 유지)
- keywords는 영어

### JSON 버전
- `design-vocabulary.json`: version `"2.0.0"` (15종 추가)
- `color-themes.json`: version `"2.0.0"` (15종 추가)

## 3. HTML 프리뷰 시스템

### 기술 스택 제약
- **개별 스타일 페이지**: 순수 HTML + CSS (JavaScript 없음)
- **index.html, compare.html**: HTML + CSS + **바닐라 JavaScript** (필터링, iframe 로딩, 탭 전환에 필요)
- **외부 의존성 없음**: npm 패키지, CDN 사용 금지. 모든 코드가 로컬

### 디렉토리 구조
```
.claude/skills/typst/preview/
├── index.html              # 갤러리 메인 (JS: 도메인 필터링)
├── compare.html            # 사이드바이사이드 비교 (JS: iframe 로딩, 탭 전환)
├── styles/
│   ├── minimal-clean.html  # 각 스타일별 샘플 슬라이드 (25개, 순수 HTML+CSS)
│   ├── medical-clinical.html
│   └── ...
├── server.py               # 임시 웹서버 스크립트
└── assets/
    └── preview.css          # 공통 스타일시트 (리셋, 16:9 컨테이너, 타이포)
```

### 공유 샘플 콘텐츠 (모든 25개 스타일에 동일 적용)

**표지 슬라이드:**
- 제목: "2026 연간 사업 보고서"
- 부제: "성장과 혁신의 여정"
- 발표자: "홍길동 / 전략기획팀"
- 날짜: "2026년 3월"

**본문 슬라이드:**
- 제목: "핵심 성과 요약"
- 불릿 4개:
  - "매출 전년 대비 32% 성장 달성"
  - "신규 고객 1,200개사 확보"
  - "직원 만족도 4.5/5.0 기록"
  - "해외 시장 3개국 진출 완료"

**데이터 슬라이드:**
- 제목: "분기별 실적 추이"
- 데이터 4개:
  - Q1: 2.4억 (바 높이 40%)
  - Q2: 3.1억 (바 높이 52%)
  - Q3: 3.8억 (바 높이 63%)
  - Q4: 4.5억 (바 높이 75%)
- CSS로 구현한 수평 바 차트

### 갤러리 메인 (`index.html`)
- 25종 스타일을 카드 그리드로 나열 (반응형: 4열 → 2열 → 1열)
- 각 카드: 도메인 태그, 스타일 이름, 분위기 설명, 컬러 팔레트 원 5개 (primary~border 중 주요 5색)
- 카드 클릭 → 해당 스타일의 `styles/{id}.html` 로 이동
- 상단 도메인 필터 버튼 (JavaScript): 전체, 비즈니스, 교육, 테크, 크리에이티브, 공공/비영리, 라이프스타일
- 스타일 데이터는 `<script>` 태그 내 JSON 배열로 인라인 (fetch 불필요)

### 비교 뷰 (`compare.html`)
- **2개 드롭다운**으로 2개 스타일을 나란히 비교
- 각 드롭다운: 도메인별 `<optgroup>`으로 25개 스타일 그룹핑
- 선택 시 **iframe**으로 `styles/{id}.html` 로딩 (가장 단순한 동적 콘텐츠 로딩 방식)
- 표지 / 본문 / 데이터 3종 탭 전환: iframe에 `#cover`, `#content`, `#data` 앵커 전달
- 하단: 두 스타일의 컬러 팔레트 비교 테이블 (JavaScript로 동적 생성)

### 개별 스타일 페이지 (`styles/*.html`)
- 해당 스타일의 컬러/레이아웃을 적용한 샘플 슬라이드 3장
- 순수 HTML + CSS (JavaScript 없음)
- 각 슬라이드: `<section id="cover|content|data">` 로 앵커 대응
- 16:9 비율: `width: 960px; height: 540px;` (고정)
- 폰트: 시스템 폰트 스택 사용 (`-apple-system, "Noto Sans CJK KR", sans-serif`)
- CSS 변수로 테마 색상 주입: `--primary`, `--secondary`, `--accent`, `--bg`, `--text` 등

### 병렬 생성 전략
- **5개 Agent** (subagent_type: `oh-my-claudecode:executor`)가 각각 5개 스타일의 HTML을 동시 생성
- 각 agent에 공유 샘플 콘텐츠 + 해당 스타일의 컬러 테마 + CSS 템플릿 구조를 프롬프트로 전달
- `index.html`, `compare.html`, `server.py`, `preview.css`는 메인에서 생성 (병렬 agent 시작 전)

## 4. 웹서버 (`server.py`)

### 사양
- Python 표준 라이브러리만 사용 (`http.server`, `argparse`, `os`, `signal`)
- 기본 포트: 8432
- `--port` 옵션으로 변경 가능
- preview/ 디렉토리를 서빙 루트로 사용

### 에러 처리
- 포트 충돌: `socket.bind` 시도 → 실패하면 8433~8440 순차 시도 → 실제 바인딩된 포트를 stdout 출력
- 시작 시 `Server running at http://localhost:{port}` 출력
- PID 파일: `/tmp/beautiful-ppt-preview.pid`에 PID 기록 → 종료 시 자동 삭제 (`atexit`)
- `SIGTERM`, `SIGINT` 핸들러로 정리 종료

### 스킬에서의 사용 패턴
```bash
# 시작 (백그라운드)
python .claude/skills/typst/preview/server.py &

# 브라우저 열기 (macOS)
open http://localhost:8432

# 종료 (PID 파일 기반)
kill $(cat /tmp/beautiful-ppt-preview.pid)
```

## 5. 스킬 워크플로우 통합

### `/typst` 스킬 Phase 2 변경

```
기존: 페이지 수 선택 → 텍스트로 스타일 목록 → AskUserQuestion(4개 카테고리) → AskUserQuestion(카테고리 내 선택)
변경: 페이지 수 선택 → 웹서버 시작 → 브라우저 열기 → 사용자에게 탐색 안내 → 사용자가 선택을 말하면 → AskUserQuestion으로 최종 확인 → 서버 종료
```

### UX 흐름 상세

1. **서버 시작**: `python .claude/skills/typst/preview/server.py &` (백그라운드)
2. **브라우저 오픈**: `open http://localhost:8432` (macOS) / `xdg-open` (Linux)
3. **안내 메시지**: "브라우저에서 디자인 스타일을 탐색해주세요. 갤러리에서 카드를 클릭하면 상세 프리뷰를, Compare 탭에서 2개 스타일을 나란히 비교할 수 있습니다. 마음에 드는 스타일을 알려주세요."
4. **사용자 응답 대기**: 사용자가 텍스트로 스타일명 또는 번호를 말함 (예: "startup-pitch로 할게" 또는 "15번")
5. **최종 확인**: AskUserQuestion으로 "스타트업 피치 / Startup Pitch 스타일로 진행할까요?" 확인
6. **서버 종료**: `kill $(cat /tmp/beautiful-ppt-preview.pid)`

**핵심**: HTML 프리뷰는 **읽기 전용** 레퍼런스. 사용자가 스타일을 결정하면 **대화(텍스트)로** 에이전트에게 전달. AskUserQuestion은 최종 확인용 1회만 사용 (4개 옵션 제한과 무관).

### SKILL.md 업데이트 내용
- Phase 2에 프리뷰 서버 실행/종료 단계 추가
- 디자인 스타일 목록 25종으로 확장 (도메인별 카테고리 분류)
- `compare.html` 사용 안내 추가
- 프리뷰 서버가 없을 경우의 폴백: 기존 AskUserQuestion 카테고리 방식 유지

## 6. 파일 변경 목록

| 파일 | 액션 | 설명 |
|------|------|------|
| `assets/design-vocabulary.json` | 수정 | 15종 스타일 추가, version 2.0.0 |
| `assets/color-themes.json` | 수정 | 15종 컬러 테마 추가, version 2.0.0 |
| `SKILL.md` | 수정 | Phase 2 프리뷰 워크플로우, 25종 목록, 폴백 |
| `preview/index.html` | 신규 | 갤러리 메인 (JS 필터링) |
| `preview/compare.html` | 신규 | 사이드바이사이드 비교 (JS + iframe) |
| `preview/assets/preview.css` | 신규 | 공통 스타일시트 |
| `preview/server.py` | 신규 | 임시 웹서버 (포트 탐색, PID 관리) |
| `preview/styles/*.html` | 신규 | 25개 스타일별 샘플 (순수 HTML+CSS) |
| `README.md` | 수정 | 디자인 스타일 25종 테이블, 프리뷰 사용법 |

## 7. 검증 기준

### 스타일 품질
- 각 스타일의 컬러 대비 최소 4.5:1 (WCAG AA text contrast)
- 동일 도메인 내 스타일 간 시각적 차별화 확인

### HTML 프리뷰
- 25개 스타일 페이지 모두 16:9 비율 정확
- compare.html에서 임의 2개 조합 선택 시 정상 로딩
- 서버가 5초 내 시작, 포트 충돌 시 자동 대체

### 스킬 통합
- `/typst` 호출 시 Phase 2에서 서버 자동 시작/종료
- 서버 없이도 기존 AskUserQuestion 폴백 동작
