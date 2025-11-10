import os
from config import *
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_work = os.path.abspath(working_directory)
    abs_path = os.path.abspath(full_path)


    if not abs_path.startswith(abs_work + os.sep) and abs_path != abs_work:
       return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_path) as file:
            contents = file.read()
            if len(contents) > CHAR_LIMIT:
                contents = contents[:CHAR_LIMIT]
                contents += f"[...File \"{file_path}\" truncated at 10000 characters]"
            return contents
    except Exception as e:
        return f"Error: reading error {e}"


schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Gets the contents of the file trunecated to 10k chars",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path",
            ),
        },
    ),
)
