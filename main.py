import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function

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
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
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
        returned_function = call_function(calls[0], verbose) 
        if returned_function.parts[0].function_response.response != None:
            if verbose == True:
                print(f"-> {returned_function.parts[0].function_response.response}")
        else:
            raise Exception("Function response was missing or malformed!")
    
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
