import json
import sys
import os


class InfoEditor:
    
    def __init__(self, virtual_path):
        self.virtual_path = virtual_path
        InfoEditor.LoadInfo(self)
        InfoEditor.SaveInfo(self)
    
    def Main(self):
        print(f'{InfoEditor.CreateVirtualPath(self)} Добро пожаловать в редактор!')
        while True:
            received_command = input(InfoEditor.CreateVirtualPath(self))
            if received_command == 'back':
                self.virtual_path.pop()
                break
            else:
                InfoEditor.Controller(self, received_command)

    def Controller(self, command):
        if command == 'create_point':
            self.virtual_path.append('create_point')
            InfoEditor.CreatePoint(self)
        elif command == 'create_subpoint':
            self.virtual_path.append('create_subpoint')
            InfoEditor.CreateSubPoint(self)
        elif command == 'add_text':
            self.virtual_path.append('add_text')
            InfoEditor.AddText(self)
        elif command == 'del_info':
            self.virtual_path.append('del_info')
            InfoEditor.DeleteInfo(self)
        else:
            print(f'{InfoEditor.CreateVirtualPath(self)} Такая команда отсутствует')
    
    def CreatePoint(self):
        while True:
            point_name = input(f'{InfoEditor.CreateVirtualPath(self)} Введите имя пункта: ')
            confirmation = input(f'{InfoEditor.CreateVirtualPath(self)} Создать пункт "{point_name}"? (yes/no): ')
            a = InfoEditor.YesOrNoCheck(self, confirmation)
            if a:
                data = {f"{point_name}": {}}
                self.info["official_form"].update(data)
                InfoEditor.SaveInfo(self)
                break
            elif a == False:
                break
            else:
                print(a)
                break

        self.virtual_path.pop()

    def CreateSubPoint(self):
        print(f'{InfoEditor.CreateVirtualPath(self)} Создание подпункта:')
        while True:
            point_name = input(f'{InfoEditor.CreateVirtualPath(self)} Введите имя существующего пункта: ')
            subpoint_name = input(f'{InfoEditor.CreateVirtualPath(self)} Введите имя подпункта: ')
            try:
                self.info["official_form"][point_name]
            except Exception:
                print(f'{InfoEditor.CreateVirtualPath(self)} !Пункт {point_name} не найден!')
            else:
                confirmation = input(f'{InfoEditor.CreateVirtualPath(self)} Создать {point_name}/{subpoint_name}? (yes/no): ')
                a = InfoEditor.YesOrNoCheck(self, confirmation)
                if a:
                    data = {f"{subpoint_name}": None}
                    self.info["official_form"][point_name].update(data)
                    InfoEditor.SaveInfo(self)
                    break
                elif a == False:
                    break
                else:
                    print(a)
                    break

        self.virtual_path.pop()

    def AddText(self):
        print(f'{InfoEditor.CreateVirtualPath(self)} Дабавление текста')
        while True:
            point_name =  input(f'{InfoEditor.CreateVirtualPath(self)} Введите имя существующего пункта: ')
            subpoint_name = input(f'{InfoEditor.CreateVirtualPath(self)} Введите подпункт: ')
            try:
                self.info["official_form"][point_name][subpoint_name]
            except Exception:
                print(f'{InfoEditor.CreateVirtualPath(self)} !Пункт {point_name}/{subpoint_name} не найден!')
            else:
                confirmation = input(f'{InfoEditor.CreateVirtualPath(self)} Выбрать {point_name}/{subpoint_name}? (yes/no): ')
                a = InfoEditor.YesOrNoCheck(self, confirmation)
                if a:
                    photo_name = input(f'{InfoEditor.CreateVirtualPath(self)} Впишите имена через пробел фото из папки Content (no если фото не нужно): ')
                    if photo_name == 'no' or photo_name == 'n':
                        photo_name = None

                    input(f'{InfoEditor.CreateVirtualPath(self)} Введите текст в файл text.txt...')
                    
                    with open(f'{sys.path[0]}\\text.txt', 'r', encoding='utf-8') as f:
                        text = f.read()

                    if len(text) <= 4095:
                        self.info["official_form"][point_name][subpoint_name] = {"text": text, "photo": None}
                        InfoEditor.SaveInfo(self)
                    else:
                        print(f'{InfoEditor.CreateVirtualPath(self)} !Текст привышает 4095 символов!')
                    
                    break
                elif a == False:
                    continue
                else:
                    print(a)

        self.virtual_path.pop()


    def DeleteInfo(self):
        print(f'{InfoEditor.CreateVirtualPath(self)} Удаление пункта')
        while True:
            filter = input(f'{InfoEditor.CreateVirtualPath(self)} Что вы хотите удалить? (p/sp): ')
            point_name = input(f'{InfoEditor.CreateVirtualPath(self)} Введите сущетвующий пункт: ')
            if filter == 'p':
                try:
                    self.info["official_form"][point_name]
                except Exception:
                    print(f'{InfoEditor.CreateVirtualPath(self)} !Пункт {point_name} не найден!')
                else:
                    confirmation = input(f'{InfoEditor.CreateVirtualPath(self)} Удалить пункт {point_name}? (yes/no): ')
                    a = InfoEditor.YesOrNoCheck(self, confirmation)
                    if a:
                        self.info["official_form"].pop(point_name)
                        InfoEditor.SaveInfo(self)
                        break
                    elif a == False:
                        break
                    else:
                        print(a)
                        break

            elif filter == 'sp':
                subpoint_name = input(f'{InfoEditor.CreateVirtualPath(self)} Введите подпункт: ')
                try:
                    self.info["official_form"][point_name][subpoint_name]
                except Exception:
                    print(f'{InfoEditor.CreateVirtualPath(self)} !Пункт {point_name}/{subpoint_name} не найден!')
                else:
                    confirmation = input(f'{InfoEditor.CreateVirtualPath(self)} Удалить пункт {point_name}/{subpoint_name}? (yes/no): ')
                    a = InfoEditor.YesOrNoCheck(self, confirmation)
                    if a:
                        self.info["official_form"][point_name].pop(subpoint_name)
                        InfoEditor.SaveInfo(self)
                        break
                    elif a == False:
                        break
                    else:
                        print(a)
                        break

        self.virtual_path.pop()

    
    def LoadInfo(self):
        with open(f'{sys.path[1]}\\info.json', 'r', encoding='utf-8') as f:
            self.info = json.loads(f.read())

    def SaveInfo(self):
        with open(f'{sys.path[1]}\\info.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.info, ensure_ascii=False, indent=4))
        

    def CreateVirtualPath(self):
        return '\n'+'/'.join(self.virtual_path)+'$ '
    
    def YesOrNoCheck(self, value):
        if value == 'yes' or value == 'y':
            return True
        elif value == 'no' or value == 'n':
            return False
        else:
            return f'{InfoEditor.CreateVirtualPath(self)} Неверные данные'