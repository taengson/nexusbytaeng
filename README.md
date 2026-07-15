# Project NexusByTaeng Roadmap 🚀

## 1. Vision & Identity
**Project Name**: `nexusbytaeng`  
**Core Goal**: A professional-grade, AI-Network Hybrid Chat TUI that serves as a central hub for multiple AI agents and real-time network communication.  
**Inspiration**: Based on the architectural elegance of `toad` and the flexibility of the `textual` framework.

---

## 2. Key Features

### 🤖 Multi-Agent System
- **Agent Registry**: Support for multiple AI configurations (model, API key, system prompt) defined in `config.json`.
- **Dynamic Switching**: Ability to switch active agents on-the-fly.
- **Default Agent**: Maintain the existing AI chat functionality as the 'Default' agent.

### 🎨 Modernized UI/UX
- **Hierarchical Layout**: 
    - **HomeScreen**: Central hub for selecting connection modes.
    - **Workspace**: Tabbed interface for multiple concurrent sessions.
    - **Session Layout**: Split view with Project Tree (Left) and Chat Area (Right).
- **Visual Polish**: 
    - Professional dark theme using `.tcss` stylesheets.
    - Card-style message bubbles for improved readability.
- **Adaptive Components**: Role-specific widgets for `UserInput`, `AIResponse`, and `SystemNote`.

### ⌨️ Command Palette & Navigation
- **Command Palette**: A central search interface for executing commands.
- **Quick Navigation**: Keyboard shortcuts for switching views (e.g., `h` to return home).

### 🌐 Hybrid Networking
- **Integrated WebSocket**: Seamless integration of network chat within the AI-centric environment.
- **Connectivity Diagnostics**: Built-in `/test` command to verify server reachability.

---

## 3. Technical Architecture

### 📐 Structural Shift
- **Architecture**: `NexusApp` $\rightarrow$ `MainArea` $\rightarrow$ (`HomeScreen` $\leftrightarrow$ `TabbedContent` $\rightarrow$ `SessionWorkspace`).
- **Logic Decoupling**: UI components are strictly separated from business logic.

### 🛠️ Implementation Stack
- **Framework**: `textual`
- **LLM Interface**: `litellm`
- **Styling**: `.tcss` stylesheets.

---

## 4. Development Roadmap

### Phase 1: Infrastructure & Core Logic
- [x] Initialize `nexusbytaeng` repository.
- [ ] Implement `AgentRegistry` to handle multiple AI configurations.
- [ ] Refactor LLM core to support dynamic agent switching.

### Phase 2: UI Foundation (The "Modern Look")
- [x] Implement `HomeScreen` as the landing hub.
- [x] Implement `TabbedContent` based workspace layout.
- [x] Create `.tcss` theme and professional dark mode.
- [x] Build role-specific message widgets and `SessionWorkspace` (Tree + Chat).

### Phase 3: Navigation & Interaction
- [ ] Implement `Command Palette` for efficient feature access.
- [ ] Integrate the `/test` connectivity tool and detailed logging.
- [ ] Refine transition between Home and Workspaces.

### Phase 4: Polish & Stability
- [ ] Refine animations and transitions.
- [ ] Stress test multi-agent context switching.
- [ ] Finalize documentation and configuration examples.

---

## 5. License & Guidelines
- **Design Philosophy**: Reference-based implementation of UX/UI patterns to ensure license safety.
- **Code Quality**: Maintain strict separation between UI and business logic.
