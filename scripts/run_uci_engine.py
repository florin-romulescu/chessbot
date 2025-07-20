#!/usr/bin/env python3
"""Script to run the ChessBot UCI engine."""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chessbot.uci_engine import main

if __name__ == "__main__":
    main()
