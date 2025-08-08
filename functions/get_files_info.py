import os 

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.abspath(os.path.join(working_directory,directory))
        working_directory_abs = os.path.abspath(working_directory)

        if not full_path.startswith(working_directory_abs):
            return f'''Error: Cannot list "{directory}" as it is outside the permitted working directory'''
        
        if os.path.isdir(full_path) == False:
            return f'Error: "{directory}" is not a directory'
        
        file_list = os.listdir(full_path)
        string = ""
        for f in file_list:
            full_file_path = f"{full_path}/{f}"
            file_size = os.path.getsize(full_file_path)
            is_dir = os.path.isdir(full_file_path)
            string += f" - {f}: file_size={file_size} bytes, is_dir={is_dir}\n"
            
        return string
    except Exception as e:
        return f"Error: {e}"
get_files_info("")