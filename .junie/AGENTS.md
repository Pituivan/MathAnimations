# Project Information for Agents

This project uses [Manim Community](https://www.manim.community/) to create mathematical animations.

## Build and Configuration

### Environment Setup
- The project uses a Python virtual environment located in `.venv/`.
- **Manim version**: `v0.20.1` (Community Edition).
- **Dependencies**: Manim requires system-level dependencies like `ffmpeg`, `texlive` (for LaTeX), and `sox`.

## Testing

Since this is an animation project, "testing" primarily involves rendering scenes to verify visual correctness.

Given that that's fundamentally a visual task, a human should be the one performing validation, so the AI should prompt the user to review and confirm whether the results are correct instead of manually testing by itself, unless stated otherwise by the user.

### Code Style and Patterns
- **Favor Factory Methods**: The project often uses internal factory methods for consistent styling of labels and TeX elements (e.g., `_label_factory`, `_math_tex_factory` in `TrigonometricRadios.py`). This way, we avoid repeating initialization code over and over again.
- **Color Palettes**: By default, stick to Manim's built-in color constants (e.g., `YELLOW_E`, `GREEN_E`). However, other colors gotten by specific hex codes may be used if requested by the user.
- Avoid redundant parameter assignments (e.g., `color=WHITE` or `run_time=1` when these are the default values). The only exception to this is the time in waiting commands: use`self.wait(1)`, not `self.wait()`.

## Scene Organization
All scenes must be broken into logical chunks of code within the construct method, and that will be carried out by using header comments, as follows:
```text
# --- Header 1 (high-level section)
# -- Header 2 (sub-section)
# Inline comments (short explanations for the next line or a small block)
```
