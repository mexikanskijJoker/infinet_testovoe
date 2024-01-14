import logging
import os
import sys
from typing import Any, Optional

from textfsm import TextFSM, TextFSMTemplateError


class StatusParser:
    def __init__(self) -> None:
        self._file = sys.argv[1]

    # Получения данных после парсинга обрабатываемого файла при помощи шаблона
    def get_parsed_data(self) -> Optional[dict[str, Any]]:
        data = self._get_file_data()
        template = self._get_template()

        if data == None or template == None:
            return

        parsed_data = template.ParseText(data)[0]
        values = list(
            map(lambda i: '"' + i + '"' if not i.isdigit() else i, parsed_data)
        )
        output = {"LINK TIME": values[0], "MCS": values[1], "FRAMES": values[2]}

        return output

    # Извлечение содержимого обрабатываемого файла
    def _get_file_data(self) -> Optional[str]:
        text = ""

        file_extension = os.path.splitext(self._file)[1]

        if file_extension != ".txt":
            text = None
            logging.error("Обрабатываемый файл должен иметь расширение .txt")
            return

        try:
            with open(self._file, "r") as file:
                lines = file.readlines()

            if len(lines) == 1:
                text = None
                logging.error("Файл пуст")
                return

            for line in lines:
                text += line

        except FileNotFoundError:
            text = None
            logging.error("Файла с таким названием не существует")

        return text

    # Извлечение шаблона для парсинга обрабатываемого файла
    def _get_template(self) -> Optional[TextFSM]:
        template = None
        try:
            with open("template.txt", "r") as file:
                template = TextFSM(file)

        except FileNotFoundError:
            logging.error("Не найден файл шаблона для парсинга")

        except TextFSMTemplateError:
            logging.error("Неверный формат шаблона")

        return template


def main():
    logging.basicConfig(
        level=logging.INFO,
        filename="output.log",
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    status_parser = StatusParser()
    try:
        data = status_parser.get_parsed_data()
        for key, value in data.items():
            logging.info(f"{key}: {value}")
    except AttributeError:
        pass


if __name__ == "__main__":
    main()
