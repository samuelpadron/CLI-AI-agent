import os
from config import MAX_CHARS


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Fetches content of a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the file to retrieve content from",
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_abs_path = os.path.realpath(working_directory)
        target = os.path.realpath(os.path.join(working_abs_path, file_path))
        
        label = "current" if file_path == "." else f"'{file_path}'"
        
        valid_target = os.path.commonpath([working_abs_path, target]) == working_abs_path
        
        if not valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'
            
        with open(target, "r") as f:
            file_content = f.read(MAX_CHARS)
            
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
        return file_content
    
    except OSError as e:
        return f'Error: Could not read file "{file_path}": {e.strerror or e}'