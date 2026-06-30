# Physics Solver MCP Server

A Model Context Protocol (MCP) server that provides physics calculation tools for Claude Desktop and other MCP clients.

## Features

This server provides the following physics calculation tools:

- **kinetic_energy**: Calculate kinetic energy (KE = 1/2 × mass × velocity²)
- **gravitational_potential_energy**: Calculate gravitational potential energy (PE = mass × g × height)
- **subtract**: Basic subtraction operation

## Installation

### 1. Install Dependencies

```powershell
cd d:\Programming\physics-solver-mcp
pip install fastmcp
```

Or using uv:
```powershell
uv pip install fastmcp
```

### 2. Test the Server

Run the server directly to test it:
```powershell
python physics_server.py
```

## Setup for Claude Desktop

### 1. Locate Claude Desktop Config

The Claude Desktop configuration file is located at:
```
%APPDATA%\Claude\claude_desktop_config.json
```

Or:
```
C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json
```

### 2. Add MCP Server Configuration

Edit the `claude_desktop_config.json` file and add your physics server:

```json
{
  "mcpServers": {
    "physics-solver": {
      "command": "python",
      "args": [
        "d:\\Programming\\physics-solver-mcp\\physics_server.py"
      ]
    }
  }
}
```

**Note**: Use double backslashes (`\\`) in the path for JSON.

### 3. Restart Claude Desktop

After saving the configuration file, completely quit and restart Claude Desktop for the changes to take effect.

## Verification

Once configured, you should see the physics tools available in Claude Desktop. You can test them with queries like:

- "Calculate the kinetic energy of an 800 kg car moving at 25 m/s"
- "What is the potential energy of a 10 kg object at a height of 50 meters?"

## Troubleshooting

### Server Won't Start

1. Make sure FastMCP is installed:
   ```powershell
   pip install fastmcp
   ```

2. Test the server manually:
   ```powershell
   python physics_server.py
   ```

### Claude Can't Find the Server

1. Check the path in `claude_desktop_config.json` is correct
2. Use absolute paths with double backslashes
3. Restart Claude Desktop completely (quit from system tray)

### Tools Not Appearing

1. Check Claude Desktop logs at: `%APPDATA%\Claude\logs`
2. Verify the JSON configuration is valid (use a JSON validator)
3. Make sure there are no syntax errors in the config file

## Development

To modify or add new physics formulas, edit `physics_server.py` and add new functions decorated with `@mcp.tool()`.

Example:
```python
@mcp.tool()
def calculate_force(mass: float, acceleration: float) -> float:
    """Calculate force using F = ma"""
    return mass * acceleration
```

## License

MIT
