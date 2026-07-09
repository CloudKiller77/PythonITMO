"""
Project 2_S. Задания по работе с сетевым оборудованием
Задание 2. Создать скрипт, реализующий вывод всей конфигурации маршрутизатора/коммутатора на экран пользователя
и в текстовый файл.
Указание. Для инициализации SSH-соединений применить модуль Paramiko.
"""

import paramiko
import time
import logging
import os
from datetime import datetime
import sys


def create_logging():
    """Настройка системы логирования"""

    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = f"{log_dir}/router_config.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


class DeviceConfigRetriever:
    """Класс для получения конфигурации с сетевого устройства"""

    def __init__(self, host, username, password, port=22, device_type="cisco_ios"):
        """
        Инициализация параметров подключения

        Args:
            host: IP-адрес или hostname устройства
            username: имя пользователя
            password: пароль
            port: порт SSH (по умолчанию 22)
            device_type: тип устройства (cisco_ios, juniper, huawei, ....)
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.device_type = device_type
        self.client = None
        self.logger = logging.getLogger(__name__)

        # Словарь команд для разных типов устройств
        self.commands = {
            "cisco_ios": "show running-config",
            "cisco_nxos": "show running-config",
            "juniper": "show configuration | display set",
            "huawei": "display current-configuration",
            "arista": "show running-config",
            "hp_comware": "display current-configuration",
            "mikrotik": "export",
            "linux": "cat /etc/network/interfaces"  # пример для Linux
        }

    def connect_ssh(self):
        """
        Установка SSH-соединения с устройством

        Args:
            host: IP-адрес или hostname устройства
            username: Имя пользователя
            password: Пароль
            port: Порт SSH (по умолчанию 22)
            timeout: Таймаут подключения в секундах
        Returns:
            SSHClient: объект SSH-клиента или None при ошибке
        """

        try:
            self.logger.info(f"Подключение к {self.host}:{self.port}...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                timeout=15,
                allow_agent=False,
                look_for_keys=False
            )

            self.logger.info(f"Успешное подключение к {self.host}")
            return ssh

        except paramiko.AuthenticationException:
            self.logger.error("Ошибка аутентификации: проверьте логин и пароль")
            return None
        except paramiko.SSHException as e:
            self.logger.error(f"Ошибка SSH: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка подключения: {e}")
            return None

    def send_command(self, command, timeout=30):
        """
        Отправка команды на устройство и получение вывода

        Args:
            command: команда для выполнения
            timeout: таймаут выполнения команды в секундах
        """
        try:
            self.logger.info(f"Отправка команды: {command}")

            # Создание сессии
            channel = self.client.invoke_shell()
            channel.settimeout(timeout)
            channel.recv(65535)

            # Отправка команды
            channel.send(command + "\n")

            # Ожидание завершения выполнения команды
            time.sleep(2)

            # Получение вывода
            output = ""
            while True:
                if channel.recv_ready():
                    output += channel.recv(65535).decode('utf-8', errors='ignore')
                    time.sleep(1)
                else:
                    # Проверка, завершилась ли команда
                    if channel.exit_status_ready():
                        break
                    time.sleep(0.5)
            channel.close()

            self.logger.info(f"Команда выполнена. Получено {len(output)} байт")
            return output

        except Exception as e:
            self.logger.error(f"Ошибка при выполнении команды '{command}': {e}")
            return None

    def get_config(self):
        """Получение конфигурации устройства"""
        command = self.commands.get(self.device_type, "show running-config")
        self.logger.info(f"Запрос конфигурации с устройства {self.host}")

        # Получение конфигурации устройства
        config = self.send_command(command)
        return config

    def disconnect(self):
        """Закрытие SSH-соединения"""
        if self.client:
            try:
                self.client.close()
                self.logger.info(f"Соединение с {self.host} закрыто")
            except Exception as e:
                self.logger.error(f"Ошибка при закрытии соединения: {e}")


def save_config_to_file(config, hostname):
    """Сохранение конфигурации в файл"""
    try:
        filename = "config_device.txt"

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Конфигурация устройства: {hostname}\n")
            file.write(f"Дата получения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 30 + "\n\n")
            file.write(config)

        logging.info(f"Конфигурация сохранена в файл: {filename}")
        return filename

    except Exception as e:
        logging.error(f"Ошибка при сохранении конфигурации в файл: {e}")
        return None


def main():
    """Основная функция"""
    logger = create_logging()
    logger.info("=" * 30)
    logger.info("Запуск скрипта получения конфигурации устройства")

    try:
        # Запрос параметров подключения
        print("ПОЛУЧЕНИЕ КОНФИГУРАЦИИ СЕТЕВОГО УСТРОЙСТВА\n")

        hostname = input("Введите IP-адрес или hostname устройства: ").strip()
        if not hostname:
            logger.error("Hostname не может быть пустым")
            sys.exit(1)

        username = input("Введите имя пользователя: ").strip()
        if not username:
            logger.error("Имя пользователя не может быть пустым")
            sys.exit(1)

        password = input("Введите пароль: ")
        if not password:
            logger.error("Пароль не может быть пустым")
            sys.exit(1)

        port_input = input("Введите порт SSH (по умолчанию 22): ").strip()
        port = int(port_input) if port_input else 22

        # Выбор типа устройства
        print("\nТипы устройств:")
        print("1. Cisco")
        print("2. Juniper")
        print("3. Huawei")
        print("4. MikroTik")

        device_map = {
            "1": "cisco_ios",
            "2": "juniper",
            "3": "huawei",
            "4": "mikrotik"
        }

        device_choice = input("Выберите тип устройства (1-4): ").strip()
        device_type = device_map.get(device_choice)

        # Создание экземпляра класса
        retriever = DeviceConfigRetriever(
            host=hostname,
            username=username,
            password=password,
            port=port,
            device_type=device_type
        )

        # Подключение и получение конфигурации
        if retriever.connect_ssh():
            config = retriever.get_config()

            if config:
                # Вывод конфигурации на экран
                print("\n" + "=" * 30)
                print("КОНФИГУРАЦИЯ УСТРОЙСТВА")
                print("=" * 30)

                # Вывод с возможностью паузы для длинных конфигураций
                lines = config.split('\n')
                for i in range(0, len(lines), 50):  # Постраничный вывод по 50 строк
                    chunk = lines[i:i + 50]
                    print('\n'.join(chunk))

                    if i + 50 < len(lines):
                        input("\nНажмите Enter для продолжения...")

                # Сохранение в файл
                filename = save_config_to_file(config, hostname)
                if filename:
                    logger.info(f"Конфигурация успешно сохранена в {filename}")
                    print(f"\nКонфигурация сохранена в файл: {filename}")

            else:
                logger.error("Не удалось получить конфигурацию")
                print("ОШИБКА: Не удалось получить конфигурацию с устройства")
        else:
            logger.error("Не удалось подключиться к устройству")
            print("ОШИБКА: Не удалось подключиться к устройству")

        # Закрытие соединения
        retriever.disconnect()

    except KeyboardInterrupt:
        logger.info("Скрипт был прерван пользователем")
        print("\nСкрипт был прерван пользователем")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}", exc_info=True)
        print(f"Произошла ошибка: {e}")
    finally:
        logger.info("Завершение работы скрипта")
        logger.info("=" * 30)
        print("\nРабота скрипта завершена")


if __name__ == "__main__":
    main()