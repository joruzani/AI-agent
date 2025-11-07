import os
from config import *
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_work = os.path.abspath(working_directory)
    abs_path = os.path.abspath(full_path)

    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_path.startswith(abs_work + os.sep) and abs_path != abs_work:
       return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            ["python", abs_path, *args],
            timeout=30,
            capture_output=True, 
            text=True, 
            cwd=abs_work
        )
        st_out =f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}\n"
        st_out += f"Process exited with code {completed_process.returncode}\n" if completed_process.returncode != 0 else ""
        st_out += f"No output produced" if not completed_process.stdout else ""
        return st_out
    except Exception as e:
        return f"Error: running subprocess: {e}"


