from manim import *
from numpy import ndarray

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 7.5

config.frame_rate = 15

EMPTY_MOBJECT = VMobject()
MOROCCAN_BLUE = ManimColor("#27ADF5")

class TrigonometricRadios(MovingCameraScene):
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
        leg_x.add_updater(lambda line: line.put_start_and_end_on(
            ORIGIN,
            handle.get_x() * RIGHT
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

        one = TrigonometricRadios._math_tex_factory("r=1")
        one.move_to(handle.get_x() / 2 * RIGHT + .5 * UP)
        self.play(Write(one), run_time=.75)

        self.wait(.75)

        self.play(Unwrite(one), run_time=.5)

        self.wait(.5)

        # -- Present Theta

        self.add(leg_x, leg_y, angle)
        self.play(theta.animate.set_value(TAU / 8), run_time=1.5)

        theta_label = TrigonometricRadios._math_tex_factory(r"\theta", font_size=40)
        theta_label.move_to(.7 * RIGHT + .35 * UP)
        self.play(SpinInFromNothing(theta_label))

        def make_theta_param_tex(normalize_theta=False) -> MathTex:
            value = round(np.rad2deg(theta.get_value()), 1)
            if normalize_theta: value %= 360
            result = TrigonometricRadios._math_tex_factory(
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
        theta_eq2_part = TrigonometricRadios._math_tex_factory("=", r"45^\circ")
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
        #self.play(self.camera.frame.animate.shift(DOWN * .75))

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
            leg_y.get_center() + RIGHT * .75, LEFT * .3 + DOWN * .1, None,
            leg_y
        )
        self.wait(.5)
        adj_leg_label = self._label_triangle_side(
            "adjacent\nleg", "adj", GREEN_E,
            leg_x.get_center() + DOWN * .5, UP * .15, None,
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
            FadeOut(sin_formula[3:5]),
            FadeOut(cos_formula[3:5]),
            ReplacementTransform(sin_formula[0:3], sin_simple),
            ReplacementTransform(cos_formula[0:3], cos_simple),
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
            # sin_simple.animate.shift(UP * 6),
            # cos_simple.animate.shift(UP * 6),
            # tan_formula.animate.shift(UP * 2)
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
            FadeIn(sin_value),
            FadeIn(cos_value),
            FadeIn(tan_value),
            FadeOut(sin_simple[2]),
            FadeOut(cos_simple[2]),
            FadeOut(tan_formula[2:]),
        )

        # -- Reorganize elements in screen

        theta_param_tex = always_redraw(lambda: make_theta_param_tex(normalize_theta=True))
        self.play(
             self.camera.frame.animate
                # .move_to(ORIGIN + UP * .2)
                .scale(1.3),
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
        tan_line = Line(
            r * RIGHT,
            r * RIGHT + (r * np.tan(theta.get_value())) * UP,
            color=PURPLE
        )
        tan_line.add_updater(lambda line: line.put_start_and_end_on(
            r * RIGHT,
            r * RIGHT + r * np.tan(theta.get_value()) * UP
        ))

        opp_side_label = always_redraw(lambda:
            self._math_tex_factory(r"\sin(\theta)", font_size=30, color=MOROCCAN_BLUE)
            .move_to(leg_y.get_center() + RIGHT * .6)
        )
        adj_side_label = always_redraw(lambda:
            self._math_tex_factory(r"\cos(\theta)", font_size=30, color=GREEN_E)
            .move_to(leg_x.get_center() + DOWN * .4)
        )
        tan_side_label = always_redraw(lambda:
            self._math_tex_factory(r"\tan(\theta)", font_size=30, color=PURPLE)
            .move_to(tan_line.get_center() + RIGHT * .7)
        )

        self.play(
            FadeIn(opp_side_label), FadeIn(adj_side_label), FadeIn(tan_side_label),
            Create(tan_line), Create(hyp_extension)
        )
        self.wait(1)

        self.remove(angle)
        angle = always_redraw(lambda: draw_angle(normalize=True))
        self.add(angle)

        # Move theta and see it update
        right_triangle.resume_updating()
        for i in range(1, 6):
            self.play(
                theta.animate.set_value(TAU + TAU / 8 if i == 5 else i * TAU / 4),
                run_time=2.25 if i == 1 or i == 5 else 4,
                rate_func=lambda t: (1 - .15) * t + .075 * (1 - np.cos(PI * t))
            )

        self.wait(1)

    def _label_triangle_side(self, full_name: str, abbreviation: str, color: ManimColor,
                             pos: ndarray, abbreviation_offset: ndarray | None, rotation: float | None,
                             side: Mobject) -> Paragraph:
        full_name_text = TrigonometricRadios._label_factory(full_name, color=color)
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

        abbreviated_text = TrigonometricRadios._label_factory(abbreviation, color=color)
        abbreviated_text.move_to(pos if abbreviation_offset is None else pos + abbreviation_offset)
        if rotation is not None:
            abbreviated_text.rotate(rotation)

        self.play(
            Transform(full_name_text, abbreviated_text),
            run_time=.5
        )

        return full_name_text

    @staticmethod
    def _label_factory(text: str, font_size: float = 20, color: ManimColor = WHITE) -> Paragraph:
        return Paragraph(
            *text.split("\n"),
            font_size=font_size,
            color=color,
            alignment="center"
        )

    @staticmethod
    def _math_tex_factory(*tex_strings: str, font_size: float = 48, color: ManimColor = WHITE) -> MathTex:
        return MathTex(
            *tex_strings,
            font_size=font_size,
            color=color
        )