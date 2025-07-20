# ChessBot Documentation

Welcome to the ChessBot documentation! This document provides comprehensive information about the chess bot implementation, its architecture, and how to use it.

## Table of Contents

- [Installation](installation.md) - How to install and set up ChessBot
- [User Guide](user_guide.md) - How to use ChessBot
- [API Reference](api_reference.md) - Detailed API documentation
- [Architecture](architecture.md) - System architecture and design decisions
- [Development](development.md) - Development guidelines and contributing
- [Examples](examples.md) - Code examples and use cases

## Quick Start

```python
from chessbot import ChessBot

# Create a chess bot
bot = ChessBot(engine_depth=3)

# Play a game
bot.play_game()
```

## Features

- **Chess Engine**: Implements minimax algorithm with alpha-beta pruning
- **Move Validation**: Comprehensive move validation using python-chess
- **Game Management**: Full game state management and end-game detection
- **Interactive Play**: Command-line interface for playing against the engine
- **Extensible**: Modular design for easy extension and customization

## Dependencies

- `python-chess`: Chess library for move validation and board representation
- `pytest`: Testing framework
- `ruff`: Code linting and formatting

## License

MIT License - see LICENSE file for details. 