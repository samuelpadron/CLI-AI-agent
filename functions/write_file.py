import os


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write to, relative to the working directory",
                },
                "content": {
                  "type": "string",
                  "description": "Content to write to file"  
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str,content: str) -> str:
    try:
        working_abs_path = os.path.realpath(working_directory)
        target_path = os.path.realpath(os.path.join(working_abs_path, file_path))
        
        valid_path = os.path.commonpath([working_abs_path, target_path]) == working_abs_path
        
        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Make sure parent directories exist
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        with open(target_path, mode="w+") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
    except Exception:
        return f"Error: Something went wrong writing to file: {file_path}"