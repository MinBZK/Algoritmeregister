from typing import Tuple
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfgen.textobject import PDFTextObject
from . import font_styles_config
from . import TextStyle, StyleDict, TextFieldEntry, TextEntry, TextBlockConfig


def prepare_text_for_textfield(value: str | None) -> str:
    if not value:
        return ""
    value = value.replace("’", "'")
    value = value.replace("‘", "'")
    value = value.replace("≥", ">")
    value = value.replace("“", '"')
    value = value.replace("”", '"')
    value = value.replace("–", "-")
    value = value.replace("‑", "-")
    value = value.replace("•", "")
    return value


class CanvasEditor(canvas.Canvas):
    y_start = 780
    x_start = 50
    y_end = 50

    def __init__(self, stream):
        super().__init__(stream, pagesize=A4)

        self._x: int = self.x_start
        self._y: int = self.y_start
        self.styles: dict[TextStyle, StyleDict] = font_styles_config

    def next_page(self):
        self.showPage()
        self._x = self.x_start
        self._y = self.y_start

    def print_textfield(self, textfield: TextFieldEntry, height: int) -> None:
        self.acroForm.textfield(
            name=f"name__{textfield['key']}",
            tooltip=f"tooltip__{textfield['key']}",
            value=prepare_text_for_textfield(textfield["text"]),
            maxlen=textfield["max_length"],
            x=self._x,
            y=self._y,
            fieldFlags="multiline",
            width=500,
            height=height,
            borderWidth=0,
        )

    def print_block(self, block: TextBlockConfig, height: int) -> None:
        if height > self.y_start - self.y_end:
            raise ValueError("Block exceeds page size")

        if self._y - height < self.y_end:
            self.next_page()

        for element in block:
            if element["type"] == "text":
                self._y, text_object = self.build_text_object(element, self._y)

                style: StyleDict = self.styles[element["style"]]
                self.setFont(*style["font"])
                self.setFillColor(style["color"])
                self.drawText(text_object)
            elif element["type"] == "textfield":
                height = self.get_textfield_height(element)
                self._y -= height + 10
                self.print_textfield(element, height)

    def get_textfield_height(self, textfield_element: TextFieldEntry) -> int:
        return round(max(textfield_element["max_length"], 500) / 500) * 20

    def estimate_block_height(self, block: TextBlockConfig) -> int:
        y_loop = 0
        for element in block:
            if element["type"] == "text":
                y_loop, _ = self.build_text_object(element, y_loop)
            elif element["type"] == "textfield":
                height = self.get_textfield_height(element)
                y_loop -= height
        return -y_loop

    def build_text_object(
        self, text_element: TextEntry, y: int
    ) -> Tuple[int, PDFTextObject]:
        style: StyleDict = self.styles[text_element["style"]]
        y_out = y - style["height"]

        text_object: PDFTextObject = self.beginText(self.x_start, y_out)
        text_object.textLines(text_element["text"])

        return y_out, text_object

    def get_page_progression(self) -> float:
        """
        Return the fractional progression along the page. 1 means at the top, 0 means at the bottom
        """
        return (self._y - self.y_end) / (self.y_start - self.y_end)
