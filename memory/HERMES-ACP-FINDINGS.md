# Hermes ACP 분석 결과 (for Code Developer)

## 분석 범위
`~/.hermes/hermes-agent/acp_adapter/` — server.py, session.py, entry.py, events.py

---

## 1. Message Specification (완료)

hermes acp가 송신하는 세션 업데이트 메시지:

| 이벤트 | callback | 메시지 |
|--------|---------|--------|
| 응답 텍스트 | `make_message_cb` | `acp.update_agent_message_text(text)` |
| 생각 | `make_thinking_cb` | `acp.update_agent_thought_text(text)` |
| 도구 시작 | `make_tool_progress_cb` | `build_tool_start(tc_id, name, args)` |
| 도구 완료 | `make_step_cb` | `build_tool_complete(tc_id, name, result, args)` |
| Todo/Plan | `make_step_cb` | `AgentPlanUpdate(entries=[])` |

**UI 매핑**: 메시지→채팅버블, 생각→접이식블록, 도구→상태표시, Plan→Todo패널

## 2. Handshake Sequence (완료)

```python
InitializeResponse(
    protocol_version="0.3.0",
    agent_capabilities=AgentCapabilities(
        prompt_capabilities=PromptCapabilities(structured=False, unstructured_commands=True),
        thinking=True,
    ),
)
```

클라이언트 필수 capabilities 없음. structured=False이므로 구조화 프롬프트 미지원.

## 3. Terminal Control Flow (❌ 방향 다름)

**중요**: hermes acp는 에이전트 서버이므로 Toad 패턴("에이전트→UI 요청→UI 실행")과 반대.
hermes가 `terminal_tool`로 내부에서 직접 실행.

**체크포인트**:
- [ ] hermes terminal_tool 출력을 UI에 실시간 노출할 전략 정의 필요
- [ ] Phase 3 "에이전트→UI→터미널→에이전트" 패턴은 hermes acp에 적용 불가

## 4. Error Handling (체크포인트)

JSON-RPC 표준 에러코드 사용 (`-32700` ~ `-32000`).

**체크포인트**:
- [ ] JSON-RPC 에러를 UI에 표시할 방식 정의 필요 (토스트? 에러 카드?)
- [ ] `-32601`(unknown method)은 `_BenignProbeMethodFilter`로 필터링됨 — 에러로 보지 말 것

---

## 핵심 발견

hermes acp는 **에이전트 서버**이므로 Phase 3의 "에이전트가 UI에 요청" 패턴 적용 불가. herms가 내부에서 처리하므로 UI에 노출하는 방식만 고려. PLAN.md에서 이 방향 명시 필요.
