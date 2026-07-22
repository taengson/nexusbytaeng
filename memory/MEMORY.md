# NexusByTaeng: Master Memory & Agentic Guideline

본 문서는 `nexusbytaeng` 프로젝트의 최상위 개발 기억(Memory) 컨트롤 타워입니다. 에이전틱 코딩(Agentic Coding) 시 AI가 컨텍스트를 즉시 동기화하고 일관된 설계 방향을 유지하도록 돕는 가이드라인을 포함합니다.

---

## 🧭 Project Architecture & Philosophy

- **Toad-Style Pattern**: `SideBar (ProjectTreePanel)` ➡️ `MainScreen (Workspace)` ➡️ `Conversation` ➡️ `MessageWidgets` 흐름의 독립적/유기적 연동.
- **AI-Network Workspace**: 단순 채팅앱을 넘어 소스 트리 탐색, 소스 디프(Diff) 분석, 독자적인 패널(AI Chat, Network Chat, File Viewer)이 통합된 결합형 워크스페이스 구축.
- **Strict Decoupling (UI ↔️ Logic)**: `src/widgets/` 및 `src/screens/` 등의 UI 컴포넌트는 오직 시각적 표현과 상태 피드백만 담당하며, 실제 LLM 연산 및 쉘 실행 등의 비즈니스 로직은 `src/core/` 하위 모듈에서 처리하도록 엄격히 격리.
- **License Compliance**: AGPL-3.0 오염 방지를 위해 기존 레거시(`examples/private_space`) 코드는 레퍼런스(UX/UI 모방)로만 사용하고 완전 재구현.

---

## 🗺️ Roadmap & Milestones

- [x] **Phase 1: Layout & Navigation Base** (완료 - 2026-07-15) [[MEMORY-2026-07-15]]
  - `HomeScreen` 허브 대시보드 구축 및 복귀 바인딩 (`h` 키) 제공.
  - `TabbedContent` 기반 세션 워크스페이스 활성화 흐름 설계.
- [x] **Phase 2: Toad-style Input System** (완료 - 2026-07-16) [[MEMORY-2026-07-16]]
  - `!` (쉘 실행), `/` (슬래시 명령어), `@` (경로/파일 제안) 실시간 파싱 및 상태 기반 라우팅 완료.
  - `ConfirmationModal` 및 `SuggestionPanel` 통합 UI 구현 완료.
- [ ] **Phase 3: Input UI/UX Polishing & Suggestions Logic** (진행 중 - 2026-07-16) [[MEMORY-2026-07-20]]
  - `#confirm-modal-container` 크기 최적화 및 쉘 출력용 `.shell-bubble` 스타일 적용.
  - `InputDispatcher` 실시간 `get_suggestions` 데이터 바인딩 및 자동완성 키 입력 이벤트 연결.
- [ ] **Phase 4: LLM Client & Network (WebSocket) Integration** (대기) [[MEMORY-2026-07-21]]
  - Multi-provider LLM을 지원하는 `AgentRegistry` 구현 및 `litellm` 연동.
  - 비동기 백기그라운드 태스크 기반 WebSocket 브로커 서버 및 네트워크 패널 완성.

---

## 🗺️ Component State Map

| 컴포넌트명 | 관련 파일 경로 | 현재 구현 상태 | 비고/제약 사항 |
| :--- | :--- | :--- | :--- |
| **Main Entry** | `src/main.py` | [완성] 메인 앱 루프 및 스크린 라우팅 | `HomeScreen` ↔️ `#workspace-container` 토글 처리 [[MEMORY-2026-07-15]] |
| **Home Screen** | `src/screens/home_screen.py` | [완성] 4개 AI/Network 연결 진입 허브 | 복귀 시 세션 작업 영역 자동 숨김 보장 [[MEMORY-2026-07-15]] |
| **Project Tree** | `src/widgets/project_tree.py` | [완성] 워크스페이스 내 프로젝트 소스 트리 | 탭 활성화 시에만 노출되도록 격리 [[MEMORY-2026-07-16]] |
| **Input Engine** | `src/core/input_engine.py` | [진행] `InputDispatcher` 등 파싱/검증 로직 | 실시간 `get_suggestions(text)` 제안 기능 고도화 필요 [[MEMORY-2026-07-16]], [[MEMORY-2026-07-20]] |
| **Input Area** | `src/widgets/input_area.py` | [진행] 모드별 테마 및 제안 패널 연동 UI | `on_change` 이벤트 연동 및 `.shell-bubble` 적용 대기 [[MEMORY-2026-07-20]] |
| **Suggestion UI**| `src/widgets/suggestions.py` | [진행] 추천 키워드 리스트 뷰 패널 | 패널 상단 안내 가이드 `Label` 추가 대기 [[MEMORY-2026-07-16]] |
| **Global Style** | `src/styles/nexus.tcss` | [진행] 다크 다이얼 테마 및 카드 메시지 버블 | 모달 창 컷팅 현상 방지 및 모드별 색상 튜닝 중 [[MEMORY-2026-07-20]] |
| **Global State** | `src/core/state.py` | [스켈레톤] 모드 및 액티브 세션 상태 제어 | 추후 세션 데이터 직렬화 시 확장 필요 [[MEMORY-2026-07-21]] |

---

## ⚠️ Crucial Guardrails (What NOT to do)

1. **MountError 절대 방지 (핵심)**:
   - Textual TUI에서 화면 전환 시 위젯을 반복해서 `mount` 및 `unmount`하면 마운트 레이스 컨디션 및 `MountError`가 발생합니다.
   - 항상 레이아웃 컨테이너를 한 번만 렌더링한 후, CSS `.hidden` 클래스 추가/제거 또는 `display: none/block` 처리를 통해 토글하십시오.
2. **사이드바 중복 금지**:
   - `NexusApp` 레벨의 전역 임시 사이드바를 절대 만들지 마십시오. 소스 트리 사이드바는 오직 `SessionWorkspace` 내부의 `ProjectTreePanel`로만 제한적으로 표현되어야 합니다.
3. **엄격한 패키지 모드 실행**:
   - 프로젝트는 항상 상위 디렉토리에서 패키지 모드인 `python3 -m src.main`으로 실행되어야 컴포넌트 간 상대 임포트가 깨지지 않습니다. `python src/main.py` 단독 실행을 금지합니다.
4. **네트워크 호출 타임아웃 보장**:
   - WebSocket 및 LLM 통신 시 메인 TUI 스레드가 얼지 않도록 항상 비동기(Async Task) 또는 쓰레드 풀을 활용하고, 명확한 `timeout` 설정을 적용해야 합니다.

---

## 🤖 AI Agent Execution Protocol

AI 에이전트는 작업을 할당받을 때마다 아래의 **5단계 라이프사이클**을 강제 준수해야 합니다.

```
 [1. Read] ──➡️ [2. Plan & Record] ──➡️ [3. Code] ──➡️ [4. Validate] ──➡️ [5. Update]
   - 마스터 리드      - 계획 수립 및 기록       - surgical edit     - 실행/테스트 검증     - 최종 결과 반영
   - 상태 동기화      - 일일 세션 파일 생성     - 안티패턴 방지     - 버그 및 에러 체크    - 인덱스/메모리 갱신
```

1. **Read Stage (컨텍스트 동기화)**:
   - 작업을 시작할 때 본 `memory/MEMORY.md`와 가장 최근 세션 로그(`memory/MEMORY-YYYY-MM-DD.md`)를 먼저 읽고 개발 컨텍스트를 완벽히 이해해야 합니다.
2. **Plan & Record Stage (계획 수립 및 기록)**:
   - **구현 계획이나 수정 계획이 수립되면, 즉시 당일 세션 파일(`memory/MEMORY-YYYY-MM-DD.md`)을 생성하거나 업데이트하여 해당 계획을 기록해야 합니다.**
   - 코드를 수정하기 전, 무엇을 어떻게 바꿀 것인지 기록하여 "바이브 코딩"의 의도와 설계 방향을 명확히 합니다.
3. **Code Stage (외과수술식 수정)**:
   - 불필요하게 연관 없는 주변 코드를 건드려 버그를 만들지 마십시오. 오직 해결해야 할 모듈을 타겟하여 정교하게(`surgical`) 수정하십시오.
   - 위의 **`Crucial Guardrails`**를 훼손하는 코드를 작성해서는 안 됩니다.
4. **Validate Stage (실행 및 무결성 검증)**:
   - 변경 사항을 적용한 후, 반드시 `python3 -m src.main` 실행 테스트 또는 단위 테스트 스크립트를 통해 에러 유무를 육안과 쉘 명령어로 검증해야 합니다.
5. **Update Stage (컨텍스트 영속화)**:
   - 작업 완료 후, 당일 세션 파일에 최종적으로 어떤 변경을 주었고 어떤 기술적 의사결정을 내렸는지 일지를 업데이트하여 마무리합니다.
   - 새로 발견된 제약 사항이 있다면 이 마스터 파일의 `Crucial Guardrails`에 추가하고, 컴포넌트의 구현 상황이 변했다면 `Component State Map`을 갱신하십시오.

---

## 📂 Session Logs Archive

과거 세션들의 구체적인 진행 상세 기록 목록입니다:

* [2026-07-14: 레거시 분석 기반 세션 복구 및 초기 핵심 목표 수립](./MEMORY-2026-07-14.md)
* [2026-07-15: 홈 화면 분리, 사이드바 중복 제거 및 네비게이션 구조화](./MEMORY-2026-07-15.md)
* [2026-07-16: Toad-style 실시간 명령어/쉘/경로 입력 엔진 설계 및 파일 레이아웃 완성](./MEMORY-2026-07-16.md)
