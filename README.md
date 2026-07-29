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
# Run the application
python3 -m src.main
```

---

## 1. Vision & Identity
**Project Name**: `nexusbytaeng`  
**Core Goal**: A professional-grade, AI-Network Hybrid Chat TUI that serves as a central hub for multiple AI agents and real-time network communication.  
**Inspiration**: Based on the architectural elegance of `toad` and the flexibility of the `textual` framework.

---

## 2. Key Features

### 🤖 ACP (Agent Client Protocol) Support
- **Multi-Agent Integration**: Support for multiple ACP-compatible agents (Hermes, Gemini).
- **Real-time Streaming**: Streaming AI responses with Thought/Response visual separation.
- **Session Management**: ACP-based session creation, prompt transmission, and notification handling.
- **Shell Integration**: Shell command execution (`!` prefix) with input visibility and logging.

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
- **Supported Agents**: Hermes ACP, Gemini ACP

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

### Phase 3: ACP Integration & UI/UX Polishing
- [x] ACP (Agent Client Protocol) integration via JSON-RPC 2.0.
- [x] Hermes ACP support (handshake, session, streaming).
- [x] Gemini ACP support (Phase 3.8).
- [x] UI/UX polishing (message stack, Think/Response separation, ACP status bar).
- [x] Logging integrity (token-based timer, buffer flush, session mode logging).
- [x] Shell input leak prevention and command visibility.

### Phase 4: LLM Client & Network (WebSocket) Integration
- [ ] Multi-provider LLM support via `AgentRegistry` and `litellm`.
- [ ] Async WebSocket broker server and network panel.

### Phase 5: Polish & Stability
- [ ] Refine animations and transitions.
- [ ] Stress test multi-agent context switching.
- [ ] Finalize documentation and configuration examples.

---

## 5. License & Guidelines
- **Design Philosophy**: Reference-based implementation of UX/UI patterns to ensure license safety.
- **Code Quality**: Maintain strict separation between UI and business logic.
