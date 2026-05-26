# Project Information for Agents

This project uses [Manim Community](https://www.manim.community/) to create mathematical animations.

## Build and Configuration

### Environment Setup
- The project uses a Python virtual environment located in `.venv/`.
- **Manim version**: `v0.20.1` (Community Edition).

## Testing

Since this is an animation project, "testing" primarily involves rendering scenes to verify visual correctness.

Given that that's fundamentally a visual task, a human should be the one performing validation. 
Thus, the AI agent should prompt the user to review and confirm whether the results are correct instead
of manually testing by itself, unless stated otherwise by the human.

## Code Style and Patterns

### Scene Organization
All scenes must be broken into logical chunks of code within the `construct` method, using header comments to
clearly separate each section of code, as shown below:
```text
# --- Header 1 (high-level section)
# -- Header 2 (sub-section)
# Inline comments (short explanations for the next line or a small block)
```

### Vector Construction Convention
When using coordinates or positions in Manim, do not construct vectors directly using `np.array([x, y, z])`.
Instead, using directional vectors (`UP`, `DOWN`, `LEFT`, `RIGHT`, `IN`, `OUT`) scaled by a coefficient placed on
the left side of the expression. For example, `(3, -1)` would be written as `3 * UP + DOWN`.

### Other Style Guidelines
- **Favor Factory Methods**: The project often uses internal factory methods for consistent styling of labels
  and TeX elements (e.g., `_label_factory`, `_math_tex_factory` in `TrigonometricRadios.py`). This way, we avoid
  repeating initialization code over and over again.
- Write decimal numbers without a leading zero for values between 0 and 1 (e.g., `.5` instead of `0.5`).
- Avoid redundant parameter assignments (e.g., `color=WHITE` or `run_time=1` when these are the default values).
  The only exception to this rule is the time in waiting commands: use`self.wait(1)`, not `self.wait()`.

