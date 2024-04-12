# Здесь все переменные текста
BOT_TOKEN = '7060009186:AAERSgw9vyj4hEkXVH0vkka_mzjVDojxmnw'
DB_NAME = 'BotBD.sqlite'

# Кнопки интерфейса:
question_new = 'Запрос на знание'
question_active = 'Активные запросы'
question_all = 'Все запросы'
question_my = 'Мои запросы'
author_card = 'Карточка автора'

# Кнопки сообщений:
answer_add = 'Ответить'
answers_list = 'Все ответы'
contact_add = 'Добавить контакт'
contact_del = 'Удалить контакт'
tag_new = 'Новый тег'
tag_list = 'Список тегов'
tag_select = 'Выбрать'
question_close = 'Закрыть запрос'

# Системные сообщения:
error = 'Что-то пошло не так!'
command_error = 'Комманда не распознана'
register = 'Регистрация в системе завершена!'
hello = 'Здравствуйте'
need_tag = 'Выбирите или создайте тег запроса.'
tag_list = 'Полный список запросов:'
tag_name = 'Внесите название тега:'
question_create = 'Создание запроса:'
question_list = 'Полный список запросов:'
question_list_active = 'Список активных запросов:'
question_list_my = 'Список моих запросов:'
question_insert = 'Внесите текст запроса:'
autor_data = 'Данные автора:'
done = 'Выполнено'

# SQL команды таблиц --------------------------------------------------------------
# команды создания:
Users_table = 'CREATE TABLE IF NOT EXISTS Users (user_id varchar(255) primary key unique, name varchar(50))'
Tags_table = 'CREATE TABLE IF NOT EXISTS Tags (id integer  primary key autoincrement, name varchar(255) unique)'
Questions_table = 'CREATE TABLE IF NOT EXISTS Questions (id integer  primary key autoincrement, user_id varchar(255), tag_id integer, data blob, active bool default true, evaluation int default 0, FOREIGN KEY (user_id) REFERENCES Users(user_id),FOREIGN KEY (tag_id) REFERENCES Tags(id))'
Answers_table = 'CREATE TABLE IF NOT EXISTS Answers (id integer  primary key autoincrement, user_id varchar(255), question_id integer, data blob, evaluation int default 0, FOREIGN KEY (user_id) REFERENCES Users(user_id),FOREIGN KEY (question_id) REFERENCES Questions(id))'