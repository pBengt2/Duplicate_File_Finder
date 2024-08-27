import sys
import os

FOLDER_TO_CHECK = "D:\camera"


def get_subdirectories(root_path, recursive=True):
    subdirectories = []
    all_paths = os.listdir(root_path)
    for path in all_paths:
        temp_path = os.path.join(root_path, path)
        if os.path.isdir(temp_path):
            subdirectories.append(temp_path)
    if recursive:
        for subdir in subdirectories:
            new_subdirs = get_subdirectories(subdir, True)
            subdirectories.extend(new_subdirs)
    return subdirectories


def gather_files(directory, base_only=False):
    if base_only:
        file_list = []
        all_paths = os.listdir(directory)
        for path in all_paths:
            temp_path = os.path.join(directory, path)
            if not os.path.isdir(temp_path):
                file_list.append(temp_path)
        return file_list
    else:
        file_list = []
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                file_list.append(subdir + os.sep + file)

        return file_list


def add_to_dict(file_dict, file_path):
    try:
        file_dict[os.path.getsize(file_path)].append(file_path)
    except KeyError:
        file_dict[os.path.getsize(file_path)] = [file_path]


def find_dups_old(root_path, check_subdirs=True, recursive_subdirs=True):
    all_dirs = [root_path]
    if check_subdirs:
        all_dirs.extend(get_subdirectories(root_path, recursive_subdirs))

    full_file_list = []
    for directory in all_dirs:
        file_list = gather_files(directory, True)
        full_file_list.extend(file_list)

    file_dict = {}
    for temp_file in full_file_list:
        add_to_dict(file_dict, temp_file)

    for item in file_dict.items():
        if len(item[1]) > 1:
            print(item)


def find_dups(root_path, check_subdirs=True, recursive_subdirs=True):
    full_file_list = gather_files(root_path)
    print(full_file_list)

    file_dict = {}
    for temp_file in full_file_list:
        add_to_dict(file_dict, temp_file)

    for item in file_dict.items():
        if len(item[1]) > 1:
            print(item)


def main():
    find_dups(FOLDER_TO_CHECK)


if __name__ == '__main__':
    main()
