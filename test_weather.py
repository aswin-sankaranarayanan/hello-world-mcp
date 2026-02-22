#!/usr/bin/env python3
"""
Quick test script to check weather API and get London weather
"""
import asyncio
import sys
import os

# Add the current directory to Python path so we can import from main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import WeatherService

async def test_weather():
    """Test weather service directly"""
    print("🌤️ Testing Weather Service...")
    
    weather_service = WeatherService()
    
    # Check API key status
    if weather_service.api_key:
        print(f"✅ API Key found: {weather_service.api_key[:8]}...")
    else:
        print("ℹ️ No API key found - will use mock data")
    
    try:
        print("\n🌍 Getting weather for London...")
        weather_data = await weather_service.get_current_weather("London")
        
        # Format the output nicely
        print(f"\n🌤️ **Weather for {weather_data.location}**")
        print(f"📊 **Temperature**: {weather_data.temperature}°C ({weather_data.temperature_fahrenheit}°F)")
        print(f"🌡️ **Feels Like**: {weather_data.feels_like}°C")
        print(f"💧 **Humidity**: {weather_data.humidity}%")
        print(f"🌪️ **Wind**: {weather_data.wind_speed} m/s")
        print(f"🏔️ **Pressure**: {weather_data.pressure} hPa")
        print(f"☁️ **Conditions**: {weather_data.description}")
        print(f"👁️ **Visibility**: {weather_data.visibility} km")
        print(f"🕐 **Updated**: {weather_data.timestamp}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nℹ️ This could be due to:")
        print("  - Invalid API key")
        print("  - Network connectivity issues")
        print("  - API service being down")

if __name__ == "__main__":
    asyncio.run(test_weather())