import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = sys.argv
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
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file
    ]
)

    if len(prompt) > 1:
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt[1])]),
        ]
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
        )
        if len(prompt) > 2:
            if prompt[2] == "--verbose":
                print(f"User prompt: {prompt[1]}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("Need to provide a prompt")
        sys.exit(1)


    if response.function_calls:
        for fc in response.function_calls:
           print(f"Calling function: {fc.name}({fc.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
