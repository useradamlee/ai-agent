import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import schema_get_files_info, available_functions

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    sys.exit("Please provide a prompt as the first argument.")

user_input = sys.argv[1]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=user_input,
    config=genai.types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )
)

if response.function_calls:
    message_to_print = f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})"
else:
    message_to_print = response.text

if "--verbose" in sys.argv:
    print(f"User prompt: {user_input}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(message_to_print)
else:
    print(message_to_print)

