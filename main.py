import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")



def main():
    verbose = False
    if len(sys.argv) == 1:
        print("no prompt passed. program exiting") 
        sys.exit(1)
    if len(sys.argv) == 3 and sys.argv[2].lower() == "--verbose":
        verbose = True
    
    user_prompt = sys.argv[1]
    
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

    client = genai.Client(api_key=api_key)
    repsonse = client.models.generate_content(
        model='gemini-2.0-flash-001',
          contents= messages,
          config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
))
    
    calls = repsonse.function_calls
    if len(calls) > 0: 
        print(f"Calling function: {calls[0].name}({calls[0].args})") 
    else:
        if verbose == True:
            print(f"User prompt: {user_prompt}")
            print(repsonse.text)
            print(f"Prompt tokens: {repsonse.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {repsonse.usage_metadata.candidates_token_count}")
        else: 
            print(repsonse.text)



if __name__ == "__main__":
    main()
