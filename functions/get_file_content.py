import os 
from functions.config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):

    full_path = os.path.abspath(os.path.join(working_directory,file_path))
    working_directory_abs = os.path.abspath(working_directory)

    if not full_path.startswith(working_directory_abs):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
        if len(file_content_string) == MAX_CHARS + 1:
            file_content_string = file_content_string[:MAX_CHARS]
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file and gets the first 10,000 characters from a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of file you want to read",
            ),
        },
    ),
)