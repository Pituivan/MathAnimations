from manim import MathTex, TransformMatchingTex, Wait, Animation
from typing import Generator


START_G = r"\left."
END_G = r"\right."


class DerivationStep:
    def __init__(self, *tex_strings: str, transition_duration: float = 1, delay: float = 0):
        """
        Parameters:
            *tex_strings (str):
                A series of LaTeX strings that form the resulting MathTex expression.

            transition_duration (float, optional):
                Duration of the transition from the previous step to this one.

            delay (float, optional):
                Delay before performing the transition from the previous step to this one.
        """

        self.tex_strings = tex_strings
        self.transition_duration = transition_duration
        self.delay = delay

    def build_tex(self) -> MathTex:
        return MathTex(*self.tex_strings)


def derive_equation(base_equation: MathTex, steps: list[DerivationStep]) -> Generator[Animation]:
    current_tex = base_equation
    for next_step in steps:
        next_tex = next_step.build_tex()
        yield Wait(next_step.delay)
        yield TransformMatchingTex(
            current_tex, next_tex,
            run_time=next_step.transition_duration
        )

        current_tex = next_tex