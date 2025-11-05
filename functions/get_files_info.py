import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_work = os.path.abspath(working_directory)
    abs_path = os.path.abspath(full_path)

    #print(full_path)
    #print(abs_work)
    #print(abs_path)

    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    if not abs_path.startswith(abs_work + os.sep) and abs_path != abs_work:
       return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:    
        dir_contents = os.listdir(abs_path)
        contents = "\n".join(list(map(lambda file: f"- {file}: file_size={os.path.getsize(abs_path+os.sep+file)} bytes, is_dir={os.path.isdir(abs_path+os.sep+file)}", dir_contents)))
        #if directory == ".":
        #    return f"Results for current directory:\n{contents}"
        #else:
        #    return f"Results for '{directory}' directory:\n{contents}"
        return contents
    except Exception as e:
        return f"Error listing files: {e}"

