from manim import (MathTex, TransformMatchingTex,
                   Wait, Succession)


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

        if tex_strings: self.tex = MathTex(*tex_strings)
        self.transition_duration = transition_duration
        self.delay = delay

def derive_equation(base_equation: MathTex, steps: list[DerivationStep]) -> Succession:
    if not steps:
        return Succession()

    animations = []

    current_step = DerivationStep()
    current_step.tex = base_equation
    for next_step in steps:
        animations.append(Wait(next_step.delay))
        animations.append(TransformMatchingTex(
            current_step.tex, next_step.tex,
            run_time=next_step.transition_duration
        ))

        current_step = next_step

    return Succession(*animations)