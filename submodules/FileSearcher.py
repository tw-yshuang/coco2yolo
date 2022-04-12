'''
    This code edit by YU-SHUN,
    Welcome to contact me if you have any questions.
    e-mail: tw.yshuang@gmail.com
    Github: https://github.com/tw-yshuang
'''

import os, sys, glob
from os import walk, mknod

sys.path.append(os.path.abspath(__package__))
from WordOperator import str_format


def get_filenames(dir_path: str, specific_name: str, withDirPath=True, isImported=False) -> list:
    '''
    get_filenames
    -----
    This function can find any specific name under the dir_path, even the file inside directories.

    specific_name:
        >>> Can type any word or extension.
        e.g. '*cat*', '*.csv', '*cat*.csv'
    '''
    filenames = []
    if dir_path[-1] != '/':
        dir_path += '/'

    if isImported is True:
        imported_root_ls = read_imported_root_from_txt()
    else:
        imported_root_ls = []

    for root, dirs, file in walk(dir_path):
        load_filenames = glob.glob(f'{root}/{specific_name}')

        if imported_root_ls == ['']:
            if len(load_filenames) == 1:
                filenames.append(load_filenames)
            else:
                filenames.extend(load_filenames)
        else:
            for filename in load_filenames:
                check_num = 0
                for imported_root in imported_root_ls:
                    if imported_root == filename:
                        check_num = 1
                        break
                if check_num == 1:
                    continue
                filenames.append(filename if withDirPath is True else filename[len(dir_path) :])

    return filenames


def read_imported_root_from_txt() -> list:
    path = "./already_imported_root.txt"
    try:
        imported_root_info = open(path).read()
    except FileNotFoundError:
        mknod(path)
        imported_root_info = []

    imported_root_ls = imported_root_info.split(',\n')
    return imported_root_ls


def write_imported_root_to_txt(filename_root: str) -> None:
    imported_root_info = open("already_imported_root.txt", "r")
    if imported_root_info.read() == "":
        imported_root_info = open("already_imported_root.txt", "w", encoding="utf-8")
        imported_root_info.write(str(filename_root))
    else:
        imported_root_info = open("already_imported_root.txt", "a", encoding="utf-8")
        imported_root_info.write(",\n" + str(filename_root))
    imported_root_info.close()


def check2create_dir(dir: str):
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
            print(str_format(f"Successfully created the directory: {dir}", fore='g'))
            return False
        else:
            return True
    except OSError:
        raise OSError(str_format(f"Fail to create the directory {dir} !", fore='r'))


if __name__ == "__main__":
    path = "Data"
    specific_name = ".jpg"
    filenames = get_filenames(path, specific_name, isImported=True)

    for filename in filenames:
        write_imported_root_to_txt(filename)
