from InitBot import bot
from telebot import types
from InitDB import create_connection
import hashlib
import bcrypt
import datetime


def Create_Task(message):
    zaiavka = {}

    def create_Task(message):
        db = create_connection()
        cursor = db.cursor()
        date = datetime.datetime.today().strftime("%Y-%m-%d %H.%M.%S")
        cursor.execute("SELECT name_company, numberWork, City, name_users FROM Telegramm_active_users WHERE Tg_id = %s",(message.chat.id,))
        user_name = cursor.fetchone()
        cursor.execute("INSERT INTO tasks(message,fio,numberWorker,city,author,status,datePlan,created_at) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (zaiavka["message"], user_name[3], user_name[1], user_name[2],user_name[0],"Новая",date,date))
        db.commit()

        bot.send_message(message.chat.id,"Ваша заявка сформирована!")

        if zaiavka['photo'] != []:
            bot.send_photo( chat_id = -1001978039387,
                            photo = zaiavka['photo'][0].file_id,
                            caption= f"""Новая заявка 
-----------
Компания: {user_name[0]}
Составитель: {user_name[3]}
Рабочий номер: {user_name[1]}
Город: {user_name[2]}
Сообщение: {zaiavka['message']
}
                            """)
        else:
            bot.send_message(chat_id = -1001978039387,
                            text = f"""Новая заявка 
-----------
Компания: {user_name[0]}
Составитель: {user_name[3]}
Рабочий номер: {user_name[1]}
Город: {user_name[2]}
Сообщение: {zaiavka['message']
}
                            """)
      

    def wiriteMessage(message):
        if message.content_type == "photo":
            photos = []
            for i in message.photo:
                photos.append(i)
            zaiavka['message'] = message.caption
            zaiavka['photo'] = photos
        else:
            zaiavka['message'] = message.text
            zaiavka['photo'] = []
        create_Task(message)

    bot.send_message(message.chat.id, "Приступаем к заполению заявки!")
    bot.send_message(message.chat.id, "Укажите ваще сообщение: \nВы можете отправить фото")
    bot.register_next_step_handler(message, wiriteMessage)


def Top10tasks(message):
    mark = types.InlineKeyboardMarkup(row_width=3)
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("SELECT name_company,name_users FROM Telegramm_active_users WHERE Tg_id = %s", (message.chat.id,))
    name_company = cursor.fetchone()
    cursor.execute("SELECT id FROM tasks WHERE author = %s AND fio = %s LIMIT 10",(name_company[0],name_company[1]))
    tasks = cursor.fetchall()
    for i in tasks:
        mark.add(types.InlineKeyboardButton(f"Номер {i[0]}",
                                            callback_data=i[0]))

    mark.add(types.InlineKeyboardButton("Назад",
                                        callback_data="Back"))

    bot.edit_message_text(text="Выберите, пожалуйста заявку для получения инофрмации: ",
                          chat_id=message.chat.id,
                          message_id=message.id,
                          reply_markup=mark)
    db.commit()


def Top20tasks(message):
    mark = types.InlineKeyboardMarkup(row_width=3)
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("SELECT name_company, name_users FROM Telegramm_active_users WHERE Tg_id = %s", (message.chat.id,))
    name_company = cursor.fetchone()
    cursor.execute("SELECT id FROM tasks WHERE author = %s AND fio = %s LIMIT 20",(name_company[0], name_company[1]))
    tasks = cursor.fetchall()
    for i in tasks:
        mark.add(types.InlineKeyboardButton(f"Номер {i[0]}",
                                            callback_data=i[0]))

    mark.add(types.InlineKeyboardButton("Назад",
                                        callback_data="Back"))
    bot.edit_message_text(text="Выберите, пожалуйста заявку для получения инофрмации: ",
                          chat_id=message.chat.id,
                          message_id=message.id,
                          reply_markup=mark)
    db.commit()


def Setting(message):
    mark = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text="ФИО автора", callback_data="NewName")
    button2 = types.InlineKeyboardButton(text="Город", callback_data="NewCity")
    button3 = types.InlineKeyboardButton(text="Рабочий номер", callback_data="NewWorkNumber")
    button4 = types.InlineKeyboardButton(text="◀ Обратно ◀", callback_data="Back")
    mark.add(button1, button2, button3, button4)
    bot.edit_message_text(text="Уважаемый пользователь. Просим вас актуализировать ваши данные, это необходимо, для понижения времени составления заявки",
                          message_id=message.id,
                          reply_markup=mark,
                          chat_id=message.chat.id)


def ViewInformation(message, id):
    db = create_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, message, fio, numberWorker,author, status, datePlan, dateFact FROM tasks WHERE id = %s ",(id,))
    info = cursor.fetchone()
    """info about number of day"""
    if info[7] is None or info[6] is None:
        count_day = " - "
    else:
        count_day = abs((info[7] - info[6]).days)
    mark = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Назад", callback_data="back1")
    mark.add(button1)
    bot.edit_message_text(f"""Информация по заявке {id}
-----------------
1) Номер: {info[0]}
2) Компания: {info[4]}
3) Автор заявки: {info[2]}
4) Рабочий номер: {info[3]}
5) Сообщение: {info[1]}
6) Время выполняния: {count_day} дней
7) Статус: {info[5]}
""",
                          chat_id=message.chat.id,
                          message_id=message.id,
                          reply_markup=mark)


def CreateNewUser(message):
    zaiavka = {}

    def InputCity(message):
        zaiavka['City'] = message.text
        bot.send_message(chat_id=message.chat.id,
                         text="Введите Фамилию и инициалы: \n Формат: Иванов И.И.")

        bot.register_next_step_handler(message, InputPassword)

    def InputWorkNumber(message):
        zaiavka['WorkNumber'] = message.text
        bot.send_message(chat_id=message.chat.id,
                         text="Введите ваш город: ")

        bot.register_next_step_handler(message, InputCity)

    def InputFIO(message):
        if message.text == "123123":
            bot.send_message(chat_id=message.chat.id,
                             text="Введите ваш рабочий номер: ")

            bot.register_next_step_handler(message, InputWorkNumber)
        else:
            hashed = bcrypt.checkpw(message.text.encode(), user_conf[1].encode())
            if hashed:
                bot.send_message(chat_id=message.chat.id,
                                 text="Введите ваш рабочий номер: ")

                bot.register_next_step_handler(message, InputWorkNumber)

    def InputPassword(message):
        cursor = contect.cursor()
        cursor.execute("SELECT max(id) FROM Telegramm_active_users")
        ids = cursor.fetchone()
        if ids[0] is None:
            idmax = 0
        else:
            idmax = ids[0] + 1
        if user_conf[0] == "Admin":
            cursor = contect.cursor()
            cursor.execute("INSERT INTO Telegramm_active_users(id,name_company,Tg_id,name_users,admin, numberWork, City) VALUES (%s,%s,%s,%s,1,%s,%s)",(idmax,user_conf[2], message.chat.id, message.text,zaiavka['WorkNumber'],zaiavka["City"]))
            contect.commit()
            bot.send_message(message.chat.id,
                             "Вы авторизовались. /start")

            return True
        else:
            cursor = contect.cursor()
            cursor.execute("INSERT INTO Telegramm_active_users(id, name_company,Tg_id,name_users,admin, numberWork, City) VALUES (%s, %s,%s,%s,0,%s,%s)",(idmax,user_conf[2], message.chat.id, message.text,zaiavka['WorkNumber'],zaiavka["City"]))
            contect.commit()
            bot.send_message(message.chat.id,
                             "Вы авторизовались. /start")       

    def Inputlogin(message):

        global user_conf
        cursor = contect.cursor()
        cursor.execute("SELECT login, password,name FROM users WHERE login = %s", (message.text,))
        user_conf = cursor.fetchone()
        if user_conf is None:
            bot.send_message(chat_id=message.chat.id,
                             text="Такого пользователя нет!")
            return False
        else:
            bot.send_message(chat_id=message.chat.id,
                             text="Введите пароль:")
            bot.register_next_step_handler(message, InputFIO)

    global contect
    contect = create_connection()        
    bot.send_message(chat_id=message.chat.id,
                     text="Приступаем к авторизации!")
    bot.send_message(chat_id=message.chat.id,
                     text="Отправьте пожалуйста ваш логин")
    bot.register_next_step_handler(message, Inputlogin)


def EditName(message):
    def editName(message):
        try:
            db = create_connection()
            cursor = db.cursor()
            cursor.execute("UPDATE Telegramm_active_users SET name_users = %s WHERE Tg_id = %s", (message.text, message.chat.id))
            bot.send_message(message.chat.id, "ФИО изменено!")
            db.commit()
        except Exception:
            bot.send_message(message.chat.id, "Что-то пошло не так!")

    bot.send_message(message.chat.id, "Введите новое ФИО: ")
    bot.register_next_step_handler(message, editName)


def EditWork(message):
    def editWork(message):
        try:
            db = create_connection()
            cursor = db.cursor()
            cursor.execute("UPDATE Telegramm_active_users SET numberWork = %s WHERE Tg_id = %s", (message.text, message.chat.id))
            bot.send_message(message.chat.id, "рабочий номер изменен!")
            db.commit()
        except Exception:
            bot.send_message(message.chat.id, "Что-то пошло не так!")

    bot.send_message(message.chat.id, "Введите новый номер: ")
    bot.register_next_step_handler(message, editWork)


def HelpUser(message):
    mark = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton("<<-- Назад ", callback_data="Back")
    mark.add(but1)
    bot.edit_message_text("""
Доброго времени суток!
Данный бот поможет вам облегчить составление заявки!
Все, что вам нужно делать, это следовать этой инструкции!
---------------------------------------------------------
ЕСЛИ ВЫ ХОТИТЕ СОСТАВИТЬ ЗАЯВКУ:
1) Нажмите на кнопку 'Новая заявка' на панели;
2) После отправленного сообщения, отправьте фото ошибки и сообщение, с подробным описанием этой самой ошибки;

* ФОТО ДОЛЖНО БЫТЬ ПРИКРЕПЛЕНО К СООБЩЕНИЮ! НИ В КОЕМ СЛУЧАЕ, НЕ ОТПРАВЛЯЙТЕ ФОТО КАК ДОКУМЕНТ
ГОТОВО! Заявка отправлена. 
---------------------------------------------------------
ЕСЛИ У ВАС ИЗМЕНИЛИСЬ КАКИЕ-ТО ДАННЫЕ (ФАМИЛИЯ, РАБОЧИЙ НОМЕР ИЛИ ГОРОД)
1) Нажмите на кнопку 'Настройка пользователя' на панели; 
2) Выберите необходимый параметр для изменения;
3) После полученного сообщение, введите новые данные. 

Ваши данные изменены! 
---------------------------------------------------------

!!!!!! Что делать, если сообщение о том, что заявка готова не пришло?
1) Перепроверьте, смогли ли вы правильно отправить фото! 
2) Если фото отправлено верно, то повторите вашу попытку через 2 минуты.
3) Если при второй попытке, сообщение все равно не приходит, напишите вашу заявку без приложения фотографий.

!!!!!! Что делать, если бот не реагирует на какие-то либо сообщения? 
1) Не паниковать! 
2) Если бот не отвечает на сообщения в течении 5-10 минут, нужно составить заявку на сайте https://support.akperm.ru/login

-----------------------------------------------------------

ХОРОШЕЙ РАБОТЫ) МЫ ВАМ РАДЫ!""",
                          chat_id=message.chat.id,
                          message_id=message.id,
                          reply_markup=mark,
                          parse_mode="HTML")


def EditCity(message):
    def editCity(message):
        try:
            db = create_connection()
            cursor = db.cursor()
            cursor.execute("UPDATE Telegramm_active_users SET City = %s WHERE Tg_id = %s",(message.text,message.chat.id))
            bot.send_message(message.chat.id,"город изменен!")
            db.commit()
        except:
            bot.send_message(message.chat.id,"Что-то пошло не так!")
    
    bot.send_message(message.chat.id,"Введите новый город: ")
    bot.register_next_step_handler(message, editCity)