# Installation

This guide will help you install ChessBot and set up your development environment.

## Prerequisites

- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`

## Installing with uv (Recommended)

### 1. Install uv

If you don't have `uv` installed, install it first:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repository

```bash
git clone https://github.com/yourusername/chessbot.git
cd chessbot
```

### 3. Install dependencies

```bash
# Install core dependencies
uv sync

# Install development dependencies (optional)
uv sync --extra dev
```

### 4. Verify installation

```bash
# Run tests to verify everything works
uv run pytest

# Try running the chess bot
uv run python -m chessbot.main
```

## Installing with pip

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/chessbot.git
cd chessbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Development Setup

### 1. Install all development tools

```bash
uv sync --extra dev
```

This installs:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `ruff` - Linting and formatting
- `black` - Code formatting
- `mypy` - Type checking
- `mkdocs` - Documentation
- `mkdocs-material` - Documentation theme

### 2. Configure your editor

For the best development experience, configure your editor to use the virtual environment:

- **VS Code**: Select the Python interpreter from `.venv/bin/python`
- **PyCharm**: Set the project interpreter to `.venv/bin/python`
- **Vim/Neovim**: Use a Python LSP that respects the virtual environment

### 3. Pre-commit hooks (Optional)

Set up pre-commit hooks for automatic code quality checks:

```bash
# Install pre-commit
uv add pre-commit --dev

# Set up the hooks
uv run pre-commit install
```

## Troubleshooting

### Common Issues

#### Import Error: No module named 'chess'

This means the `python-chess` dependency isn't installed correctly. Try:

```bash
uv sync --reinstall
```

#### Permission Errors

If you encounter permission errors on Linux/macOS:

```bash
# Make sure you own the directory
sudo chown -R $USER:$USER .

# Or install with user permissions
uv sync --user
```

#### Python Version Issues

Make sure you're using Python 3.8 or higher:

```bash
python --version
```

If you need to use a different Python version:

```bash
# With uv
uv sync --python 3.11

# With pip
python3.11 -m venv venv
```

### Getting Help

If you encounter any issues:

1. Check the [GitHub Issues](https://github.com/yourusername/chessbot/issues)
2. Create a new issue with details about your problem
3. Include your Python version, operating system, and error messages

## Next Steps

Once installation is complete, you can:

- [Quick Start Guide](quickstart.md) - Learn how to use ChessBot
- [User Guide](../user-guide/basic-usage.md) - Detailed usage instructions
- [API Reference](../api/chessbot.md) - Complete API documentation 