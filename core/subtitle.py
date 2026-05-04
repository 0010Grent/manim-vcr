from manim import *
from core.theme import *


class BilingualSubtitle(VGroup):
    def __init__(self, en_text: str, cn_text: str, **kwargs):
        super().__init__(**kwargs)
        self.en = Text(
            en_text,
            font=EN_FONT,
            font_size=EN_SIZE,
            color=TEXT_WHITE,
        )
        self.cn = Text(
            cn_text,
            font=CN_FONT,
            font_size=CN_SIZE,
            color=TEXT_WHITE,
            opacity=0.6,
        )
        self.add(self.en, self.cn)
        self.arrange(DOWN, buff=0.12)
        self.to_edge(DOWN, buff=SUBTITLE_BUFF)
