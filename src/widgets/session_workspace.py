# ponytail: Independent SessionWorkspace widget for TabbedContent

import asyncio
from textual.widgets import Input, Static
from textual.containers import Container, VerticalScroll
from textual.message import Message
from src.widgets.project_tree import ProjectTreePanel
from src.widgets.chat_elements import MessageWidget
from src.widgets.input_area import InputArea, InputResult
from src.core.state import ConnectionMode

class SessionWorkspace(Container):
    """The workspace session widget, intended for mounting in tabs."""
    
    def __init__(self, initial_mode: str = ConnectionMode.LOCAL, **kwargs):
        super().__init__(**kwargs)
        self.current_mode = initial_mode

    def compose(self):
        # Right side: Chat workspace & Settings Input
        with Container(id="chat-panel"):
            yield VerticalScroll(id="message-list")
            yield InputArea(initial_mode=self.current_mode)

    def on_mount(self):
        # Emit session initial status logs
        display_name = ConnectionMode.get_display_name(self.current_mode)
        _, _, symbol = ConnectionMode.get_theme_color(self.current_mode)
        
        self.add_system_message(f"--- {symbol} {display_name} 워크스페이스 세션이 시작되었습니다 ---")
        self.add_system_message(
            "왼쪽의 파일 트리를 통해 실제 폴더 구조를 탐색할 수 있습니다. "
        )

    def on_input_result(self, message: InputResult):
        """Handles results from shell, commands, and suggestions routed via InputArea."""
        if message.is_system:
            self.add_system_message(message.text, is_shell=message.is_shell)
        else:
            self.add_message("ai", message.text)

    def on_input_area_mode_changed(self, message: InputArea.ModeChanged):
        """Reacts to connection switches from the InputArea settings."""
        self.current_mode = message.mode
        display_name = ConnectionMode.get_display_name(self.current_mode)
        _, _, symbol = ConnectionMode.get_theme_color(self.current_mode)
        
        # Log system event
        self.add_system_message(f"🔔 연결 인스턴스가 {symbol} {display_name}(으)로 조절되었습니다.")


    def on_input_submitted(self, event: Input.Submitted):
        """Triggers upon pressing Enter inside the message input."""
        # This is now handled by InputArea.on_input_submitted internally, 
        # but we keep this for user message bubbles.
        input_field = event.input
        text = input_field.value.strip()
        
        if not text:
            return
            
        # Only append User chat bubble if it's not a system command
        if not text.startswith("!"):
            self.add_message("user", text)

        
        # Note: InputArea will handle the logic and post an InputResult message
        # if it's a command or shell execution.

    async def generate_mock_response(self, user_text: str):
        """Asynchronously triggers simulated response cards."""
        await asyncio.sleep(0.3)
        
        mock_responses = {
            ConnectionMode.LOCAL: f"🤖 [로컬 AI 응답]\n입력하신 쿼리 '{user_text}' 분석 완료.",
            ConnectionMode.NETWORK: f"🌐 [네트워크 응답]\n에코 패킷 수신 성공: '{user_text}'",
            ConnectionMode.GEMINI: f"✨ [GEMINI-CLI 응답]\n구문 해석 성공.",
            ConnectionMode.OPENCODE: f"💻 [OpenCode 응답]\n프로젝트 컨텍스트 주입 완료."
        }
        
        response_text = mock_responses.get(self.current_mode, "시뮬레이션 데이터 수신 오류.")
        self.add_message("ai", response_text)

    def add_message(self, sender: str, text: str, is_shell: bool = False):
        """Mounts a message card and scrolls the viewport."""
        message_list = self.query_one("#message-list", VerticalScroll)
        message_list.mount(MessageWidget(sender, text, is_shell=is_shell))
        message_list.scroll_end(animate=False)

    def add_system_message(self, text: str, is_shell: bool = False):
        self.add_message("system", text, is_shell=is_shell)
