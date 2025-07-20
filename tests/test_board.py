"""Tests for the ChessBoard class."""

import chess

from chessbot.board import ChessBoard


class TestChessBoard:
    """Test cases for the ChessBoard class."""

    def test_initialization(self):
        """Test board initialization with default FEN."""
        board = ChessBoard()
        assert board.get_fen() == chess.STARTING_FEN
        assert board.turn == 'w'

    def test_initialization_with_custom_fen(self):
        """Test board initialization with custom FEN."""
        custom_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        board = ChessBoard(custom_fen)
        assert board.get_fen() == custom_fen

    def test_turn_property(self):
        """Test the turn property."""
        board = ChessBoard()
        assert board.turn == 'w'

        # Make a move to change turn
        board.make_move('e2e4')
        assert board.turn == 'b'

    def test_legal_moves(self):
        """Test getting legal moves."""
        board = ChessBoard()
        legal_moves = board.legal_moves
        assert len(legal_moves) == 20  # Starting position has 20 legal moves
        assert 'e2e4' in legal_moves
        assert 'd2d4' in legal_moves

    def test_valid_move(self):
        """Test move validation."""
        board = ChessBoard()
        assert board.is_valid_move('e2e4') is True
        assert board.is_valid_move('e2e5') is False  # Invalid move
        assert board.is_valid_move('invalid') is False

    def test_make_move(self):
        """Test making moves."""
        board = ChessBoard()
        assert board.make_move('e2e4') is True
        assert board.get_fen() != chess.STARTING_FEN

        # Test invalid move
        assert board.make_move('e2e5') is False

    def test_undo_move(self):
        """Test undoing moves."""
        board = ChessBoard()
        original_fen = board.get_fen()

        board.make_move('e2e4')
        assert board.get_fen() != original_fen

        board.undo_move()
        assert board.get_fen() == original_fen

    def test_game_end_conditions(self):
        """Test game end condition detection."""
        board = ChessBoard()

        # Starting position should not be checkmate/stalemate
        assert board.is_checkmate is False
        assert board.is_stalemate is False
        assert board.is_insufficient_material is False

    def test_check_detection(self):
        """Test check detection."""
        board = ChessBoard()
        assert board.is_check is False

        # Set up a position with check (Fool's mate setup)
        check_fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        board.set_fen(check_fen)
        assert board.is_check is True

    def test_get_piece_at(self):
        """Test getting piece at square."""
        board = ChessBoard()

        # Test pieces at starting position
        assert board.get_piece_at('e1') == 'K'  # White king
        assert board.get_piece_at('e8') == 'k'  # Black king
        assert board.get_piece_at('e4') is None  # Empty square

    def test_set_fen(self):
        """Test setting board from FEN."""
        board = ChessBoard()
        custom_fen = "8/8/8/8/8/8/8/8 w - - 0 1"  # Empty board

        assert board.set_fen(custom_fen) is True
        assert board.get_fen() == custom_fen

        # Test invalid FEN
        assert board.set_fen("invalid fen") is False

    def test_string_representation(self):
        """Test string representation of the board."""
        board = ChessBoard()
        board_str = str(board)

        # Should contain the board representation
        assert 'r' in board_str  # Black rook
        assert 'R' in board_str  # White rook
        assert 'k' in board_str  # Black king
        assert 'K' in board_str  # White king

    def test_repr(self):
        """Test representation for debugging."""
        board = ChessBoard()
        repr_str = repr(board)

        assert "ChessBoard" in repr_str
        assert "fen=" in repr_str
