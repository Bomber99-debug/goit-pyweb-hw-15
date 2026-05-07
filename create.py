import subprocess
import sys
import socket

from time import sleep
from pathlib import Path
from shutil import copy2

DIR_END_ALEMBIC = Path(__file__).parent.joinpath("alembic")



def docker_init() -> None:
    print("Перевірка чи встановлений Docker і запущений")
    try:
        docker_info = subprocess.run(["docker", "info"], capture_output=True, text=True)
        result_err(docker_info)
    except FileNotFoundError:
        print("Помилка: Docker не знайдено в системі. Будь ласка, встановіть його.")
    except subprocess.CalledProcessError as e:
        print(f"Docker встановлено, але сталася помилка при виконанні: {e.stderr}")


def is_port_busy(host='localhost', port=5432) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
        except OSError:
            return True
        return False


def docker_create_container(container_name: str = 'dev-pyweb-15') -> None:
    docker_init()  # Перевірка чи встановлений Docker і запущений

    print("Створення контейнера")
    file_name_db = subprocess.run(['docker', 'ps', '-a', '--filter', f'name={container_name}', '--format', '{{.Names}}'],
                                  capture_output=True, text=True)

    if container_name in file_name_db.stdout.splitlines():
        print(f"Контейнер з {container_name} вже існує, задайте іншу назву")
        sleep(1)
        sys.exit()

    if is_port_busy():
        print("Порт 5432 зайнятий, звільніть порт і спробуйте ще раз")
        sleep(1)
        sys.exit()

    create = ["docker", "run", "--name", container_name,
              "-e", "POSTGRES_USER=dev_pyweb",
              "-e", "POSTGRES_PASSWORD=123456",
              "-e", "POSTGRES_DB=dev_pyweb",
              "-p", "5432:5432",
              "-d", "postgres:16"]
    result = subprocess.run(create, capture_output=True, text=True)
    result_err(result)


def init_alembic() -> bool:
    result = subprocess.run(['alembic', 'history'], capture_output=True, text=True)
    if result.returncode == 0:
        return False
    return True


def edit_setting_alembic(dir_file: str = DIR_END_ALEMBIC) -> None:
    print("Створення міграції у базі даних")
    try:
        source = Path(__file__).parent.joinpath('setting').joinpath('env.py')
        copy2(source, dir_file)
    except FileNotFoundError as err:
        print("Файл env.py не знайдено.")
    except PermissionError as err:
        print("Файл env.py заблокований або не має прав на копіювання і переміщення.")
    except OSError as err:
        print(err)


def init_migrate_db(dir_end: str) -> None:
    destination = Path(__file__).parent.joinpath(dir_end).joinpath('env.py')
    if not destination.exists():
        print('Ініціалізація alembic')
        result = subprocess.run(['alembic', 'init', dir_end], capture_output=True, text=True)
        result_err(result)

        print('Заміна налаштувань alembic')
        edit_setting_alembic(destination)


def create_migrate_db():
    print('Створення міграцій')
    result = subprocess.run(['alembic', 'revision', '--autogenerate', '-m', "'Init'"], capture_output=True, text=True)
    result_err(result)


def application_migrate_db():
    print('Застосування міграції')
    result = subprocess.run(['alembic', 'upgrade', 'head'], capture_output=True, text=True)
    result_err(result)


def insert_db() -> None:
    print("Створення фейкових даних і наповнення бази даних")
    file = Path(__file__).parent.joinpath('seeds').joinpath('seed_db.py')
    subprocess.run([sys.executable, file])


def get_db() -> None:
    print("Запити до БД")
    file = Path(__file__).parent.joinpath('my_select.py')
    result = subprocess.run(file, capture_output=True, text=True)
    result_err(result)


def result_err(err) -> None:
    if err.returncode != 0:
        print(err.stderr)
        sleep(1)
        sys.exit()


def main() -> None:
    docker_create_container()  # Створення контейнера

    if init_alembic():
        edit_setting_alembic(DIR_END_ALEMBIC)  # Створення міграції у базі даних

        create_migrate_db()  # Створення міграцій

        application_migrate_db()  # Застосування міграції

    insert_db()  # Створення фейкових даних і наповнення бази даних

    get_db()  # Запити до БД


if __name__ == '__main__':
    main()
