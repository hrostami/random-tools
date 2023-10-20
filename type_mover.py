import os
import json


red = '\033[0;31m'
blue = '\033[0;34m'
yellow = '\033[0;33m'
green = '\033[0;32m'
plain = '\033[0m'

def colored(message: str, color: str, is_input=False) -> str:
    if not is_input:
        try:
            print(f"{color}{message}{plain}")
        except Exception as e:
            print(f'Error occurred while coloring:\n{e}\n')
            print(message)
        user_input = ''
    else:
        try:
            user_input = input(f"{color}{message}{plain}")
        except Exception as e:
            print(f'Error occurred while coloring:\n{e}\n')
            user_input = input(message)

    return user_input


def get_user_input():
    cwd = colored('\nEnter the path to check or press Enter to check the current directory: ', yellow, is_input=True)
    cwd = os.getcwd() if cwd == '' else cwd

    file_type = colored("\nPlease enter the file type you want to move: ", yellow, is_input=True)
    file_type = file_type if file_type.startswith('.') else f'.{file_type}'

    return cwd, file_type


def reverser(cwd: str, file_type: str):
    moved_files = {}
    move_dir = os.path.join(cwd,f'{file_type[1:]}_files')


    def move_files_in_directory(directory):
        files_to_move = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isdir(file_path):
                move_files_in_directory(file_path)
            elif file_type in file:
                files_to_move.append(file_path)

        if files_to_move:
            for file_path in files_to_move:
                subdirectory = os.path.dirname(file_path).replace(f'{move_dir}\\', "")
                moved_subdirectory = os.path.join(cwd, subdirectory)
                new_path = os.path.join(moved_subdirectory, os.path.basename(file_path))
                os.rename(file_path, new_path)
                moved_files[subdirectory] = moved_files.get(subdirectory, []) + [os.path.basename(new_path)]

    try:
        move_files_in_directory(move_dir)
        for dir in moved_files.keys():os.rmdir(os.path.join(move_dir, dir))
        os.rmdir(move_dir)
    except Exception as e:
        colored(f"An error occurred: {e}", red)
    finally:
        output = os.path.join(cwd,f'reversed_{file_type[1:]}.json')
        with open(output, 'w') as file:
            json.dump(moved_files, file, indent=4)
        os.remove(os.path.join(cwd,f'moved_{file_type[1:]}.json'))
        colored("\nReversed Files:", green)
        colored('----------------------------------------------', blue)
        for directory, files in moved_files.items():
            colored(f"\nSubdirectory: {directory}", green)
            for file in files:
                colored(f"  {file}", plain)
        colored('----------------------------------------------\n', blue)

def mover(cwd: str, file_type: str):
    moved_files = {}

    def move_files_in_directory(directory):
        files_to_move = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isdir(file_path):
                move_files_in_directory(file_path)
            elif file_type in file:
                files_to_move.append(file_path)

        if files_to_move:
            move_dir = os.path.join(cwd,f'{file_type[1:]}_files')
            for file_path in files_to_move:
                subdirectory = os.path.dirname(file_path).replace(f'{cwd}\\', "")
                moved_subdirectory = os.path.join(move_dir, subdirectory)
                os.makedirs(moved_subdirectory, exist_ok=True)
                new_path = os.path.join(moved_subdirectory, os.path.basename(file_path))
                os.rename(file_path, new_path)
                moved_files[subdirectory] = moved_files.get(subdirectory, []) + [os.path.basename(new_path)]

    try:
        move_files_in_directory(cwd)
    except Exception as e:
        colored(f"An error occurred: {e}", red)
    finally:
        output = os.path.join(cwd,f'moved_{file_type[1:]}.json')
        with open(output, 'w') as file:
            json.dump(moved_files, file, indent=4)
        colored("\nMoved Files:", green)
        colored('----------------------------------------------', blue)
        for directory, files in moved_files.items():
            colored(f"\nSubdirectory: {directory}", green)
            for file in files:
                colored(f"  {file}", plain)
        colored('----------------------------------------------\n', blue)

cwd, file_type = get_user_input()
move_dir = os.path.join(cwd,f'{file_type[1:]}_files')
if os.path.exists(move_dir):
    colored(f'\nThe directory {file_type[1:]}_files already exists!', red)
    op = colored('\nDo you want Reverse the operation or Proceed (R/P)? ',yellow,is_input=True)
    if op.lower() == 'p':
        mover(cwd, file_type)
    elif op.lower() == 'r':
        reverser(cwd, file_type)
    else:
        colored('\nWrong input, exiting...\n', yellow)
else:
    mover(cwd, file_type)