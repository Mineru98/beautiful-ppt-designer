# Beautiful-PPT

Typst 기반 프레젠테이션 자동 생성 도구. PDF/문서를 분석하고, 디자인 스타일을 선택하면 슬라이드를 생성하고 PPT로 내보냅니다.

## 워크플로우

```
PDF/문서 입력 → NotebookLM 콘텐츠 분석 → 페이지 수/디자인 선택 → Typst 슬라이드 생성 → 시각 검증 (3회) → PPT 내보내기
```

### 1. 콘텐츠 분석
NotebookLM 스킬을 통해 원본 문서의 핵심 내용을 추출합니다.

### 2. 사용자 설정
- **페이지 수**: 10 / 15 / 20 슬라이드 또는 직접 입력
- **디자인 스타일**: 10종 중 선택

### 3. 슬라이드 생성
선택한 테마의 색상과 템플릿을 적용하여 Typst로 슬라이드를 생성합니다.

### 4. 시각 검증
각 슬라이드를 PNG로 추출하여 텍스트 넘침, 여백, 가독성을 검증합니다. 3회 반복으로 품질을 보장합니다.

### 5. PPT 내보내기
최종 슬라이드를 `output/presentation.pptx`로 변환합니다.

## 디자인 스타일

| 스타일 | 분위기 |
|--------|--------|
| 미니멀 클린 | 차분한 전문성 |
| 코퍼레이트 모던 | 균형 잡힌 신뢰감 |
| 그라디언트 플로우 | 역동적이고 현대적 |
| 다크 엘레건트 | 세련된 프리미엄 |
| 네이처 오가닉 | 따뜻하고 친근한 |
| 테크 네온 | 미래지향적 혁신 |
| 파스텔 소프트 | 부드럽고 친절한 |
| 볼드 지오메트릭 | 강렬한 임팩트 |
| 클래식 아카데믹 | 격조 있는 학술풍 |
| 스칸디나비안 휘게 | 편안하고 세련된 |

## 사전 준비

```bash
brew install typst          # macOS
pip install python-pptx     # PPT 변환
uv tool install notebooklm-mcp-cli  # 콘텐츠 분석 (선택, pip install notebooklm-mcp-cli 도 가능)
nlm login                   # Google 계정 인증
```

## 사용법

Claude Code에서 다음과 같이 요청하세요:

```
프레젠테이션 만들어줘
```

또는 `/typst` 스킬을 직접 호출할 수 있습니다.

## 프로젝트 구조

```
.claude/skills/typst/
├── SKILL.md                          # 스킬 정의 (5단계 워크플로우)
├── assets/
│   ├── design-vocabulary.json        # 디자인 스타일 사전
│   └── color-themes.json             # 컬러 팔레트
├── references/
│   └── slide-templates.md            # Typst 슬라이드 템플릿 (9종)
└── scripts/
    └── export-ppt.py                 # PNG → PPTX 변환
.claude/skills/notebooklm/           # NotebookLM 연동 스킬
output/                               # PPT 출력 디렉토리 (.gitignore)
```
