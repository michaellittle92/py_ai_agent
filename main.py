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
    

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    
    client = genai.Client(api_key=api_key)
    try:
        for i in range(20):
            if i >= 19:
                print("Maximum number of iterations reached, a solution has not been found, program is exiting.")
                break
            result = generate_content(client=client, messages=messages, verbose=verbose)
            if result:  # if we got a final text response
                print(result)
                break
    except Exception as e:
        print(e)

def generate_content(client, messages, verbose=False):
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
          contents= messages,
          config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
))
    
    calls = response.function_calls
    if calls and len(calls) > 0: 

        for candidate in response.candidates:
            messages.append(candidate.content)
        function_responses = []
        for call in calls:
            returned_function = call_function(call, verbose) 
            if returned_function.parts[0].function_response.response != None:
                function_responses.append(returned_function.parts[0])
                if verbose == True:
                    print(f"-> {returned_function.parts[0].function_response.response}")
            else:
                raise Exception("Function response was missing or malformed!")
        messages.append(types.Content(role="user", parts=function_responses))
        return None
        
        
    else:
        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    return response.text

if __name__ == "__main__":
    main()