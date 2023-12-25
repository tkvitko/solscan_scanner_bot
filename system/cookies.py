import os


def load_cookies():
    cookies_folder = '../cookies'
    list_cookies = []

    cookies_files_list = [f for f in os.listdir(cookies_folder) if os.path.isfile(os.path.join(cookies_folder, f))]
    for cookies_file in cookies_files_list:

        with open(os.path.join(cookies_folder, cookies_file), 'r') as source:
            cookies = source.read().splitlines()

        for cookie in cookies:
            if cookie:
                if cookie.startswith('#'):
                    continue

                dict_cookie = {}
                list_val = cookie.split('\t')
                # print(list_val)
                if list_val[-1].find(';') == -1:
                    dict_cookie['name'] = list_val[-2]
                    dict_cookie['value'] = list_val[-1]
                    dict_cookie['domain'] = list_val[0]
                    dict_cookie['expires'] = list_val[-3]
                    dict_cookie['path'] = list_val[2]
                    # dict_cookie['secure'] = list_val[3]
                if dict_cookie:
                    list_cookies.append(dict_cookie)

    return list_cookies


if __name__ == '__main__':
    print(load_cookies())

