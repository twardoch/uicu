

## Project Overview

`uicu` is a Python package that aims to create a pythonic wrapper around PyICU, supplemented by fontTools.unicodedata. The goal is to provide a natural, performant API that exposes rich, well-documented objects integrating with Python's native Unicode handling while adding extensive Unicode functionality.

## Development Commands

### Environment Setup
```bash
# Install and use uv for package management
pip install uv
# Use hatch for development workflow
uv pip install hatch
```

### Common Development Tasks
```bash
# Activate development environment
hatch shell

# Run tests
hatch run test
python -m pytest

# Run tests with coverage
hatch run test-cov

# Run linting
hatch run lint

# Format code
hatch run format

# Run type checking
hatch run type-check

# After Python changes, run the full formatting pipeline:
fd -e py -x autoflake {}; fd -e py -x pyupgrade --py311-plus {}; fd -e py -x ruff check --output-format=github --fix --unsafe-fixes {}; fd -e py -x ruff format --respect-gitignore --target-version py311 {}; python -m pytest;
```

## Code Architecture

### Project Structure
- **src/uicu/**: Main package source (using src-layout)
  - `__init__.py`: Package initialization
  - `__version__.py`: Version management using hatch-vcs
  - `uicu.py`: Main module (currently skeleton)
- **tests/**: Test suite using pytest
- **pyproject.toml**: PEP 621 compliant project configuration

### Key Dependencies to Research
- **PyICU**: The main Unicode library to wrap
- **fontTools.unicodedata**: Supplementary Unicode data with writing system info

## Development Guidelines

### Python-Specific Rules
- Use `uv pip` instead of `pip`
- Always use `python -m` when running modules
- Use type hints in simple form (list, dict, | for unions)
- Add verbose loguru-based logging and debug-log
- For CLI scripts, use fire & rich libraries
- Scripts should start with `#!/usr/bin/env -S uv run -s`

### Code Quality Standards
- PEP 8 compliant (enforced by Ruff)
- Clear, imperative docstrings (PEP 257)
- Use f-strings for formatting
- Structural pattern matching where appropriate
- Maintain `this_file` comments at the top of each source file

### Development Workflow
1. Create/update `PLAN.md` with detailed flat plan using `[ ]` items
2. Identify important TODOs and update `TODO.md`
3. Implement changes incrementally
4. Update `CHANGELOG.md` after each round of changes
5. Update `README.md` to reflect changes
6. Run the formatting pipeline after Python changes

### Current Project Status
- Initial project structure created
- Main objective: Create pythonic wrapper around PyICU
- First task: Research and document APIs from fontTools.unicodedata and PyICU
- Implementation phase not yet started

## Testing Strategy
- pytest with coverage tracking
- Use pytest-xdist for parallel test execution
- pytest-benchmark for performance testing
- Maintain high test coverage for all new functionality

## Key Principles
- Iterate gradually, avoiding major changes
- Preserve existing code/structure unless necessary
- Write explanatory docstrings that explain what and WHY
- Handle failures gracefully with retries and fallbacks
- Focus on minimal viable increments
- Keep code simple and explicit (PEP 20)

# When you write code

- Iterate gradually, avoiding major changes
- Minimize confirmations and checks
- Preserve existing code/structure unless necessary
- Use constants over magic numbers
- Check for existing solutions in the codebase before starting
- Check often the coherence of the code you're writing with the rest of the code.
- Focus on minimal viable increments and ship early
- Write explanatory docstrings/comments that explain what and WHY this does, explain where and how the code is used/referred to elsewhere in the code
- Analyze code line-by-line
- Handle failures gracefully with retries, fallbacks, user guidance
- Address edge cases, validate assumptions, catch errors early
- Let the computer do the work, minimize user decisions
- Reduce cognitive load, beautify code
- Modularize repeated logic into concise, single-purpose functions
- Favor flat over nested structures
- Consistently keep, document, update and consult the holistic overview mental image of the codebase. 

## Keep track of paths

In each source file, maintain the up-to-date `this_file` record that shows the path of the current file relative to project root. Place the `this_file` record near the top of the file, as a comment after the shebangs, or in the YAML Markdown frontmatter.

## When you write Python

- Use `uv pip`, never `pip`
- Use `python -m` when running code
- PEP 8: Use consistent formatting and naming
- Write clear, descriptive names for functions and variables
- PEP 20: Keep code simple and explicit. Prioritize readability over cleverness
- Use type hints in their simplest form (list, dict, | for unions)
- PEP 257: Write clear, imperative docstrings
- Use f-strings. Use structural pattern matching where appropriate
- ALWAYS add "verbose" mode logugu-based logging, & debug-log
- For CLI Python scripts, use fire & rich, and start the script with

```
#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["PKG1", "PKG2"]
# ///
# this_file: PATH_TO_CURRENT_FILE
```

Work in rounds: 

- Create `PLAN.md` as a detailed flat plan with `[ ]` items. 
- Identify the most important TODO items, and create `TODO.md` with `[ ]` items. 
- Implement the changes. 
- Update `PLAN.md` and `TODO.md` as you go. 
- After each round of changes, update `CHANGELOG.md` with the changes.
- Update `README.md` to reflect the changes.

Ask before extending/refactoring existing code in a way that may add complexity or break things.

When you're finished, print "Wait, but" to go back, think & reflect, revise & improvement what you've done (but don't invent functionality freely). Repeat this. But stick to the goal of "minimal viable next version". Lead two experts: "Ideot" for creative, unorthodox ideas, and "Critin" to critique flawed thinking and moderate for balanced discussions. The three of you shall illuminate knowledge with concise, beautiful responses, process methodically for clear answers, collaborate step-by-step, sharing thoughts and adapting. If errors are found, step back and focus on accuracy and progress.

## After Python changes run:

```
fd -e py -x autoflake {}; fd -e py -x pyupgrade --py311-plus {}; fd -e py -x ruff check --output-format=github --fix --unsafe-fixes {}; fd -e py -x ruff format --respect-gitignore --target-version py311 {}; python -m pytest;
```

Be creative, diligent, critical, relentless & funny!

## Development Guidelines

- Only modify code directly relevant to the specific request. Avoid changing unrelated functionality.
- Never replace code with placeholders like `# ... rest of the processing ...`. Always include complete code.
- Break problems into smaller steps. Think through each step separately before implementing.
- Always provide a complete PLAN with REASONING based on evidence from code and logs before making changes.
- Explain your OBSERVATIONS clearly, then provide REASONING to identify the exact issue. Add console logs when needed to gather more information.


`uicu` is a specialized Python package that creates a Pythonic wrapper around PyICU with supplementary Unicode functionality from fontTools.unicodedata. The core business logic revolves around providing rich Unicode data manipulation capabilities through well-documented objects.

## Core Business Components

1. Unicode Data Processing (90)
- Custom wrapper around PyICU providing intuitive Unicode manipulation
- Integration with fontTools.unicodedata for writing system information
- Domain-specific data validation and transformation rules
Location: `src/uicu/uicu.py`

2. Supplementary Unicode Features (85)
- Extended Unicode functionality beyond Python's native capabilities
- Writing system detection and classification
- Custom normalization and decomposition rules
Location: `src/uicu/uicu.py`

3. Unicode Validation Framework (75)
- Custom validation rules for Unicode data integrity
- Error handling specific to Unicode processing
- Fallback mechanisms for unsupported characters
Location: `src/uicu/uicu.py`

## Integration Architecture

The package implements a layered approach to Unicode processing:

1. Base Layer: PyICU Integration
- Direct wrapping of PyICU functionality
- Custom error handling and retry logic
Location: `src/uicu/uicu.py`

2. Enhancement Layer: fontTools Integration
- Additional Unicode metadata and writing system support
- Custom data enrichment rules
Location: `src/uicu/uicu.py`

3. Application Layer: Pythonic Interface
- Natural Python API for Unicode operations
- Rich object model with extensive Unicode properties
Location: `src/uicu/uicu.py`

## Development Workflow

The project follows an iterative development approach with:
- Detailed planning in `PLAN.md`
- Task tracking in `TODO.md`
- Change documentation in `CHANGELOG.md`
- Updated documentation in `README.md`

$END$