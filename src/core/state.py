# ponytail: Simple connection mode state definition

class ConnectionMode:
    LOCAL = "local"
    NETWORK = "network"
    GEMINI_ACP = "gemini_acp"
    OPENCODE = "opencode"
    HERMES_ACP = "hermes_acp"

    @classmethod
    def get_display_name(cls, mode: str) -> str:
        names = {
            cls.LOCAL: "로컬 AI 연결",
            cls.NETWORK: "네트워크 연결",
            cls.GEMINI_ACP: "Gemini ACP 연결",
            cls.OPENCODE: "OpenCode 연결",
            cls.HERMES_ACP: "Hermes ACP 연결",
        }
        return names.get(mode, "알 수 없음")

    @classmethod
    def get_theme_color(cls, mode: str) -> str:
        # returns (color name, border color, indicator symbol)
        colors = {
            cls.LOCAL: ("$primary", "blue", "🤖"),
            cls.NETWORK: ("$success", "green", "🌐"),
            cls.GEMINI_ACP: ("$accent", "purple", "✨"),
            cls.OPENCODE: ("$warning", "orange", "💻"),
            cls.HERMES_ACP: ("$secondary", "yellow", "⚡"),
        }
        return colors.get(mode, ("$text", "gray", "❓"))
