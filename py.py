#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import os
from six.moves import http_client


class Web:
    def __init__(self, path="", host="localhost", port=50070, user="tmp"):
        self.filePaths = {}
        self.path = path
        self.localPath = os.getcwd()
        print(self.localPath)
        self.host = host
        self.port = port
        self.user = user
        self.queque = []
        self.urlPattern = f"http://{self.host}:{self.port}/webhdfs/v1/"
        os.curdir = self.localPath
        url = self.urlPattern
        response = ""
        url += f"{self.path}?\\user.name={self.user}&op=LISTSTATUS"
        try:
            response = requests.Session().get(url)
        except ConnectionError:
            print("Произошла ошибка при подключении.")
        if response.status_code == http_client.OK:
            for fileStatus in response.json()['FileStatuses']['FileStatus']:
                fileName = {fileStatus['pathSuffix']: fileStatus['type']}
                self.filePaths.update(fileName)

    def mkdir(self, directoryName):
        response = ""
        url = self.urlPattern
        url += f"{self.path}{directoryName}?\\user.name={self.user}&op=MKDIRS"
        print(url)
        try:
            response = requests.Session().put(url)
        except ConnectionError:
            print("Произошла ошибка при создании.")
        if response.status_code == http_client.OK:
            print("Создание прошло успешно.")
        else:
            print("Произошла ошибка при создании.")

    def put(self, fileName):
        url = self.urlPattern
        newResponse = ""
        url += f"{self.path}{fileName}?\\user.name={self.user}&op=CREATE&overwrite=true"
        print(url)
        file = f"{os.curdir}/{fileName}"
        print(file)
        if not os.path.exists(file) & os.path.isfile(file):
            print("Такого файла нет.")
            return
        try:
            response = requests.Session().put(url, file)
            print(response)
            # if response.status_code == http_client.TEMPORARY_REDIRECT:
            #     newUrl = response.headers['location']
            #     newResponse = requests.Session().put(newUrl, file)
            #     if newResponse.status_code == http_client.CREATED:
            #         print("Загрузка прошла успешно.")
            #     else:
            #         print("Произошла ошибка при загрузке.")
        except ConnectionError:
            print("Произошла ошибка при загрузке.")

    def get(self, fileName):
        url = self.urlPattern
        newResponse = ""
        # url += f"{self.path}{fileName}?\\user.name={self.user}&op=OPEN"
        url = "http://localhost:50070/webhdfs/v1/user/radhold/wordcount/input/file01?\\user.name=radhold&op=OPEN"
        print(url)
        file = f"{os.curdir}/{fileName}"
        try:
            response = requests.Session().get(url, allow_redirects=True)
            newUrl = response.headers['location']
            newResponse = requests.Session().get(newUrl)
            open(file, "wb").write(newResponse.content)
        except ConnectionError:
            print("Произошла ошибка при соединении.")
        if newResponse.status_code == http_client.CREATED:
            print("Загрузка на устройство прошла успешно.")
        else:
            print("Произошла ошибка при загрузке.")

    def append(self, newFile, hdfsFile):
        url = self.urlPattern
        newResponse = ""
        url += f"{self.path}{hdfsFile}?\\user.name={self.user}&op=APPEND"
        print(url)
        file = f"{os.curdir}/{newFile}"
        if not os.path.exists(file) & os.path.isfile(file):
            print("Такого файла нет или Вы указали директорию.")
            return
        try:
            response = requests.Session().post(url)
            newUrl = response.headers['location']
            newResponse = requests.Session().put(newUrl, file)
        except ConnectionError:
            print("Произошла ошибка при объединении.")
        if newResponse.status_code == http_client.OK:
            print("Объединение прошла успешно.")
        else:
            print("Произошла ошибка при объединении.")

    # def rename(url, newName, oldName):
    #     newPathName = "/"
    #     for (i, it) in oldName:
    #         url += f"{i}/"
    #         if len(oldName) != it:
    #             newPathName += f"{i}/"
    #     newPathName += newName
    #     url += f"?\\user.name={self.user}&op=RENAME&destination={newPathName}"
    #     print(url)
    #     try:
    #         response = requests.Session().put(url)
    #     except ConnectionError:
    #         print("Произошла ошибка при переименовании.")
    #     if response.status_code == http_client.OK:
    #         print("Переименование прошло успешно.")
    #     else:
    #         print("Произошла ошибка при переименовании.")

    def delete(self, fileName):
        response = ""
        url = self.urlPattern
        url += f"{self.path}{fileName}?\\user.name={self.user}&op=DELETE"
        print(url)
        try:
            response = requests.Session().delete(url)
        except ConnectionError:
            print("Произошла ошибка при соединении.")
        if response.status_code == http_client.OK:
            print("Удаление прошло успешно.")
        else:
            print("Произошла ошибка при удалении.")

    def ls(self):
        url = self.urlPattern
        response = ""
        url += f"{self.path}?\\user.name={self.user}&op=LISTSTATUS"
        print(url)
        self.filePaths.clear()
        try:
            response = requests.Session().get(url)
        except ConnectionError:
            print("Произошла ошибка при выводе.")
        if response.status_code == http_client.OK:
            print("Вывод прошел успешно.")
            for fileStatus in response.json()['FileStatuses']['FileStatus']:
                fileName = {fileStatus['pathSuffix']: fileStatus['type']}
                print(fileName)
                self.filePaths.update(fileName)
            print(*self.filePaths)
        else:
            print("Произошла ошибка при выводе.")

    def cd(self, name):
        if self.filePaths.get(name) == "FILE":
            print("Это не директория")
        elif self.filePaths.get(name) == "DIRECTORY":
            self.queque.append(name)
            self.path += f"{name}/"
            self.ls()
        elif name == "..":
            if len(self.queque) > 0:
                self.path = self.path.replace(f"{self.queque[-1]}/", "")
                self.queque.pop(-1)
            else:
                print("Достигнут корневой раздел")
        else:
            print("Нет такого файла или директории")

    def lls(self):
        path = os.getcwd()
        os.curdir = path
        print(os.curdir)
        try:
            pathList = os.listdir(path)
            if len(pathList) != 0:
                files = []
                dirs = []
                for i in pathList:
                    if os.path.isfile(f"{path}/{i}"):
                        files.append(i)
                    elif os.path.isdir(f"{path}/{i}"):
                        dirs.append(i)
                print("Директории: ")
                print(*dirs)
                print("Файлы: ")
                print(*files)
            else:
                print("Директория пуста.")
        except FileNotFoundError:
            print("Директория не найдена")

    def lcd(self, name):
        if name != "..":
            os.pardir = os.curdir
            os.curdir += f"/{name}"
            try:
                os.chdir(os.curdir)
            except NotADirectoryError:
                print("Не директория.")
            print(os.curdir)
            self.lls()
        elif name == "..":
            if os.curdir != self.localPath:
                os.chdir(os.pardir)
                os.pardir = os.path.abspath(f"../{os.pardir}")
                self.lls()
            else:
                print("Корневая папка.")
        else:
            print("Нет такого файла или директории")


localHost = ""
localPort = ""
localUser = ""
if __name__ == "__main__":
    if len(sys.argv) == 4:
        if isinstance(sys.argv[1], str) & sys.argv[2].isdigit() & isinstance(sys.argv[3], str):
            localHost = sys.argv[1]
            localPort = int(sys.argv[2])
            localUser = sys.argv[3]
        else:
            print("Ошибка в формате данных")
            sys.exit(1)
    else:
        print("Ошибка. Неверное количество параметров.")
        sys.exit(1)
web = Web(host=localHost, port=localPort, user=localUser)
while True:
    defName = input("Введите название функции: ").lower()
    if defName == "mkdir":
        dirName = input("Введите название директории, которую хотите создать: ")
        web.mkdir(dirName)
    elif defName == "put":
        localFile = input("Введите название локального файла, который хотите загрузить ")
        web.put(localFile)
    elif defName == "get":
        loadFile = input("Введите название файла, который хотите загрузить ")
        web.get(loadFile)
    elif defName == "append":
        oldName = input("Введите имя файла, в который хотите дописать: ")
        newName = input("Введите имя файла, из которого хотите дописать")
        web.append(newName, oldName)
    elif defName == "delete":
        deleteName = input("Введите имя удаляемого объекта: ")
        web.delete(deleteName)
    elif defName == "ls":
        web.ls()
    elif defName == "cd":
        cdName = input("Введите название директории: ")
        web.cd(cdName)
    elif defName == "lls":
        web.lls()
    elif defName == "lcd":
        lcdName = input("Введите название директории: ")
        web.lcd(lcdName)
    elif defName == "exit":
        print("Выход")
        sys.exit(1)
    elif defName == "help":
        print("Доступные команды:\n mkdir - создает новую директорию\n put - добавляет файл\n get - загружает файл\n "
              "append - дописывает файл\n delete - удаляет файл\n ls - выводит содержимое текущего каталога HDFS\n "
              "cd - переход в другой каталог HDFS\n lls - выводит содержимое локального каталога\n lcd - переход в "
              "другой локальный каталог\n exit - выход из программы\n")
    else:
        print("Некорректная функция.")
