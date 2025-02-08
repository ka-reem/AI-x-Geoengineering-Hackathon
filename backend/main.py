import os
from dotenv import load_dotenv
import groq

# Load environment variables
load_dotenv()

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

# Test the setup
if __name__ == "__main__":
    print("Welcome to the AI Chat Interface!")
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        try:
            response = get_response(user_input)
            print("\nAI:", response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")