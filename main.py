import telebot
from telebot import types
from db import ensure_connection
from db import init_db
from db import add_task
from db import delete_task
from db import change_task
from db import show_week
from db import show_month
from db import show_all


bot = telebot.TeleBot('token')
init_db()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f"""Hi, {message.from_user.first_name}, I'm a <b>To Do List</b> bot, I am here to help you with organising your life.

I can add, update or delete your tasks from a to do list. You can also see all tasks for this week or for a whole month.

If you want to see detailed description of all my functions use /help command.""",
                     parse_mode='html')


@bot.message_handler(commands=['help'])
def help_mes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    add_new = types.KeyboardButton('/add')
    delete = types.KeyboardButton('/delete')
    update = types.KeyboardButton('/update')
    show_7 = types.KeyboardButton('/show_all_for_week')
    show_30 = types.KeyboardButton('/show_all_for_month')
    show_all = types.KeyboardButton('/show_all')

    markup.add(add_new, delete, update, show_7, show_30, show_all)

    bot.send_message(message.chat.id,
                     """Okay, so I have several functions, here is a description of each one:
                     
<strong>Creating a task</strong> - you can create a new task, just enter what and when. /add

<strong>Updating a task</strong> - change the name or the date of the particular task. /update

<strong>Deleting a task</strong> - delete a task from your planner. /delete

<strong>Show all tasks for a week</strong> - if you want to see all tasks that you need to do for this week, use this function. /show_all_for_week

<strong>Show all the tasks for a month</strong> - exactly like the previous one, but for a month. /show_all_for_month

<strong>Show all the tasks</strong> - shows you all tasks you have. /show_all

That's all, now you ready to go! Let's start? Press /add button, so I'll be able to help you.
""", parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, """
Okay, you want to add a new task, huh? Then write your task and date in this precise format: <b>task, date, add</b>
Remember, it's important to include <b>at the end</b> of your message what function you want to use specifically!

For example: 
do chores, 2022-12-31, add
read a book, 2022-08-01, add
watch a film, 2015-03-15, add

<b>WARNING!</b> Enter your date exactly like this: <b>YYYY-MM-DD</b>(2017-01-03, 2015-05-17 and ect.)
""", parse_mode='html')

    @bot.message_handler(func=lambda mess: mess.text.endswith('add'))
    def adding_to_db(mess):
        if mess.text != '' and ',' in mess.text:
            res = mess.text.split(', ')
            # print(res)
            # print(str(mess.text))
            bot.send_message(mess.chat.id, "Your task is in a ToDo list now!")
            add_task(user_id=mess.from_user.id, task=res[0], date=res[1])
        else:
            bot.send_message(mess.chat.id, 'Sorry, your formatting is missing a comma or is empty, try again: /add')


@bot.message_handler(commands=['delete'])
def delete(message):
    all_tasks = '\n'.join([f'{task}, {date}' for task, date in show_all(user_id=message.from_user.id)])
    bot.send_message(message.chat.id, f"""
If you want to delete a task then you need to enter some information about this task, like so: <b>task, date, delete</b>.
Remember, it's important to include <b>at the end</b> of your message what function you want to use specifically!

For example: 
do chores, 2022-12-31, delete
read a book, 2022-08-01, delete
watch a film, 2015-03-15, delete
    
<b>WARNING!</b> Enter your date exactly like this: <b>YYYY-MM-DD</b>(2017-01-03, 2015-05-17 and ect.)
    
Here is a list of all your tasks: 
{all_tasks}""", parse_mode='html')

    @bot.message_handler(func=lambda mess: mess.text.endswith('delete'))
    def deleting_from_db(mess):
        if mess.text != '' and ',' in mess.text:
            bot.send_message(mess.chat.id, 'Okay, I will delete it in a second!')
            res = mess.text.split(', ')
            delete_task(user_id=mess.from_user.id, task=res[0], date=res[1])
            bot.send_message(mess.chat.id, f"""Done! Here is how your to do list is looking now:
{all_tasks}""")
        else:
            bot.send_message(mess.chat.id, 'Sorry, your formatting is missing a comma or is empty, try again: /delete')


@bot.message_handler(commands=['update'])
def update(message):
    all_tasks = '\n'.join([f'{task}, {date}' for task, date in show_all(user_id=message.from_user.id)])

    bot.send_message(message.chat.id, f"""
Need to update or change your task? Just write a message in, again, the same format, but add there an updated version of a task: <b>task, date, new task, update</b>
Remember, it's important to include <b>at the end</b> of your message what function you want to use specifically!

For example: 
do chores, 2022-12-31, wash dishes, update
read a book, 2022-08-01, listen to music, update
watch a film, 2015-03-15, play guitar, update

<b>WARNING!</b> Enter your date exactly like this: <b>YYYY-MM-DD</b>(2017-01-03, 2015-05-17 and ect.)

Here is a list of all your tasks, so it would be conveniently to chose which to change:
{all_tasks}  
""", parse_mode='html')

    @bot.message_handler(func=lambda mess: mess.text.endswith('update'))
    def update_task(mess):
        if mess.text != '' and ',' in mess.text:
            bot.send_message(mess.chat.id, "Okay, I'm updating your task...")
            res = mess.text.split(', ')
            change_task(user_id=mess.from_user.id, task=res[0], date=res[1], update=res[2])
            bot.send_message(mess.chat.id, f"""Now your ToDo list is changed:
{res[2]}, {res[1]}""")
        else:
            bot.send_message(mess.chat.id, 'Sorry, your formatting is missing a comma or is empty, try again.')


@bot.message_handler(commands=['show_all_for_week'])
def show_7(message):
    res = '\n'.join([f'{task}, {date}' for task, date in show_week(user_id=message.from_user.id)])
    bot.send_message(message.chat.id, f"""Here are your tasks for the next week:
{res}""")


@bot.message_handler(commands=['show_all_for_month'])
def show_30(message):
    res = '\n'.join([f'{task}, {date}' for task, date in show_month(user_id=message.from_user.id)])
    bot.send_message(message.chat.id, f"""Here are your tasks for a month:
    {res}""")


@bot.message_handler(commands=['show_for_all_time'])
def show_for_all_time(message):
    res = '\n'.join([f'{task}, {date}' for task, date in show_all(user_id=message.from_user.id)])
    bot.send_message(message.chat.id, f"""Here are all your tasks:
    {res}""")


bot.infinity_polling()
