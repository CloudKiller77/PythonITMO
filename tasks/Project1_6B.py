"""
Создайте сценарий, который использует список имен файлов CSV в качестве источника для копирования содержимого этих
файлов в плоский файл. Текущая дата и время должны быть добавлены к имени файла в качестве префикса перед копированием.
Каждая операция копирования должна быть записана в файл журнала на локальном компьютере.
Исключения для файлов, которые не были найдены, также должны быть записаны в журнал.
Пояснение к заданию:
На входе программы должен быть список имён файлов CSV, сами файлы произвольно содержания, например те,
с которыми вы уже работали. Программа должна принять список, скопировать содержимое каждого из них в текстовый файл
(на ваше усмотрение в отдельные файлы или общий, идея - должна быть копия данных, в задании только есть требование к
имени этого файла). При выполнении копировании информацию об этом программа сохраняет в файле журнала.
Может возникнуть ситуация, при которой некоторых файлов из исходного списка не окажется, тогда нужно это учесть в
программе с помощью механизма обработки исключений - если файла нет, то в файл журнал нужно сделать запись,
что файл не найден.
"""

import os
import csv
import logging
from datetime import datetime
from pathlib import Path

list_of_files = []


def setup_logger(file_path) -> logging:
    """
    Настройка системы логирования.
    Создает логгер, который записывает сообщения как в файл, так и в консоль.
    """

    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)

    logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для записи в файл журнала
    file_handler = logging.FileHandler(file_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def copy_from_csv_to_new_file(file_list, output_directory, logger):
    """
    Копирует содержимое CSV файлов в плоский текстовый файл.
    Параметры:
    - file_list: список путей к CSV файлам
    - output_directory: директория для сохранения выходных файлов
    - logger: объект логгера для записи операций
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Создаем выходную директорию, если она не существует
    os.makedirs(output_directory, exist_ok=True)
    logger.info(f"Выходная директория: {output_directory}")

    # Создаем имя выходного файла с префиксом времени
    output_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_combined_data.txt"
    output_file_path = os.path.join(output_directory, output_filename)

    # Открываем выходной файл для записи
    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            logger.info(f"Создан выходной файл: {output_file_path}")

            # Записываем заголовок в выходной файл
            output_file.write(f"=== Комбинированные данные из CSV файлов ===\n")
            output_file.write(f"=== Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            output_file.write(f"=== Количество исходных файлов: {len(file_list)} ===\n\n")

            # Обрабатываем каждый CSV файл из списка
            for idx, csv_file_path in enumerate(file_list, 1):
                logger.info(f"Обработка файла {idx}/{len(file_list)}: {csv_file_path}")

                try:
                    # Проверяем существование файла
                    if not os.path.exists(csv_file_path):
                        raise FileNotFoundError(f"Файл не найден: {csv_file_path}")

                    # Проверяем расширение файла
                    if not csv_file_path.lower().endswith('.csv'):
                        logger.warning(f"Файл '{csv_file_path}' не имеет расширения .csv, но будет обработан")

                    # Читаем содержимое CSV файла
                    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                        csv_reader = csv.reader(csv_file)

                        # Записываем разделитель и информацию о файле
                        output_file.write(f"\n{'=' * 60}\n")
                        output_file.write(f"Файл: {os.path.basename(csv_file_path)}\n")
                        output_file.write(f"Полный путь: {csv_file_path}\n")
                        output_file.write(f"{'=' * 60}\n\n")

                        # Копируем содержимое CSV в плоский файл
                        row_count = 0
                        for row in csv_reader:
                            # Преобразуем строку CSV в текстовую строку с разделителями
                            line = '\t'.join(row)  # Используем табуляцию для разделения полей
                            output_file.write(line + '\n')
                            row_count += 1

                        logger.info(f"Успешно скопирован файл: {csv_file_path} "
                                    f"(строк: {row_count})")

                except FileNotFoundError as e:
                    error_msg = f"✗ Файл не найден: {csv_file_path}"
                    logger.error(error_msg)
                    # Записываем информацию об ошибке в выходной файл
                    output_file.write(f"\n{'=' * 60}\n")
                    output_file.write(f"Файл: {os.path.basename(csv_file_path)}\n")
                    output_file.write(f"ОШИБКА: Файл не найден\n")
                    output_file.write(f"{'=' * 60}\n\n")

                except Exception as e:
                    error_msg = f"✗ Ошибка при обработке файла {csv_file_path}: {str(e)}"
                    logger.error(error_msg)
                    # Записываем информацию об ошибке в выходной файл
                    output_file.write(f"\n{'=' * 60}\n")
                    output_file.write(f"Файл: {os.path.basename(csv_file_path)}\n")
                    output_file.write(f"ОШИБКА: {str(e)}\n")
                    output_file.write(f"{'=' * 60}\n\n")

            # Записываем итоговую статистику
            output_file.write(f"\n\n{'=' * 60}\n")
            output_file.write(f"ИТОГИ ОБРАБОТКИ:\n")
            output_file.write(f"Всего файлов в списке: {len(file_list)}\n")
            output_file.write(f"{'=' * 60}\n")

        # Логируем итоговую статистику
        logger.info("=" * 60)
        logger.info("ОБРАБОТКА ЗАВЕРШЕНА")
        logger.info(f"Выходной файл: {output_file_path}")

    except Exception as e:
        logger.critical(f"Критическая ошибка при создании выходного файла: {str(e)}")
        raise


def main():
    """
    Основная функция программы.
    """
    # Список CSV файлов для обработки
    csv_files_list = [
        'D:\My_work\pythonITMO\data\input.csv',
        'D:\My_work\pythonITMO\data\input_m.csv',
        'D:\My_work\pythonITMO\data\orderdata_new.csv',
        'D:\My_work\pythonITMO\data\\nonexistent_file.csv',  # Этого файла нет
    ]

    # С путей
    current_dir = Path.cwd()
    log_directory = current_dir / 'logs'
    output_directory = current_dir / 'output'

    # Создаем директорию для логов
    os.makedirs(log_directory, exist_ok=True)

    # Настройка логирования
    log_file_name = f"csv_copy_{datetime.now().strftime('%Y%m%d')}.log"
    log_file_path = log_directory / log_file_name
    logger = setup_logger(str(log_file_path))

    logger.info("=" * 60)
    logger.info("ЗАПУСК ПРОГРАММЫ КОПИРОВАНИЯ CSV ФАЙЛОВ")
    logger.info(f"Дата и время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    logger.info(f"Список файлов для обработки ({len(csv_files_list)} файлов):")
    for file_path in csv_files_list:
        logger.info(f"  - {file_path}")

    try:
        # Запускаем процесс копирования
        copy_from_csv_to_new_file(csv_files_list, str(output_directory), logger)
        logger.info("Программа успешно завершила работу")

    except Exception as e:
        logger.critical(f"Программа завершилась с критической ошибкой: {str(e)}")
        raise

    logger.info("=" * 60 + "\n")

if __name__ == '__main__':
    main()