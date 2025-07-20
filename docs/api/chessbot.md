# ChessBot API Reference

The main `ChessBot` class that orchestrates chess games.

## Class: `ChessBot`

The main chess bot class that manages the game state, handles moves, and coordinates between the board representation and the chess engine.

### Constructor

```python
ChessBot(engine_depth: int = 3)
```

**Parameters:**
- `engine_depth` (int): Search depth for the chess engine (default: 3)

**Example:**
```python
from chessbot import ChessBot

# Create with default depth
bot = ChessBot()

# Create with custom depth
bot = ChessBot(engine_depth=5)
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `board` | `ChessBoard` | The chess board instance |
| `engine` | `ChessEngine` | The chess engine instance |
| `game_over` | `bool` | Whether the game has ended |

### Methods

#### `make_move(move_uci: str) -> bool`

Make a move on the chess board.

**Parameters:**
- `move_uci` (str): Move in UCI format (e.g., 'e2e4')

**Returns:**
- `bool`: True if the move was legal and executed, False otherwise

**Example:**
```python
bot = ChessBot()

# Make a legal move
success = bot.make_move('e2e4')
if success:
    print("Move successful!")
else:
    print("Invalid move!")

# Try an invalid move
success = bot.make_move('e2e5')  # Invalid pawn move
print(success)  # False
```

#### `get_best_move() -> Optional[str]`

Get the best move from the chess engine.

**Returns:**
- `Optional[str]`: The best move in UCI format, or None if no move is available

**Example:**
```python
bot = ChessBot()

# Get engine's best move
best_move = bot.get_best_move()
if best_move:
    print(f"Engine suggests: {best_move}")
    bot.make_move(best_move)
else:
    print("No moves available")
```

#### `play_game() -> None`

Play a complete chess game against the engine.

This method runs an interactive chess game where the user plays against the chess engine. The game continues until checkmate, stalemate, or the user quits.

**Example:**
```python
bot = ChessBot()
bot.play_game()
```

**Game Flow:**
1. Displays the current board position
2. Prompts for user input (UCI move format)
3. Validates and executes the user's move
4. Calculates and executes the engine's response
5. Checks for game end conditions
6. Repeats until game ends

## Usage Examples

### Basic Game Setup

```python
from chessbot import ChessBot

# Create a chess bot
bot = ChessBot(engine_depth=3)

# Play a complete game
bot.play_game()
```

### Programmatic Game Control

```python
from chessbot import ChessBot

bot = ChessBot()

# Make opening moves
bot.make_move('e2e4')
bot.make_move('e7e5')
bot.make_move('g1f3')

# Get engine's response
engine_move = bot.get_best_move()
print(f"Engine plays: {engine_move}")

# Check game state
print(f"Game over: {bot.game_over}")
print(f"Current turn: {bot.board.turn}")
```

### Custom Game Analysis

```python
from chessbot import ChessBot

bot = ChessBot(engine_depth=4)

# Set up a specific position
custom_fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
bot.board.set_fen(custom_fen)

# Analyze the position
best_move = bot.get_best_move()
print(f"Best move in this position: {best_move}")

# Make the move and continue
if best_move:
    bot.make_move(best_move)
```

### Error Handling

```python
from chessbot import ChessBot

bot = ChessBot()

try:
    # Handle invalid moves gracefully
    if not bot.make_move('invalid'):
        print("Invalid move, please try again")
    
    # Handle game end conditions
    if bot.game_over:
        print("Game has ended")
        return
    
    # Get engine move safely
    engine_move = bot.get_best_move()
    if engine_move is None:
        print("No moves available for engine")
    else:
        bot.make_move(engine_move)
        
except Exception as e:
    print(f"Error during game: {e}")
```

## Integration with Other Components

### Using with ChessBoard

```python
from chessbot import ChessBot
from chessbot.board import ChessBoard

bot = ChessBot()

# Access the board directly
board = bot.board
print(f"Current FEN: {board.get_fen()}")
print(f"Legal moves: {board.legal_moves}")

# Check game state
if board.is_checkmate:
    print("Checkmate!")
elif board.is_stalemate:
    print("Stalemate!")
elif board.is_insufficient_material:
    print("Insufficient material!")
```

### Using with ChessEngine

```python
from chessbot import ChessBot
from chessbot.engine import ChessEngine

bot = ChessBot()

# Access the engine directly
engine = bot.engine
engine.set_depth(5)  # Change search depth

# Evaluate current position
evaluation = engine.evaluate_position(bot.board._board)
print(f"Position evaluation: {evaluation}")
```

## Performance Considerations

- **Engine Depth**: Higher depth values provide stronger play but take longer to calculate
- **Memory Usage**: The engine uses minimax with alpha-beta pruning for efficient search
- **Move Validation**: All moves are validated using the python-chess library for correctness

## Thread Safety

The `ChessBot` class is not thread-safe. If you need to use it in a multi-threaded environment, ensure proper synchronization. 