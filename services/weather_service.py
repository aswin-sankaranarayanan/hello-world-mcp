"""Weather service for fetching and managing weather data."""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

import httpx

from .models import WeatherData

logger = logging.getLogger(__name__)


class WeatherService:
    """Production-grade weather service with error handling and caching."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.timeout = 10.0
        self._cache: Dict[str, tuple[WeatherData, datetime]] = {}
        self._cache_duration = timedelta(minutes=10)  # Cache for 10 minutes
        
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY not found. Using free tier with limitations.")
    
    def _get_cache_key(self, location: str) -> str:
        """Generate cache key for location."""
        return f"weather_{location.lower().strip()}"
    
    def _is_cache_valid(self, timestamp: datetime) -> bool:
        """Check if cached data is still valid."""
        return datetime.now() - timestamp < self._cache_duration
    
    def _get_from_cache(self, location: str) -> Optional[WeatherData]:
        """Get weather data from cache if valid."""
        cache_key = self._get_cache_key(location)
        if cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if self._is_cache_valid(timestamp):
                logger.info(f"Returning cached weather data for {location}")
                return data
            else:
                # Remove expired cache entry
                del self._cache[cache_key]
        return None
    
    def _cache_data(self, location: str, data: WeatherData) -> None:
        """Cache weather data."""
        cache_key = self._get_cache_key(location)
        self._cache[cache_key] = (data, datetime.now())
    
    async def get_current_weather(self, location: str) -> WeatherData:
        """Get current weather for a location with comprehensive error handling."""
        # Input validation
        if not location or not location.strip():
            raise ValueError("Location cannot be empty")
        
        location = location.strip()
        
        # Check cache first
        cached_data = self._get_from_cache(location)
        if cached_data:
            return cached_data
        
        # If no API key, use mock data for demo purposes
        if not self.api_key:
            logger.warning(f"No API key provided, returning mock data for {location}")
            return self._get_mock_weather_data(location)
        
        url = f"{self.base_url}/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Fetching weather data for {location}")
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                weather_data = self._parse_weather_response(data, location)
                
                # Cache the result
                self._cache_data(location, weather_data)
                
                return weather_data
                
        except httpx.TimeoutException:
            logger.error(f"Timeout while fetching weather data for {location}")
            raise Exception(f"Weather service timeout for location: {location}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Location '{location}' not found. Please check the spelling.")
            elif e.response.status_code == 401:
                raise Exception("Invalid API key. Please check your OpenWeather API key.")
            elif e.response.status_code == 429:
                raise Exception("API rate limit exceeded. Please try again later.")
            else:
                logger.error(f"HTTP error {e.response.status_code} for {location}: {e.response.text}")
                raise Exception(f"Weather service error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Unexpected error fetching weather for {location}: {str(e)}")
            raise Exception(f"Failed to fetch weather data: {str(e)}")
    
    def _parse_weather_response(self, data: Dict[str, Any], location: str) -> WeatherData:
        """Parse OpenWeather API response into structured data."""
        try:
            main = data["main"]
            weather = data["weather"][0]
            wind = data.get("wind", {})
            
            temp_celsius = main["temp"]
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            
            return WeatherData(
                location=f"{data['name']}, {data['sys']['country']}",
                temperature=round(temp_celsius, 1),
                temperature_fahrenheit=round(temp_fahrenheit, 1),
                humidity=main["humidity"],
                description=weather["description"].title(),
                feels_like=round(main["feels_like"], 1),
                pressure=main["pressure"],
                wind_speed=round(wind.get("speed", 0), 1),
                wind_direction=wind.get("deg"),
                visibility=round(data.get("visibility", 0) / 1000, 1) if data.get("visibility") else None,
                uv_index=None,  # UV index requires separate API call
                timestamp=datetime.now().isoformat()
            )
        except KeyError as e:
            logger.error(f"Missing required field in weather response: {e}")
            raise Exception(f"Invalid weather data format: missing {e}")
    
    def _get_mock_weather_data(self, location: str) -> WeatherData:
        """Return mock weather data when no API key is available."""
        return WeatherData(
            location=f"{location} (Mock Data)",
            temperature=22.5,
            temperature_fahrenheit=72.5,
            humidity=65,
            description="Partly Cloudy (Demo)",
            feels_like=24.0,
            pressure=1013,
            wind_speed=3.2,
            wind_direction=180,
            visibility=10.0,
            uv_index=5.0,
            timestamp=datetime.now().isoformat()
        )