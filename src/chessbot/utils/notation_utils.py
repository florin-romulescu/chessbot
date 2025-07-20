"""Utility functions for chess notation handling."""

from typing import Optional, Tuple

import chess


def square_to_coordinates(square: str) -> Tuple[int, int]:
    """
    Convert a chess square to coordinates.

    Args:
        square: Square in algebraic notation (e.g., 'e4')

    Returns:
        Tuple of (file, rank) coordinates (0-7, 0-7)
    """
    try:
        chess_square = chess.parse_square(square)
        return chess.square_file(chess_square), chess.square_rank(chess_square)
    except ValueError:
        raise ValueError(f"Invalid square: {square}") from None


def coordinates_to_square(file: int, rank: int) -> str:
    """
    Convert coordinates to a chess square.

    Args:
        file: File coordinate (0-7, a-h)
        rank: Rank coordinate (0-7, 1-8)

    Returns:
        Square in algebraic notation
    """
    if not (0 <= file <= 7 and 0 <= rank <= 7):
        raise ValueError(f"Invalid coordinates: ({file}, {rank})")

    chess_square = chess.square(file, rank)
    return chess.square_name(chess_square)


def uci_to_san_move(board: chess.Board, uci_move: str) -> Optional[str]:
    """
    Convert a UCI move to SAN notation.

    Args:
        board: Chess board
        uci_move: Move in UCI format

    Returns:
        Move in SAN format, or None if invalid
    """
    try:
        move = chess.Move.from_uci(uci_move)
        return board.san(move)
    except (ValueError, chess.InvalidMoveError):
        return None


def san_to_uci_move(board: chess.Board, san_move: str) -> Optional[str]:
    """
    Convert a SAN move to UCI format.

    Args:
        board: Chess board
        san_move: Move in SAN format

    Returns:
        Move in UCI format, or None if invalid
    """
    try:
        move = board.parse_san(san_move)
        return move.uci()
    except (ValueError, chess.InvalidMoveError):
        return None


def get_piece_symbol(piece: chess.Piece) -> str:
    """
    Get the symbol for a chess piece.

    Args:
        piece: Chess piece

    Returns:
        Piece symbol (P, N, B, R, Q, K for white; p, n, b, r, q, k for black)
    """
    return piece.symbol()


def get_piece_name(piece: chess.Piece) -> str:
    """
    Get the full name of a chess piece.

    Args:
        piece: Chess piece

    Returns:
        Piece name (pawn, knight, bishop, rook, queen, king)
    """
    piece_names = {
        chess.PAWN: "pawn",
        chess.KNIGHT: "knight",
        chess.BISHOP: "bishop",
        chess.ROOK: "rook",
        chess.QUEEN: "queen",
        chess.KING: "king",
    }
    return piece_names[piece.piece_type]


def get_color_name(color: bool) -> str:
    """
    Get the name of a chess color.

    Args:
        color: Chess color (True for white, False for black)

    Returns:
        Color name ("white" or "black")
    """
    return "white" if color else "black"


def format_fen(board: chess.Board) -> str:
    """
    Get a formatted FEN string for the board.

    Args:
        board: Chess board

    Returns:
        Formatted FEN string
    """
    return board.fen()


def parse_fen(fen: str) -> Optional[chess.Board]:
    """
    Parse a FEN string and create a board.

    Args:
        fen: FEN string

    Returns:
        Chess board, or None if FEN is invalid
    """
    try:
        return chess.Board(fen)
    except ValueError:
        return None


def get_move_description(board: chess.Board, move_uci: str) -> str:
    """
    Get a human-readable description of a move.

    Args:
        board: Chess board
        move_uci: Move in UCI format

    Returns:
        Human-readable move description
    """
    try:
        move = chess.Move.from_uci(move_uci)
        san = board.san(move)

        # Get piece information
        board.piece_at(move.from_square)
        to_piece = board.piece_at(move.to_square)

        description = f"{san}"

        if to_piece:
            description += f" (captures {get_piece_name(to_piece)})"

        if board.is_castling(move):
            description += " (castling)"
        elif board.is_en_passant(move):
            description += " (en passant)"
        elif move.promotion:
            description += f" (promotes to {get_piece_name(chess.Piece(move.promotion, board.turn))})"

        return description
    except (ValueError, chess.InvalidMoveError):
        return f"Invalid move: {move_uci}"


def get_board_visualization(board: chess.Board, show_coordinates: bool = True) -> str:
    """
    Get a visual representation of the board.

    Args:
        board: Chess board
        show_coordinates: Whether to show file and rank coordinates

    Returns:
        Visual board representation
    """
    board_str = str(board)

    if show_coordinates:
        # Add file coordinates at the bottom
        board_str += "\n  a b c d e f g h"

        # Add rank coordinates on the left
        lines = board_str.split("\n")
        numbered_lines = []
        for i, line in enumerate(lines[:-1]):  # Skip the last line (file coordinates)
            rank = 8 - i
            numbered_lines.append(f"{rank} {line}")

        board_str = "\n".join(numbered_lines)

    return board_str
