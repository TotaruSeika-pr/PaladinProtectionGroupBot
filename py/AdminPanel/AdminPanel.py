import json
import sqlite3
import sys
import os
from InfoEditor import InfoEditor

sys.path.insert(1, os.path.abspath('py\\Bot'))

class AdminPanel:

    def __init__(self):
        self.con = sqlite3.connect('DataBase/DataBase.db')
        self.cur = self.con.cursor()
        self.virtual_path = ['AP']
        AdminPanel.LoadInfo(self)
        AdminPanel.Main(self)

    def Main(self):
        print('\tДобро пожаловать в ПА!')
        while True:
            received_command = input(AdminPanel.CreateVirtualPath(self))
            if received_command == 'exit':
                break
            else:
                AdminPanel.Controller(self, command=received_command)

    def Controller(self, command):
        if command == 'print_info':
            self.virtual_path.append('print_info')
            AdminPanel.PrintInfo(self)
        elif command == 'add_worker':
            self.virtual_path.append('add_worker')
            AdminPanel.AddWorker(self)
        elif command == 'del_worker':
            self.virtual_path.append('del_worker')
            AdminPanel.DeleteWorker(self)
        elif command == 'check_progress':
            self.virtual_path.append('check_progress')
            AdminPanel.CheckProgress(self)
        elif command == 'info_editor':
            self.virtual_path.append('info_editor')
            self.ie = InfoEditor(virtual_path=self.virtual_path)
            self.ie.Main()
        elif command == 'sql_request':
            self.virtual_path.append('sql_request')
            AdminPanel.SQLRequest(self)
        else:
            print(f'{AdminPanel.CreateVirtualPath(self)} Такая команда отсутствует')

    
    def AddWorker(self):
        print(f'{AdminPanel.CreateVirtualPath(self)} Создание нового сотрудника')
        while True:
            telegram_id = int(input(AdminPanel.CreateVirtualPath(self)+'telegram_id: '))
            real_name = input(AdminPanel.CreateVirtualPath(self)+'ФИО: ')
            specialization = input(AdminPanel.CreateVirtualPath(self)+'Должность: ')
            confirmation = input(AdminPanel.CreateVirtualPath(self)+'Подтвердить создание сотрудника по данным выше? (yes/no): ')
            a = AdminPanel.YesOrNoCheck(self, confirmation) 
            if a:
                answer = AdminPanel.Response(self, filter='*')
                if len(answer) == 0:
                    self.cur.execute("INSERT INTO workers VALUES (?, ?, ?, ?, ?, ?);", (1, telegram_id, real_name, specialization, 0, 0))
                    self.con.commit()
                    print(f'{real_name} добавлен в БД!')
                    break
                else:
                    self.cur.execute("SELECT MAX(id) FROM workers")
                    self.cur.execute("INSERT INTO workers VALUES (?, ?, ?, ?, ?, ?);", (self.cur.fetchone()[0]+1, telegram_id, real_name, specialization, 0, 0))
                    self.con.commit()
                    print(f'{real_name} добавлен в БД!')
                    break
            elif a == False:
                continue
            else:
                print(a)


        self.virtual_path.pop()

    def DeleteWorker(self):
        print(f'{AdminPanel.CreateVirtualPath(self)} Удаление сотрудника')
        column = input(AdminPanel.CreateVirtualPath(self)+'Имя столбца: ')
        del_filter = input(AdminPanel.CreateVirtualPath(self)+'Данные поиска: ')
        answer = AdminPanel.Response(self, filter='real_name')
        confirmation = input(f'{AdminPanel.CreateVirtualPath(self)} Удалить {answer}? (yes/no) ')
        a = AdminPanel.YesOrNoCheck(self, confirmation)
        if a:
            self.cur.execute(f"DELETE FROM workers WHERE {column}={del_filter}")
            self.con.commit()
            print(f'{AdminPanel.CreateVirtualPath(self)} Сотрудник {answer} удалён')
        elif a == False:
            pass
        else:
            print(a)
        
        self.virtual_path.pop()


    def CheckProgress(self):
        print(f'{AdminPanel.CreateVirtualPath(self)} Прогресс ознакомления сотрудников:\n')
        index = 1
        for i in AdminPanel.Response(self, filter='real_name, official_progress, quest_progress'):
            print(f'{index}) {i[0]}: |{i[1]}| [{i[2]}]')

        self.virtual_path.pop()


    def LoadInfo(self):
        with open(f'{sys.path[1]}\\info.json', 'r', encoding='utf-8') as f:
            self.info = json.loads(f.read())
    
    def PrintInfo(self):
        AdminPanel.LoadInfo(self)
        print(f'{InfoEditor.CreateVirtualPath(self)} Словарь с информацией:')
        print(json.dumps(self.info, ensure_ascii=False, indent=4))
        self.virtual_path.pop()

    
    def SQLRequest(self):
        self.virtual_path.pop()
    
    def YesOrNoCheck(self, value):
        if value == 'yes' or value == 'y':
            return True
        elif value == 'no' or value == 'n':
            return False
        else:
            return f'{AdminPanel.CreateVirtualPath(self)} Неверные данные'
    
    def Response(self, filter):
        self.cur.execute(f"SELECT {filter} FROM workers")
        return self.cur.fetchall()
    
    def CreateVirtualPath(self):
        return '\n'+'/'.join(self.virtual_path)+'$ '
