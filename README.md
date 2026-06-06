This repository is a collection of mathematical animations I create using Manim Community, 
along with some structure and utilities for making my life easier when creating new animations. 

## Project Structure

All animations are implemented as independent Manim scenes within Python files. 
They're self-contained and don't depend on other animation files, but may import helpers from `utils/` package.

Each animation resides in its own file under the `animations/` directory. 
By convention, the animation class and file names **must** match 
(e.g., class `QuadraticFormulaDerivation` is defined in `QuadraticFormulaDerivation.py`, and that Python file should not define any other high-level member).

## Workflow

This repository is designed with a very specific workflow in mind. You create a new Python file under `animations/` for your animation,
define a class which inherits from Manim's `Scene` named the same as the script, and start coding.

When you need to test your code, you'll run `./manim-run.sh <your-file-path.py>` in your terminal, optionally adding flags for specific needs,
and a video of your animation will be rendered and opened. If something breaks, check Manim's output in your console.

### `manim-run.sh` optional flags:
- `--quality <lvl>`: Sets render quality (0 = low, 1 = medium, 2 = high). **Default is low**.
- `--fps <number>`: Sets render frames per second. Default is 60.
- `--background_color <value>`: Sets the camera's background color, which may be expressed as a Manim keyword or a hexadecimal value (preceded by a `#`).

Once push your changes, a check will be run on your last commit, which will test if your animation can be rendered without problems.
If you modified `utils/`, all animations will be re-validated, so you'll know if you colaterally broke a previously working animation.

## Contributing

If you have an idea for a mathematical animation you'd like to see, you think one of my animations could be improved, 
or there's anything else you'd like to suggest, please open an issue!

Also, if you'd like to contribute with an animation created by yourself, feel free to open or draft a pull request! 
I'd love to see more people bringing mathematical notions to life.

There are no strict style guidelines in this project, as it's more of a learning experience and more focused on the results.
Check the ***Code Style and Patterns*** section in [project information for agents](AGENTS.md) if you want to see what code should look like in this project,
but keep in mind that they're still just guidelines for AIs, not for full-reasoning beings — here, common sense is above any ruleset.

Given that animations are fully self-contained and won't be reutilized anywhere, they don't need to be carefully written.
However, if you're writing helpers under `utils/`, please make your code clean, understandable and documented.
