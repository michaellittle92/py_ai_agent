import sys
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")



def main():
    if len(sys.argv) == 1:
        print("no prompt passed. program exiting") 
        sys.exit(1)
    prompt = sys.argv[1]
    client = genai.Client(api_key=api_key)
    repsonse = client.models.generate_content(model='gemini-2.0-flash-001', contents= prompt)
    print(repsonse.text)
    print(f"Prompt tokens: {repsonse.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {repsonse.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
