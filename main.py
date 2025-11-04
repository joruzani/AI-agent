import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = sys.argv
    if len(prompt) > 1:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=f"{prompt[1]}"
        )
    else:
        print("Need to provide a prompt")
        sys.exit(1)


    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
