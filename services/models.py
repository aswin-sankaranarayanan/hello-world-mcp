"""Weather data models and schemas."""

from typing import Optional
from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    """Weather data model for structured responses."""
    location: str = Field(..., description="Location name")
    temperature: float = Field(..., description="Temperature in Celsius")
    temperature_fahrenheit: float = Field(..., description="Temperature in Fahrenheit")
    humidity: int = Field(..., description="Humidity percentage")
    description: str = Field(..., description="Weather description")
    feels_like: float = Field(..., description="Feels like temperature in Celsius")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    wind_direction: Optional[int] = Field(None, description="Wind direction in degrees")
    visibility: Optional[float] = Field(None, description="Visibility in km")
    uv_index: Optional[float] = Field(None, description="UV index")
    timestamp: str = Field(..., description="Data timestamp")