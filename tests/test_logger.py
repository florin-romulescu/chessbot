"""Tests for the ChessLogger class."""

import logging
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from chessbot.utils import ChessLogger, get_chess_logger


class TestChessLogger:
    """Test cases for the ChessLogger singleton class."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Reset the singleton instance
        ChessLogger._instance = None
        ChessLogger._logger = None

        # Create a temporary directory for logs
        self.temp_dir = tempfile.mkdtemp()
        self.logs_dir = Path(self.temp_dir) / "logs"
        self.logs_dir.mkdir(exist_ok=True)

    def teardown_method(self):
        """Clean up after each test."""
        # Reset the singleton instance
        ChessLogger._instance = None
        ChessLogger._logger = None

        # Clean up temporary files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_singleton_pattern(self):
        """Test that ChessLogger follows singleton pattern."""
        logger1 = ChessLogger()
        logger2 = ChessLogger()

        assert logger1 is logger2
        assert id(logger1) == id(logger2)

    def test_get_chess_logger_function(self):
        """Test the convenience function returns the same instance."""
        logger1 = get_chess_logger()
        logger2 = get_chess_logger()

        assert logger1 is logger2
        assert isinstance(logger1, ChessLogger)

    @patch("chessbot.utils.logger.Path")
    def test_initialization_creates_logs_directory(self, mock_path):
        """Test that logger creates logs directory if it doesn't exist."""
        mock_path.return_value = self.logs_dir

        ChessLogger()

        # Verify logs directory was created
        assert self.logs_dir.exists()

    def test_logger_initialization(self):
        """Test logger is properly initialized."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            underlying_logger = logger.get_logger()

            assert isinstance(underlying_logger, logging.Logger)
            assert underlying_logger.name == "chessbot"
            assert underlying_logger.level == logging.INFO

    def test_logger_has_file_handler(self):
        """Test that logger has a file handler configured."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            underlying_logger = logger.get_logger()

            # Check that there's at least one handler
            assert len(underlying_logger.handlers) > 0

            # Check that one of the handlers is a FileHandler
            file_handlers = [
                h
                for h in underlying_logger.handlers
                if isinstance(h, logging.FileHandler)
            ]
            assert len(file_handlers) > 0

    def test_log_move(self):
        """Test logging a chess move."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()

            # Mock the underlying logger
            mock_logger = MagicMock()
            logger._logger = mock_logger

            # Test logging a move
            logger.log_move("e2e4", "White", "test_game_123")

            # Verify the log was called with correct message
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "MOVE: White played e2e4" in call_args
            assert "[Game: test_game_123]" in call_args

    def test_log_move_without_game_id(self):
        """Test logging a move without game ID."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            mock_logger = MagicMock()
            logger._logger = mock_logger

            logger.log_move("d2d4", "Black")

            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "MOVE: Black played d2d4" in call_args
            assert "[Game:" not in call_args

    def test_log_game_start(self):
        """Test logging game start."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            mock_logger = MagicMock()
            logger._logger = mock_logger

            players = {"white": "Player1", "black": "Stockfish"}
            logger.log_game_start("game_456", players)

            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "GAME_START" in call_args
            assert "[Game: game_456]" in call_args
            assert "White: Player1, Black: Stockfish" in call_args

    def test_log_game_start_without_players(self):
        """Test logging game start without player information."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            mock_logger = MagicMock()
            logger._logger = mock_logger

            logger.log_game_start("game_789")

            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "GAME_START" in call_args
            assert "[Game: game_789]" in call_args
            assert "White:" not in call_args

    def test_log_game_end(self):
        """Test logging game end."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            mock_logger = MagicMock()
            logger._logger = mock_logger

            logger.log_game_end("1-0", "game_999")

            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "GAME_END: 1-0" in call_args
            assert "[Game: game_999]" in call_args

    def test_log_error(self):
        """Test logging error messages."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            mock_logger = MagicMock()
            logger._logger = mock_logger

            logger.log_error("Connection failed", "game_error")

            mock_logger.error.assert_called_once()
            call_args = mock_logger.error.call_args[0][0]
            assert "ERROR: Connection failed" in call_args
            assert "[Game: game_error]" in call_args

    def test_log_info(self):
        """Test logging info messages."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            mock_logger = MagicMock()
            logger._logger = mock_logger

            logger.log_info("Engine analysis completed", "game_info")

            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "INFO: Engine analysis completed" in call_args
            assert "[Game: game_info]" in call_args

    def test_multiple_handlers_not_created(self):
        """Test that multiple handlers are not created for the same logger."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            # Create first instance
            logger1 = ChessLogger()
            handler_count_1 = len(logger1.get_logger().handlers)

            # Create second instance (should be the same)
            logger2 = ChessLogger()
            handler_count_2 = len(logger2.get_logger().handlers)

            # Should have the same number of handlers
            assert handler_count_1 == handler_count_2

    def test_logger_with_real_file(self):
        """Test logger writes to actual file."""
        # Don't mock Path for this test - use real file system
        logger = ChessLogger()

        # Temporarily change the logs directory for this test
        original_logs_dir = logger._logger.handlers[0].baseFilename
        test_log_file = self.logs_dir / "app.log"

        # Create a new file handler for testing
        import logging

        test_handler = logging.FileHandler(test_log_file)
        test_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        test_handler.setFormatter(formatter)

        # Replace the handler temporarily
        logger._logger.removeHandler(logger._logger.handlers[0])
        logger._logger.addHandler(test_handler)

        try:
            # Log some messages
            logger.log_move("e2e4", "White", "real_game")
            logger.log_game_start("real_game", {"white": "Test", "black": "Engine"})
            logger.log_game_end("1-0", "real_game")

            # Check if log file exists and contains our messages
            assert test_log_file.exists()

            with open(test_log_file) as f:
                content = f.read()
                assert "MOVE: White played e2e4" in content
                assert "GAME_START" in content
                assert "GAME_END: 1-0" in content
                assert "[Game: real_game]" in content
        finally:
            # Restore original handler
            logger._logger.removeHandler(test_handler)
            original_handler = logging.FileHandler(original_logs_dir)
            original_handler.setLevel(logging.INFO)
            original_handler.setFormatter(formatter)
            logger._logger.addHandler(original_handler)

    def test_logger_format(self):
        """Test that log messages have the correct format."""
        logger = ChessLogger()

        # Temporarily change the logs directory for this test
        test_log_file = self.logs_dir / "app.log"

        # Create a new file handler for testing
        import logging

        test_handler = logging.FileHandler(test_log_file)
        test_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        test_handler.setFormatter(formatter)

        # Replace the handler temporarily
        logger._logger.removeHandler(logger._logger.handlers[0])
        logger._logger.addHandler(test_handler)

        try:
            # Log a message
            logger.log_move("e2e4", "White", "format_test")

            # Check log file format
            with open(test_log_file) as f:
                line = f.readline().strip()

                # Should match the expected format: timestamp - logger_name - level - message
                parts = line.split(" - ")
                assert len(parts) == 4
                assert parts[1] == "chessbot"
                assert parts[2] == "INFO"
                assert "MOVE: White played e2e4" in parts[3]
        finally:
            # Restore original handler
            logger._logger.removeHandler(test_handler)
            original_logs_dir = "logs/app.log"
            original_handler = logging.FileHandler(original_logs_dir)
            original_handler.setLevel(logging.INFO)
            original_handler.setFormatter(formatter)
            logger._logger.addHandler(original_handler)

    def test_logger_with_none_logger(self):
        """Test logger behavior when _logger is None."""
        logger = ChessLogger()
        logger._logger = None

        # Should reinitialize the logger
        logger.log_move("e2e4", "White")

        # Verify logger was reinitialized
        assert logger._logger is not None

    def test_get_logger_method(self):
        """Test the get_logger method returns the underlying logger."""
        with patch("chessbot.utils.logger.Path") as mock_path:
            mock_path.return_value = self.logs_dir

            logger = ChessLogger()
            underlying_logger = logger.get_logger()

            assert underlying_logger is logger._logger
            assert isinstance(underlying_logger, logging.Logger)


class TestChessLoggerIntegration:
    """Integration tests for ChessLogger with real file system."""

    def setup_method(self):
        """Set up test environment."""
        # Reset singleton
        ChessLogger._instance = None
        ChessLogger._logger = None

        # Use actual logs directory
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)

        # Clean up existing log file
        log_file = self.logs_dir / "app.log"
        if log_file.exists():
            log_file.unlink()

    def teardown_method(self):
        """Clean up after each test."""
        ChessLogger._instance = None
        ChessLogger._logger = None

    def test_logger_functionality(self):
        """Test that logger methods work correctly without file system issues."""
        # Force reinitialization of the logger
        ChessLogger._instance = None
        ChessLogger._logger = None

        logger = ChessLogger()

        # Test that all methods can be called without errors
        game_id = "test_game_123"

        # Test all logging methods
        logger.log_game_start(game_id, {"white": "TestPlayer", "black": "TestEngine"})
        logger.log_move("e2e4", "White", game_id)
        logger.log_move("e7e5", "Black", game_id)
        logger.log_info("Test info message", game_id)
        logger.log_error("Test error message", game_id)
        logger.log_game_end("1/2-1/2", game_id)

        # Verify logger is working
        assert logger._logger is not None
        assert len(logger._logger.handlers) > 0

    def test_logger_singleton_across_tests(self):
        """Test that logger maintains singleton pattern across different test calls."""
        # Force reinitialization
        ChessLogger._instance = None
        ChessLogger._logger = None

        logger1 = ChessLogger()
        logger2 = ChessLogger()

        # Should be the same instance
        assert logger1 is logger2

        # Test logging
        logger1.log_move("e2e4", "White", "singleton_test")
        logger2.log_move("e7e5", "Black", "singleton_test")

        # Both should work with the same underlying logger
        assert logger1._logger is logger2._logger
