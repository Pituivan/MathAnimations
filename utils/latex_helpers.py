from manim import Scene, MathTex, ManimColor, Transform, TransformMatchingTex
from manim.animation.transform_matching_parts import TransformMatchingAbstractBase
from typing import Callable


START_G = r"\left."
END_G = r"\right."


class DerivationStep:
    default_transform_type: type[Transform] | type[TransformMatchingAbstractBase] = TransformMatchingTex

    def __init__(self, *parts: str | tuple[str, ManimColor], transition_duration: float = 1, delay: float =1,
                 transform_type: type[Transform] | type[TransformMatchingAbstractBase] = default_transform_type,
                 rate_func: Callable[[float], float] = None,
                 on_build: Callable[[MathTex], None] = None):
        """
        Parameters:
            *parts (str | tuple[str, ManimColor]):
                A series of LaTeX strings that form the resulting MathTex expression. They may optionally define
                a custom color for their corresponding section in the expression when in the form of a tuple.

            transition_duration (float, optional):
                Duration of the transition from the previous step to this one.

            delay (float, optional):
                Delay before performing the transition from the previous step to this one.

            transform_type (type[Transform] | type[TransformMatchingAbstractBase], optional):
                Type of Transform animation that will be used as transitioning animation from the previous step to this one.

            rate_func (Callable[[float], float], optional):
                Easing function that will be applied to the Transform transition animation.

            on_build (Callable[[MathTex], None], optional):
                Callback called after the step is initialized and its corresponding TeX is built.
        """

        tex_strings = [
            part if isinstance(part, str) else part[0]
            for part in parts
        ]

        self.tex = MathTex(*tex_strings)
        self.transition_duration = transition_duration
        self.delay = delay
        self.transform_type = transform_type
        self.rate_func = rate_func

        for i, part in enumerate(parts):
            if isinstance(part, tuple):
                self.tex[i].set_color(part[1])

        if on_build: on_build(self.tex)


def derive_equation(scene: Scene, base_equation: MathTex, steps: list[DerivationStep]) -> MathTex:
    """
    Returns:
        MathTex:
            The final equation after all derivation steps have been applied.
    """

    current_tex = base_equation
    for next_step in steps:
        next_step.tex.move_to(current_tex)

        if next_step.delay: scene.wait(next_step.delay)
        scene.play(next_step.transform_type(
            current_tex, next_step.tex,
            run_time=next_step.transition_duration
        ))

        current_tex = next_step.tex

    return current_tex


def color_tex_by_ranges(tex: MathTex, color: ManimColor, *ranges: tuple[int | None, int | None]):
    for start, end in ranges:
        tex[start:end].set_color(color)