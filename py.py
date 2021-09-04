import sys


def mkdir():
    pass


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
defName = input("Введите название функции")
