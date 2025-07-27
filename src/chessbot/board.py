"""Chess board representation and move handling."""

from typing import List, Optional

import chess


class ChessBoard:
    """
    Chess board representation using the python-chess library.

    This class provides a high-level interface for managing chess game state,
    including move validation, board visualization, and game end detection.
    """

    def __init__(self, fen: str = chess.STARTING_FEN):
        """
        Initialize the chess board.

        Args:
            fen: FEN string representing the initial board position
        """
        self._board = chess.Board(fen)

    @property
    def turn(self) -> str:
        """
        Get the current player's turn.

        Returns:
            'w' for white's turn, 'b' for black's turn
        """
        return "w" if self._board.turn else "b"

    @property
    def is_check(self) -> bool:
        """
        Check if the current player is in check.

        Returns:
            True if the current player is in check
        """
        return self._board.is_check()

    @property
    def is_checkmate(self) -> bool:
        """
        Check if the current player is checkmated.

        Returns:
            True if the current player is checkmated
        """
        return self._board.is_checkmate()

    @property
    def is_stalemate(self) -> bool:
        """
        Check if the current position is a stalemate.

        Returns:
            True if the position is a stalemate
        """
        return self._board.is_stalemate()

    @property
    def is_insufficient_material(self) -> bool:
        """
        Check if there is insufficient material for checkmate.

        Returns:
            True if there is insufficient material
        """
        return self._board.is_insufficient_material()

    @property
    def legal_moves(self) -> List[str]:
        """
        Get all legal moves in UCI format.

        Returns:
            List of legal moves as UCI strings
        """
        return [move.uci() for move in self._board.legal_moves]

    def is_valid_move(self, move_uci: str) -> bool:
        """
        Check if a move is legal.

        Args:
            move_uci: Move in UCI format

        Returns:
            True if the move is legal
        """
        try:
            move = chess.Move.from_uci(move_uci)
            return move in self._board.legal_moves
        except ValueError:
            return False

    def make_move(self, move_uci: str) -> bool:
        """
        Make a move on the board.

        Args:
            move_uci: Move in UCI format

        Returns:
            True if the move was successfully made
        """
        if not self.is_valid_move(move_uci):
            return False

        move = chess.Move.from_uci(move_uci)
        self._board.push(move)
        return True

    def undo_move(self) -> None:
        """Undo the last move made on the board."""
        if self._board.move_stack:
            self._board.pop()

    def get_fen(self) -> str:
        """
        Get the current board position in FEN format.

        Returns:
            FEN string representing the current position
        """
        return self._board.fen()

    def set_fen(self, fen: str) -> bool:
        """
        Set the board position from a FEN string.

        Args:
            fen: FEN string representing the desired position

        Returns:
            True if the FEN was valid and set successfully
        """
        try:
            self._board = chess.Board(fen)
            return True
        except ValueError:
            return False

    def get_piece_at(self, square: str) -> Optional[str]:
        """
        Get the piece at a given square.

        Args:
            square: Square in algebraic notation (e.g., 'e4')

        Returns:
            Piece symbol or None if square is empty
        """
        try:
            chess_square = chess.parse_square(square)
            piece = self._board.piece_at(chess_square)
            if piece is None:
                return None
            return piece.symbol()
        except ValueError:
            return None
        
    @property
    def pieces(self) -> List[chess.Piece]:
        """
        Get all pieces on the board.
        
        Returns:
            List of chess.Piece objects representing all pieces on the board
        """
        piece_map = self._board.piece_map()
        return list(piece_map.values())
    
    @property
    def pieces_with_positions(self) -> dict:
        """
        Get all pieces on the board with their positions.
        
        Returns:
            Dictionary mapping square indices to chess.Piece objects
        """
        return self._board.piece_map()

    def __str__(self) -> str:
        """
        Get a string representation of the board.

        Returns:
            ASCII representation of the chess board
        """
        return str(self._board)

    def __repr__(self) -> str:
        """Get a string representation for debugging."""
        return f"ChessBoard(fen='{self.get_fen()}')"
