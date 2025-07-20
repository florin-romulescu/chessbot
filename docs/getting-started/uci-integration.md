# UCI Integration

ChessBot supports the Universal Chess Interface (UCI) protocol, allowing it to work with popular chess GUIs like XBoard, Arena, Fritz, and others.

## What is UCI?

The Universal Chess Interface (UCI) is a standard protocol for chess engines to communicate with chess GUIs. It allows engines to:

- Receive position information
- Calculate and return the best moves
- Handle time controls
- Configure engine options

## Using ChessBot with XBoard

### 1. Install XBoard

First, install XBoard on your system:

**Ubuntu/Debian:**
```bash
sudo apt-get install xboard
```

**macOS:**
```bash
brew install xboard
```

**Windows:**
Download from the [XBoard website](https://www.gnu.org/software/xboard/).

### 2. Configure ChessBot as an Engine

#### Option A: Using the Engine Configuration File

1. Copy the engine configuration file:
```bash
cp config/chessbot.eng ~/.xboard/engines/
```

2. Edit the configuration file to point to your ChessBot installation:
```bash
nano ~/.xboard/engines/chessbot.eng
```

Update the paths:
```ini
[ENGINE]
Name=ChessBot
Command=python3 /path/to/your/chessbot/scripts/run_uci_engine.py
Protocol=uci
Dir=/path/to/your/chessbot
```

#### Option B: Manual Configuration in XBoard

1. Start XBoard
2. Go to **Engine** → **Manage Engine List**
3. Click **Add**
4. Configure the engine:
   - **Name**: ChessBot
   - **Command**: `python3 /path/to/your/chessbot/scripts/run_uci_engine.py`
   - **Protocol**: UCI
   - **Directory**: `/path/to/your/chessbot`

### 3. Playing Against ChessBot

1. Start XBoard
2. Go to **Engine** → **ChessBot** (or your configured engine name)
3. The engine will connect and you can start playing

## Using ChessBot with Other GUIs

### Arena

1. Start Arena
2. Go to **Engines** → **Install New Engine**
3. Select **UCI** protocol
4. Browse to your ChessBot script: `scripts/run_uci_engine.py`
5. Configure engine options if needed

### Fritz/CB

1. Start Fritz or ChessBase
2. Go to **Engine** → **Install Engine**
3. Select the UCI protocol
4. Point to your ChessBot script
5. The engine will be available for play

## Engine Options

ChessBot supports the following UCI options:

- **Depth**: Search depth (1-10, default: 3)
- **Debug**: Enable debug output (true/false, default: false)

### Setting Options

You can set engine options in several ways:

1. **In XBoard**: Engine → Configure Engine
2. **In Arena**: Engine → Configure
3. **Via UCI command**: `setoption name Depth value 5`

## Testing the UCI Engine

You can test the UCI engine locally:

```bash
# Test basic functionality
python3 scripts/test_uci.py

# Run the engine directly
python3 scripts/run_uci_engine.py
```

Then send UCI commands manually:
```
uci
isready
position startpos
go movetime 1000
```

## Advanced UCI Engine

For better time management and more features, use the advanced UCI engine:

```bash
# Install the advanced engine
uv run chessbot-uci-advanced

# Or run directly
python3 -m chessbot.uci_engine_advanced
```

The advanced engine includes:
- Better time management
- Support for time controls
- Threaded search
- More UCI options

## Troubleshooting

### Common Issues

1. **Engine not found**: Check the path in your engine configuration
2. **Permission denied**: Make sure the script is executable: `chmod +x scripts/run_uci_engine.py`
3. **Python not found**: Ensure Python 3 is installed and in your PATH
4. **Import errors**: Make sure you're running from the correct directory

### Debug Mode

Enable debug mode to see detailed communication:

```bash
# In XBoard: Engine → Configure → Debug: true
# Or via UCI: setoption name Debug value true
```

### Testing Communication

You can test the UCI communication manually:

```bash
echo -e "uci\nisready\nposition startpos\ngo movetime 1000" | python3 scripts/run_uci_engine.py
```

## Performance Tips

1. **Increase search depth** for stronger play (but slower)
2. **Use the advanced engine** for better time management
3. **Adjust time controls** based on your preferences
4. **Monitor CPU usage** during long games

## Next Steps

- [Learn about the engine algorithms](../api/chessengine.md)
- [Explore the board representation](../api/chessboard.md)
- [Contribute to the project](../development/contributing.md) 