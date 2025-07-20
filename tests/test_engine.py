"""Tests for the ChessEngine class."""

import chess

from chessbot.board import ChessBoard
from chessbot.engine import ChessEngine


class TestChessEngine:
    """Test cases for the ChessEngine class."""

    def test_initialization(self):
        """Test engine initialization."""
        engine = ChessEngine(depth=3)
        assert engine.depth == 3

        # Test default depth
        engine = ChessEngine()
        assert engine.depth == 3

    def test_piece_values(self):
        """Test piece value constants."""
        assert ChessEngine.PIECE_VALUES[chess.PAWN] == 100
        assert ChessEngine.PIECE_VALUES[chess.KNIGHT] == 320
        assert ChessEngine.PIECE_VALUES[chess.BISHOP] == 330
        assert ChessEngine.PIECE_VALUES[chess.ROOK] == 500
        assert ChessEngine.PIECE_VALUES[chess.QUEEN] == 900
        assert ChessEngine.PIECE_VALUES[chess.KING] == 20000

    def test_evaluate_starting_position(self):
        """Test evaluation of starting position."""
        engine = ChessEngine()
        board = chess.Board()

        # Starting position should be equal (close to 0)
        evaluation = engine.evaluate_position(board)
        assert abs(evaluation) < 100  # Should be roughly equal

    def test_evaluate_checkmate(self):
        """Test evaluation of checkmate positions."""
        engine = ChessEngine()

        # Fool's mate position
        board = chess.Board(
            "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        )
        evaluation = engine.evaluate_position(board)

        # Should heavily favor black (negative score)
        assert evaluation < -5000

    def test_evaluate_material_advantage(self):
        """Test evaluation with material advantage."""
        engine = ChessEngine()

        # Position where white has an extra queen
        board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNQ w KQkq - 0 1")
        evaluation = engine.evaluate_position(board)

        # Should favor white (positive score)
        assert (
            evaluation > 300
        )  # Queen value is 900, but positional factors may reduce it

    def test_minimax_basic(self):
        """Test basic minimax functionality."""
        engine = ChessEngine(depth=2)
        board = chess.Board()

        # Test minimax on starting position
        evaluation, best_move = engine.minimax(
            board, 2, float("-inf"), float("inf"), True
        )

        assert best_move is not None
        assert best_move in board.legal_moves

    def test_get_best_move(self):
        """Test getting best move from engine."""
        engine = ChessEngine(depth=2)
        board = ChessBoard()

        best_move = engine.get_best_move(board)
        assert best_move is not None
        assert len(best_move) == 4  # UCI format
        assert board.is_valid_move(best_move)

    def test_get_best_move_game_over(self):
        """Test getting best move when game is over."""
        engine = ChessEngine()

        # Set up checkmate position
        board = ChessBoard(
            "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        )
        board.make_move("f1c4")  # Make the checkmate move

        best_move = engine.get_best_move(board)
        assert best_move is None  # No moves available in checkmate

    def test_set_depth(self):
        """Test setting engine depth."""
        engine = ChessEngine(depth=3)
        assert engine.depth == 3

        engine.set_depth(5)
        assert engine.depth == 5

        # Test minimum depth
        engine.set_depth(0)
        assert engine.depth == 1

    def test_positional_evaluation(self):
        """Test positional evaluation factors."""
        engine = ChessEngine()
        board = chess.Board()

        # Test that positional evaluation doesn't crash
        score = engine._evaluate_positional_factors(board)
        assert isinstance(score, int)

    def test_get_move_with_time_limit(self):
        """Test getting move with time limit."""
        engine = ChessEngine()
        board = ChessBoard()

        # Should return a move within time limit
        best_move = engine.get_move_with_time_limit(board, time_limit=1.0)
        assert best_move is not None
        assert board.is_valid_move(best_move)

    def test_engine_with_different_depths(self):
        """Test engine behavior with different search depths."""
        board = ChessBoard()

        # Test with different depths
        for depth in [1, 2, 3]:
            engine = ChessEngine(depth=depth)
            best_move = engine.get_best_move(board)
            assert best_move is not None
            assert board.is_valid_move(best_move)

    def test_evaluation_consistency(self):
        """Test that evaluation is consistent for same position."""
        engine = ChessEngine()
        board = chess.Board()

        eval1 = engine.evaluate_position(board)
        eval2 = engine.evaluate_position(board)

        assert eval1 == eval2  # Same position should have same evaluation
