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

weather_function = {
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

def weather_agent(message: str):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": message}],
        functions=[weather_function],
        function_call="auto"
    )
    
    if response.choices[0].message.function_call:
        function_name = response.choices[0].message.function_call.name
        arguments = json.loads(response.choices[0].message.function_call.arguments)
        
        if function_name == "get_current_weather":
            weather_data = get_current_weather(arguments["city"])
            return weather_data
    
    return response.choices[0].message.content

if __name__ == "__main__":
    user_input = input("Ask about weather: ")
    result = weather_agent(user_input)
    print(result)