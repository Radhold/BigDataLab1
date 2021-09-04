import sys
import requests
from six.moves import http_client


def mkdir(url, directoryName, path):
    for i in path:
        url += f"{i}/"
    url += f"{directoryName}?\\user.name={user}&op=MKDIRS"
    print(url)
    response = requests.Session().put(url)
    if response.status_code == http_client.OK:
        print("Создание прошло успешно")
    else:
        print("Произошла ошибка при создании")


def put():
    pass


def get():
    pass


def append():
    pass


def delete():
    pass


def ls():
    pass


def cd():
    pass


def lls():
    pass


def lcd():
    pass


host = ""
port = ""
user = ""
if __name__ == "__main__":
    if len(sys.argv) == 4:
        if isinstance(sys.argv[1], str) & sys.argv[2].isdigit() & isinstance(sys.argv[3], str):
            host = sys.argv[1]
            port = sys.argv[2]
            user = sys.argv[3]
        else:
            print("Ошибка в формате данных")
            sys.exit(1)
    else:
        print("Ошибка. Неверное количество параметров.")
        sys.exit(1)
request = requests.Session()
urlPattern = f"http://{host}:{port}/webhdfs/v1/"
while True:
    defName = input("Введите название функции: ").lower()
    if defName == "mkdir":
        directoryName = input("Введите название директории, которую хотите создать: ")
        path = input("Введите путь к директории без / через пробел: ").split(" ")
        mkdir(urlPattern, directoryName, path)
    elif defName == "put":
        pass
    elif defName == "get":
        pass
    elif defName == "append":
        pass
    elif defName == "delete":
        pass
    elif defName == "ls":
        pass
    elif defName == "cd":
        pass
    elif defName == "lls":
        pass
    elif defName == "lcd":
        pass
    elif defName == "exit":
        print("Выход")
        sys.exit(1)
    else:
        print("Некорректная функция.")

