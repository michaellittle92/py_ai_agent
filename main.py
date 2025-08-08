import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    repsonse = client.models.generate_content(model='gemini-2.0-flash-001', contents= messages,)
    
    if verbose == True:
        print(f"User prompt: {user_prompt}")
        print(repsonse.text)
        print(f"Prompt tokens: {repsonse.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {repsonse.usage_metadata.candidates_token_count}")
    else: 
        print(repsonse.text)

if __name__ == "__main__":
    main()
