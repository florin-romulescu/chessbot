# ChessBot

A powerful Python chess bot built with the python-chess library, featuring a complete chess engine with minimax algorithm and interactive gameplay.

## 🎯 Features

- **Complete Chess Engine**: Implements minimax algorithm with alpha-beta pruning
- **Interactive Play**: Command-line interface for playing against the engine
- **Move Validation**: Comprehensive move validation using python-chess
- **Game Management**: Full game state management and end-game detection
- **Extensible Design**: Modular architecture for easy customization
- **Comprehensive Testing**: Full test suite with coverage reporting

## 🚀 Quick Start

```bash
# Install the package
uv sync

# Play a game
uv run python -m chessbot.main
```

## 📖 Documentation

- **[Installation Guide](getting-started/installation.md)** - How to install and set up ChessBot
- **[Quick Start](getting-started/quickstart.md)** - Get up and running in minutes
- **[User Guide](user-guide/basic-usage.md)** - Learn how to use ChessBot effectively
- **[API Reference](api/chessbot.md)** - Complete API documentation

## 🎮 Example Usage

```python
from chessbot import ChessBot

# Create a chess bot
bot = ChessBot(engine_depth=3)

# Play a complete game
bot.play_game()
```

## 🏗️ Architecture

ChessBot is built with a modular architecture:

- **`ChessBot`**: Main orchestrator class
- **`ChessBoard`**: Board state management
- **`ChessEngine`**: Move evaluation and selection
- **`utils`**: Helper functions for moves and notation

## 🧪 Testing

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/chessbot
```

## 📦 Installation

```bash
# Install with uv
uv sync

# Install development dependencies
uv sync --extra dev
```

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](development/contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/yourusername/chessbot/blob/main/LICENSE) file for details.

---

<div align="center">

**Ready to play chess?** [Get started now!](getting-started/quickstart.md)

</div> 