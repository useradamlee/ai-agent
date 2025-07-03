import os
from google import genai

def get_files_info(working_directory, directory=None):
    try:
        # debug statements:
        # print(f"-- Working dir absolute: {os.path.abspath(working_directory)}")
        # print(f"-- Directory absolute: {os.path.abspath(directory)}")      
        if directory == None or directory == ".":
            directory = working_directory
        else:
            directory = os.path.join(working_directory, directory)
        if not os.path.abspath(directory).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
        content_info = ""
        for item in os.listdir(directory):
            content_info += f"- {item}: file_size={os.path.getsize(os.path.join(directory, item))} bytes, is_dir={os.path.isdir(os.path.join(directory, item))}\n"
        return content_info
    except Exception as e:
        return(f"Error: {e}")
    

schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)