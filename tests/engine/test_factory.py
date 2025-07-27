"""Tests for the EngineFactory and EngineType."""

import pytest

from chessbot.board import ChessBoard
from chessbot.engine.factory import EngineFactory, EngineType
from chessbot.engine.minimax import MinimaxEngine


class TestEngineType:
    """Test cases for the EngineType enum."""

    def test_engine_type_values(self):
        """Test that EngineType has the expected values."""
        assert EngineType.MINIMAX.value == "minimax"

    def test_engine_type_enum(self):
        """Test that EngineType is a proper enum."""
        assert isinstance(EngineType.MINIMAX, EngineType)
        assert EngineType.MINIMAX.value == "minimax"


class TestEngineFactory:
    """Test cases for the EngineFactory class."""

    def test_engines_dict_structure(self):
        """Test that the engines dictionary has the correct structure."""
        assert hasattr(EngineFactory, "engines")
        assert isinstance(EngineFactory.engines, dict)
        assert EngineType.MINIMAX in EngineFactory.engines

    def test_engines_dict_content(self):
        """Test that the engines dictionary contains the expected engines."""
        minimax_engine = EngineFactory.engines[EngineType.MINIMAX]
        assert isinstance(minimax_engine, MinimaxEngine)

    def test_get_engine_minimax(self):
        """Test getting the minimax engine."""
        engine = EngineFactory.get_engine(EngineType.MINIMAX)
        assert isinstance(engine, MinimaxEngine)

    def test_get_engine_singleton_behavior(self):
        """Test that get_engine returns the same instance."""
        engine1 = EngineFactory.get_engine(EngineType.MINIMAX)
        engine2 = EngineFactory.get_engine(EngineType.MINIMAX)
        assert engine1 is engine2

    def test_get_engine_invalid_type(self):
        """Test that get_engine raises KeyError for invalid engine type."""
        with pytest.raises(KeyError):
            EngineFactory.get_engine("invalid_engine_type")

    def test_engine_functionality(self):
        """Test that the factory returns a functional engine."""
        engine = EngineFactory.get_engine(EngineType.MINIMAX)
        board = ChessBoard()

        # Test that the engine can evaluate positions
        evaluation = engine.evaluate(board)
        assert isinstance(evaluation, int)

        # Test that the engine can get moves
        move = engine.get_move(board)
        assert move is None or (isinstance(move, str) and len(move) == 4)

    def test_engine_depth_setting(self):
        """Test that the engine can have its depth modified."""
        engine = EngineFactory.get_engine(EngineType.MINIMAX)
        original_depth = engine.depth

        engine.set_depth(5)
        assert engine.depth == 5

        # Reset to original depth
        engine.set_depth(original_depth)
