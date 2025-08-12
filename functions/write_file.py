import os 
from google.genai import types

def write_file(working_directory, file_path, content):

    full_path = os.path.join(working_directory, file_path)

    full_path_abs = os.path.abspath(full_path)
    working_directory_abs = os.path.abspath(working_directory)

    if not full_path_abs.startswith(working_directory_abs):
         return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        except Exception as e:
            return f"Error: {e}"
        
    try:
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes a new file or overwrites existing files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of file you want to write to or over",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content that you want to write",
            )
        },
    ),
)