# Project NexusByTaeng Roadmap 🚀

## 1. Vision & Identity
**Project Name**: `nexusbytaeng`  
**Core Goal**: A professional-grade, AI-Network Hybrid Chat TUI that serves as a central hub for multiple AI agents and real-time network communication.  
**Inspiration**: Based on the architectural elegance of `toad` and the flexibility of the `textual` framework.

---

## 2. Key Features

### 🤖 Multi-Agent System
- **Agent Registry**: Support for multiple AI configurations (model, API key, system prompt) defined in `config.json`.
- **Dynamic Switching**: Ability to switch active agents on-the-fly via a sidebar or command palette.
- **Default Agent**: Maintain the existing AI chat functionality as the 'Default' agent for backward compatibility.

### 🎨 Modernized UI/UX (Toad-inspired)
- **Hierarchical Layout**: 
    - **Main Area**: High-readability conversation view with card-style message bubbles.
    - **SideBar**: Slide-out panel for agent selection, project directory, and status.
    - **Footer**: Concise key-bindings and status indicators.
- **Visual Polish**: 
    - Implementation of a professional dark theme using Textual's standard variables (`$primary`, `$surface`, etc.).
    - Use of `.tcss` files for a clean separation of logic and styling.
- **Adaptive Components**: Different widget types for different message roles (`UserInput`, `AIResponse`, `SystemNote`, `ShellResult`).

### ⌨️ Command Palette & Navigation
- **Command Palette**: A central search interface (Ctrl+K/P) to discover and execute commands (e.g., `/test`, `/clear`, `/agent-switch`).
- **Block Navigation**: Ability to navigate through conversation blocks using keyboard shortcuts (Alt+Up/Down).

### 🌐 Hybrid Networking
- **Integrated WebSocket**: Seamless integration of network chat within the AI-centric environment.
- **Connectivity Diagnostics**: Built-in `/test` command to verify server reachability via `curl` with detailed logging.

---

## 3. Technical Architecture

### 📐 Structural Shift
- **Old**: `MainChatApp` (All-in-one) $\rightarrow$ **New**: `NexusApp` $\rightarrow$ `MainScreen` $\rightarrow$ `Conversation` $\rightarrow$ `MessageWidgets`.
- **Logic Decoupling**: Moving LLM calling logic to a provider-based system that accepts an `Agent` configuration.

### 🛠️ Implementation Stack
- **Framework**: `textual` (Latest)
- **LLM Interface**: `litellm` (for multi-provider support)
- **Styling**: CSS-like `.tcss` stylesheets.
- **Configuration**: JSON-based agent and system settings.

---

## 4. Development Roadmap

### Phase 1: Infrastructure & Core Logic
- [ ] Initialize `nexusbytaeng` repository.
- [ ] Implement `AgentRegistry` to handle multiple AI configurations.
- [ ] Refactor LLM core to support dynamic agent switching.

### Phase 2: UI Foundation (The "Modern Look")
- [ ] Implement the `MainScreen` and `Conversation` layout.
- [ ] Create `.tcss` theme and implement standard dark mode colors.
- [ ] Build role-specific message widgets (`UserInput`, `AIResponse`, etc.).

### Phase 3: Navigation & Interaction
- [ ] Implement the animated `SideBar` for agent and network management.
- [ ] Build the `Command Palette` for efficient feature access.
- [ ] Integrate the `/test` connectivity tool and detailed logging.

### Phase 4: Polish & Stability
- [ ] Refine animations and transitions.
- [ ] Stress test multi-agent context switching.
- [ ] Finalize documentation and configuration examples.

---

## 5. License & Guidelines
- **Design Philosophy**: Focus on "Idea-based" implementation. Reference the UX/UI patterns of `toad` without direct code duplication to ensure license safety (avoiding AGPL-3.0 contamination).
- **Code Quality**: Maintain a strict separation between UI and business logic.
