"""Advanced UCI engine implementation with better time management."""

import sys
import threading
import time
from typing import Any, Dict, Optional

from .board import ChessBoard
from .engine import ChessEngine


class AdvancedUCIEngine:
    """
    Advanced UCI engine implementation with better time management.

    This class implements a more sophisticated UCI engine with:
    - Better time management
    - Search information output
    - Move ordering
    - Iterative deepening
    """

    def __init__(self, engine_depth: int = 3):
        """
        Initialize the advanced UCI engine.

        Args:
            engine_depth: Search depth for the chess engine
        """
        self.chess_engine = ChessEngine(depth=engine_depth)
        self.board = ChessBoard()
        self.running = False
        self.debug = False
        self.search_stopped = False
        self.current_search_thread: Optional[threading.Thread] = None

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
            print(f"info string Received command: {command}", file=sys.stderr)

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
        print("id name ChessBot Advanced")
        print("id author Florin Romulescu")
        print("option name Depth type spin default 3 min 1 max 10")
        print("option name Debug type check default false")
        print("option name MultiPV type spin default 1 min 1 max 1")
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
        self.search_stopped = False

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
        Handle go command with advanced time management.

        Args:
            args: Go command arguments
        """
        time_controls = self._parse_time_controls(args)

        # Start search in a separate thread
        self.search_stopped = False
        search_thread = threading.Thread(
            target=self._search_move,
            args=(time_controls,)
        )
        self.current_search_thread = search_thread
        search_thread.start()

    def _parse_time_controls(self, args: list) -> Dict[str, Any]:
        """
        Parse time control arguments.

        Args:
            args: Time control arguments

        Returns:
            Dictionary with time control parameters
        """
        controls: Dict[str, Any] = {
            'movetime': None,
            'wtime': None,
            'btime': None,
            'winc': None,
            'binc': None,
            'depth': None,
            'nodes': None,
            'infinite': False
        }

        i = 0
        while i < len(args):
            arg = args[i]

            if arg == "movetime" and i + 1 < len(args):
                try:
                    controls['movetime'] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif arg == "wtime" and i + 1 < len(args):
                try:
                    controls['wtime'] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif arg == "btime" and i + 1 < len(args):
                try:
                    controls['btime'] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif arg == "winc" and i + 1 < len(args):
                try:
                    controls['winc'] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif arg == "binc" and i + 1 < len(args):
                try:
                    controls['binc'] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif arg == "depth" and i + 1 < len(args):
                try:
                    controls['depth'] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif arg == "nodes" and i + 1 < len(args):
                try:
                    controls['nodes'] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif arg == "infinite":
                controls['infinite'] = True
                i += 1
            else:
                i += 1

        return controls

    def _search_move(self, time_controls: Dict[str, Any]) -> None:
        """
        Search for the best move with time management.

        Args:
            time_controls: Time control parameters
        """
        start_time = time.time()

        # Calculate time limit
        time_limit = self._calculate_time_limit(time_controls)

        if time_controls.get('infinite'):
            time_limit = float('inf')

        # Set search depth if specified
        if time_controls.get('depth'):
            self.chess_engine.set_depth(time_controls['depth'])

        # Get the best move
        best_move = self.chess_engine.get_move_with_time_limit(self.board, time_limit)
        time.time() - start_time

        if not self.search_stopped:
            if best_move:
                print(f"bestmove {best_move}")
            else:
                print("bestmove 0000")  # No legal moves

    def _calculate_time_limit(self, time_controls: Dict[str, Any]) -> float:
        """
        Calculate time limit based on time controls.

        Args:
            time_controls: Time control parameters

        Returns:
            Time limit in seconds
        """
        # If movetime is specified, use it directly
        if time_controls.get('movetime'):
            return time_controls['movetime'] / 1000.0

        # Calculate based on remaining time
        if self.board.turn == "w" and time_controls.get('wtime'):
            base_time = time_controls['wtime'] / 1000.0
            increment = time_controls.get('winc', 0) / 1000.0
        elif self.board.turn == "b" and time_controls.get('btime'):
            base_time = time_controls['btime'] / 1000.0
            increment = time_controls.get('binc', 0) / 1000.0
        else:
            return 5.0  # Default 5 seconds

        # Simple time management: use 1/30th of remaining time
        time_limit = base_time / 30.0 + increment

        # Ensure minimum and maximum limits
        time_limit = max(0.1, min(time_limit, 30.0))

        return time_limit

    def _handle_stop(self) -> None:
        """Handle stop command."""
        self.search_stopped = True
        if self.current_search_thread and self.current_search_thread.is_alive():
            self.current_search_thread.join(timeout=1.0)

    def _handle_quit(self) -> None:
        """Handle quit command."""
        self.search_stopped = True
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
    """Main entry point for the advanced UCI engine."""
    engine = AdvancedUCIEngine()
    engine.run()


if __name__ == "__main__":
    main()
