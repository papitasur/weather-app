import requests
import json

def get_weather(city_name, api_key):
    try:
        # OpenWeatherMap API URL
        url = f"http://api.openweathermap.org/data/2.5/weather"
        
        # Parameters for the API request
        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric'  # Use Celsius
        }
        
        # Make API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Return JSON data
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error getting weather data: {e}")
        return None

def display_weather(weather_data):
    if not weather_data:
        print("No weather data to display")
        return
    
    # Extract basic information
    city = weather_data['name']
    country = weather_data['sys']['country']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    
    # Display the weather information
    print("\n" + "="*40)
    print(f"WEATHER FOR {city}, {country}")
    print("="*40)
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Description: {description.title()}")
    print("="*40)

def main():
    """
    Main function to run the weather program
    """
    print("🌤️  Simple Weather Display")
    print("="*30)
    
    # API Key - Get this from openweathermap.org
    api_key = "your-api-key-here"
    
    while True:
        # Get city name from user
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        
        if city.lower() == 'quit':
            print("Goodbye!")
            break
        
        if city:
            # Get and display weather
            weather_data = get_weather(city, api_key)
            display_weather(weather_data)
        else:
            print("Please enter a valid city name")

if __name__ == "__main__":
    main()
