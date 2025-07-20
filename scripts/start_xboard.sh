#!/bin/bash
# Script to start XBoard with ChessBot engine

echo "Starting XBoard with ChessBot engine..."
echo "Engine path: /home/florinrm/chessbot/scripts/run_uci_engine.py"
echo ""

# Start XBoard with engine configuration
xboard -fcp "uv run python3 /home/florinrm/chessbot/scripts/run_uci_engine.py" -fd "/home/florinrm/chessbot" 