import logging
from datetime import datetime

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from services.weather_service import WeatherService
from utils.logging import setup_logging
from utils.formatters import format_weather_response, format_error_response, format_json_error_response

# Load environment variables
load_dotenv()

# Configure logging
logger = setup_logging()


def main():
    """Main function to run the MCP server."""
    logger.info("Starting Weather MCP Server")
    mcp = FastMCP(name="Weather MCP Server")
    weather_service = WeatherService()

    @mcp.tool(
        "get_current_weather", 
        description="Get current weather information for any location worldwide. Provides temperature, humidity, wind, and other weather details."
    )
    async def get_current_weather(location: str) -> str:
        """
        Get current weather information for a specific location.
        
        Args:
            location: The city name, city with country, or coordinates (e.g., "London", "New York, US", "40.7128,-74.0060")
        
        Returns:
            Detailed weather information including temperature, humidity, wind, and description.
        """
        # Log incoming request
        logger.info(f"[TOOL REQUEST] get_current_weather called with location: '{location}'")
        
        try:
            logger.debug(f"Fetching weather data for location: {location}")
            weather_data = await weather_service.get_current_weather(location)
            
            # Log successful data retrieval
            logger.info(f"[DATA SUCCESS] Weather data retrieved for {weather_data.location}: {weather_data.temperature}°C, {weather_data.description}")
            
            # Format response using utility function
            response = format_weather_response(weather_data)
            
            # Log successful response
            logger.info(f"[RESPONSE SUCCESS] get_current_weather completed for '{location}' - formatted weather report generated")
            
            return response
            
        except ValueError as e:
            logger.warning(f"[VALIDATION ERROR] get_current_weather failed for location '{location}': {str(e)}")
            error_response = format_error_response(str(e))
            logger.debug(f"[RESPONSE ERROR] Returning validation error response: {error_response[:100]}...")
            return error_response
        except Exception as e:
            logger.error(f"[SYSTEM ERROR] get_current_weather failed for '{location}': {str(e)}")
            error_response = format_error_response(f"Failed to get weather data: {str(e)}")
            logger.debug(f"[RESPONSE ERROR] Returning system error response: {error_response[:100]}...")
            return error_response

    @mcp.tool(
        "get_weather_json", 
        description="Get current weather information in structured JSON format for integration purposes."
    )
    async def get_weather_json(location: str) -> str:
        """
        Get current weather information in JSON format.
        
        Args:
            location: The city name, city with country, or coordinates
        
        Returns:
            Weather information as a JSON string for easy parsing and integration.
        """
        # Log incoming request
        logger.info(f"[TOOL REQUEST] get_weather_json called with location: '{location}'")
        
        try:
            logger.debug(f"Fetching JSON weather data for location: {location}")
            weather_data = await weather_service.get_current_weather(location)
            
            # Log successful data retrieval
            logger.info(f"[DATA SUCCESS] JSON weather data retrieved for {weather_data.location}: {weather_data.temperature}°C, {weather_data.description}")
            
            json_response = weather_data.model_dump_json(indent=2)
            
            # Log successful response
            logger.info(f"[RESPONSE SUCCESS] get_weather_json completed for '{location}' - JSON response generated ({len(json_response)} chars)")
            logger.debug(f"[JSON RESPONSE] Content preview: {json_response[:200]}...")
            
            return json_response
            
        except Exception as e:
            logger.error(f"[SYSTEM ERROR] get_weather_json failed for '{location}': {str(e)}")
            error_response = format_json_error_response(str(e), location)
            logger.debug(f"[RESPONSE ERROR] Returning JSON error response: {error_response}")
            return error_response
    
    logger.info("Weather MCP Server started successfully")
    logger.info("Available tools: get_current_weather, get_weather_json")
    
    if not weather_service.api_key:
        logger.info("💡 To get real weather data, set the OPENWEATHER_API_KEY environment variable")
        logger.info("💡 Get a free API key at: https://openweathermap.org/api")
    
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
