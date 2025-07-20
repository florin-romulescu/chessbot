# Examples

This page contains various examples of how to use ChessBot.

## Basic Examples

### Simple Game

```python
from chessbot import ChessBot

# Create and play a game
bot = ChessBot()
bot.play_game()
```

### Custom Engine Depth

```python
from chessbot import ChessBot

# Create a stronger engine
bot = ChessBot(engine_depth=5)
bot.play_game()
```

### Programmatic Moves

```python
from chessbot import ChessBot

bot = ChessBot()

# Make some moves
bot.make_move('e2e4')
bot.make_move('e7e5')
bot.make_move('g1f3')

# Get engine's response
engine_move = bot.get_best_move()
print(f"Engine plays: {engine_move}")
```

## Advanced Examples

### Position Analysis

```python
from chessbot import ChessBot
from chessbot.board import ChessBoard

# Set up a specific position
custom_fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
board = ChessBoard(custom_fen)

# Create bot with this position
bot = ChessBot()
bot.board = board

# Analyze the position
best_move = bot.get_best_move()
print(f"Best move: {best_move}")
```

### Board Operations

```python
from chessbot.board import ChessBoard

board = ChessBoard()

# Check game state
print(f"Turn: {board.turn}")
print(f"In check: {board.is_check}")
print(f"Legal moves: {board.legal_moves[:5]}")

# Make moves
board.make_move('e2e4')
board.make_move('e7e5')

# Get FEN representation
print(f"FEN: {board.get_fen()}")
```

### Engine Analysis

```python
from chessbot.engine import ChessEngine
from chessbot.board import ChessBoard

engine = ChessEngine(depth=3)
board = ChessBoard()

# Evaluate position
evaluation = engine.evaluate_position(board._board)
print(f"Evaluation: {evaluation}")

# Get best move
best_move = engine.get_best_move(board)
print(f"Best move: {best_move}")
```

## Running Examples

You can run the included examples:

```bash
# Run the basic examples
uv run python examples/basic_usage.py

# Or run individual examples
uv run python -c "
from chessbot import ChessBot
bot = ChessBot()
bot.make_move('e2e4')
print(bot.board)
"
```

## More Examples

For more detailed examples, see:

- [Quick Start Guide](quickstart.md)
- [API Reference](../api/chessbot.md)
- [User Guide](../user-guide/basic-usage.md) 