"""Main entry point for the ChessBot application."""

import sys
from typing import Optional

from .board import ChessBoard
from .engine import ChessEngine


class ChessBot:
    """
    Main chess bot class that orchestrates the game.

    This class manages the chess game state, handles moves, and coordinates
    between the board representation and the chess engine.
    """

    def __init__(self, engine_depth: int = 3):
        """
        Initialize the chess bot.

        Args:
            engine_depth: The search depth for the chess engine
        """
        self.board = ChessBoard()
        self.engine = ChessEngine(depth=engine_depth)
        self.game_over = False

    def make_move(self, move_uci: str) -> bool:
        """
        Make a move on the chess board.

        Args:
            move_uci: Move in UCI format (e.g., 'e2e4')

        Returns:
            True if the move was legal and executed, False otherwise
        """
        if self.game_over:
            return False

        if self.board.is_valid_move(move_uci):
            self.board.make_move(move_uci)
            return True
        return False

    def get_best_move(self) -> Optional[str]:
        """
        Get the best move from the chess engine.

        Returns:
            The best move in UCI format, or None if no move is available
        """
        if self.game_over:
            return None

        return self.engine.get_best_move(self.board)

    def play_game(self) -> None:
        """
        Play a complete chess game against the engine.

        This method runs an interactive chess game where the user
        plays against the chess engine.
        """
        print("Welcome to ChessBot!")
        print("Enter moves in UCI format (e.g., 'e2e4')")
        print("Type 'quit' to exit")

        while not self.game_over:
            print(f"\n{self.board}")

            # Player's turn
            if self.board.turn == "w":
                move = input("Your move: ").strip()
                if move.lower() == "quit":
                    break

                if not self.make_move(move):
                    print("Invalid move! Try again.")
                    continue
            else:
                # Engine's turn
                print("Engine is thinking...")
                engine_move = self.get_best_move()
                if engine_move:
                    print(f"Engine plays: {engine_move}")
                    self.make_move(engine_move)
                else:
                    print("Engine has no moves available.")
                    break

            # Check for game end conditions
            if self.board.is_checkmate:
                winner = "Black" if self.board.turn == "w" else "White"
                print(f"\nCheckmate! {winner} wins!")
                self.game_over = True
            elif self.board.is_stalemate:
                print("\nStalemate! The game is a draw.")
                self.game_over = True
            elif self.board.is_insufficient_material:
                print("\nInsufficient material! The game is a draw.")
                self.game_over = True


def main() -> None:
    """Main entry point for the chess bot application."""
    try:
        bot = ChessBot()
        bot.play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
