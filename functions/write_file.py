import os
from config import *
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_work = os.path.abspath(working_directory)
    abs_path = os.path.abspath(full_path)


    if not abs_path.startswith(abs_work + os.sep) and abs_path != abs_work:
       return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_path):
        try:
            with open(abs_path, "w") as file:
                file.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {file_path} couldn't be created"
    try:
        with open(abs_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {file_path} couldn't be written"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Create a file withe the provided content, if the file exists it overrides the contet",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file ar string",
            ),
        },
    ),
)
