"""Chess engine for move evaluation and selection."""

import random
from typing import Optional, Tuple

import chess
import chess.engine


class ChessEngine:
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

    def evaluate_position(self, board: chess.Board) -> int:
        """
        Evaluate a chess position.

        This is a simple material-based evaluation. Positive values
        favor white, negative values favor black.

        Args:
            board: Chess board to evaluate

        Returns:
            Position evaluation score
        """
        if board.is_checkmate():
            # Checkmate is the highest priority
            return -10000 if board.turn else 10000

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0

        # Material evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                value = self.PIECE_VALUES[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value

        # Position evaluation (simplified)
        score += self._evaluate_positional_factors(board)

        return score

    def _evaluate_positional_factors(self, board: chess.Board) -> int:
        """
        Evaluate positional factors like piece mobility and king safety.

        Args:
            board: Chess board to evaluate

        Returns:
            Positional evaluation score
        """
        score = 0

        # Mobility evaluation
        white_moves = len(list(board.legal_moves))
        board.push(chess.Move.null())
        black_moves = len(list(board.legal_moves))
        board.pop()

        score += (white_moves - black_moves) * 10

        # Center control (simplified)
        center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    score += 20
                else:
                    score -= 20

        return score

    def minimax(
        self,
        board: chess.Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> Tuple[float, Optional[chess.Move]]:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            board: Current chess board
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing: True if maximizing player's turn

        Returns:
            Tuple of (evaluation, best_move)
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        best_move = None

        if maximizing:
            max_eval = float("-inf")
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self, board) -> Optional[str]:
        """
        Get the best move for the current position.

        Args:
            board: ChessBoard instance representing the current position

        Returns:
            Best move in UCI format, or None if no moves available
        """
        # Convert our ChessBoard to python-chess Board
        chess_board = board._board

        if chess_board.is_game_over():
            return None

        # Use minimax to find the best move
        _, best_move = self.minimax(
            chess_board, self.depth, float("-inf"), float("inf"), chess_board.turn
        )

        if best_move is not None:
            return best_move.uci()

        # Fallback: return a random legal move
        legal_moves = list(chess_board.legal_moves)
        if legal_moves:
            return random.choice(legal_moves).uci()

        return None

    def get_move_with_time_limit(self, board, time_limit: float = 5.0) -> Optional[str]:
        """
        Get the best move within a time limit.

        Args:
            board: ChessBoard instance representing the current position
            time_limit: Maximum time to spend thinking in seconds

        Returns:
            Best move in UCI format, or None if no moves available
        """
        # For now, just use the regular get_best_move
        # In a more sophisticated implementation, this would use iterative deepening
        return self.get_best_move(board)

    def set_depth(self, depth: int) -> None:
        """
        Set the search depth for the engine.

        Args:
            depth: New search depth
        """
        self.depth = max(1, depth)  # Ensure depth is at least 1
