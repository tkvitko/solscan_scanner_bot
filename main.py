import configparser
from time import sleep

from system.manager import LinksManager

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read("./config.ini")
    source_file = (config["parser"]["links_filename"])
    timeout = int(config["parser"]["timeout_in_secs"])

    manager = LinksManager()
    while True:
        manager.read_links_from_file(filename=source_file)  # обновить данные из файла
        manager.parse_links()   # спарсить актуальный список
        sleep(timeout)
