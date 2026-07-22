# 📄 [Plan] ACP 기반 에이전트 통합 및 자율 제어 프레임워크 구축

## 1. 개요 (Overview)
현재의 Raw Text 파이프 기반 통신은 단순 텍스트 스트리밍에 최적화되어 있어, 에이전트의 복잡한 상태(생각, 도구 호출, 터미널 제어)를 UI에 효율적으로 렌더링하는 데 한계가 있음. 이를 **표준 JSON-RPC 기반의 ACP(Agent Client Protocol)**로 전환하여, 에이전트가 UI의 기능을 능동적으로 제어할 수 있는 **'자율 에이전트 인프라'**를 구축함.

## 2. 핵심 변경 사항 (Core Changes)

### A. 통신 프로토콜의 현대화 (Transport Layer)
- **Raw Text $\rightarrow$ JSON-RPC**: 단순 문자열 전송에서 구조화된 메시지 교환 방식으로 변경.
- **양방향 제어**: UI가 응답을 읽기만 하는 구조에서, 에이전트가 `terminal/create`, `fs/write` 등의 요청을 UI에 보내는 양방향 구조로 전환.

### B. 에이전트 추상화 계층 도입 (Agent Adapter)
- **`AgentAdapter` 인터페이스**: 다양한 프로토콜(ACP, Legacy Raw Text 등)을 수용할 수 있는 추상화 계층 도입.
- **ACP Adapter 구현**: `initialize` $\rightarrow$ `session_new` $\rightarrow$ `session_prompt`로 이어지는 ACP 생명주기 관리.

### C. UI 렌더링 엔진 고도화 (UI Mapping)
- **메시지 타입별 렌더링**:
    - `Update(text)` $\rightarrow$ 채팅 버블 (Streaming)
    - `Thinking(text)` $\rightarrow$ 접이식 생각 섹션 (Accordion/Thought block)
    - `ToolCall` $\rightarrow$ 도구 호출 상태 표시 및 결과 렌더링
- **동적 위젯 생성**: 에이전트의 `CreateTerminal` 요청 시, UI 상에 새로운 터미널 위젯을 동적으로 생성하고 연결.

## 3. 단계적 구현 로드맵 (Implementation Roadmap)

### Phase 1: ACP 기초 인프라 구축 (The Foundation)
- [ ] JSON-RPC 메시지 파서 및 시리얼라이저 구현.
- [ ] `AgentProcessManager`를 ACP 표준에 맞게 리팩토링 (명령어: `opencode acp`).
- [ ] 기초 세션 핸드셰이크(`initialize` $\rightarrow$ `session_new`) 검증.

### Phase 2: 구조화된 스트리밍 및 UI 매핑 (Structured Streaming)
- [ ] `session/update` 메시지 타입별 분기 처리.
- [ ] UI 위젯에서 '생각'과 '결과'를 구분하여 표시하는 스트리밍 UX 적용.
- [ ] (기존 버퍼링 문제 해결) JSON-RPC 프레임 단위의 즉각적인 플러싱 확인.

### Phase 3: 에이전트 자율 제어 기능 구현 (Autonomous Control)
- [ ] **Terminal Control**: 에이전트의 터미널 생성/출력/종료 요청 처리 루틴 구현.
- [ ] **File System Access**: 에이전트가 요청하는 파일 읽기/쓰기 권한 승인 및 실행 로직 구축.
- [ ] 에이전트 $\rightarrow$ UI $\rightarrow$ 시스템 $\rightarrow$ 에이전트로 이어지는 완전한 피드백 루프 검증.

## 4. 기대 효과 (Expected Impact)
- **확장성**: ACP 표준을 따르는 어떤 에이전트(opencode-ai 등)든 TOML 설정만으로 즉시 추가 가능.
- **UX 혁신**: 단순 채팅창을 넘어, AI가 실제로 터미널을 조작하고 파일을 수정하는 과정이 실시간으로 시각화됨.
- **안정성**: 구조화된 프로토콜을 통해 예외 처리 및 세션 복구가 명확해짐.

---

**리뷰어/기획자 확인 요청 사항:**
- 위 단계 중 **Phase 3의 터미널 제어 범위**(단순 출력 vs 완전한 인터랙티브 쉘)에 대한 구체적인 요구사항 정의 필요.
- ACP 도입 시 기존 Raw Text 기반 에이전트들의 하위 호환성 유지 여부 결정.
