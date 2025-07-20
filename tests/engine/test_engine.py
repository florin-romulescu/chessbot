"""Tests for the ChessEngine abstract base class."""

from abc import ABC

import pytest

from chessbot.engine.engine import ChessEngine


class TestChessEngine:
    """Test cases for the ChessEngine abstract base class."""

    def test_is_abstract_base_class(self):
        """Test that ChessEngine is an abstract base class."""
        assert issubclass(ChessEngine, ABC)

        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            ChessEngine()

    def test_abstract_methods_exist(self):
        """Test that all required abstract methods are defined."""
        # Check that all required methods exist
        assert hasattr(ChessEngine, "get_best_move")
        assert hasattr(ChessEngine, "get_move_with_time_limit")
        assert hasattr(ChessEngine, "set_depth")
        assert hasattr(ChessEngine, "get_move")

    def test_method_signatures(self):
        """Test that method signatures are correct."""
        # Check get_best_move signature
        import inspect
        from typing import Optional

        sig = inspect.signature(ChessEngine.get_best_move)
        assert "board" in sig.parameters
        assert sig.return_annotation == Optional[str]

        # Check get_move_with_time_limit signature
        sig = inspect.signature(ChessEngine.get_move_with_time_limit)
        assert "board" in sig.parameters
        assert "time_limit" in sig.parameters
        assert sig.return_annotation == Optional[str]

        # Check set_depth signature
        sig = inspect.signature(ChessEngine.set_depth)
        assert "depth" in sig.parameters
        assert sig.return_annotation is None

        # Check get_move signature
        sig = inspect.signature(ChessEngine.get_move)
        assert "board" in sig.parameters
        assert "time_limit" in sig.parameters
        assert sig.parameters["time_limit"].default is None
        assert sig.return_annotation == Optional[str]
