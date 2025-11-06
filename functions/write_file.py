import os
from config import *

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