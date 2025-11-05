import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = sys.argv

    if len(prompt) > 1:
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt[1])]),
        ]
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
        )
        if len(prompt) > 2:
            if prompt[2] == "--verbose":
                print(f"User prompt: {prompt[1]}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("Need to provide a prompt")
        sys.exit(1)


    print(response.text)


if __name__ == "__main__":
    main()
