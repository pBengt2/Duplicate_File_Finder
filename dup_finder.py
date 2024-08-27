import os
import filecmp
from enum import Enum

# Make sure to set desired FOLDER_TO_CHECK + MIN_FILE_SIZE_MB +
FOLDER_TO_CHECK = r"F:\pictures"
FILE_TYPE = ""
ONLY_COMPARE_SIZE_AND_NAME = True  #
SHALLOW_CMP = False  # faster but false positives
DISPLAY_IN_MB = True
MIN_FILE_SIZE_MB = 0
DEBUG_PRINT = False


class CompareType(Enum):
    SIZE_ONLY = 0  # Very fast, lots of false positives.
    SIZE_AND_NAME = 1  # Very fast, can miss files (ie, if renamed), and also can have false positives (ie, same name + file size, different contents)
    SHALLOW_CMP = 2  # Slower, can still potentially have a false positive, but unlikely in most cases.
    FULL_CMP = 3  # Slowest. Shouldn't lead to any false positives or misses.


CURRENT_COMPARE_TYPE = CompareType.SIZE_AND_NAME


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
                if FILE_TYPE is not None and FILE_TYPE != "" and FILE_TYPE not in file:
                    continue
                full_name = subdir + os.sep + file
                if os.path.getsize(full_name) <= MIN_FILE_SIZE_MB * 1048576:
                    continue
                file_list.append(full_name)

        return file_list


def add_to_dict(temp_dict, key, val):
    try:
        temp_dict[key].append(val)
    except KeyError:
        temp_dict[key] = [val]


def _get_potential_dups(file_list):
    file_dict = {}
    for temp_file in file_list:
        add_to_dict(file_dict, os.path.getsize(temp_file), temp_file)

    potential_dups = []
    for item in file_dict.items():
        if len(item[1]) > 1:
            # print(item)
            potential_dups.append(item[1])
    return potential_dups


def _file_compare(f1, f2):
    if CURRENT_COMPARE_TYPE == CompareType.SIZE_AND_NAME:
        return f1.split('\\')[-1] == f2.split('\\')[-1]
    elif CURRENT_COMPARE_TYPE == CompareType.SHALLOW_CMP:
        return filecmp.cmp(f1, f2, shallow=True)
    else:
        return filecmp.cmp(f1, f2, shallow=False)


def _get_verified_dups_dict(potential_dups):
    # Can be sped up with hashing potentially...
    dups_dict = {}
    for dups_list in potential_dups:
        dup_indices = []
        for i in range(len(dups_list) - 1):
            for j in range(i + 1, len(dups_list)):
                if j not in dup_indices and _file_compare(dups_list[i], dups_list[j]):
                    dup_indices.append(j)
                    add_to_dict(dups_dict, dups_list[i], dups_list[j])
    return dups_dict


def find_dups(root_path, check_subdirs=True, recursive_subdirs=True):
    full_file_list = gather_files(root_path)

    if DEBUG_PRINT:
        print("** checking " + str(len(full_file_list)) + " files.")

    potential_dups = _get_potential_dups(full_file_list)

    if DEBUG_PRINT:
        print("** checking " + str(len(potential_dups)) + " potential dups.")

    dups_dict = _get_verified_dups_dict(potential_dups)

    return dups_dict


def print_dups(dups_dict):
    print("\nDuplicates found: ")
    dups_list = []
    for item in dups_dict.items():
        if DISPLAY_IN_MB:
            file_size = int(os.path.getsize(item[0]) / 1048576)
        else:
            file_size = os.path.getsize(item[0])
        dups = [file_size, item[0]]
        dups.extend(item[1])
        dups_list.append(dups)

    dups_list.sort(reverse=True)
    for dup in dups_list:
        print(dup)


def main():
    dups_dict = find_dups(FOLDER_TO_CHECK)
    print_dups(dups_dict)


if __name__ == '__main__':
    main()
