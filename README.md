# ChessBot

A Python chess bot built using the python-chess library.

## Installation

```bash
# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Usage

```bash
# Run the chess bot
python -m chessbot.main

# Or use the installed script
chessbot
```

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