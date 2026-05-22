# Project Information for Agents

This project uses [Manim Community](https://www.manim.community/) to create mathematical animations.

## Build and Configuration

### Environment Setup
- The project uses a Python virtual environment located in `.venv/`.
- **Manim version**: `v0.20.1` (Community Edition).
- **Dependencies**: Manim requires system-level dependencies like `ffmpeg`, `texlive` (for LaTeX), and `sox`.

### Helper Scripts
- `manim-run.sh`: A shell script to run a scene.
  - *Note*: Script name (ignoring `.py` suffix) and scene name must match.
  - *Note 2*: Ensure it uses the virtual environment's Python (`.venv/bin/python`) or that the virtual environment is activated.

## Testing

Since this is an animation project, "testing" primarily involves rendering scenes to verify visual correctness.

Given that that's fundamentally a visual task, validation should be performed by a human, so the AI should prompt the user to review and confirm whether the results are correct instead of manually testing by itself, unless stated otherwise by the user.

## Additional Development Information

### Code Style and Patterns
- **Favor Factory Methods**: The project often uses internal factory methods for consistent styling of labels and TeX elements (e.g., `_label_factory`, `_math_tex_factory` in `TrigonometricRadios.py`). This way, we avoid repeating initialization code over and over again.
- **Color Palettes**: By default, stick to Manim's built-in color constants (e.g., `YELLOW_E`, `GREEN_E`). However, other colors gotten by specific hex codes may be used if requested by the user.

### Scene Organization
All scenes must be broken into logical chunks of code within the construct method, which should be organized as follows:
```text
# --- Logical Section (high-level domain / feature area)
# -- Module (cohesive sub-area within the section)
# - Submodule (specific component or responsibility within the module)
# Inline comments (short explanations for the next line or a small block)
```
