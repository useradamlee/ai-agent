import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import schema_get_files_info, available_functions
from functions.call_function import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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

verbose = "--verbose" in sys.argv

if response.candidates[0].content.parts[0].function_call:
    function_call_part = response.candidates[0].content.parts[0].function_call
    function_call_result = call_function(function_call_part, verbose)
    
    try:
        response_data = function_call_result.parts[0].function_response.response
        if verbose:
            if 'result' in response_data:
                result_text = response_data['result']
                print(f"-> {result_text}")
            else:
                print(f"-> {response_data}")
        print("\nFunction Completed!\n")
    except (AttributeError, IndexError):
        raise Exception("Invalid function call result structure")
else:
    message_to_print = response.text
    print(message_to_print)

if verbose:
    print(f"User prompt: {user_input}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")