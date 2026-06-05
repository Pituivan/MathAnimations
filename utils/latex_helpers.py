from manim import Scene, MathTex, TransformMatchingTex
from manim.animation.transform_matching_parts import TransformMatchingAbstractBase


START_G = r"\left."
END_G = r"\right."


class DerivationStep:
    def __init__(self, *tex_strings: str, transition_duration: float = 1, delay: float = 0,
                 transform_type: type[TransformMatchingAbstractBase] = TransformMatchingTex):
        """
        Parameters:
            *tex_strings (str):
                A series of LaTeX strings that form the resulting MathTex expression.

            transition_duration (float, optional):
                Duration of the transition from the previous step to this one.

            delay (float, optional):
                Delay before performing the transition from the previous step to this one.
        """

        self.tex = MathTex(*tex_strings)
        self.transition_duration = transition_duration
        self.delay = delay
        self.transform_type = transform_type

def derive_equation(scene: Scene, base_equation: MathTex, steps: list[DerivationStep]) -> MathTex:
    """
    Returns:
        MathTex:
            The final equation after all derivation steps have been applied.
    """

    current_tex = base_equation
    for next_step in steps:
        if next_step.delay: scene.wait(next_step.delay)
        scene.play(next_step.transform_type(
            current_tex, next_step.tex,
            run_time=next_step.transition_duration
        ))

        current_tex = next_step.tex

    return current_tex