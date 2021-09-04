#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import os
from six.moves import http_client


class Web:
    def __init__(self, filePaths={}, queque=[], path="", host="localhost", port=50070, user="tmp", urlPattern=""):
        self.filePaths = filePaths
        self.path = path
        self.host = host
        self.port = port
        self.user = user
        self.queque = queque
        self.urlPattern = f"http://{self.host}:{self.port}/webhdfs/v1/"

    # def mkdir(url, directoryName):
    #     for i in path:
    #         url += f"{i}/"
    #     url += f"{directoryName}?\\user.name={self.user}&op=MKDIRS"
    #     print(url)
    #     try:
    #         response = requests.Session().put(url)
    #     except ConnectionError:
    #         print("Произошла ошибка при создании.")
    #     if response.status_code == http_client.OK:
    #         print("Создание прошло успешно.")
    #     else:
    #         print("Произошла ошибка при создании.")

    def put(self, filePath, dirPath):
        url = self.urlPattern
        newResponse = ""
        for i in dirPath:
            url += f"{i}/"
        url += f"?\\user.name={self.user}&op=CREATE&overwrite=true"
        print(url)
        file = "~"
        for i in filePath:
            file += f"/{i}"
        try:
            response = requests.Session().put(url)
            newUrl = response.headers['location']
            newResponse = requests.Session().put(newUrl, file)
        except ConnectionError:
            print("Произошла ошибка при загрузке.")
        if newResponse.status_code == http_client.CREATED:
            print("Загрузка прошла успешно.")
        else:
            print("Произошла ошибка при загрузке.")

    def get(self):
        pass

    def append(self, newFile, hdfsFile):
        url = self.urlPattern
        newResponse = ""
        for i in hdfsFile:
            url += f"{i}/"
        url += f"?\\user.name={self.user}&op=APPEND"
        print(url)
        file = "~"
        for i in newFile:
            file += f"/{i}"
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

    def delete(self, path):
        response = ""
        url = self.urlPattern
        for i in path:
            url += f"{i}/"
        url += f"?\\user.name={self.user}&op=DELETE"
        print(url)
        try:
            response = requests.Session().delete(url)
        except ConnectionError:
            print("Произошла ошибка при удалении.")
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
                print (self.path)
                print(f"{self.queque[-1]}/")
                self.path.count(f"{self.queque[-1]}/")
                print(self.path)
                print(f"{self.queque[-1]}/")
                self.queque.pop(-1)
                print(self.queque)
            else:
                print("Достигнут корневой раздел")
        else:
            print("Нет такого файла или директории")

    def lls(self):
        pass

    def lcd(self):
        pass


host = ""
port = ""
user = ""
if __name__ == "__main__":
    if len(sys.argv) == 4:
        if isinstance(sys.argv[1], str) & sys.argv[2].isdigit() & isinstance(sys.argv[3], str):
            host = sys.argv[1]
            port = int(sys.argv[2])
            user = sys.argv[3]
        else:
            print("Ошибка в формате данных")
            sys.exit(1)
    else:
        print("Ошибка. Неверное количество параметров.")
        sys.exit(1)
web = Web(host=host, port=port, user=user)
while True:
    defName = input("Введите название функции: ").lower()
    if defName == "mkdir":
        dirName = input("Введите название директории, которую хотите создать: ")
        fileName = input("Введите путь к директории без / через пробел: ").split(" ")
        # mkdir(urlPattern, dirName, fileName)
    elif defName == "put":
        dirName = input("Введите через пробел путь и имя файла, который хотите создать: ").split(" ")
        fileName = input("Введите путь и название локального файла, который хотите загрузить ").split(" ")
        web.put(fileName, dirName)
    elif defName == "get":
        pass
    elif defName == "append":
        oldName = input("Введите через пробел путь к файлу, в который хотите дописать: ").split(" ")
        newName = input("Введите через пробел путь к файлу, из которого хотите дописать").split(" ")
        web.append(newName, oldName)
    elif defName == "delete":
        fileName = input("Введите путь к удаляемому объекту с пробелами: ").split(" ")
        web.delete(fileName)
    elif defName == "ls":
        web.ls()
    elif defName == "cd":
        cdName = input("Введите название директории: ")
        web.cd(cdName)
    elif defName == "lls":
        pass
    elif defName == "lcd":
        pass
    elif defName == "exit":
        print("Выход")
        sys.exit(1)
    else:
        print("Некорректная функция.")
