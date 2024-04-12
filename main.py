import telebot
import sqlite3
import text 
from telebot import types

# подключение к боту в ТГ
BOT = telebot.TeleBot(f'{text.BOT_TOKEN}')

# Глобальные переменные
selected_tag = None
quesid = None


#обработка комманд --------------------------------------------------------------
@BOT.message_handler(commands = ['start'])
def start(message):
    # кнопки интерфейса
    Markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(f'{text.question_new}')
    btn2 = types.KeyboardButton(f'{text.question_active}')
    btn3 = types.KeyboardButton(f'{text.question_all}')
    btn4 = types.KeyboardButton(f'{text.question_my}')
    btn5 = types.KeyboardButton(f'{text.author_card}')
    Markup.row(btn1)
    Markup.row(btn2,btn3)
    Markup.row(btn4,btn5)

    # обработка данных пользователя для регистрации
    first_name = ''
    last_name = ''
    if(message.from_user.first_name):
        first_name = message.from_user.first_name
    if(message.from_user.last_name):
        last_name = message.from_user.last_name
    name = first_name + ' ' + last_name

    # подключение к бд
    conn = sqlite3.connect(f'{text.DB_NAME}')
    cur = conn.cursor()

    # создание таблицы Пользователей
    cur.execute(f'{text.Users_table}')
    conn.commit()
    # создание таблицы Тегов
    cur.execute(f'{text.Tags_table}')
    conn.commit()
    # создание таблицы Вопросов
    cur.execute(f'{text.Questions_table}')
    conn.commit()
    # создание таблицы Ответов
    cur.execute(f'{text.Answers_table}')
    conn.commit()

    # внесение нового пользователя
    cur.execute("INSERT OR IGNORE INTO Users(user_id, name) VALUES ('%s','%s')" % (message.from_user.username,name))
    conn.commit()

    # закрытие подключения к бд
    cur.close()
    conn.close()
    
    BOT.send_message(message.chat.id, f'{text.register}')
    BOT.send_message(message.chat.id, f'{text.hello}, {first_name}', reply_markup=Markup)

# обработка сообщений --------------------------------------------------------------
@BOT.message_handler()
def info(message):
    match message.text.lower():
        case 'привет':
            # кнопки интерфейса
            Markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton(f'{text.question_new}')
            btn2 = types.KeyboardButton(f'{text.question_active}')
            btn3 = types.KeyboardButton(f'{text.question_all}')
            btn4 = types.KeyboardButton(f'{text.question_my}')
            btn5 = types.KeyboardButton(f'{text.author_card}')
            Markup.row(btn1)
            Markup.row(btn2,btn3)
            Markup.row(btn4,btn5)

            BOT.send_message(message.chat.id,f'{text.hello}, {message.from_user.first_name}', reply_markup=Markup)
        case 'запрос на знание':
            # кнопки сообщения
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.tag_new}',callback_data='tag_new')
            sbtn2 = types.InlineKeyboardButton(f'{text.tag_list}',callback_data='tag_list')
            Markup.row(sbtn1,sbtn2)

            BOT.send_message(message.chat.id,f'{text.question_create}')
            BOT.send_message(message.chat.id,f'{text.need_tag}',reply_markup=Markup)
        case 'активные запросы':
            # кнопки сообщения
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.answer_add}',callback_data='answer_add')
            sbtn2 = types.InlineKeyboardButton(f'{text.answers_list}',callback_data='answers_list')
            Markup.row(sbtn1,sbtn2)

            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()

            # получение данных пользователя
            cur.execute("SELECT * FROM Questions WHERE active = '1'")
            questions_data = cur.fetchall()

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(message.chat.id,f'<b>{text.question_list_active}</b>',parse_mode='html')
            for item in questions_data:
                BOT.send_message(message.chat.id,item[3], reply_markup=Markup)
        case 'все запросы':
            # кнопки сообщения (активный вопрос)
            MarkupActive = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.answer_add}',callback_data='answer_add')
            sbtn2 = types.InlineKeyboardButton(f'{text.answers_list}',callback_data='answers_list')
            MarkupActive.row(sbtn1,sbtn2)

            # кнопки сообщения (неактивный вопрос)
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.answers_list}',callback_data='answers_list')
            Markup.row(sbtn1)

            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()

            # получение данных пользователя
            cur.execute("SELECT * FROM Questions")
            questions_data = cur.fetchall()

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(message.chat.id,f'<b>{text.question_list}</b>',parse_mode='html')
            for item in questions_data:
                if(item[4]):
                    BOT.send_message(message.chat.id,item[3], reply_markup=MarkupActive)
                else:
                    BOT.send_message(message.chat.id,item[3], reply_markup=Markup)
        case 'мои запросы':
            # кнопки сообщения (активный вопрос)
            MarkupActive = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.question_close}',callback_data='question_close')
            sbtn2 = types.InlineKeyboardButton(f'{text.answers_list}',callback_data='answers_list')
            MarkupActive.row(sbtn1,sbtn2)

            # кнопки сообщения (неактивный вопрос)
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.answers_list}',callback_data='answers_list')
            Markup.row(sbtn1)

            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()

            # получение данных пользователя
            cur.execute("SELECT * FROM Questions WHERE user_id = '%s'" % (message.from_user.username))
            questions_data = cur.fetchall()

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(message.chat.id,f'<b>{text.question_list_my}</b>',parse_mode='html')
            for item in questions_data:
                if(item[4]):
                    BOT.send_message(message.chat.id,item[3], reply_markup=MarkupActive)
                else:
                    BOT.send_message(message.chat.id,item[3], reply_markup=Markup)
        case 'карточка автора':
            # кнопки сообщения
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.contact_add}',callback_data='contact_add')
            sbtn2 = types.InlineKeyboardButton(f'{text.contact_del}',callback_data='contact_del')
            Markup.row(sbtn1,sbtn2)

            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()

            # получение данных пользователя
            cur.execute("SELECT * FROM Users WHERE user_id = '%s'" %  (message.from_user.username))
            user_data = cur.fetchall()[0]

            # получение количества запросов пользователя
            cur.execute("SELECT * FROM Questions WHERE user_id = '%s'" %  (message.from_user.username))
            questions_count = len(cur.fetchall())

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(message.chat.id,f'<b>{text.autor_data}</b>',parse_mode='html')
            BOT.send_message(message.chat.id,f'<b>Имя:</b> {user_data[1]}\n<b>Кол-во запросов:</b> {questions_count}\n<b>Кол-во ответов:</b> сделать',parse_mode='html', reply_markup=Markup)
            
        #временная комманда для тестирования
        case 'тест':
            BOT.send_message(message.chat.id,f'{selected_tag}')
            
        case _:
            BOT.send_message(message.chat.id,f'{text.command_error}')
    

# обработка кнопок сообщения --------------------------------------------------------------
@BOT.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    match callback.data:
        case 'answer_add':

            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()


            # получение данных вопроса
            cur.execute("SELECT id FROM Questions WHERE data = '%s'" %  (callback.message.text))
            global quesid
            quesid = cur.fetchall()[0]


            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(callback.message.chat.id,"Введите ваш ответ:")
            BOT.register_next_step_handler(callback.message,new_answer)
        case 'answers_list':
            
            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()
            try:
            
                cur.execute("SELECT id FROM Questions WHERE data = '%s'" %  (callback.message.text))
                quesid = cur.fetchall()[0]

                # получение данных пользователя
                cur.execute("SELECT * FROM Answers WHERE question_id = '%s'" % (quesid[0]))
                print(quesid)
                answ_data = cur.fetchall()
            
                
                for item in answ_data:
                    BOT.send_message(callback.message.chat.id,item[3])
            except ValueError:
                BOT.send_message(callback.message.chat.id,f'{text.error}')

             # закрытие подключения к бд
            cur.close()
            conn.close()
        case 'tag_new':
            BOT.send_message(callback.message.chat.id,f'<b>{text.tag_name}</b>',parse_mode='html')
            BOT.register_next_step_handler(callback.message,tag_new)
        case 'tag_list':
            # кнопки сообщения
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.tag_select}',callback_data='tag_select')
            Markup.row(sbtn1)

            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()

            # получение данных пользователя
            cur.execute("SELECT * FROM Tags")
            tags_data = cur.fetchall()

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(callback.message.chat.id,f'<b>{text.tag_list}</b>',parse_mode='html')
            for item in tags_data:
                BOT.send_message(callback.message.chat.id,item[1], reply_markup=Markup)
        case 'tag_select':
            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()
        
            # получение данных тега
            cur.execute("SELECT * FROM Tags WHERE name = '%s'" %  (callback.message.text))
            global selected_tag
            selected_tag = cur.fetchall()[0]
    

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(callback.message.chat.id,f'<b>{text.question_insert}</b>',parse_mode='html')
            
            BOT.register_next_step_handler(callback.message,question_new)
        case 'question_close':
             # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()
             # получение данных вопроса
            print
            cur.execute("SELECT id FROM Questions WHERE data = '%s'" %  (callback.message.text))
            
            quesid = cur.fetchall()[0]


            cur.execute("UPDATE Questions SET active=0 WHERE id =('%s')" %(quesid[0]))
            conn.commit()
            # закрытие подключения к бд
            cur.close()
            conn.close()
            BOT.send_message(callback.message.chat.id,'Вопрос закрыт')
        case _:
            BOT.send_message(callback.message.chat.id,'Комманда не работает')

# Функции кнопок интерфейса -------------------------------------------------------------- !!! работают из любого места где есть кнопка :(
# создание нового тега
def tag_new(message):
    try:
        if(message.content_type == 'text'):
            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()

            # сохраниение тега в бд
            cur.execute("INSERT OR IGNORE INTO Tags(name) VALUES ('%s')" % (message.text))
            conn.commit()
        
            # получение данных тега
            cur.execute("SELECT * FROM Tags WHERE name = '%s'" %  (message.text))
            global selected_tag
            selected_tag = cur.fetchall()[0]

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(message.chat.id,'Тег создан')
            BOT.send_message(message.chat.id,f'<b>{text.question_insert}</b>',parse_mode='html')
            BOT.register_next_step_handler(message,question_new)
        else:
            BOT.send_message(message.chat.id,'Тег должен быть текстом')
    except ValueError:
        BOT.send_message(message.chat.id,f'{text.error}')

# создание нового запроса
def question_new(message):
    try:
        # подключение к бд
        conn = sqlite3.connect(f'{text.DB_NAME}')
        cur = conn.cursor()

        # комманда для теста
        cur.execute("INSERT OR IGNORE INTO Questions(user_id, tag_id, data) VALUES ('%s','%s','%s')" % (message.from_user.username,selected_tag[0],message.text))
        conn.commit()

        # закрытие подключения к бд
        cur.close()
        conn.close()

        # обнуление выбранного тега
        selected_tag_id = ''

        BOT.send_message(message.chat.id,f'{text.done}')
    except ValueError:
        BOT.send_message(message.chat.id,f'{text.error}')


def new_answer(message):
    try:
        # подключение к бд
        conn = sqlite3.connect(f'{text.DB_NAME}')
        cur = conn.cursor()

        # комманда для теста
        cur.execute("INSERT OR IGNORE INTO Answers(user_id,question_id, data) VALUES ('%s','%s','%s')" % (message.from_user.username,quesid[0],message.text))
        conn.commit()
      
        # закрытие подключения к бд
        cur.close()
        conn.close()
        BOT.send_message(message.chat.id,f'{text.done}')
    except ValueError:
        BOT.send_message(message.chat.id,f'{text.error}')

# бесконечный перезапуск скрипта
BOT.infinity_polling()