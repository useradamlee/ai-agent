import os

def get_file_content(working_directory, file_path):
    try:
        # print(file_path)
        # print("Working directory: " + os.path.abspath(working_directory))
        file_path = os.path.join(working_directory, file_path)

        if not os.path.abspath(file_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        MAX_CHARS = 10000
        with open(os.path.abspath(file_path), "r") as f:
            length = len(f.read())

        with open(os.path.abspath(file_path), "r") as f:
            if length > MAX_CHARS:
                return f.read(MAX_CHARS) + f' [...File "{file_path}" truncated at 10000 characters]'
            return f.read()
    except Exception as e:
        return(f"Error: {e}")