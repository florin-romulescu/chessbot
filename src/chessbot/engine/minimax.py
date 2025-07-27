"""Chess engine for move evaluation and selection."""

from typing import Optional

import chess

from chessbot.board import ChessBoard
from chessbot.utils import get_chess_logger

from .engine import ChessEngine


class MinimaxEngine(ChessEngine):
    """
    Chess engine that evaluates positions and selects the best moves.

    This engine implements basic chess AI algorithms including minimax
    with alpha-beta pruning and position evaluation.
    """

    # Piece values for material evaluation
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000,
    }

    def __init__(self, depth: int = 3):
        """
        Initialize the chess engine.

        Args:
            depth: Search depth for the minimax algorithm
        """
        self.depth = depth
        self.logger = get_chess_logger()

    def evaluate(self, board: ChessBoard) -> int:
        score = 0
        for piece in board.pieces:
            score += self.PIECE_VALUES[piece.piece_type] * piece.color
        return score

    def maxi(self, board: ChessBoard, depth: int) -> float:
        if depth == 0:
            return self.evaluate(board)

        max_eval = float("-inf")
        for _move in board.legal_moves:
            score = self.mini(board, depth - 1)
            max_eval = max(max_eval, score)
        return max_eval

    def mini(self, board: ChessBoard, depth: int) -> float:
        if depth == 0:
            return self.evaluate(board)

        min_eval = float("inf")
        for _move in board.legal_moves:
            score = self.maxi(board, depth - 1)
            min_eval = min(min_eval, score)
        return min_eval

    def get_best_move(self, board: ChessBoard) -> Optional[str]:
        best_move = None
        best_score = float("-inf")
        self.logger.log_info(f"Getting best move with depth {self.depth}")
        for move in board.legal_moves:
            score = self.maxi(board, self.depth - 1)
            if score > best_score:
                best_score = score
                best_move = move
                self.logger.log_info(f"Best move: {best_move} with score {best_score}")
        return best_move

    def get_move_with_time_limit(
        self, board: ChessBoard, time_limit: float
    ) -> Optional[str]:
        return self.get_best_move(board)

    def set_depth(self, depth: int) -> None:
        self.depth = depth

    def get_move(
        self, board: ChessBoard, time_limit: Optional[float] = None
    ) -> Optional[str]:
        return self.get_best_move(board)
