# Project NexusByTaeng Roadmap 🚀

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- A virtual environment (recommended)

### Installation
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required dependencies
pip install textual litellm
```

### Execution
```bash
# Run the application (always use the venv Python in package mode)
./venv/bin/python -m src.main
```

---

## 1. Vision & Identity
**Project Name**: `nexusbytaeng`  
**Core Goal**: A professional-grade, AI-Network Hybrid Chat TUI that serves as a central hub for multiple AI agents and real-time network communication.  
**Inspiration**: Based on the architectural elegance of `toad` and the flexibility of the `textual` framework.

---

## 2. Key Features

### 🤖 ACP (Agent Client Protocol) Support
- **Multi-Agent Integration**: Support for multiple ACP-compatible agents (Hermes, Gemini, OpenCode).
- **Real-time Streaming**: Streaming AI responses with Thought/Response visual separation.
- **Session Management**: ACP-based session creation, prompt transmission, and notification handling.
- **Shell Integration**: Safe shell command execution (`!` prefix) using `shlex.split` + `shell=False`, with input visibility and logging.

### 🎨 Modernized UI/UX
- **Hierarchical Layout**: 
    - **HomeScreen**: Central hub for selecting connection modes.
    - **Workspace**: Tabbed interface for multiple concurrent sessions.
    - **Session Layout**: Split view with Project Tree (Left) and Chat Area (Right).
- **Visual Polish**: 
    - Professional dark theme using `.tcss` stylesheets.
    - Card-style message bubbles for improved readability.
- **Adaptive Components**: Role-specific widgets for `UserInput`, `AIResponse`, and `SystemNote`.

### ⌨️ Toad-style Input System
- **Shell Execution**: `!` prefix for shell command execution.
- **Slash Commands**: `/` prefix for slash commands.
- **Path/File Suggestions**: `@` prefix for path/file suggestions.
- **Quick Navigation**: Keyboard shortcuts for switching views (e.g., `h` to return home).

### 📝 Logging & Diagnostics
- **Chat Logging**: Daily Markdown log files with session mode, ACP session ID, and shell commands.
- **Buffer Flush**: Automatic response buffer flush on session close.

---

## 3. Technical Architecture

### 📐 Structural Shift
- **Architecture**: `NexusApp` $\rightarrow$ `MainArea` $\rightarrow$ (`HomeScreen` $\leftrightarrow$ `TabbedContent` $\rightarrow$ `SessionWorkspace`).
- **Logic Decoupling**: UI components are strictly separated from business logic.

### 🛠️ Implementation Stack
- **Framework**: `textual`
- **Protocol**: ACP (Agent Client Protocol) via JSON-RPC 2.0
- **Styling**: `.tcss` stylesheets.
- **Supported Agents**: Hermes ACP, Gemini ACP, OpenCode ACP

---

## 4. Development Roadmap

### Phase 1: Infrastructure & Core Logic
- [x] Initialize `nexusbytaeng` repository.
- [x] Implement `HomeScreen` as the landing hub.
- [x] Implement `TabbedContent` based workspace layout.

### Phase 2: UI Foundation (The "Modern Look")
- [x] Create `.tcss` theme and professional dark mode.
- [x] Build role-specific message widgets and `SessionWorkspace` (Tree + Chat).
- [x] Toad-style input system (`!`, `/`, `@` prefix parsing).

### Phase 3: ACP Integration, UI/UX Polishing & Security/Stability Hardening
- [x] ACP (Agent Client Protocol) integration via JSON-RPC 2.0.
- [x] Hermes ACP support (handshake, session, streaming).
- [x] Gemini ACP support (Phase 3.8).
- [x] OpenCode ACP support (Phase 3.9).
- [x] UI/UX polishing (message stack, Think/Response separation, ACP status bar).
- [x] Logging integrity (token-based timer, buffer flush, session mode logging, buffered I/O).
- [x] Shell input leak prevention, command visibility, and command-injection-safe execution.
- [x] Live path/file suggestions (`@` prefix) via `InputDispatcher` + `SuggestionPanel`.
- [x] Codebase audit remediation (thread-safe `call_next`, ACP process stop timeout, response deduplication, TypedDict fixes, dynamic project tree, data-driven home screen buttons).

### Phase 4: ACP Enhancement & Agent Stability
- [x] ACP protocol 강화: 재연결, 세션 지속성, 스트리밍 최적화
- [x] 3 에이전트 (Hermes, Gemini, OpenCode) 안정성 확보
- [x] 에러 처리 및 복구 로직 고도화

### Phase 5: A2A Client Integration
- [ ] A2A (Agent2Agent Protocol) 클라이언트 구현.
- [ ] 외부 A2A 에이전트 발견 (AgentCard discovery via `/.well-known/agent.json`).
- [ ] Task lifecycle 기반 메시지 흐름 (`submitted → working → completed`).
- [ ] `nexusbytaeng`를 A2A 클라이언트로 활용하여 외부 에이전트와 협업.

### Phase 6: ANP / DID Federation
- [ ] ANP (Agent Network Protocol) 기반 연합 실험.
- [ ] W3C DID 기반 에이전트 정체성 탐구.
- [ ] 메타-프로토콜 협상 개념 검토 및 적용 방안 수립.

### Phase 7: Polish & Stability
- [ ] Refine animations and transitions.
- [ ] Stress test multi-agent context switching.
- [ ] Finalize documentation and configuration examples.

---

## 5. License & Guidelines
- **Design Philosophy**: Reference-based implementation of UX/UI patterns to ensure license safety.
- **Code Quality**: Maintain strict separation between UI and business logic.
