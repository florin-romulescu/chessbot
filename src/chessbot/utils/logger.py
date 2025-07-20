import logging
from pathlib import Path
from typing import Optional


class ChessLogger:
    """
    Singleton logger class for logging UCI board moves and other chess-related events.
    """

    _instance: Optional["ChessLogger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> "ChessLogger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self) -> None:
        """Initialize the logger with proper configuration."""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        self._logger = logging.getLogger("chessbot")
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            log_file = logs_dir / "app.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(formatter)

            self._logger.addHandler(file_handler)

    def log_move(
        self, move: str, player: str = "Unknown", game_id: Optional[str] = None
    ) -> None:
        """
        Log a chess move with timestamp and player information.

        Args:
            move: The chess move in UCI format (e.g., 'e2e4')
            player: The player making the move (e.g., 'White', 'Black', 'Engine')
            game_id: Optional game identifier
        """
        if self._logger is None:
            self._initialize_logger()
            assert self._logger is not None

        game_info = f" [Game: {game_id}]" if game_id else ""
        message = f"MOVE: {player} played {move}{game_info}"
        self._logger.info(message)

    def log_game_start(
        self, game_id: Optional[str] = None, players: Optional[dict] = None
    ) -> None:
        """
        Log the start of a new game.

        Args:
            game_id: Optional game identifier
            players: Dictionary with player information (e.g., {'white': 'Player1', 'black': 'Engine'})
        """
        if self._logger is None:
            self._initialize_logger()
            assert self._logger is not None

        game_info = f" [Game: {game_id}]" if game_id else ""
        player_info = ""
        if players:
            white = players.get("white", "Unknown")
            black = players.get("black", "Unknown")
            player_info = f" - White: {white}, Black: {black}"

        message = f"GAME_START{game_info}{player_info}"
        self._logger.info(message)

    def log_game_end(self, result: str, game_id: Optional[str] = None) -> None:
        """
        Log the end of a game with the result.

        Args:
            result: Game result (e.g., '1-0', '0-1', '1/2-1/2')
            game_id: Optional game identifier
        """
        if self._logger is None:
            self._initialize_logger()
            assert self._logger is not None

        game_info = f" [Game: {game_id}]" if game_id else ""
        message = f"GAME_END: {result}{game_info}"
        self._logger.info(message)

    def log_error(self, error_message: str, game_id: Optional[str] = None) -> None:
        """
        Log an error message.

        Args:
            error_message: The error message to log
            game_id: Optional game identifier
        """
        if self._logger is None:
            self._initialize_logger()
            assert self._logger is not None

        game_info = f" [Game: {game_id}]" if game_id else ""
        message = f"ERROR: {error_message}{game_info}"
        self._logger.error(message)

    def log_info(self, info_message: str, game_id: Optional[str] = None) -> None:
        """
        Log an informational message.

        Args:
            info_message: The informational message to log
            game_id: Optional game identifier
        """
        if self._logger is None:
            self._initialize_logger()
            assert self._logger is not None

        game_info = f" [Game: {game_id}]" if game_id else ""
        message = f"INFO: {info_message}{game_info}"
        self._logger.info(message)

    def get_logger(self) -> logging.Logger:
        """Get the underlying logger instance."""
        if self._logger is None:
            self._initialize_logger()
            assert self._logger is not None
        return self._logger


def get_chess_logger() -> ChessLogger:
    """Get the singleton chess logger instance."""
    return ChessLogger()
