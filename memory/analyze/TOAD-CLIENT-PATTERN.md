# Toad ACP 클라이언트 패턴 분석

## 분석 대상
`examples/toad/src/toad/acp/` — Toad의 ACP 클라이언트 구현

---

## session/update Notification 구조

`session_update`는 JSON-RPC notification (id 필드 없음). `update` 객체 내 `sessionUpdate` 필드로 타입 분기:

```python
# sessionUpdate별 파싱 패턴
match update:
    case {"sessionUpdate": "agent_message_chunk", "content": {"type": type, "text": text}}:
        # AI 응답 텍스트
    case {"sessionUpdate": "agent_thought_chunk", "content": {"type": type, "text": text}}:
        # 생각/추론 과정
    case {"sessionUpdate": "tool_call", "toolCallId": tool_call_id}:
        # 도구 호출 시작
    case {"sessionUpdate": "tool_call_update", "toolCallId": tool_call_id}:
        # 도구 호출 상태 업데이트
    case {"sessionUpdate": "plan", "entries": entries}:
        # Plan 업데이트
    case {"sessionUpdate": "usage_update", "used": used, "size": size}:
        # 토큰 사용량
```

---

## 프롬프트 전송 형식

```json
{
  "jsonrpc": "2.0",
  "method": "session/prompt",
  "params": {
    "session_id": "uuid-here",
    "prompt": [{"type": "text", "text": "사용자 메시지"}]
  },
  "id": 1
}
```

- `prompt` 파라미터: `ContentBlock[]` 배열
- 단순 텍스트: `[{"type": "text", "text": "메시지"}]`
- 응답: `SessionPromptResponse` → `stopReason` 필드로 완료 확인

---

## Toad vs Hermes 차이

| 구분 | Toad (클라이언트) | Hermes (서버) |
|------|-------------------|---------------|
| 역할 | `session/update` 수신 | `session/update` 발송 |
| 분기 기준 | `update.sessionUpdate` 필드 | `acp.update_*` 헬퍼 함수 |
| JSON-RPC | `jsonrpc.Server` + `@expose` | `acp.run_agent()` |

핵심: **서버에서 보내는 notification은 동일한 스펙을 따름**. `sessionUpdate` 필드로 타입 확인하는 로직은 보편적.

---

## 개발 참고 사항

1. **`sessionUpdate` 필드가 핵심** — 모든 notification의 타입 분기 기준
2. **tool_call vs tool_call_update** — tool_call이 먼저 오지 않을 수 있음 (Toad 코드 참고)
3. **에이전트별 파라미터명 차이** — `session_id` vs `sessionId` (camelCase vs snake_case) 확인 필요
4. **ContentBlock.type** — `"text"`, `"image"`, `"resource"` 등. 텍스트 전용이면 `"text"`만 처리
