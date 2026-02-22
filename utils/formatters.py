"""Response formatting utilities."""

from services.models import WeatherData


def format_weather_response(weather_data: WeatherData) -> str:
    """Format weather data into a readable response."""
    return f"""🌤️ **Weather for {weather_data.location}**

📊 **Temperature**: {weather_data.temperature}°C ({weather_data.temperature_fahrenheit}°F)
🌡️ **Feels Like**: {weather_data.feels_like}°C
💧 **Humidity**: {weather_data.humidity}%
🌪️ **Wind**: {weather_data.wind_speed} m/s
🏔️ **Pressure**: {weather_data.pressure} hPa
☁️ **Conditions**: {weather_data.description}
👁️ **Visibility**: {weather_data.visibility} km
🕐 **Updated**: {weather_data.timestamp}

*Data provided by OpenWeatherMap*"""


def format_error_response(error_message: str) -> str:
    """Format error message into a standardized response."""
    return f"❌ Error: {error_message}"


def format_json_error_response(error_message: str, location: str) -> str:
    """Format error message as JSON response."""
    from datetime import datetime
    error_response = {
        "error": error_message,
        "location": location, 
        "timestamp": datetime.now().isoformat()
    }
    return str(error_response)