import os
from typing import List


def load_cookies() -> List:
    cookies_folder = '../cookies'
    cookies = []

    cookies_files_list = [f for f in os.listdir(cookies_folder) if os.path.isfile(os.path.join(cookies_folder, f))]

    for cookies_file in cookies_files_list:
        with open(os.path.join(cookies_folder, cookies_file), encoding='utf-8') as source:
            cookies = source.read().splitlines()

        for cookie in cookies:
            if cookie:
                if cookie.startswith('#'):
                    continue

                dict_cookie = {}
                list_val = cookie.split('\t')
                if list_val[-1].find(';') == -1:
                    dict_cookie['name'] = list_val[-2]
                    dict_cookie['value'] = list_val[-1]
                    dict_cookie['domain'] = list_val[0]
                    dict_cookie['expires'] = list_val[-3]
                    dict_cookie['path'] = list_val[2]
                    # dict_cookie['secure'] = list_val[3]
                if dict_cookie:
                    cookies.append(dict_cookie)

    return cookies


if __name__ == '__main__':
    # test
    print(load_cookies())
