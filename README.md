# Weather MCP Server 🌤️

A production-grade Model Context Protocol (MCP) server that provides real-time weather information for any location worldwide.

## Features ✨

- **Real-time Weather Data**: Get current weather conditions for any location
- **Multiple Output Formats**: Both human-readable and JSON formats available
- **Production-Grade**: Comprehensive error handling, input validation, and logging
- **Caching**: Built-in intelligent caching to reduce API calls and improve performance
- **Free Tier Support**: Works with mock data when no API key is provided
- **Global Coverage**: Supports cities worldwide with country-specific queries

## Tools Available 🛠️

### 1. `get_current_weather`
Get current weather information in a human-readable format with emojis and clear formatting.

**Parameters:**
- `location` (string): City name, "City, Country", or coordinates ("lat,lon")

**Example Usage:**
```
Location: "London"
Location: "New York, US" 
Location: "40.7128,-74.0060"
```

### 2. `get_weather_json`
Get current weather information in structured JSON format for integration purposes.

**Parameters:**
- `location` (string): Same as above

## Setup Instructions 🚀

### 1. Install Dependencies

```bash
# Navigate to project directory
cd hello-world-mcp

# Install dependencies
pip install -e .
```

### 2. Configure API Key (Optional but Recommended)

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Copy the environment template:
   ```bash
   copy .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```

### 3. Run the Server

```bash
# Run the MCP server
python main.py
```

Or use the VS Code task:
- Press `Ctrl+Shift+P`
- Search for "Tasks: Run Task"
- Select "Run MCP Server (STDIO)"

## Production Features 🏭

### Error Handling
- **Network timeouts**: Graceful handling of slow connections
- **Invalid locations**: Clear error messages for non-existent places
- **API rate limits**: Proper handling of API quota exceeded scenarios
- **Malformed responses**: Validation of API response structure

### Caching System
- **Intelligent caching**: 10-minute cache duration for each location
- **Memory efficient**: Automatic cleanup of expired cache entries
- **Performance boost**: Reduced API calls and faster responses

### Input Validation
- **Location sanitization**: Automatic trimming and validation
- **Empty input protection**: Prevents API calls with invalid data
- **Type checking**: Runtime validation using Pydantic models

### Logging
- **Comprehensive logging**: All operations are logged with appropriate levels
- **Error tracking**: Detailed error information for debugging
- **Performance monitoring**: Request timing and caching statistics

## Weather Data Provided 📊

Each weather response includes:

- 🌡️ **Temperature**: Current temperature in Celsius and Fahrenheit
- 🌡️ **Feels Like**: Apparent temperature considering humidity and wind
- 💧 **Humidity**: Relative humidity percentage
- 🌪️ **Wind**: Speed (m/s) and direction (degrees)
- 🏔️ **Pressure**: Atmospheric pressure in hectopascals
- ☁️ **Conditions**: Current weather description
- 👁️ **Visibility**: Visibility distance in kilometers
- 🕐 **Timestamp**: When the data was last updated

## Examples 💡

### Human-Readable Format
```
🌤️ **Weather for London, GB**

📊 **Temperature**: 15.2°C (59.4°F)
🌡️ **Feels Like**: 14.1°C
💧 **Humidity**: 64%
🌪️ **Wind**: 4.6 m/s
🏔️ **Pressure**: 1019 hPa
☁️ **Conditions**: Partly Cloudy
👁️ **Visibility**: 10.0 km
🕐 **Updated**: 2026-02-22T10:30:00

*Data provided by OpenWeatherMap*
```

### JSON Format
```json
{
  "location": "London, GB",
  "temperature": 15.2,
  "temperature_fahrenheit": 59.4,
  "humidity": 64,
  "description": "Partly Cloudy",
  "feels_like": 14.1,
  "pressure": 1019,
  "wind_speed": 4.6,
  "wind_direction": 240,
  "visibility": 10.0,
  "uv_index": null,
  "timestamp": "2026-02-22T10:30:00"
}
```

## Troubleshooting 🔧

### Common Issues

1. **"Invalid API key" error**
   - Verify your API key is correct in the `.env` file
   - Ensure you've activated your OpenWeatherMap account

2. **"Location not found" error**
   - Check spelling of the city name
   - Try adding country code: "Paris, FR" instead of just "Paris"
   - For US cities, use state code: "Portland, OR"

3. **Timeout errors**
   - Check your internet connection
   - The server will retry automatically in most cases

4. **Rate limit exceeded**
   - Free tier allows 1000 calls/day and 60 calls/minute
   - Consider upgrading your OpenWeatherMap plan for higher limits

### Mock Data Mode
When no API key is provided, the server runs in mock data mode for demonstration purposes. This is useful for:
- Testing the MCP server functionality
- Development and debugging
- Demonstrations without API dependencies

## Integration with VS Code 🔗

### Option 1: Direct MCP Client Configuration

To use this MCP server with MCP-compatible clients (VS Code extensions, Claude Desktop, etc.):

1. **Start the server** in this VS Code instance or via command line
2. **Configure your MCP client** with the following configuration:

```json
{
    "servers": {
        "Weather MCP Server": {
            "type": "stdio",
            "command": "python",
            "args": [
                "main.py"
            ],
            "cwd": "/path/to/your/hello-world-mcp"
        }
    },
    "inputs": []
}
```

**Platform-specific paths:**
- **Windows**: `"cwd": "C:\\Users\\YourName\\path\\to\\hello-world-mcp"`
- **macOS/Linux**: `"cwd": "/home/username/path/to/hello-world-mcp"`

### Configuration File Locations

**Claude Desktop:**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

**VS Code Extensions:**
- Configuration varies by extension (Continue, MCP Client, etc.)
- Usually found in VS Code settings or extension-specific config files

### Option 2: VS Code Extension Integration

For VS Code extensions that support MCP:

1. **Install MCP client extension** in the target VS Code instance (e.g., "Continue", "MCP Client")
2. **Configure the extension** to connect to this server:
   - **Command**: `python main.py` or full path to python executable
   - **Working Directory**: Path to your `hello-world-mcp` folder
   - **Type**: `stdio`
3. **Use the weather tools** through the client interface

### Option 3: Command Line Usage

You can also run the server directly and interact with it via stdio:

```bash
# Navigate to your project directory
cd /path/to/hello-world-mcp

# Activate virtual environment (if using one)
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Run the server
python main.py
```

## API Reference 📚

### OpenWeatherMap API
- **Base URL**: https://api.openweathermap.org/data/2.5
- **Documentation**: https://openweathermap.org/api
- **Rate Limits**: 60 calls/minute, 1,000 calls/day (free tier)

## License 📄

This project is open source. Check the license file for details.

## Support 🆘

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs for detailed error information
3. Ensure your OpenWeatherMap API key is valid
4. Verify internet connectivity