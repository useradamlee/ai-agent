import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    sys.exit("Please provide a prompt as the first argument.")

user_input = sys.argv[1]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=user_input)
    
if "--verbose" in sys.argv:
    print(f"User prompt: {user_input}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)
else:
    print(response.text)


