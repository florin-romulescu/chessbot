#!/usr/bin/env python3
"""Test script for the UCI engine."""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chessbot.uci_engine import UCIEngine


def test_uci_communication():
    """Test basic UCI communication."""
    print("Testing UCI engine communication...")

    # Create engine instance
    engine = UCIEngine()

    # Test UCI info
    print("\n1. Testing UCI info:")
    engine._send_uci_info()

    # Test ready
    print("\n2. Testing ready:")
    engine._send_ready()

    # Test position setting
    print("\n3. Testing position setting:")
    engine._handle_position(["startpos"])
    print(f"Board FEN: {engine.board.get_fen()}")

    # Test move generation
    print("\n4. Testing move generation:")
    engine._handle_go(["movetime", "1000"])

    print("\nUCI engine test completed!")


def test_uci_commands():
    """Test UCI command parsing."""
    print("\nTesting UCI command parsing...")

    engine = UCIEngine()

    # Test commands
    test_commands = [
        "uci",
        "isready",
        "setoption name Depth value 5",
        "ucinewgame",
        "position startpos",
        "position startpos moves e2e4 e7e5",
        "go movetime 1000",
        "stop",
        "quit"
    ]

    for cmd in test_commands:
        print(f"\nTesting command: {cmd}")
        engine._handle_command(cmd)


if __name__ == "__main__":
    print("ChessBot UCI Engine Test")
    print("=" * 30)

    test_uci_communication()
    test_uci_commands()

    print("\nAll tests completed!")
