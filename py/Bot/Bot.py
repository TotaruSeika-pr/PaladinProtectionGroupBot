import telebot
from telebot import types
import sys
from copy import deepcopy
from keyboa import Keyboa
import json


class Bot:

    def __init__(self, dbm):
        self.token = Bot.GetToken()
        Bot.LoadInfo(self)
        self.dbm = dbm


    def GetToken():
        with open(f'{sys.path[3]}\\token.txt', 'r') as f:
            return str(f.read())
        
    def Main(self):
        self.bot = telebot.TeleBot(self.token)
        self.virtual_path = []
        
        @self.bot.message_handler(commands=['start', 'info'])
        def StartMessage(message):
            Bot.LoadInfo(self)
            Bot.CheckUser(self, message)
            self.virtual_path = ['start']


            markup_info = types.InlineKeyboardMarkup()
            item_official = types.InlineKeyboardButton(text='📝 Официальная форма 📝', callback_data='official')
            item_quest = types.InlineKeyboardButton(text='👑 Квест 🗡️', callback_data='quest')

            markup_info.add(item_official, item_quest)
            self.main_message = self.bot.send_message(message.chat.id, '📖 Выберите формат ознакомления с компанией:', reply_markup=markup_info)

        
        @self.bot.callback_query_handler(func=lambda call: True)
        def AnswerFromKeyboards(call):
            Bot.LoadInfo(self)
            self.form = 'official'
            if call.data == 'official':
                self.form = 'official'
                Bot.OfficialForm(self, call.message)
            elif call.data == 'quest':
                self.bot.send_message(call.message.chat.id, 'Квест до сих пор в разработке :(')
            elif call.data == 'back':
                if self.virtual_path[-1] == 'DoSubPoints':
                    self.virtual_path = ['start', 'OfficialForm']
                    if self.photo_message != None:
                        self.bot.delete_message(call.message.chat.id, self.photo_message.id)
                    self.bot.delete_message(call.message.chat.id, self.other_message.id)
                    del self.photo_message, self.other_message
                    Bot.OfficialForm(self, call.message)
                elif self.virtual_path[-1] == 'DoPoints':
                    self.virtual_path.pop()
                    self.virtual_path.pop()
                    Bot.OfficialForm(self, call.message)
                elif self.virtual_path[-1] == 'OfficialForm':
                    self.virtual_path.pop()
                    self.bot.send_message(call.message.chat.id, 'Напишите команду /start или /info чтобы вернуться на начальный экрна')
            else:
                if self.form == 'official':
                    self.form = 'official'
                    arg = call.data[:1]
                    call.data = call.data[1:]
                    if arg == 'p':
                        Bot.DoPoints(self, call)
                    elif arg == 's':
                        Bot.DoSubPoints(self, call)

                elif self.form == 'quest':
                    pass
                
        self.bot.infinity_polling()

    def OfficialForm(self, message):
        self.virtual_path.append('OfficialForm')
        menu = []
        for_callback = []
        for i in self.info["official_form"]:
            for_callback.append(i)
            menu.append({"text": f"{i}", "callback_data": f"p{Bot.CutCallback(i)}"})

        menu.append({"text": "Обратно", "callback_data": "back"})
        self.p_reduction_to_original_dict = Bot.CreateDict(for_callback)

        keyboard = Keyboa(items=menu, alignment_reverse=True)
        self.bot.edit_message_text(chat_id=message.chat.id, message_id=self.main_message.id, text='Выбирите пункт:', reply_markup=keyboard())

    def DoPoints(self, call):
        self.virtual_path.append('DoPoints')
        self.point_name = call.data
        menu = []
        for_callback = []
        for i in self.info["official_form"][self.p_reduction_to_original_dict[call.data]]:
            for_callback.append(i)
            menu.append({"text": f"{i}", "callback_data": f"s{Bot.CutCallback(i)}"})

        menu.append({"text": "Обратно", "callback_data": "back"})
        self.sp_reduction_to_original_dict = Bot.CreateDict(for_callback)

        keyboard = Keyboa(items=menu, alignment_reverse=True)
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=self.main_message.id, text='Выбирите пункт:', reply_markup=keyboard())
    
    def DoSubPoints(self, call):
        self.virtual_path.append('DoSubPoints')

        self.photo_message = None
        self.other_message = None
        
        menu = {"text": "Обратно", "callback_data": "back"}
        keyboard = Keyboa(items=menu, alignment_reverse=True)
        data = self.info["official_form"][self.p_reduction_to_original_dict[self.point_name]][self.sp_reduction_to_original_dict[call.data]]
        if data["photo"] != None:
            self.photo_message = self.bot.send_photo(call.message.chat.id, open(f'Content\\{data["photo"]}', 'rb'))
        self.other_message = self.bot.send_message(call.message.chat.id, data["text"], reply_markup=keyboard())

    
    def StartQuest(self, call):
        
        part1 = {
                'text': 'Вы стоите перед величественным троном короля, чье лицо выражает серьезность и сосредоточенность. "Мое королевство находится в опасности," говорит он, "зловещие темные силы начали набирать силу в темных уголках нашей земли. Я нуждаюсь в храбром и опытном герое, который отправится на задание и справится с этим ужасным злом". Король глубоко вздыхает и продолжает: "Но это будет опасное путешествие, и я не могу гарантировать вашу безопасность. Я прошу вас, если вы готовы принять этот вызов, то дайте мне свое слово, что вы будете сражаться до конца и не вернетесь, пока не устраните эту угрозу". Вы ощущаете, что это ваше призвание, ваша миссия, и, не колеблясь, вы киваете королю в знак согласия.',
                'photo': 'Content\\quest\\Король.png'}
    
        part2 = {
            'text': 'Король улыбается вам благодарно и указывает на охранника, который выходит из-за колонны, не замеченный раньше. "Этот охранник будет вашим проводником и напарником в этом путешествии," объясняет он, "он хорошо знает эту местность и сможет помочь вам защититься от любых опасностей".',
            'photo': 'Content\\quest\\Проводник.png'}
        
        part3 = {
            'text': 'Вы соглашаетесь и поднимаете свою сумку, в которой находятся ваши инструменты информационной безопасности. Охранник уводит вас от трона и ведет вас к выходу из замка. Когда вы выходите из замка, вы видите, что окружающие земли выглядят мрачно и зловеще. Лес, который раньше казался приветливым и дружелюбным, теперь выглядит темным и запутанным, и вы чувствуете, как волосы на затылке начинают подниматься.\n\nВы начинаете свой путь по лесу, когда слышите звук из кустов рядом с вами. Ваши инстинкты говорят вам, что что-то не так, и вы готовы к действию.\n\nЧто вы будете делать?',
            'A': 'Вы подойдёте в кусту и когда уже нагнетесь к нему, вы замечаете, что он начинает шевелиться, и из него выпрыгивает громадный волк. Он выглядит голодным и агрессивным, и готов атаковать вас.',
            'B': 'Вы используете ваш нож для обороны и начинаете осторожно приближаться к кусту, готовы к атаке.',
            'C': 'Вы внимательным и чуть осторожным взором смотрите на куст и вы замечаете, что он начинает шевелиться, и из него выпрыгивает громадный волк. Он выглядит голодным и агрессивным, и готов атаковать вас.',
            'photo': 'Content\\quest\\Лес.png'}
        
        part4 = {
            'text': 'Когда вы подходите к кусту, вы замечаете, что он начинает шевелиться, и из него выпрыгивает громадный волк. Он выглядит голодным и агрессивным, и готов атаковать вас.\n\nЧто вы будете делать?',
            'A': 'Вы пытаетесь убежать от врага, но он достигает вас преграждая дорогу вынуждая вас сражаться.\nВы быстро вынимаете свой электрошокер из сумки и направляете его на волка. Он реагирует на шок и отступает на несколько шагов, давая вам время на более безопасное расстояние. Вы решаете не тратить время на то, чтобы атаковать волка вашим ножом, и начинаете быстро двигаться в сторону вашего следующего пункта назначения.',
            'B': 'Вы готовите нож бою и начинаете понимать, что нож коротковат для такой особи, Вы быстро вынимаете свой электрошокер из сумки и направляете его на волка. Он реагирует на шок и отступает на несколько шагов, давая вам время на более безопасное расстояние. Вы решаете не тратить время на то, чтобы атаковать волка вашим ножом, и начинаете быстро двигаться в сторону вашего следующего пункта назначения.',
            'C': 'Вы быстро вынимаете свой электрошокер из сумки и направляете его на волка. Он реагирует на шок и отступает на несколько шагов, давая вам время на более безопасное расстояние. Вы решаете не тратить время на то, чтобы атаковать волка вашим ножом, и начинаете быстро двигаться в сторону вашего следующего пункта назначения.',
            'photo': 'Content\\quest\\Волк.png'}
        
        part5 = {
            'text': 'Вы продолжаете свое путешествие, пересекая реку и поднимаясь по склону горы, пока наконец не видите маленькую деревушку в долине. Вы подходите к первому дому и стучите в дверь, но никто не отвечает. Вы пробуете другой дом, и на этот раз вам открывают дверь.',
            'photo': 'Content\\quest\\Деревня.png'}
        
        part6 = {
            'text': 'Вы видите старую женщину, сидящую на стуле, и спрашиваете ее о темных силах, о которых говорил король.\nСтарая женщина вздыхает и говорит: "О, эти темные силы. Они уже давно здесь, в этих лесах. Они тайно подстерегают тех, кто проходит мимо, и нападают, когда находят уязвимое место. Я слышала, что они используют вирусы и другие методы информационной атаки, чтобы захватить контроль над устройствами и сетями. Если вы хотите справиться с ними, вам нужно быть настороже и готовым к бою".\n\nЧто вы будете делать?',
            'photo': 'Content\\quest\\Старуха.png'}
        
        part7 = {
            'A': 'Вы думайте продолжить путь, но вам пришла мысль сомнения: " Как я герой буду скрываться за спинами тех кого надо защищать ?!?!", Вы останавливайтесь и принимаете решение начать своё расследование и поискать следы темных сил самостоятельно.\nВы поблагодарили старую женщину за информацию и решили начать свое расследование. Вы знаете, что темные силы используют информационные атаки, поэтому вам нужно быть готовым к защите своих устройств и сетей. Вы начинаете с проверки своих устройств на наличие вирусов и других вредоносных программ, используя антивирусное ПО.',
            'B': 'Вы думайте вернуться к королю но в голову начинают лезть сомнения " Что если тут нечего нет? Вдруг старая дева обманула меня ради какой то выгоды?"\nВы решаете, что для начало нужно найти доказательство, чтобы просить поддержку короля.\nВы решаете начать свое расследование и поискать следы темных сил самостоятельно.\nВы поблагодарили старую женщину за информацию и решили начать свое расследование. Вы знаете, что темные силы используют информационные атаки, поэтому вам нужно быть готовым к защите своих устройств и сетей. Вы начинаете с проверки своих устройств на наличие вирусов и других вредоносных программ, используя антивирусное ПО.',
            'C':'Вы решаете начать свое расследование и поискать следы темных сил самостоятельно.\nВы поблагодарили старую женщину за информацию и решили начать свое расследование. Вы знаете, что темные силы используют информационные атаки, поэтому вам нужно быть готовым к защите своих устройств и сетей. Вы начинаете с проверки своих устройств на наличие вирусов и других вредоносных программ, используя антивирусное ПО.',
            'photo': 'Content\\quest\\Деревня.png'}
        
        part8 = {
            'text': 'Затем вы решаете провести расследование в деревне, чтобы узнать, есть ли у местных жителей какие-либо подозрения на темные силы. Вы говорите с жителями и узнаете, что они заметили несколько необычных активностей в последнее время, таких как странные звуки и свет в лесу. Они также говорят о том, что некоторые из их устройств начали работать нестабильно, и они подозревают, что это может быть связано с действиями темных сил.',
            'photo': 'Content\\quest\\Жители.png'}
        
        part9 = {
            'text': 'Вы решаете продолжить свое расследование и идти в лес, чтобы найти следы темных сил. По пути вы замечаете несколько подозрительных знаков, таких как необычные следы на земле и поврежденные провода. Вы продолжаете следовать за этими признаками, пока не находите скрытое укрытие, где темные силы хранят свою технику и оборудование.',
            'photo': 'Content\\quest\\Укрытие.png'}
        
        part10 = {
            'text': 'Вы решаете вызвать подкрепление и сообщить о своем открытии королю. С помощью поддержки королевских войск вы атакуете темные силы и успешно их побеждаете.',
            'photo': 'Content\\quest\\Битва.png'}
        
        part11 = {
            'text': 'Вы возвращаетесь к королю, который благодарит вас за вашу храбрость и решимость в борьбе с информационной угрозой. В награду он предлагает вам место в своей команде по информационной безопасности, и вы соглашаетесь, зная, что ваши навыки и опыт могут быть использованы в будущих миссиях.',
            'photo': 'Content\\quest\\Конец.png'}
        
        self.bot.send_photo(call.message.chat.id, open(part1['photo'], 'rb'), part1['text'])
        self.bot.send_photo(call.message.chat.id, open(part2['photo'], 'rb'), part2['text'])
        menu = [{'text': 'A', 'callback_data': 'Ap3'},
                {'text': 'B', 'callback_data': 'Bp3'},
                {'text': 'C', 'callback_data': 'Cp3'}]
        keyboard = Keyboa(items=menu, alignment_reverse=True)
        self.bot.send_photo(call.message.chat.id, open(part3['photo'], 'rb'), part3['text'], reply_markup=keyboard())
        

            
    
    def CheckingForAddedUser(self, table, id):
        self.dbm.cur.execute(f"SELECT * FROM {table}")
        data = self.dbm.cur.fetchall()
        if len(data) == 0:
            return None
        else:
            for i in data:
                if id == i[1]:
                    print(f'{i[1]} | {i[2]}')
                    return False
                else:
                    continue
        return True
                
    def CheckUser(self, message):
        self.dbm.cur.execute("SELECT telegram_id, real_name FROM workers")
        find_id = False
        for i in self.dbm.cur.fetchall():
            if i[0] == message.from_user.id:
                self.bot.send_message(message.chat.id, f'Приветствую, {i[1]}!')
                find_id = True
                break
        if find_id:
            pass
        else:
            self.bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.username}!')

        answer = Bot.CheckingForAddedUser(self, table='telegram_users', id=message.from_user.id)
        if answer == None:
            self.dbm.cur.execute("INSERT INTO telegram_users VALUES (?, ?, ?);", (1, message.from_user.id, message.from_user.username))
            self.dbm.con.commit()
        elif answer == True:
            self.dbm.cur.execute("SELECT MAX(id) FROM telegram_users")
            self.dbm.cur.execute("INSERT INTO telegram_users VALUES (?, ?, ?);", (self.dbm.cur.fetchone()[0]+1, message.from_user.id, message.from_user.username))
            self.dbm.con.commit()
        else:
            pass

    def LoadInfo(self):
        with open(f'{sys.path[3]}\\info.json', 'r', encoding='utf-8') as f:
            self.info = json.loads(f.read())

    def CreateDict(value):
        answer = {}
        index = 0
        for i in value:
            answer.update({f"{Bot.CutCallback(i)}": value[index]})
            index += 1

        return answer

    
    def CutCallback(value):
        answer = ''
        for i in value.split():
            answer += i[:1]
        return answer