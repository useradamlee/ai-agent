import os

def write_file(working_directory, file_path, content):
    # file_path = os.path.join(working_directory, file_path)
    try:
        file_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(file_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(os.path.abspath(file_path), "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return(f"Error: {e}")