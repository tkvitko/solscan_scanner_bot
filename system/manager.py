from typing import List, Set

from system.messenger import Messenger
from system.parser import Parser
from system.logs import logger


class LinksManager:
    def __init__(self) -> None:
        self.links = dict()  # список ссылок для парсинга
        self.parser = Parser()
        self.messenger = Messenger()

    def _add_link(self, link: str) -> None:
        # добавить новую ссылку в список для парсинга
        self.links[link] = None
        logger.info(f'Link has been added: {link}')

    def _remove_link(self, link: str) -> None:
        # удалить ссылку из списка для парсинга
        self.links.pop(link)
        logger.info(f'Link has been deleted: {link}')

    def _refresh_links_list(self, new_links: Set[str]) -> None:
        """
        Актуализирует список ссылок для парсинга на основе переданного нового списка
        :param new_links: актуальный список ссылок
        :return:
        """
        current_links_set = set(self.links.keys())
        links_to_add = new_links - current_links_set
        links_to_remove = current_links_set - new_links

        for link in links_to_add:
            self._add_link(link)
        for link in links_to_remove:
            self._remove_link(link)
        logger.debug(f'Links list has been renewed')

    def parse_links(self) -> None:
        """
        Парсинг всех ссылок по списку и отправка данных в телеграм, если данные изменились
        :return:
        """
        for link, old_data in self.links.items():
            new_data, new_amount_text = self.parser.get_from_url(url=link)
            if new_data:
                logger.debug(f'Old data is {old_data}')
                logger.debug(f'New data is {new_data}')
                self.links[link] = new_data
                if old_data is not None and new_data is not None and old_data != new_data:
                # if old_data != new_data:
                    self.messenger.send_message_to_telegram(
                        f'New transaction on {link}:\n\n[Transaction Details]({new_data}) {new_amount_text}')
                    logger.debug(f'Data {new_data} for link {link} has been sent to telegram')
            else:
                logger.warning(f'Cant parse new data for {link}')
        logger.debug(f'{len(self.links)} links has been parsed')

    def read_links_from_file(self, filename: str) -> None:
        """
        Чтение списка ссылок для парсинга из файла
        :param filename: имя файла
        :return:
        """
        with open(filename, encoding='utf-8') as f:
            links_from_source = [line.strip() for line in f.readlines()]
            logger.debug(f'Links list has read from file')
            self._refresh_links_list(new_links=set(links_from_source))


if __name__ == '__main__':
    # testing
    manager = LinksManager()
    links = {'1', '2', '3', '4'}
    manager._refresh_links_list(new_links=links)
    manager.links['2'] = 'test'
    print(manager.links)
    links_2 = {'2', '4', '6'}
    manager._refresh_links_list(new_links=links_2)
    print(manager.links)
