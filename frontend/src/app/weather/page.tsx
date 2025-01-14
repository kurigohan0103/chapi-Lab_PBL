"use client";

import { useState, useEffect } from "react";
import "../../styles/Weather.css";

interface WeatherData {
    id: number;
    location: string;
    precipitation_chance: number;
}

export default function WeatherPage() {
    const [weatherData, setWeatherData] = useState<WeatherData[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchWeather() {
            try {
                const response = await fetch("http://localhost:8000/api/weather");
                if (response.ok) {
                    const data: WeatherData[] = await response.json();
                    setWeatherData(data);
                } else {
                    setError("Failed to fetch weather data");
                }
            } catch (error) {
                console.error("Error fetching weather data:", error);
                setError("Error fetching weather data");
            } finally {
                setLoading(false);
            }
        }

        fetchWeather();
    }, []);

    return (
        <div className="container">
            {loading ? (
                <p className="loading">Loading...</p>
            ) : error ? (
                <p className="error">{error}</p>
            ) : (
                <ul className="weatherList">
                    {weatherData.map((weather) => (
                        <li key={weather.id} className="weatherItem">
                            {weather.precipitation_chance >= 60 ? (
                                <>
                                    <img
                                        src="/images/rainy-icon.png"
                                        alt="Rainy"
                                        className="weatherIcon"
                                    />
                                </>
                            ) : (
                                <>
                                    <img
                                        src="/images/sunny-icon.png"
                                        alt="Sunny"
                                        className="weatherIcon"
                                    />
                                </>
                            )}
                            <p className="weatherLocation">場所: {weather.location}</p>
                            <p className="weatherChance">
                                降水確率: {weather.precipitation_chance}%
                            </p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
