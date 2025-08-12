import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]): 
    
    full_path = os.path.join(working_directory, file_path)

    full_path_abs = os.path.abspath(full_path)
    working_directory_abs = os.path.abspath(working_directory)

    if not full_path_abs.startswith(working_directory_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path_abs):
         return f'Error: File "{file_path}" not found.'
    
    if file_path[-3:] != '.py':
        return  f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["python", full_path_abs]
        if args:
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, timeout=30, cwd=working_directory)
        
        std_out = completed_process.stdout.decode("utf-8")
        std_err = completed_process.stderr.decode("utf-8")

        if len(std_err) == 0 and len(std_out) == 0:
            return "No output produced."
        
        output = f"STDOUT: {std_out}, STDERR: {std_err}."

        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and returns any output that is generated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of file you want to run",
            ),
            "args": 
            types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments that are needed to pass into the python program you want to run. If the program taks no arguments, pass in an empty list",
            )
        },
    ),
)    
#completed_process has:

   # completed_process.stdout - the output
   # completed_process.stderr - any errors
   # completed_process.returncode