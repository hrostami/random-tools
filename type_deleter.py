import os
try:
    from icecream import ic
except ImportError:
    os.system('pip install icecream')
    from icecream import ic

def get_user_input():
    cwd = input('Enter the path to check or press Enter to check the current directory: ')
    cwd = os.getcwd() if cwd == '' else cwd

    file_type = input("Please enter the file type you want to delete: ")
    file_type = file_type if file_type.startswith('.') else f'.{file_type}'

    return cwd, file_type

def deleter( cwd: str, file_type: str) -> dict:
    removed_files = {}
    def delete_files_in_directory(directory):
        files_to_delete = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isdir(file_path):
                delete_files_in_directory(file_path)
            elif file_type in file:
                files_to_delete.append(file_path)

        if files_to_delete:
            removed_files[directory] = files_to_delete
            for file_path in files_to_delete:
                os.remove(file_path)

    try:
        delete_files_in_directory(cwd)
    except Exception as e:
        ic(e)
    finally:
        ic(removed_files)
    return removed_files
                
if __name__ == "__main__":
    cwd, file_type = get_user_input()
    deleter(cwd, file_type)