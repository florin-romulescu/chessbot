"""Utility functions for chess move handling."""

from typing import List, Optional

import chess


def is_legal_move(board: chess.Board, move_uci: str) -> bool:
    """
    Check if a move is legal on the given board.

    Args:
        board: Chess board to check the move on
        move_uci: Move in UCI format

    Returns:
        True if the move is legal
    """
    try:
        move = chess.Move.from_uci(move_uci)
        return move in board.legal_moves
    except ValueError:
        return False


def get_move_san(board: chess.Board, move_uci: str) -> Optional[str]:
    """
    Convert a UCI move to Standard Algebraic Notation (SAN).

    Args:
        board: Chess board
        move_uci: Move in UCI format

    Returns:
        Move in SAN format, or None if invalid
    """
    try:
        move = chess.Move.from_uci(move_uci)
        return board.san(move)
    except (ValueError, chess.InvalidMoveError):
        return None


def get_move_uci(board: chess.Board, move_san: str) -> Optional[str]:
    """
    Convert a SAN move to UCI format.

    Args:
        board: Chess board
        move_san: Move in SAN format

    Returns:
        Move in UCI format, or None if invalid
    """
    try:
        move = board.parse_san(move_san)
        return move.uci()
    except (ValueError, chess.InvalidMoveError):
        return None


def get_captured_piece(board: chess.Board, move_uci: str) -> Optional[chess.Piece]:
    """
    Get the piece that would be captured by a move.

    Args:
        board: Chess board
        move_uci: Move in UCI format

    Returns:
        Captured piece, or None if no piece is captured
    """
    try:
        move = chess.Move.from_uci(move_uci)
        return board.piece_at(move.to_square)
    except ValueError:
        return None


def is_capture_move(board: chess.Board, move_uci: str) -> bool:
    """
    Check if a move is a capture move.

    Args:
        board: Chess board
        move_uci: Move in UCI format

    Returns:
        True if the move captures a piece
    """
    return get_captured_piece(board, move_uci) is not None


def is_check_move(board: chess.Board, move_uci: str) -> bool:
    """
    Check if a move gives check.

    Args:
        board: Chess board
        move_uci: Move in UCI format

    Returns:
        True if the move gives check
    """
    try:
        move = chess.Move.from_uci(move_uci)
        board.push(move)
        is_check = board.is_check()
        board.pop()
        return is_check
    except ValueError:
        return False


def is_checkmate_move(board: chess.Board, move_uci: str) -> bool:
    """
    Check if a move gives checkmate.

    Args:
        board: Chess board
        move_uci: Move in UCI format

    Returns:
        True if the move gives checkmate
    """
    try:
        move = chess.Move.from_uci(move_uci)
        board.push(move)
        is_checkmate = board.is_checkmate()
        board.pop()
        return is_checkmate
    except ValueError:
        return False


def get_move_type(board: chess.Board, move_uci: str) -> str:
    """
    Get the type of a move (normal, capture, check, checkmate, etc.).

    Args:
        board: Chess board
        move_uci: Move in UCI format

    Returns:
        String describing the move type
    """
    if not is_legal_move(board, move_uci):
        return "illegal"

    move_types = []

    if is_capture_move(board, move_uci):
        move_types.append("capture")

    if is_checkmate_move(board, move_uci):
        move_types.append("checkmate")
    elif is_check_move(board, move_uci):
        move_types.append("check")

    # Check for special moves
    try:
        move = chess.Move.from_uci(move_uci)
        if board.is_castling(move):
            move_types.append("castling")
        elif board.is_en_passant(move):
            move_types.append("en_passant")
        elif board.is_promotion(move):
            move_types.append("promotion")
    except ValueError:
        pass

    return " ".join(move_types) if move_types else "normal"


def get_all_capture_moves(board: chess.Board) -> List[str]:
    """
    Get all capture moves for the current position.

    Args:
        board: Chess board

    Returns:
        List of capture moves in UCI format
    """
    return [move.uci() for move in board.legal_moves if board.is_capture(move)]


def get_all_check_moves(board: chess.Board) -> List[str]:
    """
    Get all moves that give check.

    Args:
        board: Chess board

    Returns:
        List of check moves in UCI format
    """
    check_moves = []
    for move in board.legal_moves:
        board.push(move)
        if board.is_check():
            check_moves.append(move.uci())
        board.pop()
    return check_moves
