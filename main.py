import os
import sys
from dotenv import load_dotenv
from google import genai
from functions.get_files_info import schema_get_files_info, available_functions
from functions.call_function import call_function
from google.genai.types import Content, Part

system_prompt = """
Your goal is to provide a comprehensive answer using the tools, or to fix the code as requested

When a user asks a question or makes a request, make a function call plan. 

You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

*Only* give a response that isn't a tool call once you believes you has completed the task and no more tool calls are needed 
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    sys.exit("Please provide a prompt as the first argument.")

user_input = sys.argv[1]

messages = []
messages.append(Content(role="user", parts=[Part(text=user_input)]))

# loop the agent
for _ in range(20):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        )
    )
    verbose = "--verbose" in sys.argv

    function_calls = []
    final_assistant_text = None

    for candidate in response.candidates:
        messages.append(candidate.content)
        for part in candidate.content.parts:
            if part.function_call is not None:
                function_calls.append(part.function_call)
            elif part.text:
                # Only use assistant's text if there were NO function calls
                final_assistant_text = part.text

    if function_calls:
        for function_call_part in function_calls:
            # call_function must return a Content object, which you append directly
            messages.append(call_function(function_call_part, verbose))
    else:
        if final_assistant_text:
            print("Final response:")
            print(final_assistant_text)
        break