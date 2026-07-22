import re
from typing import List

class StreamParser:
    """
    Parses raw terminal output streams.
    Merges chunks into logical messages based on newlines.
    """
    def __init__(self):
        self.buffer = ""

    def process_chunk(self, chunk: str) -> List[str]:
        """
        Processes a chunk of text and returns a list of messages.
        """
        self.buffer += chunk
        
        messages = []
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            for line in lines[:-1]:
                stripped = line.strip()
                if stripped:
                    messages.append(stripped)
            self.buffer = lines[-1]
        
        return messages

