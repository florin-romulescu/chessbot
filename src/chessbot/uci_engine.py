"""UCI (Universal Chess Interface) engine implementation."""

import sys
import time
from argparse import ArgumentParser

from .board import ChessBoard
from .engine import EngineFactory, EngineType
from .utils.logger import get_chess_logger


class UCIEngine:
    """
    UCI engine implementation for the chess bot.

    This class implements the Universal Chess Interface protocol,
    allowing the chess bot to communicate with XBoard, Arena, and
    other UCI-compatible chess GUIs.
    """

    def __init__(
        self, engine_type: EngineType = EngineType.MINIMAX, debug: bool = False
    ):
        """
        Initialize the UCI engine.

        Args:
            engine_depth: Search depth for the chess engine
        """
        self.engine_type = engine_type
        self.chess_engine = EngineFactory.get_engine(engine_type=engine_type)
        self.board = ChessBoard()
        self.running = False
        self.debug = debug
        self.logger = get_chess_logger()

    def run(self) -> None:
        """Run the UCI engine, listening for commands from stdin."""
        self.running = True

        while self.running:
            try:
                line = input().strip()
                if not line:
                    continue

                self._handle_command(line)
            except EOFError:
                break
            except KeyboardInterrupt:
                break

    def _handle_command(self, command: str) -> None:
        """
        Handle a UCI command.

        Args:
            command: The UCI command to handle
        """
        if self.debug:
            self.logger.log_info(f"Received command: {command}")

        parts = command.split()
        if not parts:
            return

        cmd = parts[0].lower()

        if cmd == "uci":
            self._send_uci_info()
        elif cmd == "isready":
            self._send_ready()
        elif cmd == "setoption":
            self._handle_setoption(parts[1:])
        elif cmd == "ucinewgame":
            self._handle_newgame()
        elif cmd == "position":
            self._handle_position(parts[1:])
        elif cmd == "go":
            self._handle_go(parts[1:])
        elif cmd == "stop":
            self._handle_stop()
        elif cmd == "quit":
            self._handle_quit()
        elif cmd == "debug":
            self._handle_debug(parts[1:])
        else:
            if self.debug:
                print(f"info string Unknown command: {command}", file=sys.stderr)

    def _send_uci_info(self) -> None:
        """Send UCI engine information."""
        print("id name ChessBot")
        print("id author Florin Romulescu")
        print("option name Depth type spin default 3 min 1 max 10")
        print("option name Debug type check default false")
        print("uciok")

    def _send_ready(self) -> None:
        """Send ready signal."""
        print("readyok")

    def _handle_setoption(self, args: list) -> None:
        """
        Handle setoption command.

        Args:
            args: Option arguments
        """
        if len(args) < 4 or args[0] != "name" or args[2] != "value":
            return

        option_name = args[1]
        option_value = args[3]

        if option_name == "Depth":
            try:
                depth = int(option_value)
                self.chess_engine.set_depth(depth)
            except ValueError:
                pass
        elif option_name == "Debug":
            self.debug = option_value.lower() == "true"

    def _handle_newgame(self) -> None:
        """Handle new game command."""
        self.board = ChessBoard()

    def _handle_position(self, args: list) -> None:
        """
        Handle position command.

        Args:
            args: Position arguments
        """
        if not args:
            return

        if args[0] == "startpos":
            self.board = ChessBoard()
            if len(args) > 1 and args[1] == "moves":
                for move in args[2:]:
                    self.board.make_move(move)
        elif args[0] == "fen":
            if len(args) < 2:
                return
            fen = " ".join(args[1:7])  # FEN has 6 parts
            self.board.set_fen(fen)
            if len(args) > 7 and args[7] == "moves":
                for move in args[8:]:
                    self.board.make_move(move)

    def _handle_go(self, args: list) -> None:
        """
        Handle go command.

        Args:
            args: Go command arguments
        """
        # Parse time controls (simplified)
        time_limit = 5.0  # Default 5 seconds

        for i, arg in enumerate(args):
            if arg == "movetime" and i + 1 < len(args):
                try:
                    time_limit = int(args[i + 1]) / 1000.0  # Convert ms to seconds
                except ValueError:
                    pass
            elif arg == "wtime" and self.board.turn == "w" and i + 1 < len(args):
                try:
                    time_limit = int(args[i + 1]) / 1000.0 / 30  # Rough estimate
                except ValueError:
                    pass
            elif arg == "btime" and self.board.turn == "b" and i + 1 < len(args):
                try:
                    time_limit = int(args[i + 1]) / 1000.0 / 30  # Rough estimate
                except ValueError:
                    pass

        # Get the best move
        start_time = time.time()
        best_move = self.chess_engine.get_move_with_time_limit(self.board, time_limit)
        time.time() - start_time

        if best_move:
            print(f"bestmove {best_move}")
        else:
            print("bestmove 0000")  # No legal moves

    def _handle_stop(self) -> None:
        """Handle stop command."""
        # For now, we don't implement move interruption
        # In a more sophisticated implementation, you would stop the search
        pass

    def _handle_quit(self) -> None:
        """Handle quit command."""
        self.running = False

    def _handle_debug(self, args: list) -> None:
        """
        Handle debug command.

        Args:
            args: Debug arguments
        """
        if args and args[0].lower() == "on":
            self.debug = True
        elif args and args[0].lower() == "off":
            self.debug = False


def main() -> None:
    """Main entry point for the UCI engine."""
    parser = ArgumentParser()
    parser.add_argument("--engine-type", type=EngineType, default=EngineType.MINIMAX)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    engine = UCIEngine(engine_type=args.engine_type, debug=args.debug)
    engine.run()


if __name__ == "__main__":
    main()
