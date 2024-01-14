import argparse
import logging
import os
from typing import Any, Optional

from textfsm import TextFSM, TextFSMTemplateError

from config import HELP_TEXT, LOG_LEVEL, OUTPUT_FILENAME, TEMPLATE_FILENAME
from error_messages import (
    EMPTY_FILE,
    FILE_DOES_NOT_EXIST,
    INCORRECT_EXTENSION,
    INCORRECT_TEMPLATE,
    TEMPLATE_FILE_NOT_FOUND,
)


class StatusParser:
    def __init__(self) -> None:
        self._file = self._parse_args()

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
            logging.error(INCORRECT_EXTENSION)
            return

        try:
            with open(self._file, "r") as file:
                lines = file.readlines()

            if len(lines) == 1:
                text = None
                logging.error(EMPTY_FILE)
                return

            for line in lines:
                text += line

        except FileNotFoundError:
            text = None
            logging.error(FILE_DOES_NOT_EXIST)

        return text

    # Извлечение шаблона для парсинга обрабатываемого файла
    def _get_template(self) -> Optional[TextFSM]:
        template = None
        try:
            with open(TEMPLATE_FILENAME, "r") as file:
                template = TextFSM(file)

        except FileNotFoundError:
            logging.error(TEMPLATE_FILE_NOT_FOUND)

        except TextFSMTemplateError:
            logging.error(INCORRECT_TEMPLATE)

        return template

    # Получение наименования файла, введённого в консоль для обработки
    def _parse_args(self) -> str:
        parser = argparse.ArgumentParser("Парсинг файла в формате txt")
        parser.add_argument("file", help=HELP_TEXT)
        args = parser.parse_args()

        return args.file


def main():
    logging.basicConfig(
        level=LOG_LEVEL,
        filename=OUTPUT_FILENAME,
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    status_parser = StatusParser()
    try:
        data = status_parser.get_parsed_data()
        for key, value in data.items():
            logging.info(f"{key}: {value}")
            print(f"{key}: {value}")
    except AttributeError:
        pass


if __name__ == "__main__":
    main()
