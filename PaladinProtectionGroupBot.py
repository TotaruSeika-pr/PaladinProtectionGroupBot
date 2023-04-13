import sys
import os
from py.DBManager.DBManager import DBManager
from py.Bot.Bot import Bot

sys.path.insert(1, os.path.abspath('py'))
sys.path.insert(1, os.path.abspath('py\\Bot'))
sys.path.insert(1, os.path.abspath('py\\DBManager'))
sys.path.insert(1, os.path.abspath('py\\AdminPanel'))


def main():
    dbm = DBManager()
    bot = Bot(dbm)
    bot.Main()


if __name__ == '__main__':
    main()
    