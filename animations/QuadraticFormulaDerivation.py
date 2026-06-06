from manim import *
from manim.utils.rate_functions import ease_in_cubic, ease_out_sine
from utils.latex_helpers import (derive_equation, DerivationStep,
                                 START_G, END_G)

MOROCCAN_BLUE = ManimColor("#27ADF5")


class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # --- Title

        self.wait(1)

        self.play(
            Write(Text(
                "Derivation of the Quadratic Formula",
                font_size=36
            ).to_edge(UP)),
            run_time=1.25
        )

        self.wait(1)

        # --- Phase 1: Present the quadratic equation, then convert the left hand to monic form

        equation = MathTex("a", "x^2", "+", "b", "x", "+", "c", "=", "0")

        self.play(Write(equation, run_time=1.5))
        equation = derive_equation(self, equation, [
            # We need to keep TeX groups separate so TransformMatchingTex animation doesn't turn into a fade.
            # Hence, we can't use \frac for fractions since they require grouped {numerator}{denominator} in a single TeX group.
            # We also can't use \over, since the = sign and the right side of the equation would fall into the denominator.
            # A feasible option is delimiting numerator and denominator with \left. and \right.

            # Alternate between a and {a} when it's not supposed to move between terms.

            DerivationStep(
                START_G, "a", "x^2", "+", "b", "x", "+", "c", r"\over a", END_G,
                START_G, "=", END_G,
                START_G, "0", r"\over a", END_G
            ),
            DerivationStep(
                "x^2", "+", START_G, "b", r"\over {a}", END_G, "x", "+", START_G, "c", r"\over {a}", END_G,
                START_G, "=", END_G,
                "0",
                delay=.75, transition_duration=.75
            )
        ])

        self.wait(1)

        # --- Phase 2: Analytically prove square completion using the binomial square identity

        # -- Present the binomial square identity in the form (x+p)² = x² + 2px + p²

        self.play(
            equation.animate.shift(2 * UP)
        )

        self.wait(.5)

        bsi_title = Text("Binomial Square Identity", font_size=36)
        bsi_title.move_to(5 * DOWN)

        bsi_formula = MathTex("(x +", "p", ")^2 =", "x^2", "+", "2", "p", "x", "+", "p", "^2")
        bsi_formula.add_updater(lambda m: m.next_to(bsi_title, DOWN, buff=0.5))

        self.add(bsi_title, bsi_formula)
        self.play(
            bsi_title.animate.move_to(.5 * UP),
            run_time=1.5
        )

        self.wait(.75)
        self.play(FadeOut(bsi_title))
        bsi_formula.clear_updaters()

        self.wait(.75)

        # -- Replace p with b / a in binomial square identity

        # Parentheses from the original equation don't change size at first, so the animation looks cleaner
        bsi_formula_replaced = MathTex(
            "(x +", START_G, "b", r"\over {a}", END_G, ")^2 =", "x^2", "+", "2", START_G, "b", r"\over {a}",
            END_G, "x", "+", r"\bigl(", START_G, "b", r"\over {a}", END_G, r"\bigr)", "^2"
        ).move_to(bsi_formula)

        p_indices = [(1, 5), (10, 13), (17, 20)]

        equation[2:6].set_color(ORANGE) # b / a
        b_over_a_copies = {
            (start, end): equation[2:6].copy()
            for (start, end) in p_indices
        }

        self.play(
            AnimationGroup(
                Indicate(equation[2:6], color=ORANGE, run_time=.5),
                AnimationGroup(
                    AnimationGroup(
                        *[
                            Transform(
                                b_over_a_copies[start, end],
                                bsi_formula_replaced[start:end].set_color(ORANGE)
                            )
                            for start, end in p_indices
                        ]
                    ),
                    TransformMatchingShapes(bsi_formula, bsi_formula_replaced, run_time=.65),
                    lag_ratio=.45
                ),
                lag_ratio=.35
            )
        )

        self.remove(bsi_formula, *b_over_a_copies.values())
        bsi_formula = bsi_formula_replaced
        self.add(bsi_formula)

        # Make initial parentheses bigger since they're now wrapping a fraction
        bsi_formula_replaced = MathTex(
            r"\bigl(x +", START_G, "b", r"\over {a}", END_G, r"\bigr)^2 =", "x^2", "+", "2", START_G, "{b}",
            r"\over {a}", END_G, "x", "+", r"\bigl(", START_G, "{{b}}", r"\over {a}", END_G, r"\bigr)", "^2"
        ).move_to(bsi_formula)
        for b_over_a_index in (replaced_b_over_a_indices := [2, 3, 10, 11, 17, 18]):
            bsi_formula_replaced[b_over_a_index].set_color(ORANGE)

        self.play(bsi_formula.animate.become(bsi_formula_replaced))

        self.wait(.5)

        # -- Replace b / a with b / 2a in binomial square identity

        # Separate denominators from the fractions
        # Make multiplying 2 phantom so TransformMatchingShapes doesn't copy it to the new denominators
        two_copy = bsi_formula[8].copy()
        bsi_formula.become(
            MathTex(
                r"\bigl(x +", START_G, "b", r"\over", "{a}", END_G, r"\bigr)^2 =", "x^2", "+", r"\phantom{2}", START_G, "{b}",
                r"\over", "{a}", END_G, "x", "+", r"\bigl(", START_G, "{{b}}", r"\over", "{a}", END_G, r"\bigr)", "^2"
            ).move_to(bsi_formula)
        )
        for start, end in [(1, 5), (10, 14), (18, 22)]:
            bsi_formula[start:end].set_color(ORANGE)

        bsi_formula_replaced = MathTex(
            r"\bigl(x +", START_G, "b", r"\over {2a}", END_G, r"\bigr)^2 =", "x^2", "+", "2", START_G, "b", r"\over {2a}",
            END_G, "x", "+", r"\bigl(", START_G, "b", r"\over {2a}", END_G, r"\bigr)", "^2"
        ).move_to(bsi_formula)
        for b_over_a_index in replaced_b_over_a_indices:
            bsi_formula_replaced[b_over_a_index].set_color(YELLOW_E)

        two_final = bsi_formula_replaced[8]

        self.play(
            # Separate it in two transformations so initial parentheses aren't copied to the final ones
            TransformMatchingShapes(bsi_formula[0], replaced := bsi_formula_replaced[0]),
            TransformMatchingShapes(bsi_formula[1:], replaced1 := bsi_formula_replaced[1:]),

            Transform(two_copy, two_final)
        )

        bsi_formula_replaced = MathTex(
            r"\bigl(x +", START_G, "b", r"\over {2a}", END_G, r"\bigr)^2 =", "x^2", "+", r"\phantom{2}", START_G,
            "b", r"\over {2a}", END_G, "x", "+", r"\bigl(", START_G, "b", r"\over {2a}", END_G, r"\bigr)", "^2"
        ).move_to(bsi_formula)
        for start, end in [(1, 5), (9, 13), (16, 20)]:
            bsi_formula_replaced[start:end].set_color(YELLOW_E)

        self.remove(replaced, replaced1)
        self.add(bsi_formula.become(bsi_formula_replaced))

        self.wait(1)

        # -- Cancel twos in 2(b / 2a), in binomial square identity

        bsi_formula_replaced = MathTex(
            r"\bigl(x +", START_G, "b", r"\over", "{2a}", END_G, r"\bigr)^2 =", "x^2", "+", START_G, "b",
            r"\over", "{a}", END_G, "x", "+", r"\bigl(", START_G, "b", r"\over", "{2a}", END_G, r"\bigr)",
            "^2"
        ).move_to(bsi_formula)

        bsi_formula_replaced[1:6].set_color(YELLOW_E)
        bsi_formula_replaced[9:14].set_color(ORANGE)
        bsi_formula_replaced[17:22].set_color(YELLOW_E)

        denominator_copies = [bsi_formula_replaced[index].copy() for index in [4, 12, 20]]
        for denominator in denominator_copies:
            denominator.shift(.1 * DOWN)

        bsi_formula_replaced1 = MathTex(
            r"\bigl(x +", START_G, "b", r"\over \phantom{{2a}}", END_G, r"\bigr)^2 =", "x^2", "+", START_G, "b",
            r"\over \phantom{{a}}", END_G, "x", "+", r"\bigl(", START_G, "b", r"\over \phantom{{2a}}", END_G, r"\bigr)", "^2"
        ).move_to(bsi_formula)

        bsi_formula_replaced1[1:5].set_color(YELLOW_E)
        bsi_formula_replaced1[9:11].set_color(ORANGE)
        bsi_formula_replaced1[16:18].set_color(YELLOW_E)

        self.play(
            FadeIn(*denominator_copies, run_time=.75),
            FadeOut(two_copy, run_time=.75),
            TransformMatchingShapes(bsi_formula, bsi_formula_replaced1)
        )

        self.remove(*denominator_copies, bsi_formula_replaced1)
        self.add(bsi_formula.become(bsi_formula_replaced).shift(.1 * DOWN))

        # -- (b / 2a)² to left hand of binomial square identity

        bsi_formula = derive_equation(self, bsi_formula, [
            DerivationStep( # Reformat TeX
                r"\bigl(x +", (rf"{START_G} b \over 2a {END_G}", YELLOW_E), r"\bigr)^2", "=",
                "x^2 +", (rf"{START_G} b \over a {END_G}", ORANGE), "x",
                "+", r"{\bigl(}", (rf"{START_G} b \over 2a {END_G}", YELLOW_E), r"\bigr)^2",
                delay=0, transition_duration=.25, transform_type=FadeTransform
            ),
            DerivationStep( # Add -(b / a)² to both hands
                r"\bigl(x +", (rf"{START_G} b \over 2a {END_G}", YELLOW_E), r"\bigr)^2",
                "-", r"\bigl(", (rf"{{{START_G} b \over 2a {END_G}}}", YELLOW_E), r"{\bigr)^2}", "=",
                "x^2 +", (rf"{START_G} b \over a {END_G}", ORANGE), "x"
                "+", r"{\bigl(}", (rf"{START_G} b \over 2a {END_G}", YELLOW_E), r"\bigr)^2",
                "-", r"{\bigl(}", (rf"{{{{{START_G} b \over 2a {END_G}}}}}", YELLOW_E), r"{{\bigr)^2}}",
                delay=.75, transition_duration=1.25
            ),
            DerivationStep( # Color cancelling terms in red
                r"\bigl(x +", (rf"{START_G} b \over 2a {END_G}", YELLOW_E), r"\bigr)^2",
                "-", r"\bigl(", (rf"{{{START_G} b \over 2a {END_G}}}", YELLOW_E), r"{\bigr)^2}", "=",
                "x^2 +", (rf"{START_G} b \over a {END_G}", ORANGE), "x"
                "+", r"{\bigl(}", rf"{START_G} b \over 2a {END_G}", r"\bigr)^2",
                "-", r"{\bigl(}", rf"{{{{{START_G} b \over 2a {END_G}}}}}", r"{{\bigr)^2}}",
                on_build=lambda tex: tex[11:].set_color(RED_C),
                rate_func=ease_out_sine, transition_duration=.5
            ),
            DerivationStep( # Remove cancelling terms
                r"\bigl(x +", (rf"{START_G} b \over 2a {END_G}", YELLOW_E), r"\bigr)^2",
                "-", r"\bigl(", (rf"{{{START_G} b \over 2a {END_G}}}", YELLOW_E), r"\bigr)^2", "=",
                "x^2 +", (rf"{START_G} b \over a {END_G}", ORANGE), "x",
                delay=.5
            )
        ])

        # -- Left hand of binomial square identity to quadratic equation

        self.wait(.5)
        self.play(
            bsi_formula[:7].animate.set_color(GREEN),
            bsi_formula[8:].animate.set_color(MOROCCAN_BLUE),
            equation[:7].animate.set_color(MOROCCAN_BLUE),
            run_time=1.5, rate_func=ease_in_cubic
        )

        equation = derive_equation(self, equation, [
            DerivationStep(
                r"\bigl(x +", (rf"{START_G} b \over 2a {END_G}", YELLOW_E), r"\bigr)^2",
                "-", r"\bigl(", (rf"{{{START_G} b \over 2a {END_G}}}", YELLOW_E), r"\bigr)^2",
                "+", START_G, "c", r"\over {a}", END_G, START_G, "=", END_G, "0",
                on_build=lambda tex: tex[:7].set_color(GREEN),
                delay = 1.5, transform_type=TransformMatchingShapes
            )
        ])

        # -- Fade out binomial square identity, equation back to focus

        self.wait(1.5)
        self.play(
            LaggedStart(
                FadeOut(bsi_formula),
                equation.animate.shift(2 * DOWN) \
                    .set_color(WHITE),
                lag_ratio=.5
            )
        )

        self.wait(1.5)