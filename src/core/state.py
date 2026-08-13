# ponytail: Simple connection mode state definition

class ConnectionMode:
    NETWORK = "network"
    GEMINI_ACP = "gemini_acp"
    HERMES_ACP = "hermes_acp"
    OPENCODE_ACP = "opencode_acp"

    @classmethod
    def get_display_name(cls, mode: str) -> str:
        names = {
            cls.NETWORK: "네트워크 연결",
            cls.GEMINI_ACP: "Gemini 연결",
            cls.HERMES_ACP: "Hermes 연결",
            cls.OPENCODE_ACP: "OpenCode 연결",
        }
        return names.get(mode, "알 수 없음")

    @classmethod
    def get_theme_color(cls, mode: str) -> str:
        # returns (color name, border color, indicator symbol)
        colors = {
            cls.NETWORK: ("$success", "green", "🌐"),
            cls.GEMINI_ACP: ("$accent", "purple", "✨"),
            cls.HERMES_ACP: ("$secondary", "yellow", "⚡"),
            cls.OPENCODE_ACP: ("$warning", "orange", "💻"),
        }
        return colors.get(mode, ("$text", "gray", "❓"))
