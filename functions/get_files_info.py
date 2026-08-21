import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_abs_path = os.path.realpath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_abs_path, directory))
        
        label = "current" if directory == "." else f"'{directory}'"
        
        valid_target_dir = os.path.commonpath([working_abs_path, target_dir]) == working_abs_path
        
        items = [f"Results for {label} directory:"]
        
        if not valid_target_dir:
            items.append(f' Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return "\n".join(items)
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        dir_contents = os.listdir(target_dir)
                
        for item in dir_contents:
            size = os.path.getsize(os.path.join(target_dir, item))
            is_dir = os.path.isdir(os.path.join(target_dir, item))
            items.append(f" - {item}: file_size={size} bytes, is_dir={is_dir}")
            
        return "\n".join(items)
            
    except Exception:
        return "Error: something went wrong with getting files info"
            
            
            
            
            
    
    
    