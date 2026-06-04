from manim import *
from utils.latex_helpers import (derive_equation, DerivationStep,
                                 START_G, END_G)


class QuadraticFormulaDerivation(Scene):
    def construct(self):
        # --- Title

        self.wait(1)

        self.play(
            Write(Text(
                "Derivation of the Quadratic Formula",
                font_size=36
            ).to_edge(UP).shift(DOWN)),
            run_time=1.25
        )

        self.wait(1)

        # --- Phase 1: Present the quadratic equation, then convert the left hand to monic form

        equation = MathTex("a", "x^2", "+", "b", "x", "+", "c", "=", "0")
        steps = [
            # We need to keep TeX groups separate so TransformMatchingTex animation doesn't turn into a fade.
            # Hence, we can't use \frac for fractions since they require grouped {numerator}{denominator} in a single TeX group.
            # We also can't use \over, since the = sign and the right side of the equation would fall into the denominator.
            # A feasible option is delimiting numerator and denominator with \left. and \right.

            # Alternate between a and {a} when it's not supposed to move between terms.

            DerivationStep(
                START_G, "a", "x^2", "+", "b", "x", "+", "c", r"\over a", END_G,
                START_G, "=", END_G,
                START_G, "0", r"\over a", END_G,
                delay=1
            ),
            DerivationStep(
                "x^2", "+", START_G, "b", r"\over {a}", END_G, "x", "+", START_G, "c", r"\over {a}", END_G,
                START_G, "=", END_G,
                "0",
                delay=.75, transition_duration=.75
            )
        ]

        self.play(Write(equation, run_time=1.5))
        equation = derive_equation(self, equation, steps)

        self.wait(1.5)