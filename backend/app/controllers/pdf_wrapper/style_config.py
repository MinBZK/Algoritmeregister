from . import TextStyle, StyleDict
from reportlab.lib.colors import Color

font: str = "Helvetica"
font_styles_config: dict[TextStyle, StyleDict] = {
    TextStyle.H1: {
        "font": (f"{font}-Bold", 22),
        "height": 22,
        "color": Color(0.15, 0.35, 0.56),  # type: ignore
    },
    TextStyle.H2: {
        "font": (f"{font}-Bold", 18),
        "height": 28,
        "color": Color(0.15, 0.35, 0.56),  # type: ignore
    },
    TextStyle.H3: {
        "font": (f"{font}-Bold", 15),
        "height": 23,
        "color": Color(0.15, 0.35, 0.56),  # type: ignore
    },
    TextStyle.H4: {
        "font": (f"{font}-Bold", 12),
        "height": 18,
        "color": Color(0.15, 0.35, 0.56),  # type: ignore
    },
    TextStyle.SUBTITLE: {
        "font": (font, 12),
        "height": 18,
        "color": Color(0.5, 0.5, 0.5),  # type: ignore
    },
    TextStyle.P: {
        "font": (font, 10),
        "height": 16,
        "color": Color(0, 0, 0),
    },
    TextStyle.DEFAULT: {
        "font": (font, 10),
        "height": 13,
        "color": Color(0, 0, 0),
    },
}
