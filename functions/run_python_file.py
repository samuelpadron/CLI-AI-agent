import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Fetches content of a specified filerelative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to run in python",
                },
                "args": {
                    "type": "array",
                    "description": "Arguments for the python program",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_abs_path = os.path.realpath(working_directory)
        absolute_file_path = os.path.realpath(os.path.join(working_abs_path, file_path))
        
        valid_path = os.path.commonpath([working_abs_path, absolute_file_path]) == working_abs_path
        
        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not absolute_file_path[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", absolute_file_path]
        
        if args:
            command.extend(args)
            
        process = subprocess.run(command,capture_output=True, text= True, timeout=30)
        return_code = process.returncode
        output = ""
        if return_code != 0:
             output += f"Process exited with code {return_code} "
            
        if not process.stdout and not process.stderr:
            output += "No output produced. "
            
        if process.stdout:
            output += f"STDOUT: {process.stdout} "
            
        if process.stderr:
            output += f"STDERR: {process.stderr} "
                    
        return output
            
    except Exception as e:
        return f"Error: executing Python file: {e}"