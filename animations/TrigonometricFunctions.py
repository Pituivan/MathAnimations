from manim import *
from typing import Callable
from numpy import ndarray

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 7.5

config.frame_rate = 15

EMPTY_MOBJECT = VMobject()
MOROCCAN_BLUE = ManimColor("#27ADF5")

class TrigonometricFunctions(MovingCameraScene):
    def construct(self):

        # --- Unit Circle

        r = 2

        circumference = Circle(radius=r)
        x_axis = Line(r * LEFT, r * RIGHT, color=RED, stroke_width=1, stroke_opacity=1)
        y_axis = Line(r * UP, r * DOWN, color=RED, stroke_width=1)

        # --- Right Triangle and auxiliary elements

        theta = ValueTracker(0)

        handle = Dot()
        handle.add_updater(lambda vertex: vertex.move_to(
            r * (np.cos(theta.get_value()) * RIGHT + np.sin(theta.get_value()) * UP)
        ))

        hypotenuse = Line()
        hypotenuse.add_updater(lambda line: line.put_start_and_end_on(
            ORIGIN,
            handle.get_center()
        ))
        leg_x = Line()
        leg_x_offset_y = ValueTracker(0)
        leg_x.add_updater(lambda line: line.put_start_and_end_on(
            leg_x_offset_y.get_value() * UP,
            handle.get_x() * RIGHT + leg_x_offset_y.get_value() * UP
        ))
        leg_y = Line()
        leg_y.add_updater(lambda line: line.put_start_and_end_on(
            handle.get_x() * RIGHT,
            handle.get_center()
        ))

        right_triangle = Group(hypotenuse, leg_x, leg_y, handle)

        def draw_angle(normalize=False):
          value = theta.get_value()
          if normalize: value %= TAU
          return EMPTY_MOBJECT if value % TAU == 0 \
            else Arc(
                angle=value,
                radius=.4
            )

        angle = always_redraw(draw_angle)

        # --- Unit Circle Presentation

        # -- Draw Elements

        self.wait(1)
        self.play(AnimationGroup(Create(circumference), Create(x_axis), Create(y_axis)))
        self.play(Create(handle))
        self.play(Create(hypotenuse))

        self.wait(.25)

        # -- State r = 1

        one = TrigonometricFunctions._math_tex_factory("r=1")
        one.move_to(handle.get_x() / 2 * RIGHT + .5 * UP)
        self.play(Write(one), run_time=.75)

        self.wait(.75)

        self.play(Unwrite(one), run_time=.5)

        self.wait(.5)

        # -- Present Theta

        self.add(leg_x, leg_y, angle)
        self.play(theta.animate.set_value(TAU / 8), run_time=1.5)

        theta_label = TrigonometricFunctions._math_tex_factory(r"\theta", font_size=40)
        theta_label.move_to(.7 * RIGHT + .35 * UP)
        self.play(SpinInFromNothing(theta_label))

        def make_theta_param_tex(normalize_theta=False) -> MathTex:
            value = round(np.rad2deg(theta.get_value()), 1)
            if normalize_theta: value %= 360
            result = TrigonometricFunctions._math_tex_factory(
                r"\theta", "=", rf"{value:g}^\circ"
            )

            result.move_to(UP * 3)
            return result

        initial_theta_param_tex = make_theta_param_tex()
        theta_param_tex = always_redraw(make_theta_param_tex)

        self.play(Write(initial_theta_param_tex))
        self.remove(initial_theta_param_tex)
        self.add(theta_param_tex)

        self.wait(.5)

        self.play(ShrinkToCenter(theta_label))

        self.wait(.5)

        # -- Second Spin, Angle Back to Positive & Theta Out

        self.play(theta.animate.set_value(-7 * TAU / 8), run_time=2.5)

        self.wait(1)

        theta_eq = make_theta_param_tex()
        theta_eq2_part = TrigonometricFunctions._math_tex_factory("=", r"45^\circ")
        theta_eq2_part.next_to(theta_eq, RIGHT)

        right_triangle.suspend_updating()
        self.remove(theta_param_tex)
        self.add(theta_eq)

        self.play(
            Succession(
                Write(theta_eq2_part),
                Wait(.5),
                AnimationGroup(
                    FadeOut(theta_eq[1]),
                    FadeOut(theta_eq[2]),
                    theta_eq[0].animate.move_to(initial_theta_param_tex[0].get_center()),
                    theta_eq2_part[0].animate.move_to(initial_theta_param_tex[1].get_center()),
                    theta_eq2_part[1].animate.move_to(initial_theta_param_tex[2].get_center())
                )
            ),
            ApplyMethod(theta.set_value, TAU / 8)
        )

        self.wait(1)

        self.play(FadeOut(Group(theta_eq[0], theta_eq2_part[0], theta_eq2_part[1])))

        self.wait(.25)

        # --- Right Triangle Presentation

        # -- Zoom In

        self.play(self.camera.frame.animate.scale(.75))

        self.wait(.5)

        # -- Hypotenuse

        hyp_label = self._label_triangle_side(
            "hypotenuse", "hyp", YELLOW_E,
            hypotenuse.get_center() + .3 * rotate_vector(UP, hypotenuse.get_angle()), None, hypotenuse.get_angle(),
            hypotenuse
        )
        self.wait(.5)
        opp_leg_label = self._label_triangle_side(
            "opposite\nleg", "opp", MOROCCAN_BLUE,
            leg_y.get_center() + .75 * RIGHT, .3 * LEFT + .1 * DOWN, None,
            leg_y
        )
        self.wait(.5)
        adj_leg_label = self._label_triangle_side(
            "adjacent\nleg", "adj", GREEN_E,
            leg_x.get_center() + .5 * DOWN, .15 * UP, None,
            leg_x
        )

        self.wait(1)

        self.play(
            hyp_label.animate
                .rotate(-hypotenuse.get_angle())
                .move_to(2.5 * DOWN + 2 * LEFT),
            opp_leg_label.animate.move_to(2.5 * DOWN),
            adj_leg_label.animate.move_to(2.5 * DOWN + 2 * RIGHT)
        )

        self.wait(.5)

        # --- Sine and Cosine Definitions

        # -- Create the formulas

        sin_formula = self._math_tex_factory(
            r"\sin(\theta)", "=", r"{\text{opp}", r"\over", r"\text{hyp}}",
            font_size=30
        )

        cos_formula = self._math_tex_factory(
            r"\cos(\theta)", "=", r"{\text{adj}", r"\over", r"\text{hyp}}",
            font_size=30
        )

        sin_formula.move_to(3.35 * DOWN + 1.25 * LEFT)
        cos_formula.move_to(3.35 * DOWN + 1.25 * RIGHT)

        sin_formula[2].set_color(MOROCCAN_BLUE) # opp
        cos_formula[2].set_color(GREEN_E)       # adj
        sin_formula[4].set_color(YELLOW_E)      # hyp
        cos_formula[4].set_color(YELLOW_E)      # hyp

        # Bring copies of the labels into the formulas

        opp_copy = opp_leg_label.copy()
        hyp_copy = hyp_label.copy()

        indicate_hyp_label_anim = Indicate(hyp_label, color=YELLOW_E, run_time=.35)
        indicate_opp_label_anim = Indicate(opp_leg_label, color=MOROCCAN_BLUE, run_time=.35)
        indicate_adj_label_anim = Indicate(adj_leg_label, color=GREEN_E, run_time=.35)

        self.play(Write(sin_formula[0:2]))
        self.play(
            indicate_hyp_label_anim,
            indicate_opp_label_anim,
            AnimationGroup(
                Transform(opp_copy, sin_formula[2]),
                Transform(hyp_copy, sin_formula[4]),
                Write(sin_formula[3]),
                run_time=1.5
            )
        )
        self.remove(opp_copy, hyp_copy)
        self.add(sin_formula[2], sin_formula[4])
        self.wait(.25)

        adj_copy = adj_leg_label.copy()
        hyp_copy = hyp_label.copy()

        self.play(Write(cos_formula[0:2]))
        self.play(
            indicate_hyp_label_anim,
            indicate_adj_label_anim,
            AnimationGroup(
                Transform(adj_copy, cos_formula[2]),
                Transform(hyp_copy, cos_formula[4]),
                Write(cos_formula[3]),
                run_time=1.5
            )
        )
        self.remove(adj_copy, hyp_copy)
        self.add(cos_formula[2], cos_formula[4])
        self.wait(.5)

        # Transform hyp to 1 directly in the formulas
        self.play(
            Transform(sin_formula[4], self._math_tex_factory("1", color=YELLOW_E, font_size=36).move_to(sin_formula[4])),
            Transform(cos_formula[4], self._math_tex_factory("1", color=YELLOW_E, font_size=36).move_to(cos_formula[4])),
            run_time=.5
        )
        self.wait(.5)

        # Simplify formulas (remove / 1)
        sin_simple = self._math_tex_factory(r"\sin(\theta)", "=", r"\text{opp}", font_size=30)
        cos_simple = self._math_tex_factory(r"\cos(\theta)", "=", r"\text{adj}", font_size=30)

        sin_simple.move_to(sin_formula)
        cos_simple.move_to(cos_formula)

        sin_simple[2].set_color(MOROCCAN_BLUE)
        cos_simple[2].set_color(GREEN_E)

        self.play(
            FadeOut(sin_formula[3:5]), FadeOut(cos_formula[3:5]),
            ReplacementTransform(sin_formula[0:3], sin_simple), ReplacementTransform(cos_formula[0:3], cos_simple),
            run_time=.5
        )

        self.wait(.5)

        # --- Tangent Definition

        tan_formula = self._math_tex_factory(
            r"\tan(\theta)", "=", r"{\text{opp}", r"\over", r"\text{adj}}",
            "=", r"{\sin(\theta)", r"\over", r"\cos(\theta)}",
            font_size=30
        )
        tan_formula.move_to(4.25 * DOWN)

        tan_formula[2].set_color(MOROCCAN_BLUE)  # opp
        tan_formula[4].set_color(GREEN_E)        # adj
        tan_formula[6].set_color(MOROCCAN_BLUE)  # sin
        tan_formula[8].set_color(GREEN_E)        # cos

        self.play(Write(tan_formula[0:2]))

        # Use copies of adj and opp labels for the definition of the tangent

        opp_copy_tan = opp_leg_label.copy()
        adj_copy_tan = adj_leg_label.copy()

        self.play(
            indicate_opp_label_anim,
            indicate_adj_label_anim,
            AnimationGroup(
                Transform(opp_copy_tan, tan_formula[2]),
                Transform(adj_copy_tan, tan_formula[4]),
                Write(tan_formula[3]),
                run_time=1.25
            )
        )
        self.remove(opp_copy_tan, adj_copy_tan)
        self.add(tan_formula[2], tan_formula[4])

        self.wait(.5)

        # Use a copy of sin and cos (from the previous formulas) for the definition of the tangent

        sin_copy_tan = sin_simple[0].copy()
        cos_copy_tan = cos_simple[0].copy()

        sin_copy_tan.set_color(MOROCCAN_BLUE)
        cos_copy_tan.set_color(GREEN_E)

        self.play(Write(tan_formula[5]))
        self.play(
            Indicate(sin_simple[0], color=MOROCCAN_BLUE, run_time=.35),
            Indicate(cos_simple[0], color=GREEN_E, run_time=.35),
            Transform(sin_copy_tan, tan_formula[6]),
            Transform(cos_copy_tan, tan_formula[8]),
            Write(tan_formula[7])
        )
        self.remove(sin_copy_tan, cos_copy_tan)
        self.add(tan_formula[6], tan_formula[8])
        self.wait(.5)

        # --- Dynamic Demonstration

        # Triangle sides labels will fade out, while formulas will be repositioned so they're
        # repositioned to the left, thus the tangent line doesn't draw over them.

        remove_triangle_sides_labels = AnimationGroup(
            FadeOut(hyp_label, shift=DOWN),
            FadeOut(opp_leg_label, shift=DOWN),
            FadeOut(adj_leg_label, shift=DOWN)
        )

        reposition_formulas = AnimationGroup(
            sin_simple.animate.move_to(2.5 * DOWN + 2.5 * LEFT, aligned_edge=LEFT),
            cos_simple.animate.move_to(3 * DOWN + 2.5 * LEFT, aligned_edge=LEFT),
            tan_formula.animate.move_to(3.5 * DOWN + 2.5 * LEFT, aligned_edge=LEFT),
        )

        # While the demonstration takes place, the trigonometric radios formulas second term
        # will be the actual, numerical (approximated) value.

        sin_value = DecimalNumber(np.sin(theta.get_value()), num_decimal_places=2, font_size=30, color=MOROCCAN_BLUE)
        sin_value.add_updater(lambda d: d.set_value(np.sin(theta.get_value())).next_to(sin_simple[1], RIGHT))

        cos_value = DecimalNumber(np.cos(theta.get_value()), num_decimal_places=2, font_size=30, color=GREEN_E)
        cos_value.add_updater(lambda d: d.set_value(np.cos(theta.get_value())).next_to(cos_simple[1], RIGHT))

        tan_value = DecimalNumber(np.tan(theta.get_value()), num_decimal_places=2, font_size=30, color=PURPLE)
        tan_value.add_updater(lambda d: d.set_value(np.tan(theta.get_value())).next_to(tan_formula[1], RIGHT))

        replace_formulas_values = AnimationGroup(
            FadeIn(sin_value), FadeIn(cos_value), FadeIn(tan_value),
            FadeOut(sin_simple[2]), FadeOut(cos_simple[2]), FadeOut(tan_formula[2:])
        )

        # -- Reorganize elements in screen

        theta_param_tex = always_redraw(lambda: make_theta_param_tex(normalize_theta=True))
        self.play(
             self.camera.frame.animate.scale(1.3),
            remove_triangle_sides_labels,
            reposition_formulas,
            FadeIn(theta_param_tex),
            replace_formulas_values,
            hypotenuse.animate.set_color(WHITE) # Since the hypotenuse is not relevant anymore
        )

        # -- Visual representation of the trigonometric radios

        hyp_extension = Line(stroke_width=2, stroke_opacity=.5)
        hyp_extension.add_updater(lambda line: line.put_start_and_end_on(
            handle.get_center(),
            r * RIGHT + r * np.tan(theta.get_value()) * UP
        ))

        # The opposite leg of the mentioned right triangle
        tan_line = Line(color=PURPLE)
        tan_line.add_updater(lambda line: line.put_start_and_end_on(
            r * RIGHT,
            r * RIGHT + r * np.tan(theta.get_value()) * UP
        ))

        sin_label = self._func_label_factory(
            "sin",
            MOROCCAN_BLUE,
            lambda: leg_y.get_center() + .6 * RIGHT
        )

        cos_label_offset_y = ValueTracker(-.4)
        cos_label = self._func_label_factory(
            "cos",
            GREEN_E,
            lambda: leg_x.get_center() + cos_label_offset_y.get_value() * UP
        )

        tan_label = self._func_label_factory(
            "tan",
            PURPLE,
            lambda: tan_line.get_center() + .7 * RIGHT
        )

        self.play(
             Create(hyp_extension), Create(tan_line),
            FadeIn(tan_label), FadeIn(sin_label), FadeIn(cos_label)
        )
        self.wait(1)

        self.remove(angle)
        angle = always_redraw(lambda: draw_angle(normalize=True))
        self.add(angle)

        right_triangle.resume_updating()
        self._spin_angle(theta)
        theta.set_value(TAU / 8)

        self.wait(1.5)

        # --- Define and draw Inverse Functions

        # -- Reorganize elements in screen

        x_axis_extension = Line(stroke_width=2, stroke_opacity=.5, z_index=-1)
        x_axis_extension.add_updater(lambda line: line.put_start_and_end_on(
            r * RIGHT,
            r / np.cos(theta.get_value()) * RIGHT
        ))

        hyp_extension.clear_updaters()
        tan_line.clear_updaters()
        reposition_tan = AnimationGroup(
            hyp_extension.animate.put_start_and_end_on(
                hypotenuse.get_start(),
                hypotenuse.get_end()
            ),
            tan_line.animate.put_start_and_end_on(
                np.sqrt(2) * r * RIGHT, # Pre-calculated x-intersect
                handle.get_center()
            ),
            Create(x_axis_extension)
        )

        self.play(
            FadeOut(theta_param_tex),
            reposition_tan,
            leg_x_offset_y.animate.set_value(r * np.cos(theta.get_value())),
            cos_label_offset_y.animate.set_value(.4)
        )
        self.remove(hyp_extension)
        leg_x_offset_y.add_updater(lambda m: m.set_value(r * np.sin(theta.get_value())))

        tan_line.add_updater(lambda line: line.put_start_and_end_on(
            r / np.cos(theta.get_value()) * RIGHT,
            handle.get_center()
        ))

        self.wait(1)

        # -- Visually present sec, csc and cot

        csc_line_trace = Line(
            r * UP, r / np.sin(theta.get_value()) * UP,
            stroke_width=2, stroke_opacity=.5
        )

        sec_line = Line(color=ORANGE)
        sec_line.add_updater(lambda line: line.put_start_and_end_on(
            ORIGIN,
            r / np.cos(theta.get_value()) * RIGHT
        ))

        cot_line_trace = Line(
            handle.get_center(), r / np.sin(theta.get_value()) * UP,
            stroke_width=2, stroke_opacity=.5
        )

        self.play(Create(csc_line_trace), Create(cot_line_trace))
        self.wait(.5)

        csc_line = Line(color=YELLOW_E)
        csc_line.add_updater(lambda line: line.put_start_and_end_on(
            ORIGIN,
            r / np.sin(theta.get_value()) * UP
        ))

        cot_line = Line(color=PURE_MAGENTA)
        cot_line.add_updater(lambda line: line.put_start_and_end_on(
            handle.get_center(),
            r / np.sin(theta.get_value()) * UP
        ))

        csc_label = self._func_label_factory(
            "csc",
            YELLOW_E,
            lambda: csc_line.get_center() + .6 * LEFT
        )

        sec_label = self._func_label_factory(
            "sec",
            ORANGE,
            lambda: sec_line.get_center() + .4 * DOWN
        )

        cot_label = self._func_label_factory(
            "cot",
            PURE_MAGENTA,
            lambda: cot_line.get_center() + .7 * RIGHT
        )

        self.play(
            Create(sec_line), Create(csc_line), Create(cot_line),
             FadeIn(sec_label), FadeIn(csc_label), FadeIn(cot_label)
        )
        self.remove(x_axis_extension, csc_line_trace, cot_line_trace)

        self.wait(1)

        # -- Write the inverse functions definitions

        formulas = Group(sin_simple[:2], cos_simple[:2], tan_formula[:2])
        self.play(
            formulas.animate.shift(.5 * DOWN),
            self.camera.frame.animate.shift(2 * DOWN)
        )

        csc_formula = self._math_tex_factory(r"\csc(\theta) =", r"{1 \over \sin(\theta)}", font_size=30)
        csc_formula[1][2:].set_color(MOROCCAN_BLUE)
        csc_formula.move_to(4.75 * DOWN + 2.5 * LEFT, aligned_edge=LEFT)

        sec_formula = self._math_tex_factory(r"\sec(\theta) =", r"{1 \over \cos(\theta)}", font_size=30)
        sec_formula[1][2:].set_color(GREEN_E)
        sec_formula.move_to(5.75 * DOWN + 2.5 * LEFT, aligned_edge=LEFT)

        cot_formula = self._math_tex_factory(r"\cot(\theta) =", r"{1 \over \tan(\theta)}", font_size=30)
        cot_formula[1][2:].set_color(PURPLE)
        cot_formula.move_to(6.75 * DOWN + 2.5 * LEFT, aligned_edge=LEFT)

        self.wait(.75)

        self.play(
            Write(csc_formula),
            Write(sec_formula),
            Write(cot_formula)
        )

        self.wait(1)

        csc_formula_short = self._math_tex_factory(r"\csc(\theta) =", font_size=30)
        csc_formula_short.move_to(4.75 * DOWN + 2.5 * LEFT, aligned_edge=LEFT)

        sec_formula_short = self._math_tex_factory(r"\sec(\theta) =", font_size=30)
        sec_formula_short.move_to(5.75 * DOWN + 2.5 * LEFT, aligned_edge=LEFT)

        cot_formula_short = self._math_tex_factory(r"\cot(\theta) =", font_size=30)
        cot_formula_short.move_to(6.75 * DOWN + 2.5 * LEFT, aligned_edge=LEFT)

        csc_value = DecimalNumber(1 / np.sin(theta.get_value()), num_decimal_places=2, font_size=30, color=YELLOW_E)
        csc_value.add_updater(lambda m: m.set_value(1 / np.sin(theta.get_value())).next_to(csc_formula_short, RIGHT))

        sec_value = DecimalNumber(1 / np.cos(theta.get_value()), num_decimal_places=2, font_size=30, color=ORANGE)
        sec_value.add_updater(lambda m: m.set_value(1 / np.cos(theta.get_value())).next_to(sec_formula_short, RIGHT))

        cot_value = DecimalNumber(1 / np.tan(theta.get_value()), num_decimal_places=2, font_size=30, color=PURE_MAGENTA)
        cot_value.add_updater(lambda m: m.set_value(1 / np.tan(theta.get_value())).next_to(cot_formula_short, RIGHT))

        self.play(
            AnimationGroup(
                FadeOut(csc_formula), FadeIn(csc_formula_short),
                FadeOut(sec_formula), FadeIn(sec_formula_short),
                FadeOut(cot_formula), FadeIn(cot_formula_short),

                csc_formula_short.animate.move_to(4.5 * DOWN + 2.5 * LEFT, aligned_edge=LEFT),
                sec_formula_short.animate.move_to(5 * DOWN + 2.5 * LEFT, aligned_edge=LEFT),
                cot_formula_short.animate.move_to(5.5 * DOWN + 2.5 * LEFT, aligned_edge=LEFT),

                Write(csc_value),
                Write(sec_value),
                Write(cot_value),
            ),
            self.camera.frame.animate.shift(2 * UP)
        )

        self.wait(1)

        # -- Dynamic Demonstration 2

        self._spin_angle(theta)

        self.wait(1.5)

    def _label_triangle_side(self, full_name: str, abbreviation: str, color: ManimColor,
                             pos: ndarray, abbreviation_offset: ndarray | None, rotation: float | None,
                             side: Mobject) -> Paragraph:
        full_name_text = TrigonometricFunctions._label_factory(full_name, color=color)
        full_name_text.move_to(pos)
        if rotation is not None:
            full_name_text.rotate(rotation)

        self.play(
            LaggedStart(
                DrawBorderThenFill(full_name_text),
                side.animate.set_color(color),
                lag_ratio=.5
            ),
            run_time=1
        )

        self.wait(.75)

        abbreviated_text = TrigonometricFunctions._label_factory(abbreviation, color=color)
        abbreviated_text.move_to(pos if abbreviation_offset is None else pos + abbreviation_offset)
        if rotation is not None:
            abbreviated_text.rotate(rotation)

        self.play(
            Transform(full_name_text, abbreviated_text),
            run_time=.5
        )

        return full_name_text

    def _spin_angle(self, angle: ValueTracker):
        def play_anim(target, run_time):
            self.play(
                angle.animate.set_value(target),
                run_time=run_time,
                rate_func=lambda t: .85 * t + .075 * (1 - np.cos(PI * t))
            )

        for i in range(1, 5):
            play_anim(i * TAU / 4, 2.25 if i == 1 else 4)

        angle.set_value(1e-10)
        play_anim(TAU / 8, 2.25)

    @staticmethod
    def _func_label_factory(name: str, color: ManimColor, calculate_pos: Callable[[], ndarray]) -> MathTex:
        result = TrigonometricFunctions._math_tex_factory(
            rf"\{name}(\theta)",
            font_size=30,
            color=color
        )
        result.add_updater(
            lambda tex: (
                lambda pos: tex.move_to(
                    # Don't let label go off the screen, since that'd break the text
                    np.clip(pos[0], -3, 3) * RIGHT +
                    np.clip(pos[1], -6, 6) * UP
                )
            )(calculate_pos())
        )

        return result

    @staticmethod
    def _label_factory(text: str, font_size: float = 20, color: ManimColor = WHITE) -> Paragraph:
        return Paragraph(
            *text.split("\n"),
            font_size=font_size,
            color=color,
            alignment="center",
            z_index=1
        )

    @staticmethod
    def _math_tex_factory(*tex_strings: str, font_size: float = 48, color: ManimColor = WHITE) -> MathTex:
        return MathTex(
            *tex_strings,
            font_size=font_size,
            color=color,
            z_index=1
        )