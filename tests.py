from functions.get_files_info import get_files_info

test_out = get_files_info("calculator",".")
expected_out = ''' - main.py: file_size=576 bytes, is_dir=False
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=92 bytes, is_dir=True
'''
print(test_out)

test_out = get_files_info("calculator", "pkg")
expected_out = '''
 - calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False
'''
print(test_out)

print("Result for '/bin' directory:")

test_out = get_files_info("calculator", "/bin")
expected_out = '''Error: Cannot list "/bin" as it is outside the permitted working directory'''
print(test_out)
print("Result for '../' directory:")
test_out = get_files_info("calculator", "../")
expected_out = '''Error: Cannot list "../" as it is outside the permitted working directory'''
print(test_out)
