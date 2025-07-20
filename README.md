# ChessBot

[![CI](https://github.com/florin-romulescu/chessbot/workflows/CI/badge.svg)](https://github.com/florin-romulescu/chessbot/actions/workflows/ci.yml)
[![Quick Check](https://github.com/florin-romulescu/chessbot/workflows/Quick%20Check/badge.svg)](https://github.com/florin-romulescu/chessbot/actions/workflows/quick-check.yml)
[![Codecov](https://codecov.io/gh/florin-romulescu/chessbot/branch/main/graph/badge.svg)](https://codecov.io/gh/florin-romulescu/chessbot)

A Python chess bot built using the python-chess library.

## Installation

```bash
# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Run the chess bot
python -m chessbot.main

# Or use the installed script
chessbot
```

### UCI Engine (XBoard, Arena, etc.)

```bash
# Run as UCI engine
uv run chessbot-uci

# Run advanced UCI engine with better time management
uv run chessbot-uci-advanced

# Or run directly
python -m chessbot.uci_engine
python -m chessbot.uci_engine_advanced
```

See the [UCI Integration Guide](docs/getting-started/uci-integration.md) for detailed setup instructions.

## Development

```bash
# Run tests
pytest

# Run linting
ruff check .

# Format code
ruff format .

# Type checking
mypy src/
```

## CI/CD

This project uses GitHub Actions for continuous integration:

- **CI**: Full test suite across Python 3.8-3.12, linting, type checking, and documentation building
- **Quick Check**: Fast feedback on pull requests with essential checks
- **Documentation**: Automatic deployment to GitHub Pages on main branch

### Setting up GitHub Pages

To enable automatic documentation deployment:

1. Go to your repository Settings → Pages
2. Set Source to "GitHub Actions"
3. The documentation will be automatically deployed when you push to the main branch

The documentation will be available at: `https://yourusername.github.io/chessbot/`

### Local Development

```bash
# Install development dependencies
uv sync --extra dev

# Run all checks locally
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
uv run pytest
```

## Project Structure

```
chessbot/
├── src/
│   └── chessbot/
│       ├── __init__.py
│       ├── main.py
│       ├── engine/
│       ├── board/
│       └── utils/
├── tests/
├── docs/
├── pyproject.yaml
└── README.md
```

## License

MIT License 