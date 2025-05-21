from datetime import datetime
from scripts.forecast import get_forecast_with_ui
from  scripts.actual import get_actual_weather_today
from  scripts.comparison import compare_forecast_and_actual

def main():
    cities = ["surat", "mumbai", "delhi", "london", "paris", "tokyo", "new york", "sydney", "dubai", "singapore"]

    # Fetch monthly forecast for these cities
    get_forecast_with_ui(cities)

    # Fetch today's actual data for these cities
    get_actual_weather_today(cities)

    # Compare forecast and actual data & generate reports
    compare_forecast_and_actual()

if __name__ == "__main__":
    main()
