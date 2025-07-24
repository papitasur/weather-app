import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_current_weather(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    return response.json()

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
}

def weather_agent(message: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        tools=[weather_tool],
        tool_choice="auto"
    )
    
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if function_name == "get_current_weather":
            weather_data = get_current_weather(arguments["city"])
            
            # Format the weather data nicely
            if weather_data.get("cod") == 200:
                city = weather_data["name"]
                country = weather_data["sys"]["country"]
                temp = weather_data["main"]["temp"]
                feels_like = weather_data["main"]["feels_like"]
                description = weather_data["weather"][0]["description"].title()
                humidity = weather_data["main"]["humidity"]
                
                return f"""Weather in {city}, {country}:
Temperature: {temp}°C (feels like {feels_like}°C)
Condition: {description}
Humidity: {humidity}%"""
            else:
                return f"Error: {weather_data.get('message', 'Could not get weather data')}"
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Weather Agent is ready! Ask me about weather in any city.")
    print("Type 'quit' to exit.\n")
    
    while True:
        name = input("Enter the name of a city or quit: ")
        
        if name.lower().strip() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        result = weather_agent(name)
        print(f"Agent: {result}\n")