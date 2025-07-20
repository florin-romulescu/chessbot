# API Reference

This document provides detailed API documentation for all classes and functions in the ChessBot library.

## ChessBot

The main chess bot class that orchestrates the game.

### Constructor

```python
ChessBot(engine_depth: int = 3)
```

**Parameters:**
- `engine_depth` (int): Search depth for the chess engine (default: 3)

### Methods

#### `make_move(move_uci: str) -> bool`

Make a move on the chess board.

**Parameters:**
- `move_uci` (str): Move in UCI format (e.g., 'e2e4')

**Returns:**
- `bool`: True if the move was legal and executed, False otherwise

#### `get_best_move() -> Optional[str]`

Get the best move from the chess engine.

**Returns:**
- `Optional[str]`: The best move in UCI format, or None if no move is available

#### `play_game() -> None`

Play a complete chess game against the engine.

This method runs an interactive chess game where the user plays against the chess engine.

## ChessBoard

Chess board representation using the python-chess library.

### Constructor

```python
ChessBoard(fen: str = chess.STARTING_FEN)
```

**Parameters:**
- `fen` (str): FEN string representing the initial board position

### Properties

#### `turn: str`

Get the current player's turn.

**Returns:**
- `str`: 'w' for white's turn, 'b' for black's turn

#### `is_check: bool`

Check if the current player is in check.

**Returns:**
- `bool`: True if the current player is in check

#### `is_checkmate: bool`

Check if the current player is checkmated.

**Returns:**
- `bool`: True if the current player is checkmated

#### `is_stalemate: bool`

Check if the current position is a stalemate.

**Returns:**
- `bool`: True if the position is a stalemate

#### `is_insufficient_material: bool`

Check if there is insufficient material for checkmate.

**Returns:**
- `bool`: True if there is insufficient material

#### `legal_moves: List[str]`

Get all legal moves in UCI format.

**Returns:**
- `List[str]`: List of legal moves as UCI strings

### Methods

#### `is_valid_move(move_uci: str) -> bool`

Check if a move is legal.

**Parameters:**
- `move_uci` (str): Move in UCI format

**Returns:**
- `bool`: True if the move is legal

#### `make_move(move_uci: str) -> bool`

Make a move on the board.

**Parameters:**
- `move_uci` (str): Move in UCI format

**Returns:**
- `bool`: True if the move was successfully made

#### `undo_move() -> None`

Undo the last move made on the board.

#### `get_fen() -> str`

Get the current board position in FEN format.

**Returns:**
- `str`: FEN string representing the current position

#### `set_fen(fen: str) -> bool`

Set the board position from a FEN string.

**Parameters:**
- `fen` (str): FEN string representing the desired position

**Returns:**
- `bool`: True if the FEN was valid and set successfully

#### `get_piece_at(square: str) -> Optional[str]`

Get the piece at a given square.

**Parameters:**
- `square` (str): Square in algebraic notation (e.g., 'e4')

**Returns:**
- `Optional[str]`: Piece symbol or None if square is empty

## ChessEngine

Chess engine that evaluates positions and selects the best moves.

### Constructor

```python
ChessEngine(depth: int = 3)
```

**Parameters:**
- `depth` (int): Search depth for the minimax algorithm

### Class Variables

#### `PIECE_VALUES: Dict[int, int]`

Piece values for material evaluation:

```python
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}
```

### Methods

#### `evaluate_position(board: chess.Board) -> int`

Evaluate a chess position.

**Parameters:**
- `board` (chess.Board): Chess board to evaluate

**Returns:**
- `int`: Position evaluation score (positive favors white, negative favors black)

#### `get_best_move(board) -> Optional[str]`

Get the best move for the current position.

**Parameters:**
- `board`: ChessBoard instance representing the current position

**Returns:**
- `Optional[str]`: Best move in UCI format, or None if no moves available

#### `get_move_with_time_limit(board, time_limit: float = 5.0) -> Optional[str]`

Get the best move within a time limit.

**Parameters:**
- `board`: ChessBoard instance representing the current position
- `time_limit` (float): Maximum time to spend thinking in seconds

**Returns:**
- `Optional[str]`: Best move in UCI format, or None if no moves available

#### `set_depth(depth: int) -> None`

Set the search depth for the engine.

**Parameters:**
- `depth` (int): New search depth

## Utility Functions

### Move Utilities (`chessbot.utils.move_utils`)

#### `is_legal_move(board: chess.Board, move_uci: str) -> bool`

Check if a move is legal on the given board.

#### `get_move_san(board: chess.Board, move_uci: str) -> Optional[str]`

Convert a UCI move to Standard Algebraic Notation (SAN).

#### `get_move_uci(board: chess.Board, move_san: str) -> Optional[str]`

Convert a SAN move to UCI format.

#### `is_capture_move(board: chess.Board, move_uci: str) -> bool`

Check if a move is a capture move.

#### `is_check_move(board: chess.Board, move_uci: str) -> bool`

Check if a move gives check.

#### `is_checkmate_move(board: chess.Board, move_uci: str) -> bool`

Check if a move gives checkmate.

#### `get_move_type(board: chess.Board, move_uci: str) -> str`

Get the type of a move (normal, capture, check, checkmate, etc.).

### Notation Utilities (`chessbot.utils.notation_utils`)

#### `square_to_coordinates(square: str) -> Tuple[int, int]`

Convert a chess square to coordinates.

#### `coordinates_to_square(file: int, rank: int) -> str`

Convert coordinates to a chess square.

#### `get_piece_symbol(piece: chess.Piece) -> str`

Get the symbol for a chess piece.

#### `get_piece_name(piece: chess.Piece) -> str`

Get the full name of a chess piece.

#### `get_color_name(color: bool) -> str`

Get the name of a chess color.

#### `format_fen(board: chess.Board) -> str`

Get a formatted FEN string for the board.

#### `parse_fen(fen: str) -> Optional[chess.Board]`

Parse a FEN string and create a board.

#### `get_move_description(board: chess.Board, move_uci: str) -> str`

Get a human-readable description of a move.

#### `get_board_visualization(board: chess.Board, show_coordinates: bool = True) -> str`

Get a visual representation of the board. 