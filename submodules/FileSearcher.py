'''
    This code edit by YU-SHUN,
    Welcome to contact me if you have any questions.
    e-mail: tw.yshuang@gmail.com
    Github: https://github.com/tw-yshuang
'''

import os, glob

from WordOperator import str_format


def get_filenames(dir_path: str, specific_name: str, withDirPath=True) -> list:
    '''
    get_filenames
    -----
    This function can find any specific name under the dir_path, even the file inside directories.

    specific_name:
        >>> Can type any word or extension.
        e.g. '*cat*', '*.csv', '*cat*.csv',
    '''
    
    if dir_path[-1] != '/':
        dir_path += '/'

    filenames = glob.glob(f'{dir_path}**/{specific_name}', recursive=True)

    if '*.' == specific_name[:2]:
        filenames.extend(glob.glob(f'{dir_path}**/{specific_name[1:]}', recursive=True))

    if withDirPath is False:
        dir_path_len = len(dir_path)
        filenames = [filename[dir_path_len:] for filename in filenames]

    return filenames


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
