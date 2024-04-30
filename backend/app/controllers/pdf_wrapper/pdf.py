import io
from . import TextStyle, TextEntry, TextFieldEntry, CanvasEditor, TextBlockConfig


class PDF:
    def __init__(self):
        self.stream = io.BytesIO()
        self.__canvas = CanvasEditor(self.stream)
        self.block: TextBlockConfig = []

    def set_metadata(self, *, author: str, title: str, subject: str):
        if author:
            self.__canvas.setAuthor(author)
        if title:
            self.__canvas.setTitle(title)
        if subject:
            self.__canvas.setSubject(subject)

    def save(self):
        self.__canvas.save()

    def next_page(self):
        self.__canvas.next_page()

    def clear_block(self):
        self.block = []

    def print_block(self, *, clear: bool = True, lower_limit: float = 0.0):
        """
        lower_limit: how far down the page is the block still allowed to start printing? for example:
        0.25 means: if the block starts in the last 25% of the page, print on the next page instead.
        """
        progression = self.__canvas.get_page_progression()
        if progression < lower_limit:
            self.next_page()

        height: int = self.__canvas.estimate_block_height(self.block)
        self.__canvas.print_block(self.block, height)
        if clear:
            self.clear_block()

    def add_heading(self, text: str, heading: TextStyle):
        config: TextEntry = {"type": "text", "style": heading, "text": text}
        self.block.append(config)

    def add_paragraph(self, text: str):
        config: TextEntry = {"type": "text", "style": TextStyle.P, "text": text}
        self.block.append(config)

    def add_textfield(self, text: str, key: str, *, max_length: int = 1000):
        config: TextFieldEntry = {
            "type": "textfield",
            "text": text,
            "max_length": max_length,
            "key": key,
        }
        self.block.append(config)
