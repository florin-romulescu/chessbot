"""Tests for the engine module's __init__.py file."""

from chessbot.engine import ChessEngine, EngineFactory, EngineType


class TestEngineInit:
    """Test cases for the engine module initialization."""

    def test_imports(self):
        """Test that all expected classes are imported correctly."""
        # Test that ChessEngine is imported
        assert ChessEngine is not None

        # Test that EngineFactory is imported
        assert EngineFactory is not None

        # Test that EngineType is imported
        assert EngineType is not None

    def test_chess_engine_import(self):
        """Test that ChessEngine is imported from the correct module."""
        from chessbot.engine.engine import ChessEngine as EngineChessEngine

        assert ChessEngine is EngineChessEngine

    def test_factory_import(self):
        """Test that EngineFactory is imported from the correct module."""
        from chessbot.engine.factory import EngineFactory as FactoryEngineFactory

        assert EngineFactory is FactoryEngineFactory

    def test_engine_type_import(self):
        """Test that EngineType is imported from the correct module."""
        from chessbot.engine.factory import EngineType as FactoryEngineType

        assert EngineType is FactoryEngineType

    def test_import_attributes(self):
        """Test that imported classes have the expected attributes."""
        # Test ChessEngine attributes
        assert hasattr(ChessEngine, "get_best_move")
        assert hasattr(ChessEngine, "get_move_with_time_limit")
        assert hasattr(ChessEngine, "set_depth")
        assert hasattr(ChessEngine, "get_move")

        # Test EngineFactory attributes
        assert hasattr(EngineFactory, "engines")
        assert hasattr(EngineFactory, "get_engine")

        # Test EngineType attributes
        assert hasattr(EngineType, "MINIMAX")
