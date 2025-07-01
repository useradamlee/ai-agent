import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        original_file_path = file_path
        file_path = os.path.join(working_directory, file_path)

        if not os.path.abspath(file_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{original_file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file_path):
            return f'Error: File "{original_file_path}" not found.'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        output = subprocess.run(["uv", "run", os.path.abspath(file_path)], timeout=30, capture_output=True, cwd=working_directory)
        if output.stdout == "" and output.stderr == "":
            return "No output produced"
        output_string = f"STDOUT: {output.stdout.decode('utf-8')}\n"
        output_string += f"STDERR: {output.stderr.decode('utf-8')}\n"
        if output.returncode != 0:
            output_string += f"Process exited with code {output.returncode}"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    