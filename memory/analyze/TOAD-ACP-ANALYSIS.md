# Toad ACP 에이전트 통합 분석

## 핵심: ACP (Agent Client Protocol)
https://agentclientprotocol.com - 표준 프로토콜로 JSON-RPC 기반 양방향 통신

## 통신 구조

```
Toad (클라이언트) ←→ 파이프(stdin/stdout) ←→ 에이전트 프로세스
       JSON-RPC Server                         JSON-RPC Client
       session/update 등                       initialize, session/new, session/prompt
```

### 파이프 기반 (PTY 아님)
- `asyncio.create_subprocess_shell(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)`
- 에이전트는 `run_command`에서 정의된 명령 실행 (예: `opencode acp`)
- 표준 입출력으로 JSON-RPC 메시지 교환

### JSON-RPC 양방향 흐름

**Toad → 에이전트 (API.method):**
- `initialize()` - 프로토콜 버전, 클라이언트 능력 정보 교환
- `session_new()` / `session_load()` - 세션 생성/복원
- `session_prompt(prompt, session_id)` - 프롬프트 전송
- `session_cancel()` - 중지 요청

**에이전트 → Toad (@jsonrpc.expose 핸들러):**
- `session/update` - 스트리밍 chunks (text, tool, plan, thought, usage)
- `fs/read_text_file` - 프로젝트 파일 읽기
- `fs/write_text_file` - 프로젝트 파일 쓰기
- `terminal/create` - 터미널 생성 요청 (Toad의 Terminal 위젯 사용)
- `terminal/output`, `terminal/kill`, `terminal/wait_for_exit`
- `session/request_permission` - 도구 호출 권한 요청

### 메시지 유형 (에이전트 → UI)

| Message | 설명 |
|---|---|
| `Update(text)` | 에이전트 응답 텍스트 (스트리밍) |
| `Thinking(text)` | 생각 과정 |
| `ToolCall(tool_call)` | 도구 호출 시작 |
| `ToolCallUpdate(tool_call, update)` | 도구 호출 상태 업데이트 |
| `Plan(entries)` | 작업 계획 |
| `RequestPermission(options, tool_call, future)` | 권한 요청 (Future로 응답 대기) |
| `CreateTerminal(terminal_id, command, ...)` | 터미널 생성 |
| `SetModes(current_mode, modes)` | 모드 변경 |
| `UpdateStatusLine(status)` | 토큰 사용량, 비용 |

## 에이전트 정의

TOML 파일 (`data/agents/*.toml`)로 정의:

```toml
identity = "opencode.ai"
protocol = "acp"
run_command."*" = "opencode acp"
[actions."*".install]
command = "npm i -g opencode-ai"
```

## 생명주기

```
start() → _run_agent()
    → asyncio.create_subprocess_shell(command)
    → acp_initialize()        # protocol 버전, capabilities 교환
    → acp_new_session()       # 또는 acp_load_session()
    → AgentReady() 발신
    → send_prompt() → acp_session_prompt()
    → 에이전트가 session/update로 스트리밍 chunks 계속 반환
    → prompt 완료 시 stopReason 반환
```

## NexusByTaeng와의 비교

| | Toad (ACP) | NexusByTaeng (현재) |
|---|---|---|
| 프로토콜 | JSON-RPC 표준 (ACP) | 파이프 raw text |
| 방향 | 양방향 | stdout만 읽음 |
| 에이전트 | 20개+ (TOML 플러그인) | hermes만 |
| 응답 구조 | 메시지 유형별 분기 | 단순 텍스트 스트림 |
| 파일/터미널 | 에이전트가 요청 가능 | 없음 |
| 세션 | DB 기반 저장/복원 | 없음 |

## 적용 방향 제안

1. **Phase 4.1**: 현재 파이프 방식 유지, 스트리밍 UX 개선 (hermes 전용)
2. **Phase 4.2**: AgentAdapter 추상화 인터페이스 도입
3. **Phase 4.3**: ACP 호환 래퍼 추가, 다중 에이전트 지원

skipped: ACP 전체 구현, add when: hermes 파이프 스트리밍이 안정화되고 다중 에이전트 필요 시.
