import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from manim import *
import numpy as np
from core.theme import *
from core.timing import TimingData
from core import CHARACTER_DIR


class BiSub(VGroup):
    def __init__(self, en: str, cn: str, **kw):
        super().__init__(**kw)
        self.en = Text(en, font=EN_FONT, font_size=EN_SIZE, color=WHITE)
        self.cn = Text(cn, font=CN_FONT, font_size=CN_SIZE, color=WHITE, opacity=0.6)
        self.add(self.en, self.cn)
        self.arrange(DOWN, buff=0.12)
        self.to_edge(DOWN, buff=SUBTITLE_BUFF)


class VCR(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK
        self.T = TimingData()
        self.ct = 0.0

        self.scene_01_opening()
        self.scene_02_intro()
        self.scene_03_montage()
        self.scene_04_turning()
        self.scene_05_sunset()
        self.scene_06_understand()
        self.scene_07_closing()

    def wait_until(self, t: float):
        dt = t - self.ct
        if dt > 0.01:
            self.wait(dt)
            self.ct = t

    def pt(self, *anims, run_time: float = 1.0, **kw):
        self.play(*anims, run_time=run_time, **kw)
        self.ct += run_time

    def do_blink(self, char):
        ey = char.get_center()[1] + char.get_height() * 0.15
        cover = Rectangle(
            width=char.get_width() * 0.4,
            height=char.get_height() * 0.035,
            fill_color="#FCDEC0", fill_opacity=1, stroke_width=0,
        ).move_to([char.get_center()[0], ey, 0])
        self.add(cover)
        self.wait(0.1)
        self.remove(cover)
        self.ct += 0.1

    def scene_01_opening(self):
        T = self.T
        tagline = Text(
            "She teaches AI to think.",
            font=EN_FONT, font_size=44, color=TECH_BLUE,
        ).set_opacity(0)

        dots = VGroup(*[
            Dot(point=np.array([
                np.random.uniform(-6, 6),
                np.random.uniform(-3, 3), 0
            ]), radius=0.03, color=TECH_BLUE, fill_opacity=0.6)
            for _ in range(40)
        ])

        self.pt(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03),
            run_time=0.3,
        )
        self.wait_until(T.start("s01"))
        self.pt(
            *[d.animate.move_to(tagline.get_center() +
              np.array([np.random.uniform(-2, 2), np.random.uniform(-0.3, 0.3), 0]))
              for d in dots],
            tagline.animate.set_opacity(1),
            run_time=1.0,
        )
        self.pt(FadeOut(dots), run_time=0.3)
        self.wait_until(T.end("s01"))
        self.pt(FadeOut(tagline), run_time=0.3)

    def scene_02_intro(self):
        T = self.T
        char = SVGMobject(str(CHARACTER_DIR / "fu_yao_front.svg")).set_height(4.5)
        char.shift(LEFT * 1.5)

        info_lines = VGroup(
            Text("YAO FU", font=EN_FONT, font_size=36, color=WHITE, weight=BOLD),
            Text("UIBE · Master's in Finance", font=EN_FONT, font_size=20, color=GREY_B),
            Text("Ant Group · AI Engineer Intern", font=EN_FONT, font_size=20, color=TECH_BLUE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        info_lines.next_to(char, RIGHT, buff=0.8)
        info_box = SurroundingRectangle(info_lines, color=TECH_BLUE, buff=0.3, stroke_width=1, corner_radius=0.1)
        info_group = VGroup(info_box, info_lines)

        self.pt(FadeIn(char, shift=UP * 0.3), run_time=0.4)
        self.wait_until(T.start("s02"))

        sub = BiSub("This is Yao Fu.", "这是符瑶。")
        self.pt(FadeIn(sub), FadeIn(info_group, shift=RIGHT * 0.3), run_time=0.8)
        self.wait_until(T.end("s02"))
        self.pt(FadeOut(sub), run_time=0.2)

        self.wait_until(T.start("s02b"))
        sub2 = BiSub(
            "Most engineers write answers. She writes the questions.",
            "大多数工程师写答案。她写考题。",
        )
        self.pt(FadeIn(sub2), run_time=0.3)
        self.pt(char.animate.scale(1.012), run_time=1.5, rate_func=there_and_back)
        self.do_blink(char)
        self.wait_until(T.end("s02b"))
        self.pt(FadeOut(sub2), FadeOut(info_group), run_time=0.3)

        self.pt(char.animate.shift(LEFT * 0.5).scale(0.7), run_time=0.4)
        self.current_char = char

    def scene_03_montage(self):
        T = self.T
        char = self.current_char

        code_texts = [
            "consistency = evaluate(model_a, model_b, model_c)",
            "rubric = generate_rubric(question, answer)",
            "tier = classify_quality(score, source)",
            "react_loop(search, reason, verify)",
            "flywheel.run(eval, diagnose, synthesize)",
            "deploy(bailing, stage='production')",
        ]
        code_lines = VGroup(*[
            Text(ct, font="Courier New", font_size=16, color=TECH_BLUE, opacity=0.6)
            .move_to(RIGHT * 2.5 + UP * (1.5 - i * 0.6))
            for i, ct in enumerate(code_texts)
        ])

        layers = [3, 5, 5, 3]
        nn_nodes = VGroup(*[
            Dot(point=np.array([2.0 + li * 1.2, (n - 1) / 2 * 0.5 - ni * 0.5, 0]),
                radius=0.08, color=TECH_BLUE, fill_opacity=0.4)
            for li, n in enumerate(layers)
            for ni in range(n)
        ])
        nn_edges = VGroup(*[
            Line(nn_nodes[sum(layers[:li]) + i].get_center(),
                 nn_nodes[sum(layers[:li + 1]) + j].get_center(),
                 stroke_width=0.5, color=TECH_BLUE, stroke_opacity=0.2)
            for li in range(len(layers) - 1)
            for i in range(layers[li])
            for j in range(layers[li + 1])
        ])
        nn = VGroup(nn_edges, nn_nodes).scale(0.8).shift(RIGHT * 1 + DOWN * 0.5)

        self.wait_until(T.start("s03"))
        sub1 = BiSub(
            "Every day, she tests where AI fails — on earnings, on risk, on reasoning.",
            "每天，她测试 AI 在哪里失败——盈利、风险、推理。",
        )
        self.pt(FadeIn(sub1), run_time=0.3)
        self.pt(char.animate.shift(RIGHT * 0.15), run_time=0.8)
        self.pt(LaggedStart(*[FadeIn(cl, shift=LEFT * 0.3) for cl in code_lines], lag_ratio=0.15), run_time=2.0)
        self.pt(char.animate.shift(DOWN * 0.04), run_time=0.3, rate_func=there_and_back)
        self.pt(FadeIn(nn, scale=0.8), run_time=1.5)
        self.wait_until(T.end("s03"))
        self.pt(FadeOut(sub1), run_time=0.2)

        self.wait_until(T.start("s04a"))
        sub2 = BiSub("Faster than her.", "代码比她更快。")
        self.pt(FadeIn(sub2), run_time=0.3)
        self.pt(
            *[cl.animate.shift(UP * 3).set_opacity(0) for cl in code_lines],
            *[nd.animate.set_fill(WARM_GOLD, opacity=0.9) for nd in nn_nodes],
            run_time=1.0,
        )
        self.wait_until(T.end("s04a"))
        self.pt(FadeOut(sub2), run_time=0.2)

        self.wait_until(T.start("s04b"))
        sub3 = BiSub("In some ways, smarter.", "在某些方面，比她更聪明。")
        self.pt(FadeIn(sub3), run_time=0.3)
        self.pt(*[nd.animate.scale(1.5).set_fill(WARM_GOLD, opacity=1.0) for nd in nn_nodes], run_time=1.5)
        self.wait_until(T.end("s04b"))
        self.pt(FadeOut(sub3), FadeOut(nn), FadeOut(code_lines), run_time=0.5)
        self.pt(char.animate.shift(LEFT * 0.15), run_time=0.3)

    def scene_04_turning(self):
        T = self.T
        char = self.current_char

        char_think = SVGMobject(str(CHARACTER_DIR / "fu_yao_thinking.svg")).set_height(char.get_height())
        char_think.move_to(char.get_center())
        self.pt(ReplacementTransform(char, char_think), run_time=0.4)

        self.wait_until(T.start("s05"))
        screen = Rectangle(
            width=4, height=2.5, stroke_color=GREY_C,
            stroke_width=1, fill_color="#0D1117", fill_opacity=0.8,
        ).shift(RIGHT * 2 + UP * 0.3)
        cursor = Rectangle(
            width=0.08, height=0.5, fill_color=TECH_BLUE,
            fill_opacity=1, stroke_width=0,
        ).shift(RIGHT * 2 + UP * 0.5)

        sub = BiSub(
            "But one day... the AI asked her\nsomething she couldn't answer.",
            "但有一天……AI向她提出了一个她无法回答的问题。",
        )
        self.pt(FadeIn(screen), FadeIn(sub), run_time=0.4)
        self.add(cursor)
        for _ in range(5):
            self.pt(cursor.animate.set_opacity(0), run_time=0.8, rate_func=there_and_back)
        self.wait_until(T.end("s05"))
        self.pt(FadeOut(sub), run_time=0.2)

        self.wait_until(T.start("s05b"))
        sub2 = BiSub("It asked: Why does beauty matter to you?", "它问：美对你来说为什么重要？")
        question = Text(
            "Why does beauty matter to you?",
            font="Courier New", font_size=20, color=WARM_GOLD,
        ).shift(RIGHT * 2 + UP * 0.5)
        self.pt(FadeIn(sub2), run_time=0.3)
        self.pt(FadeIn(question, shift=UP * 0.1), run_time=0.5)
        self.pt(char_think.animate.scale(1.012), run_time=1.5, rate_func=there_and_back)
        self.wait_until(T.end("s05b"))
        self.pt(FadeOut(sub2), FadeOut(screen), FadeOut(cursor), FadeOut(question), run_time=0.4)
        self.current_char = char_think

    def scene_05_sunset(self):
        T = self.T
        char = self.current_char

        char_side = SVGMobject(str(CHARACTER_DIR / "fu_yao_side_right.svg")).set_height(char.get_height())
        char_side.move_to(char.get_center())

        sunset_colors = ["#1a0533", "#4a1942", "#c2185b", "#ff6f00", "#ffab00", "#fff176"]
        sun = Circle(radius=1.2, fill_color="#FFD54F", fill_opacity=0.9, stroke_width=0).shift(RIGHT * 3 + DOWN * 0.5)
        sun_glow = Circle(radius=2, fill_color="#FFD54F", fill_opacity=0.15, stroke_width=0).move_to(sun.get_center())
        horizon = Line(LEFT * 7, RIGHT * 7, stroke_color="#ff6f00", stroke_width=2, stroke_opacity=0.6).shift(DOWN * 1.5)
        sky_layers = VGroup(*[
            Rectangle(width=14.5, height=0.8, fill_color=c, fill_opacity=0.4, stroke_width=0)
            .shift(UP * (2.5 - i * 0.9))
            for i, c in enumerate(sunset_colors)
        ])

        self.wait_until(T.start("s06a"))
        sub1 = BiSub(
            "She showed it a sunset.\nIt described the wavelengths perfectly.",
            "她给它看了一场日落。它完美地描述了光的波长。",
        )
        self.pt(
            ReplacementTransform(char, char_side),
            FadeIn(sky_layers), FadeIn(sun, scale=0.5),
            FadeIn(sun_glow), FadeIn(horizon), FadeIn(sub1),
            run_time=1.2,
        )

        data_texts = VGroup(
            Text("λ = 620-750nm", font="Courier New", font_size=14, color=TECH_BLUE),
            Text("Rayleigh scattering coefficient: 0.84", font="Courier New", font_size=12, color=TECH_BLUE),
            Text("Color temp: 2700K → 1800K", font="Courier New", font_size=12, color=TECH_BLUE),
            Text("Angular diameter: 0.53°", font="Courier New", font_size=12, color=TECH_BLUE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).shift(RIGHT * 3 + UP * 2).set_opacity(0.7)

        self.pt(LaggedStart(*[FadeIn(dt) for dt in data_texts], lag_ratio=0.2), run_time=2.0)
        self.wait_until(T.end("s06a"))
        self.pt(FadeOut(sub1), run_time=0.3)

        self.wait_until(T.start("s06b"))
        sub2 = BiSub("But it couldn't tell her why it was beautiful.", "但它说不出，为什么那很美。")
        self.pt(FadeIn(sub2), run_time=0.3)
        self.pt(*[dt.animate.set_opacity(0).shift(UP * 0.5) for dt in data_texts], run_time=2.0)
        self.wait_until(T.end("s06b"))
        self.pt(FadeOut(sub2), FadeOut(sky_layers), FadeOut(sun), FadeOut(sun_glow), FadeOut(horizon), FadeOut(data_texts), run_time=0.8)
        self.current_char = char_side

    def scene_06_understand(self):
        T = self.T
        char = self.current_char

        char_front = SVGMobject(str(CHARACTER_DIR / "fu_yao_front.svg")).set_height(char.get_height())
        char_front.move_to(char.get_center())
        self.pt(ReplacementTransform(char, char_front), run_time=0.3)

        self.wait_until(T.start("s07"))
        sub1 = BiSub(
            "That's when she understood.\nWhat makes us human isn't what we know.",
            "那一刻她明白了。人之为人，不在于我们知道什么。",
        )
        self.pt(FadeIn(sub1), run_time=0.3)
        know_text = Text("what we know", font=EN_FONT, font_size=32, color=GREY_B).shift(RIGHT * 2.5 + UP * 1)
        self.pt(FadeIn(know_text), run_time=0.5)
        self.pt(know_text.animate.set_opacity(0).shift(UP * 0.3), run_time=1.5)
        self.remove(know_text)
        self.wait_until(T.end("s07"))
        self.pt(FadeOut(sub1), run_time=0.3)

        self.wait_until(T.start("s07b"))
        sub_7b = BiSub(
            "The AI could calculate. It could optimize.\nIt could predict.",
            "AI能计算、能优化、能预测。",
        )
        self.pt(FadeIn(sub_7b), run_time=0.3)
        self.pt(char_front.animate.shift(UP * 0.12), run_time=0.2)
        self.pt(char_front.animate.shift(DOWN * 0.12), run_time=0.2)

        words = VGroup(
            Text("Calculate", font=EN_FONT, font_size=28, color=TECH_BLUE),
            Text("Optimize", font=EN_FONT, font_size=28, color=TECH_BLUE),
            Text("Predict", font=EN_FONT, font_size=28, color=TECH_BLUE),
        ).arrange(RIGHT, buff=0.8).shift(RIGHT * 2 + UP * 1)
        for w in words:
            self.pt(FadeIn(w, shift=UP * 0.2), run_time=0.6)

        char_conf = SVGMobject(str(CHARACTER_DIR / "fu_yao_confident.svg")).set_height(char_front.get_height())
        char_conf.move_to(char_front.get_center())
        self.pt(ReplacementTransform(char_front, char_conf), run_time=0.5)
        self.pt(FadeOut(words), run_time=0.4)
        self.wait_until(T.end("s07b"))
        self.pt(FadeOut(sub_7b), run_time=0.2)

        self.wait_until(T.start("s08"))
        sub2 = BiSub("It's what we choose to care about.", "而在于我们选择在乎什么。")
        self.pt(FadeIn(sub2), run_time=0.3)
        orb = Circle(radius=0.6, fill_color=WARM_GOLD, fill_opacity=0.7, stroke_width=0).shift(RIGHT * 3 + UP * 0.5)
        orb_glow = Circle(radius=1.2, fill_color=WARM_GOLD, fill_opacity=0.15, stroke_width=0).move_to(orb.get_center())
        self.pt(GrowFromCenter(orb), FadeIn(orb_glow), run_time=0.8)
        self.pt(
            char_conf.animate.shift(RIGHT * 0.3),
            orb.animate.set_fill(opacity=1.0).scale(1.2),
            orb_glow.animate.scale(1.5).set_opacity(0.25),
            run_time=1.0,
        )
        self.wait_until(T.end("s08"))
        self.pt(FadeOut(sub2), run_time=0.2)
        self.current_char = char_conf
        self.orb = orb
        self.orb_glow = orb_glow

    def scene_07_closing(self):
        T = self.T
        char = self.current_char
        orb = self.orb
        orb_glow = self.orb_glow

        self.wait_until(T.start("s09"))
        sub = BiSub(
            "She teaches AI to think.\nAnd it's teaching her what it means to be human.",
            "她教AI思考。而AI正教会她，何为人类。",
        )
        self.pt(FadeIn(sub), run_time=0.3)

        tagline = VGroup(
            Text("She teaches AI to think.", font=EN_FONT, font_size=36, color=TECH_BLUE),
            Text("And it's teaching her", font=EN_FONT, font_size=36, color=WHITE),
            Text("what it means to be human.", font=EN_FONT, font_size=36, color=WARM_GOLD),
        ).arrange(DOWN, buff=0.2).shift(UP * 1.5)

        self.pt(char.animate.shift(LEFT * 1).scale(0.8), FadeOut(orb), FadeOut(orb_glow), run_time=0.8)
        self.pt(LaggedStart(*[FadeIn(line, shift=UP * 0.2) for line in tagline], lag_ratio=0.3), run_time=2.5)
        self.wait_until(T.end("s09"))
        self.pt(FadeOut(sub), run_time=0.2)

        signature = Text("— Yao Fu", font=EN_FONT, font_size=28, color=GREY_B)
        signature.next_to(tagline, DOWN, buff=0.5)
        self.pt(FadeIn(signature, shift=UP * 0.1), run_time=0.8)
        self.wait(1.5)
        self.ct += 1.5
        self.pt(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
