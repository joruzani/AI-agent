import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import *
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    match function_call_part.name:
        case "get_file_content":
            result = get_file_content("./calculator", **function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )

        case "get_files_info":
            result = get_files_info("./calculator", **function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )

        case "write_file":
            result = write_file("./calculator", **function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )

        case "run_python_file":
            result = run_python_file("./calculator", **function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )

        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={
                            "error": f"Unknown function: {function_call_part.name}"
                        },
                    )
                ],
            )


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
            schema_run_python_file,
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
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if len(prompt) > 2:
            if prompt[2] == "--verbose":
                print(f"User prompt: {prompt[1]}")
                print(
                    f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
                )
    else:
        print("Need to provide a prompt")
        sys.exit(1)

    if response.function_calls:
        for fc in response.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")
            call_response = call_function(fc, verbose=True)
            if not call_response.parts[0].function_response.response:
                raise Exception("Fatal Exception: All your base are belong to us")
            else:
                print(f"-> {call_response.parts[0].function_response.response}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
