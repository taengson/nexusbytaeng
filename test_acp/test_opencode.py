#!/usr/bin/env python3
"""TUI 없이 opencode ACP 통신 직접 테스트 — mcpServers & 중첩 구조 검증"""

import asyncio
import json
import sys

async def main():
    print("🔄 opencode acp 시작 중...")
    proc = await asyncio.create_subprocess_exec(
        "opencode", "acp",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # initialize
    init_req = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": 1,
            "clientInfo": {"name": "acp-test", "version": "1.0"},
        },
        "id": 1,
    }
    proc.stdin.write(json.dumps(init_req).encode() + b"\n")
    await proc.stdin.drain()

    init_resp = json.loads(await asyncio.wait_for(proc.stdout.readline(), timeout=5))
    if "error" in init_resp:
        print(f"❌ initialize 실패: {init_resp['error']}")
        proc.terminate(); await proc.wait()
        return

    print("✅ initialize 성공")

    # session/new — mcpServers 필수 (opencode도 동일 요구)
    session_req = {
        "jsonrpc": "2.0",
        "method": "session/new",
        "params": {"cwd": ".", "mcpServers": []},
        "id": 2,
    }
    proc.stdin.write(json.dumps(session_req).encode() + b"\n")
    await proc.stdin.drain()

    session_resp = json.loads(await asyncio.wait_for(proc.stdout.readline(), timeout=5))
    if "error" in session_resp:
        print(f"❌ session/new 실패: {session_resp['error']}")
        proc.terminate(); await proc.wait()
        return

    session_id = session_resp["result"].get("sessionId") or session_resp["result"].get("session_id")
    if not session_id:
        print(f"❌ session_id 없음: {session_resp.get('result')}")
        proc.terminate(); await proc.wait()
        return

    print(f"✅ session/new 성공 (session: {session_id[:8]}...)")

    # 프롬프트 입력
    prompt_text = input("\n💬 프롬프트 입력: ")

    prompt_req = {
        "jsonrpc": "2.0",
        "method": "session/prompt",
        "params": {
            "sessionId": session_id,
            "prompt": [{"type": "text", "text": prompt_text}],
        },
        "id": 3,
    }
    proc.stdin.write(json.dumps(prompt_req).encode() + b"\n")
    await proc.stdin.drain()

    # 스트리밍 출력 — params["update"] 중첩 구조 적용
    print("\n🤖 AI 응답:")
    while True:
        try:
            line = await asyncio.wait_for(proc.stdout.readline(), timeout=30)
            data = json.loads(line.decode().strip())

            if "id" in data:
                if data["id"] == 3:
                    stop = data.get("result", {}).get("stopReason")
                    if stop:
                        print("\n✅ 프롬프트 완료")
                        break
                continue

            # notification — session/update 중첩 구조
            params = data.get("params", {})
            update = params.get("update", {})
            update_type = update.get("sessionUpdate")
            content = update.get("content", {})

            if update_type == "agent_message_chunk":
                text = content.get("text", "")
                print(text, end="", flush=True)
            elif update_type == "agent_thought_chunk":
                thought = content.get("text", "")
                if thought:
                    print(f"\n💭 {thought}", end="", flush=True)
            elif update_type == "tool_call":
                name = update.get("name", "unknown")
                print(f"\n🛠 Tool: {name}", end="", flush=True)
            elif update_type == "tool_call_update":
                result = update.get("result", "")[:200]
                print(f"\n🛠 Result: {result}", end="", flush=True)

        except asyncio.TimeoutError:
            print("\n⏰ 타임아웃")
            break

    proc.terminate()
    await proc.wait()
    print("\n🔚 연결 종료")

if __name__ == "__main__":
    asyncio.run(main())
