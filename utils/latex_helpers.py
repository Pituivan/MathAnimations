from manim import MathTex, TransformMatchingTex, Succession


def derive_equation(base_equation: MathTex, steps: list[tuple[MathTex, float] | MathTex]) -> Succession:
    """
    Generates a sequence of animations representing a step-by-step equation derivation.

    Args:
        base_equation (MathTex):
            The initial equation from which the derivation begins.

        steps (list[tuple[MathTex, float] | MathTex]):
            A list of the successive steps of the mathematical derivation animation to be returned.

            Each step may be a tuple of the form (MathTex, float), where:
                - The MathTex represents the resulting expression after the derivation step.
                - The float represents the duration (in seconds) of the transition from the previous step to this one.

            Or, alternatively, a single MathTex, in which case the transition duration is 1.
    """

    if len(steps) == 0:
        return Succession()

    animations = []

    current = base_equation
    for next_step in steps:
        if isinstance(next_step, tuple):
            next_step, duration = next_step
        else:
            duration = 1

        animations.append(TransformMatchingTex(current, next_step, run_time=duration))

        current = next_step

    return Succession(*animations)