import re
from typing import List

class StreamParser:
    """
    Parses raw terminal output streams.
    Filters ANSI escape sequences and merges chunks into logical messages.
    """
    def __init__(self):
        # Regex to match ANSI escape sequences: ESC [ ... m, etc.
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\_-]?'\
                                     r'(?:[0-?]*[0-9a-zA-Z]|\s*))')
        self.buffer = ""

    def clean_text(self, text: str) -> str:
        """Removes ANSI escape sequences from the text."""
        return self.ansi_escape.sub('', text)

    def process_chunk(self, chunk: str) -> List[str]:
        """
        Processes a chunk of text and returns a list of complete messages.
        A message is considered complete if it ends with a newline or is 
        sufficiently long to be a meaningful partial response.
        """
        cleaned = self.clean_text(chunk)
        self.buffer += cleaned
        
        messages = []
        # Split by newline to get complete lines
        lines = self.buffer.split('\n')
        
        # All but the last element are complete lines
        for line in lines[:-1]:
            stripped = line.strip()
            if stripped:
                messages.append(stripped)
        
        # Keep the remaining part in the buffer
        self.buffer = lines[-1]
        
        return messages
