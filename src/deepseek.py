import os
from dotenv import load_dotenv
import groq
from pathlib import Path

# Find the root directory and load environment variables from there
root_dir = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(root_dir, '.env')
load_dotenv(dotenv_path)

# Initialize Groq client
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

# Simple function to test the setup
def get_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="deepseek-r1-distill-llama-70b-specdec",
        temperature=0.7,
    )
    return chat_completion.choices[0].message.content

def analyze_weather_data(data):
    weather_prompt = f"""
    Analyze this weather radar data in 2-3 sentences maximum:
    {data}
    
    Focus on: wind speed trends, precipitation levels (dBZ), and give a one-line weather summary.
    Be very concise and direct.
    """
    return get_response(weather_prompt)

if __name__ == "__main__":
    print("Welcome to the Weather Analysis Interface!")
    print("Paste your weather data and press Enter twice to analyze.")
    print("Type 'exit' to end the program.")
    
    while True:
        print("\nEnter weather data:")
        lines = []
        while True:
            line = input()
            if line.lower() == 'exit':
                print("Goodbye!")
                exit()
            if line == '':
                break
            lines.append(line)
        
        if not lines:
            continue
            
        weather_data = '\n'.join(lines)
        try:
            response = analyze_weather_data(weather_data)
            print("\nWeather Analysis:", response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")