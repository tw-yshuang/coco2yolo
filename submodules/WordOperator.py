'''
    This code edit by YU-SHUN,
    Welcome to contact me if you have any questions.
    e-mail: tw.yshuang@gmail.com
    Github: https://github.com/tw-yshuang
'''

def str_format(word: str, style: str = 'default', fore: str = 'default', background: str = 'default'):
    '''Style_table
    ---
    |顯示方式  |         Style      |    variable   |
    |:-------:|:------------------:|:-------------:|
    |0        |       終端默認設置   |      default  |
    |1        |       高亮顯示       |      hight    |
    |2        |       低亮顯示       |      less     |
    |22       |       一般顯示       |      normal   |
    |4        |       使用下劃線     |      line     |
    |24       |       刪去下劃線     |      unline   |
    |5        |       閃爍          |     blink     |
    |25       |       去閃爍        |     unblnk    |
    |7        |       反白顯示       |      negative |
    |27       |       非反顯        |     unnegative|
    |8        |       不可見        |     blank     |
    |28       |       可見          |     unblank   |


    Color_table
    ---
    |Fore   |   Background   |    顏色   |  variable   |
    |:-----:|:--------------:|:--------:|:------------:|
    |30     |      40        |    黑色   |   black     |
    |31     |      41        |    紅色   |   r         |
    |32     |      42        |    綠色   |   g         |
    |33     |      43        |    黃色   |   y         |
    |34     |      44        |    藍色   |   b         |
    |35     |      45        |    洋紅   |   pink      |
    |36     |      46        |    青色   |   sky       |
    |37     |      47        |    白色   |   white     |
    '''
    style_dict = {
        'default': 0,
        'hight': 1,
        'less': 2,
        'normal': 22,
        'line': 4,
        'unline': 24,
        'blink': 5,
        'unblnk': 25,
        'negative': 7,
        'unnegative': 27,
        'blank': 8,
        'unblank': 28,
    }
    color_dict = {
        'r': 1,
        'g': 2,
        'y': 3,
        'b': 4,
        'pink': 5,
        'sky': 6,
        'white': 7,
        'black': 0,
    }

    variable_ls = ['style', 'fore', 'background']
    word_setting = ''
    error_ls = []

    for i, variable in enumerate([style, fore, background]):
        if variable == 'default':
            continue

        if i == 0:
            try:
                word_setting = f'{style_dict[style.lower()]}'
            except KeyError:
                word_setting = '0'
                error_ls.append(variable_ls[i])
        else:
            i -= 1
            try:
                word_setting += f';{30+i*10+color_dict[variable.lower()]}'
            except KeyError:
                error_ls.append(variable_ls[i])

    word_setting += 'm'

    error_msg = ''
    for error in error_ls:
        error_msg += f"Worng {error} parameter!! Use default parameter for {error}.\n"

    if error_msg != '':
        print(str_format(error_msg, fore='r'))

    return f'\033[{word_setting}{word}\033[0m'


def replace_keyword(filename: str, target_word: str, replace_word: str):
    new_f = ''
    with open(filename, 'r') as f:
        new_f = f.read().replace(target_word, replace_word)
    with open(filename, 'w') as f:
        f.write(new_f)


def find_keyword(filename: str, keyword: str):
    keyword_set = set()

    with open(filename, 'r') as f:
        for line in f.readlines():
            keyword_index = line.find(keyword)
            if keyword_index != -1:
                keyword_set.add(line[keyword_index + len(keyword) :])

    return list(sorted(keyword_set))


# Decorator
def spend_time(func):
    import time

    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(
            f"func: {str_format(f'{func.__name__:25.25s}', fore='g')} | time: {str_format(f'{time.time()-start_time:10.4e}', fore='y')}sec"
        )
        return result

    return wrap


def ask_yn(question, fore: str = 'default'):
    '''Style_table
    Color_table
    ---
    |Fore   |    顏色   |  variable   |
    |:-----:|:--------:|:------------:|
    |30     |    黑色   |   black     |
    |31     |    紅色   |   r         |
    |32     |    綠色   |   g         |
    |33     |    黃色   |   y         |
    |34     |    藍色   |   b         |
    |35     |    洋紅   |   pink      |
    |36     |    青色   |   sky       |
    |37     |    白色   |   white     |
    '''
    reply = input(f"{str_format(question, fore=fore)} [y/n]: ").lower().strip()
    if reply[0] in ('y', '1') or reply[:] == 'true':
        return True
    elif reply[0] in ('n', '0') or reply[:] == 'false':
        return False
    else:
        print(str_format(f"Wrong answer, please enter again.", fore='r'))
        return ask_yn(question)
