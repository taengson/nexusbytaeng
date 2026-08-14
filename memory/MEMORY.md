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
- [x] **Phase 3: Input UI/UX Polishing & Suggestions Logic** (완료 - 2026-07-20) [[MEMORY-2026-07-20]]
  - `#confirm-modal-container` 크기 최적화 및 쉘 출력용 `.shell-bubble` 스타일 적용.
  - `InputDispatcher` 실시간 `get_suggestions` 데이터 바인딩 및 자동완성 키 입력 이벤트 연결.
- [x] **Phase 3.5: ACP 통합** (완료 - 2026-07-27) [[MEMORY-2026-07-27]]
  - `HERMES_ACP` 모드로 단일화, `ACPClient` 기반 JSON-RPC 통신 완료.
  - `HomeScreen` 진입로 확보, Raw Pipe(`HERMES`) 제거.
  - `agent_process.py` 디버그 코드 정제.
- [x] **Phase 3.6: ACP UI/UX 폴리싱** (완료 - 2026-07-27) [[MEMORY-2026-07-27]]
  - P0: 메시지 스택 쌓임 문제 (`_active_ai_widget` 기반 위젯 추적).
  - P1: AI 응답 로깅 완결 (`call_later` 기반 2초 타임아웃 플러시).
  - P2: Think/Response 시각적 분리 (`sender="thought"` 별도 위젯).
  - P3: ACP 연결 상태 시각적 개선 (`#acp-status-bar` + 단계별 색상).
  - P4: Tool 이름 `None` 로깅 수정 (`name`/`toolName` 교차 확인).
- [x] **Phase 3.7: ACP 버그 수정 및 로깅 무결성 확보** (완료 - 2026-07-28) [[MEMORY-2026-07-28]]
  - Response 소실 해결: `update_last_ai_message`에 sender 일치 체크 추가.
  - Think 쪼개짐 해결: `agent_thought_chunk` 조건부 리셋으로 위젯 누적.
  - 쉘 입력 유출 차단: `on_input_result`에 `is_shell` 체크 추가.
  - 로그 분절 해결: 토큰 기반 타이머 무효화로 중복 로깅 방지.
  - 버퍼 플러시: `on_remove`에서 남은 응답 버퍼 강제 기록.
  - 세션 모드 로깅: `start_session`에 `mode_name` 파라미터 추가.
  - ACP 세션 ID 로깅: 연결 성공 시 `sessionId` 기록.
  - 쉘 명령어 가시성: 입력값을 UI/로그에 먼저 표시.
  - Dead Code 제거: Raw Pipe 모드 관련 import 및 메서드 제거.
- [x] **Phase 3.8: Gemini ACP 통합** (완료 - 2026-07-29) [[MEMORY-2026-07-29]]
  - `ConnectionMode.GEMINI_ACP` 상수 추가, 기존 `GEMINI` 모드 통합.
  - `HomeScreen` Gemini ACP 진입로 단일화.
  - `session_workspace.py`에서 `command=["gemini", "--acp"]`로 ACPClient 생성.
  - P0 해결: `on_input_result`에서 `GEMINI_ACP` 조건 추가 → 프롬프트 전송 정상화.
  - Hermes ACP, Gemini ACP 모두 정상 동작 검증 완료.
- [x] **Phase 3.9: OpenCode ACP 통합** (완료 - 2026-07-30) [[MEMORY-2026-07-30]]
  - `ConnectionMode.OPENCODE_ACP` 상수 추가, 일관성 유지를 위해 `_ACP` 접미사 유지.
  - `get_display_name()` 메서드로 사용자 친화적 이름 표시 ("OpenCode 연결").
  - `session_workspace.py` 에서 `command=["opencode", "acp"]` 로 ACPClient 연결 구현.
  - Toad 패턴 참조: 에이전트 설정 파일 기반 명령어 실행.
  - P0 해결: 3 에이전트 (Gemini, OpenCode, Hermes) 모두 정상 연결 및 응답 검증.
  - 변경 파일: `state.py`, `session_workspace.py`, `input_area.py`, `home_screen.py` (4 파일, ~22 줄).
- [x] **Phase 3.10: 코드베이스 감사 및 보안/안정성 개선** (완료 - 2026-08-13) [[MEMORY-2026-08-13]]
  - `git pull` 충돌 해결: tracked `__pycache__` 제거.
  - 보안: `shell=True` 사용 제거 → `shlex.split` + `shell=False` / `create_subprocess_exec` 적용.
  - ACP 안정성: `call_next` 람다 래핑, `stop()` 타임아웃 후 강제 종료, response 중복 라우팅 제거.
  - UI 복구: ACP 연결 실패 시 `input_area.can_focus = True` 복원.
  - 실시간 제안: `@` 접두사 파일/경로 제안 구현 및 `SuggestionPanel` 연동.
  - 로깅: 파일 I/O 버퍼링, `flush()` 인터페이스 추가.
  - 코드 정제: `TypedDict NotRequired`, `ProjectTree` 동적 경로, `TabbedContent.tab_count` API 교체, `home_screen` 데이터 기반 버튼 생성.
- [x] **Phase 4: ACP Enhancement & Agent Stability** (완료 - 2026-08-13) [[MEMORY-2026-08-13]]
  - ACP protocol 강화: 재연결, 세션 지속성, 스트리밍 최적화.
  - 3 에이전트 (Hermes, Gemini, OpenCode) 안정성 확보.
  - 에러 처리 및 복구 로직 고도화.
- [ ] **Phase 5: A2A Client Integration** (대기)
  - A2A (Agent2Agent Protocol) 클라이언트 구현.
  - 외부 A2A 에이전트 발견 (AgentCard discovery via `/.well-known/agent.json`).
  - Task lifecycle 기반 메시지 흐름 (`submitted → working → completed`).
  - `nexusbytaeng`를 A2A 클라이언트로 활용하여 외부 에이전트와 협업.
- [ ] **Phase 6: ANP / DID Federation** (대기)
  - ANP (Agent Network Protocol) 기반 연합 실험.
  - W3C DID 기반 에이전트 정체성 탐구.
  - 메타-프로토콜 협상 개념 검토 및 적용 방안 수립.
- [ ] **Phase 7: Polish & Stability** (대기)
  - 애니메이션 및 전환 효과 다듬기.
  - 다중 에이전트 컨텍스트 스위칭 스트레스 테스트.
  - 문서화 및 설정 예시 최종 정리.

---

## 🗺️ Component State Map

| 컴포넌트명 | 관련 파일 경로 | 현재 구현 상태 | 비고/제약 사항 |
| :--- | :--- | :--- | :--- |
| **Main Entry** | `src/main.py` | [완성] 메인 앱 루프 및 스크린 라우팅 | `TabbedContent` 탭 개수를 `query(TabPane)`로 안전하게 계산 [[MEMORY-2026-08-13]] |
| **Home Screen** | `src/screens/home_screen.py` | [완성] 4개 AI/Network 연결 진입 허브 | `HOME_BUTTONS` 데이터 기반 버튼 생성으로 `ConnectionMode`와 순서/아이콘 동기화 [[MEMORY-2026-08-13]] |
| **Project Tree** | `src/widgets/project_tree.py` | [완성] 워크스페이스 내 프로젝트 소스 트리 | 동적 `update_path()` 지원, 초기 `os.getcwd()` 기본값 유지 [[MEMORY-2026-08-13]] |
| **Input Engine** | `src/core/input_engine.py` | [완성] `InputDispatcher` 파싱/검증 및 실시간 제안 | `shlex.split` 기반 안전한 쉘 실행, `@` 접두사 파일/경로 제안 구현 완료 [[MEMORY-2026-08-13]] |
| **Input Area** | `src/widgets/input_area.py` | [완성] 모드별 테마 및 제안 패널 연동 UI | `on_change` 이벤트로 `SuggestionPanel` 실시간 업데이트 연동 완료 [[MEMORY-2026-08-13]] |
| **Suggestion UI**| `src/widgets/suggestions.py` | [완성] 추천 키워드 리스트 뷰 패널 | 상단 안내 가이드 `Label` 포함, `hidden`/`display` 속성 통일 [[MEMORY-2026-08-13]] |
| **Global Style** | `src/styles/nexus.tcss` | [진행] 다크 다이얼 테마 및 카드 메시지 버블 | 모달 창 컷팅 현상 방지 및 모드별 색상 튜닝 중 [[MEMORY-2026-07-20]] |
| **Global State** | `src/core/state.py` | [완성] 모드 및 액티브 세션 상태 제어 | `HERMES_ACP`, `GEMINI_ACP`, `OPENCODE_ACP` 상수 추가, `get_display_name()` 으로 사용자 친화적 이름 표시 [[MEMORY-2026-07-27]], [[MEMORY-2026-07-29]], [[MEMORY-2026-07-30]] |
| **ACP Client** | `src/core/acp.py` | [완성] JSON-RPC 2.0 통신, 핸드셰이크, 스트리밍 | `call_next` 람다 래핑, `stop()` 5초 타임아웃 후 강제 종료, response 중복 라우팅 제거 [[MEMORY-2026-08-13]] |
| **Chat Logger** | `src/core/logger.py` | [완성] 일별 Markdown 로그 기록 | 버퍼 기반 쓰기 + 명시적 `flush()`, P1 AI 응답 로깅 완결 [[MEMORY-2026-08-13]] |
| **Stream Parser** | `src/core/stream_parser.py` | [완성] Raw pipe용 줄 단위 메시지 파싱 | ACP 모드에서는 미사용, Raw pipe 모드 전용 [[MEMORY-2026-07-27]] |
| **Session Workspace** | `src/widgets/session_workspace.py` | [완성] 메시지 스택, Think 분리, 연결 상태 바, 로깅, 쉘 유출 차단, **OpenCode ACP 연결** | `_active_ai_widget` 기반 위젯 추적, `#acp-status-bar` 상태 표시, 토큰 기반 타이머 무효화, is_shell 체크, **OPENCODE_ACP 분기 추가** [[MEMORY-2026-07-27]], [[MEMORY-2026-07-28]], [[MEMORY-2026-07-29]], [[MEMORY-2026-07-30]] |

---

## ⚠️ Crucial Guardrails (What NOT to do)

1. **MountError 절대 방지 (핵심)**:
   - Textual TUI에서 화면 전환 시 위젯을 반복해서 `mount` 및 `unmount`하면 마운트 레이스 컨디션 및 `MountError`가 발생합니다.
   - 항상 레이아웃 컨테이너를 한 번만 렌더링한 후, CSS `.hidden` 클래스 추가/제거 또는 `display: none/block` 처리를 통해 토글하십시오.
2. **사이드바 중복 금지**:
   - `NexusApp` 레벨의 전역 임시 사이드바를 절대 만들지 마십시오. 소스 트리 사이드바는 오직 `SessionWorkspace` 내부의 `ProjectTreePanel`로만 제한적으로 표현되어야 합니다.
3. **엄격한 패키지 모드 실행 (venv 권장)**:
   - 프로젝트는 항상 가상 환경(venv)의 Python을 사용하고, 상위 디렉토리에서 패키지 모드인 `./venv/bin/python -m src.main`으로 실행되어야 컴포넌트 간 상대 임포트가 깨지지 않습니다. `python src/main.py` 단독 실행을 금지합니다.
4. **네트워크 호출 타임아웃 보장**:
   - WebSocket 및 LLM 통신 시 메인 TUI 스레드가 얼지 않도록 항상 비동기(Async Task) 또는 쓰레드 풀을 활용하고, 명확한 `timeout` 설정을 적용해야 합니다.
5. **쉘 명령어 실행 보안 (핵심)**:
   - 외부/사용자 입력이 포함된 모든 쉘 호출은 `shell=True`를 사용하지 말고, `shlex.split` 후 `subprocess.run(..., shell=False)` 또는 `asyncio.create_subprocess_exec`를 사용하여 명령어 인젝션을 방지하십시오.
6. **ACP 프로세스 생명주기 관리**:
   - ACP 에이전트 프로세스를 종료할 때 `terminate()` 후 `asyncio.wait_for(process.wait(), timeout=...)`로 타임아웃을 두고, 응답이 없으면 `kill()`로 강제 종료하십시오. 무한 대기는 메인 TUI 스레드를 얼릴 수 있습니다.
7. **UI 스레드 안전성**:
   - Textual의 `call_next`는 인자 없는 callable만 받습니다. UI 콜백에 데이터를 전달할 때는 반드시 `lambda: callback(data)` 형태로 래핑하십시오.

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
    - **중요**: 세션 파일 기록 시 `write` 도구로 전체를 덮어쓰지 말고, 기존 내용을 보존하며 하단에 새로운 기록을 추가(Append)하는 방식으로 히스토리를 유지하십시오.
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

## 🏷️ 협업 태그 규칙

`memory/` 폴더의 모든 세션 파일은 역할 구분 태그를 반드시 붙입니다:

| 태그 | 작성자 | 내용 |
|---|---|---|
| `[리뷰어]` | 리뷰어/기획자 | 코드 분석, 문제 발견, 수정 제안, 설계 판단 |
| `[개발자]` | 코드 개발자 | 구현 계획, 구현 결과, 테스트 보고, 피드백 |

- **규칙**: 제목과 섹션 구분선에 태그를 붙여 `[리뷰어] 분석`, `[개발자] 구현 완료` 형식 사용
- **목적**: 한 파일 안에서 누가 무엇을 썼는지 즉시 식별 가능
- 예: `## 🔍 [리뷰어] ACP 코드 리뷰 결과`, `## 🛠 [개발자] 구현 완료`

---

## 📂 Session Logs Archive

과거 세션들의 구체적인 진행 상세 기록 목록입니다:

* [2026-07-14: 레거시 분석 기반 세션 복구 및 초기 핵심 목표 수립](./MEMORY-2026-07-14.md)
* [2026-07-15: 홈 화면 분리, 사이드바 중복 제거 및 네비게이션 구조화](./MEMORY-2026-07-15.md)
* [2026-07-16: Toad-style 실시간 명령어/쉘/경로 입력 엔진 설계 및 파일 레이아웃 완성](./MEMORY-2026-07-16.md)
* [2026-07-20: Input UI/UX 폴리싱 진행](./MEMORY-2026-07-20.md)
* [2026-07-21: LLM Client & Network Integration 계획](./MEMORY-2026-07-21.md)
* [2026-07-22: 추가 작업 진행](./MEMORY-2026-07-22.md)
* [2026-07-23: ACP 기초 인프라 구축 및 근본 원인 분석](./MEMORY-2026-07-23.md)
* [2026-07-27: ACP 완전 전환, Raw Pipe 제거, UI/UX 폴리싱 문제 발견](./MEMORY-2026-07-27.md)
* [2026-07-28: ACP 버그 수정, 로깅 무결성 확보, 쉘 입력 유출 차단](./MEMORY-2026-07-28.md)
* [2026-07-29: Gemini ACP 통합, P0 응답 미수신 해결](./MEMORY-2026-07-29.md)
* [2026-07-30: OpenCode ACP 통합, ConnectionMode 리팩토링, 3 에이전트 정상 동작 검증](./MEMORY-2026-07-30.md)
* [2026-08-11: 불필요한 '로컬 AI 연결' 항목 제거 및 코드 정제](./MEMORY-2026-08-11.md)
* [2026-08-13: `git pull` 충돌 해결, 코드베이스 감사, Critical/High/Medium 이슈 수정 및 문서화](./MEMORY-2026-08-13.md)
