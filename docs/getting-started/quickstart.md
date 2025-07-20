# Quick Start

Get up and running with ChessBot in minutes!

## 🚀 Basic Usage

### 1. Create a Chess Bot

```python
from chessbot import ChessBot

# Create a chess bot with default settings
bot = ChessBot()

# Or customize the engine depth
bot = ChessBot(engine_depth=4)
```

### 2. Play a Game

```python
# Start an interactive game
bot.play_game()
```

This will start a command-line chess game where you can play against the engine.

### 3. Make Individual Moves

```python
from chessbot import ChessBot

bot = ChessBot()

# Make a move (UCI format)
success = bot.make_move('e2e4')
if success:
    print("Move successful!")
else:
    print("Invalid move!")

# Get the engine's best move
engine_move = bot.get_best_move()
print(f"Engine suggests: {engine_move}")
```

## 🎮 Interactive Game Example

When you run `bot.play_game()`, you'll see something like this:

```
Welcome to ChessBot!
Enter moves in UCI format (e.g., 'e2e4')
Type 'quit' to exit

  r n b q k b n r
  p p p p p p p p
  . . . . . . . .
  . . . . . . . .
  . . . . . . . .
  . . . . . . . .
  P P P P P P P P
  R N B Q K B N R

Your move: e2e4
Engine is thinking...
Engine plays: e7e5

  r n b q k b n r
  p p p p . p p p
  . . . . . . . .
  . . . . p . . .
  . . . . P . . .
  . . . . . . . .
  P P P P . P P P
  R N B Q K B N R

Your move: g1f3
```

## 📋 Move Notation

ChessBot uses **UCI (Universal Chess Interface)** notation for moves:

- **Pawn moves**: `e2e4`, `d2d4`
- **Piece moves**: `g1f3`, `b1c3`
- **Captures**: `e4d5`, `f3e5`
- **Castling**: `e1g1` (kingside), `e1c1` (queenside)
- **Promotions**: `e7e8q` (promote to queen)

## ⚙️ Configuration Options

### Engine Depth

Control how deeply the engine searches:

```python
# Shallow search (faster, weaker)
bot = ChessBot(engine_depth=2)

# Deep search (slower, stronger)
bot = ChessBot(engine_depth=5)
```

### Custom Starting Position

Start from a specific position using FEN notation:

```python
from chessbot.board import ChessBoard

# Create board with custom position
custom_fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
board = ChessBoard(custom_fen)
```

## 🔧 Advanced Usage

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

# Get board representation
print(board)
```

### Engine Analysis

```python
from chessbot.engine import ChessEngine

engine = ChessEngine(depth=3)
board = ChessBoard()

# Get best move
best_move = engine.get_best_move(board)
print(f"Best move: {best_move}")

# Evaluate position
evaluation = engine.evaluate_position(board._board)
print(f"Position evaluation: {evaluation}")
```

## 🧪 Testing Your Setup

Run the examples to verify everything works:

```bash
# Run the basic examples
uv run python examples/basic_usage.py

# Run tests
uv run pytest

# Start a game
uv run python -m chessbot.main
```

## 🎯 Next Steps

Now that you're up and running:

- **[User Guide](../user-guide/basic-usage.md)** - Learn more advanced features
- **[API Reference](../api/chessbot.md)** - Complete API documentation
- **[Examples](../getting-started/examples.md)** - More code examples
- **[Configuration](../user-guide/configuration.md)** - Advanced configuration options

## 🆘 Need Help?

If you encounter any issues:

1. Check the [Installation Guide](installation.md) for setup problems
2. Look at the [API Reference](../api/chessbot.md) for detailed documentation
3. Run the examples to see working code
4. Open an issue on GitHub with your problem

Happy chess playing! ♟️ 