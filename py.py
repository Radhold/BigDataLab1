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
        # print(self.localPath)
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
        if directoryName == "":
            print("Нет названия директории")
            return
        response = ""
        url = self.urlPattern
        url += f"{self.path}{directoryName}?\\user.name={self.user}&op=MKDIRS"
        # print(url)
        try:
            response = requests.Session().put(url)
        except ConnectionError:
            print("Произошла ошибка при создании.")
        if response.status_code == http_client.OK:
            print("Создание прошло успешно.")
        else:
            print("Произошла ошибка при создании.")

    def put(self, fileName):
        if fileName == "":
            print("Нет названия файла")
            return
        url = self.urlPattern
        url += f"{self.path}{fileName}?\\user.name={self.user}&op=CREATE&overwrite=true"
        # print(url)
        file = f"{os.curdir}/{fileName}"
        # print(file)
        data = open(file, 'rb').read()
        if not os.path.exists(file) & os.path.isfile(file):
            print("Такого файла нет.")
            return
        try:
            response = requests.Session().put(url, allow_redirects=False)
            # print(response)
            if response.status_code == http_client.TEMPORARY_REDIRECT:
                newUrl = response.headers['location']
                newResponse = requests.Session().put(newUrl, data)
                if newResponse.status_code == http_client.CREATED:
                    print("Загрузка прошла успешно.")
                else:
                    print("Произошла ошибка при загрузке.")
        except ConnectionError:
            print("Произошла ошибка при загрузке.")

    def get(self, fileName):
        if fileName == "":
            print("Нет названия файла")
            return
        url = self.urlPattern
        response = ""
        url += f"{self.path}{fileName}?\\user.name={self.user}&op=OPEN"
        # print(url)
        file = f"{os.curdir}/{fileName}"
        try:
            response = requests.Session().get(url, allow_redirects=True)
            open(file, "wb").write(response.content)
        except ConnectionError:
            print("Произошла ошибка при соединении.")
        if response.status_code == http_client.OK:
            print("Загрузка на устройство прошла успешно.")
        else:
            print("Произошла ошибка при загрузке.")

    def append(self, newFile, hdfsFile):
        if newFile == "" or hdfsFile == "":
            print("Нет названия файла")
            return
        url = self.urlPattern
        response = ""
        url += f"{self.path}{hdfsFile}?\\user.name={self.user}&op=APPEND"
        # print(url)
        file = f"{os.curdir}/{newFile}"
        if not os.path.exists(file) & os.path.isfile(file):
            print("Такого файла нет или Вы указали директорию.")
            return
        try:
            data = open(file, 'rb').read()
            response = requests.Session().post(url, allow_redirects=False)
            if response.status_code == http_client.TEMPORARY_REDIRECT:
                newUrl = response.headers['location']
                newResponse = requests.Session().post(newUrl, data)
                if newResponse.status_code == http_client.OK:
                    print("Объединение прошла успешно.")
                else:
                    print("Произошла ошибка при объединении.")
        except ConnectionError:
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
        if fileName == "":
            print("Нет названия файла")
            return
        response = ""
        url = self.urlPattern
        url += f"{self.path}{fileName}?\\user.name={self.user}&op=DELETE"
        # print(url)
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
        # print(url)
        self.filePaths.clear()
        try:
            response = requests.Session().get(url)
        except ConnectionError:
            print("Произошла ошибка при выводе.")
        if response.status_code == http_client.OK:
            print("Вывод прошел успешно.")
            for fileStatus in response.json()['FileStatuses']['FileStatus']:
                fileName = {fileStatus['pathSuffix']: fileStatus['type']}
                # print(fileName)
                self.filePaths.update(fileName)
            files = []
            dirs = []
            for key in self.filePaths:
                if self.filePaths[key] == "FILE":
                    files.append(key)
                elif self.filePaths[key] == "DIRECTORY":
                    dirs.append(key)
            if len(dirs) > 0:
                print("Директории: ")
                print(*dirs)
            else:
                print("Директорий нет.")
            if len(files) > 0:
                print("Файлы: ")
                print(*files)
            else:
                print("Файлов нет.")
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
                # self.path = self.path.replace(f"{self.queque[-1]}/", "")
                self.path = "".join(self.path.rsplit(self.queque[-1], 1))
                self.queque.pop(-1)
            else:
                print("Достигнут корневой раздел")
        else:
            print("Нет такого файла или директории")

    def lls(self):
        path = os.getcwd()
        os.curdir = path
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
                if len(dirs) > 0:
                    print("Директории: ")
                    print(*dirs)
                else:
                    print("Директорий нет.")
                if len(files) > 0:
                    print("Файлы: ")
                    print(*files)
                else:
                    print("Файлов нет.")
            else:
                print("Директория пуста.")
        except FileNotFoundError:
            print("Директория не найдена")

    def lcd(self, name):
        if not os.path.exists(os.curdir + f"/{name}"):
            print("Нет такого файла или директории.")
            return
        if name != ".." and name != "":
            os.pardir = os.curdir
            os.curdir += f"/{name}"
            try:
                os.chdir(os.curdir)
            except NotADirectoryError:
                print("Не директория.")
            except FileNotFoundError:
                print("Не найден файл или директория.")
        elif name == "..":
            if os.curdir != self.localPath:
                os.chdir(os.pardir)
                os.pardir = os.path.abspath(f"../{os.pardir}")
                self.lls()
            else:
                print("Корневая папка.")


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
try:
    web = Web(host=localHost, port=localPort, user=localUser)
except ConnectionError:
    print("Нет соединения с сервером")
    sys.exit(1)
while True:
    defParams = input("Введите название функции и параметры для нее: ").strip()
    defParams = defParams.split(" ")
    defName = defParams[0]
    if defName == "mkdir":
        try:
            dirName = defParams[1]
            web.mkdir(dirName.strip())
        except IndexError:
            print("Вы ввели не все параметры")
    elif defName == "put":
        try:
            localFile = defParams[1]
            web.put(localFile.strip())
        except IndexError:
            print("Вы ввели не все параметры")
    elif defName == "get":
        try:
            loadFile = defParams[1]
            web.get(loadFile.strip())
        except IndexError:
            print("Вы ввели не все параметры")

    elif defName == "append":
        try:
            oldName = defParams[1]
            newName = defParams[2]
            web.append(newName.strip(), oldName.strip())
        except IndexError:
            print("Вы ввели не все параметры")
    elif defName == "delete":
        try:
            deleteName = defParams[1]
            web.delete(deleteName.strip())
        except IndexError:
            print("Вы ввели не все параметры")
    elif defName == "ls":
        web.ls()
    elif defName == "cd":
        try:
            cdName = defParams[1]
            web.cd(cdName)
        except IndexError:
            print("Вы ввели не все параметры")
    elif defName == "lls":
        web.lls()
    elif defName == "lcd":
        try:
            lcdName = defParams[1]
            web.lcd(lcdName.strip())
        except IndexError:
            print("Вы ввели не все параметры")
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
