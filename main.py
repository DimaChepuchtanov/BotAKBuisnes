
from InitBot import bot
from telebot import types

from InitDB import create_connection
from UserCommand import (Create_Task, Setting,
                         Top10tasks, Top20tasks,
                         ViewInformation, CreateNewUser,
                         EditName, EditCity,
                         EditWork, HelpUser)

from AdminCommand import (SelectActiveTasks, SelectNewTasks,
                          ChangeInfoNewTask, AcceptNewTask,
                          ChangeInformationTask, CloseTask,
                          ExportInfoAboutWork, SelectActiveTasksChange,
                          Change,ChangeInfoAboutAccept)

"""
    Номер группы, куда переходят значения: -1001978039387
"""
bot.set_my_commands([
    types.BotCommand("/start", "Работа с ботом"),
])


@bot.message_handler(commands=["autorize"])
def main(message):
    print(message.chat.id)
    CreateNewUser(message)


@bot.message_handler(commands=["start"])
def UserMenu(message):
    def autorize():
        """
        Проверяем пользователя на авторизацию

        """ 
        connectDB = create_connection()
        cursor = connectDB.cursor()

        cursor.execute("SELECT admin FROM Telegramm_active_users WHERE Tg_id = %s;", (message.chat.id,))

        find_user = cursor.fetchone()
        if find_user is None:
            connectDB.commit()
            return False, 0
        else:
            connectDB.commit()
            return True, find_user[0]

    flag, admin = autorize()
    if flag:
        if admin == 0:
            mark = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(text="👨‍🔧 Новая заявка 👨‍🔧", callback_data="Новая заявка")
            button2 = types.InlineKeyboardButton(text="🥇 Последние 10 заявок 🥇", callback_data="lastTop10")
            button3 = types.InlineKeyboardButton(text="🥈 Последние 20 заявок 🥈", callback_data="lastTop20")
            button4 = types.InlineKeyboardButton(text="📕 Инструкция 📕", callback_data="Помощь")
            button5 = types.InlineKeyboardButton(text="Настройка пользования", callback_data="setting")
            mark.add(button1, button2, button3, button4, button5)

            bot.send_message(message.chat.id, "Уважаемый пользователь, вот команды, которыми вы можете воспользоваться в любое время", 
                             reply_markup=mark,
                             parse_mode="HTML")
        if admin == 1:
            mark = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(text="👨‍🔧 Список активных заявок 👨‍🔧", callback_data="ActiveTasks")
            button3 = types.InlineKeyboardButton(text="👨‍🔧 Продление заявок 👨‍🔧", callback_data="ProdlTasks")
            button2 = types.InlineKeyboardButton(text="🥇Новые заявки 🥇", callback_data="newTasks")
            button4 = types.InlineKeyboardButton(text="📕 Профиль 📕", callback_data="Profile")
            mark.add(button1, button2, button3, button4)

            bot.send_message(message.chat.id, "Уважаемый пользователь, вот команды, которыми вы можете воспользоваться в любое время", 
                             reply_markup=mark,
                             parse_mode="HTML")
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Вы не авторизированны! /autorize")


@bot.callback_query_handler(func=lambda call: True)
def ans(c):
    """
    Обработка простых пользователей
    """
    if c.data == "Новая заявка":
        Create_Task(c.message)
    elif c.data == "lastTop10" or c.data == "back1":
        Top10tasks(c.message)
    elif c.data == "lastTop20" or c.data == "back2":
        Top20tasks(c.message)
    elif c.data == "Помощь":
        HelpUser(c.message)
    elif c.data == "setting":
        Setting(c.message)
    elif c.data == "Back":
        mark = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text="👨‍🔧 Новая заявка 👨‍🔧", callback_data="Новая заявка")
        button2 = types.InlineKeyboardButton(text="🥇 Последние 10 заявок 🥇", callback_data="lastTop10")
        button3 = types.InlineKeyboardButton(text="🥈 Последние 20 заявок 🥈", callback_data="lastTop20")
        button4 = types.InlineKeyboardButton(text="📕 Инструкция 📕", callback_data="Помощь")
        button5 = types.InlineKeyboardButton(text="Настройка пользования", callback_data="setting")
        mark.add(button1, button2, button3, button4, button5)

        bot.edit_message_text(chat_id=c.message.chat.id,
                              text="Уважаемый пользователь, вот команды, которыми вы можете воспользоваться в любое время", 
                              reply_markup=mark,
                              parse_mode="HTML",
                              message_id=c.message.id)

    elif c.data == "NewName":
        EditName(c.message)

    elif c.data == "NewCity":
        EditCity(c.message)

    elif c.data == "NewWorkNumber":
        EditWork(c.message)

    # Обработки администраторов
    elif c.data == "ActiveTasks":
        SelectActiveTasks(c.message)

    elif c.data == "newTasks" or c.data == "NewTasks" or c.data == "backToList" :
        SelectNewTasks(c.message)

    elif c.data == "Profile":
        ExportInfoAboutWork(c.message)

    elif c.data == "BackAdmin":
        mark = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(text="👨‍🔧 Список активных заявок 👨‍🔧", callback_data="ActiveTasks")
        button3 = types.InlineKeyboardButton(text="👨‍🔧 Продление заявок 👨‍🔧", callback_data="ProdlTasks")
        button2 = types.InlineKeyboardButton(text="🥇Новые заявки 🥇", callback_data="newTasks")
        button4 = types.InlineKeyboardButton(text="📕 Профиль 📕", callback_data="Profile")
        mark.add(button1, button2, button3, button4)
        bot.edit_message_text(chat_id=c.message.chat.id,
                              text="Уважаемый пользователь, вот команды, которыми вы можете воспользоваться в любое время", 
                              reply_markup=mark,
                              parse_mode="HTML",
                              message_id=c.message.id)
    elif "New" in c.data:
        idTask = c.data.split(" ")
        ChangeInfoNewTask(c.message, int(idTask[1]))

    elif "AcceptTask" in c.data:
        idTask = c.data.split(" ")
        AcceptNewTask(c.message, int(idTask[0]))

    elif "Номер" in c.data:
        idTask = c.data.split(" ")
        ChangeInformationTask(c.message,int(idTask[1]))

    elif "CloseTask" in c.data:
        idTask = c.data.split(" ")
        CloseTask(c.message, int(idTask[0]))

    elif c.data == "ProdlTasks":
        SelectActiveTasksChange(c.message)

    elif "Number" in c.data:
        idTask = c.data.split(" ")
        ChangeInfoAboutAccept(c.message, idTask[1])

    elif "changeDate" in c.data:
        idTask = c.data.split(" ")
        Change(c.message, idTask[0])
    # итерационная проверка тестов
    elif int(c.data) > 0:
        ViewInformation(c.message, int(c.data))


if __name__ == "__main__":
    bot.infinity_polling()
