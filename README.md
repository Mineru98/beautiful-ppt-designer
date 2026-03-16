# Beautiful-PPT

Typst 기반 프레젠테이션 자동 생성 도구. PDF/문서를 분석하고, 디자인 스타일을 선택하면 슬라이드를 생성하고 PPT로 내보냅니다.

## 워크플로우

```
PDF/문서 입력 → NotebookLM 콘텐츠 분석 → 페이지 수/디자인 선택 → Typst 슬라이드 생성 → 시각 검증 (3회) → PPT 내보내기
```

### 1. 콘텐츠 분석
NotebookLM CLI(`nlm`)를 통해 원본 문서의 핵심 내용을 추출합니다.

### 2. 사용자 설정
- **페이지 수**: 10 / 15 / 20 슬라이드 또는 직접 입력
- **디자인 스타일**: 25종 중 선택 (브라우저 프리뷰 또는 텍스트 선택)

### 3. 슬라이드 생성
선택한 테마의 색상과 템플릿을 적용하여 Typst로 슬라이드를 생성합니다.

### 4. 시각 검증
각 슬라이드를 PNG로 추출하여 텍스트 넘침, 여백, 가독성을 검증합니다. 3회 반복으로 품질을 보장합니다.

### 5. PPT 내보내기
최종 슬라이드를 `output/presentation.pptx`로 변환합니다.

## 디자인 스타일 (25종)

### 비즈니스 / Business
| 스타일 | 분위기 |
|--------|--------|
| 미니멀 클린 | 차분한 전문성 |
| 코퍼레이트 모던 | 균형 잡힌 신뢰감 |
| 파이낸스 트러스트 | 제도적 신뢰감 |
| 컨설팅 스트래터지 | 전략적 명확함 |

### 모던 / Modern
| 스타일 | 분위기 |
|--------|--------|
| 그라디언트 플로우 | 역동적이고 현대적 |
| 다크 엘레건트 | 세련된 프리미엄 |
| 볼드 지오메트릭 | 강렬한 임팩트 |
| 브랜드 스토리텔링 | 에디토리얼 우아함 |

### 테크 / Tech
| 스타일 | 분위기 |
|--------|--------|
| 테크 네온 | 미래지향적 혁신 |
| SaaS 프로덕트 | 테크 명확함 |
| AI 퓨처리스틱 | 우주적 지능 |

### 교육 / Education
| 스타일 | 분위기 |
|--------|--------|
| 에듀 클래스룸 | 활기찬 학습 |
| 에듀 리서치 | 학문적 깊이 |
| 클래식 아카데믹 | 격조 있는 학술풍 |

### 의료 / Healthcare
| 스타일 | 분위기 |
|--------|--------|
| 메디컬 클리니컬 | 깨끗한 신뢰감 |
| 파마 바이오텍 | 과학적 정밀함 |

### 공공 / Public
| 스타일 | 분위기 |
|--------|--------|
| 거버먼트 액세서블 | WCAG 접근성 |
| NGO 임팩트 | 진정성 있는 따뜻함 |

### 크리에이티브 / Creative
| 스타일 | 분위기 |
|--------|--------|
| 크리에이티브 포트폴리오 | 아방가르드 |
| 스타트업 피치 | 대담한 파괴력 |
| 마케팅 캠페인 | 비비드 에너지 |

### 라이프스타일 / Lifestyle
| 스타일 | 분위기 |
|--------|--------|
| 네이처 오가닉 | 따뜻하고 친근한 |
| 파스텔 소프트 | 부드럽고 친절한 |
| 스칸디나비안 휘게 | 편안하고 세련된 |
| 리테일 라이프스타일 | 라이프스타일 따뜻함 |

## 디자인 프리뷰

브라우저에서 25종의 디자인 스타일을 시각적으로 비교할 수 있습니다.

```bash
python .claude/skills/typst/preview/server.py
# http://localhost:8432 에서 갤러리 및 비교 뷰 확인
```

## 사전 준비

```bash
brew install typst                       # macOS (Typst 설치)
pip install python-pptx                  # PPT 변환
uv tool install notebooklm-mcp-cli      # 콘텐츠 분석 (pip install notebooklm-mcp-cli 도 가능)
nlm login                                # Google 계정 인증
```

## 사용법

Claude Code에서 다음과 같이 요청하세요:

```
프레젠테이션 만들어줘
```

또는 `/typst` 스킬을 직접 호출할 수 있습니다.

## 프로젝트 구조

```
beautiful-ppt/
├── .claude/
│   └── skills/
│       ├── typst/                        # Typst 프레젠테이션 생성 스킬
│       │   ├── SKILL.md                  # 스킬 정의 (5단계 워크플로우)
│       │   ├── assets/
│       │   │   ├── design-vocabulary.json  # 디자인 스타일 사전 (25종)
│       │   │   └── color-themes.json       # 컬러 팔레트 (25종)
│       │   ├── preview/                    # HTML 프리뷰 시스템
│       │   │   ├── index.html              # 갤러리 (도메인 필터)
│       │   │   ├── compare.html            # 사이드바이사이드 비교
│       │   │   ├── server.py               # 로컬 웹서버
│       │   │   ├── assets/preview.css      # 공통 스타일시트
│       │   │   └── styles/*.html           # 25개 스타일 프리뷰
│       │   ├── references/
│       │   │   └── slide-templates.md      # Typst 슬라이드 템플릿
│       │   └── scripts/
│       │       └── export-ppt.py           # PNG → PPTX 변환 스크립트
│       └── nlm-cli-skill/                # NotebookLM CLI 연동 스킬
│           ├── SKILL.md                  # 스킬 정의 (nlm 사용 가이드)
│           └── references/
│               ├── command_reference.md    # 전체 명령어 레퍼런스
│               ├── workflows.md            # 워크플로우 예제
│               └── troubleshooting.md      # 문제 해결 가이드
├── output/                               # PPT 출력 디렉토리
├── .gitignore
├── LICENSE
└── README.md
```
