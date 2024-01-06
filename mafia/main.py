from telebot import TeleBot
import db 
from time import sleep

TOKEN = '6671628811:AAEMZaNS8HVAzT5Y3NO0dFUiICCEAYREUps'
bot = TeleBot(TOKEN)
game = False
night = False


@bot.message_handler(func=lambda m: m.text.lower() == 'готов к игре' and m.chat.type == 'private')
def send_text(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name} играет')
    bot.send_message(message.from_user.id, 'Вы добавлены в игру')
    db.insert_player(message.from_user.id,
                     username=message.from_user.first_name)


@bot.message_handler(commands["play"])
def game_on(message):
    if not game:
        bot.send_message(
            message.chat.id, text='Если хотите играть напишите "готов к игре" в лс'
        )


@bot.message_handler(commands["game"])
def game_start(message):
    global game
    players = db.players_amount()
    if players >= 5 and not game:
        db.set_roles(players)
        players_roles = db.get_players_roles()
        mafia_usernames = db.get_mafia_usernames()
        for player_id, role in players_roles:
            bot.send_message(player_id, text=role)
            if role == 'mafia':
                bot.send_message(player_id,
                                 text=f'Все члены мафии:\n{mafia_usernames}')
        game = True
        bot.send_message(message.chat.id, text='Игра начилась!')
        return
    else:
        bot.send_message(message.chat.id, text='Недостаточно игроков!')


@bot.message_handler(commands["kick"])
def kick(message):
    username = ' '.join(message.text.split(' ')[1:]) 
    usernames = db.get_all_alive()
    if not night: # Проверяем что сейчас ночь
        if not username in usernames: # Проверяем что пользователь в игре 
            bot.send_message(message.chat.id, 'Такого имени нет')
            return
        voted = db.vote('citizen_vote', username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, 'Ваш голос учитан')
            return
        bot.send_message(message.chat.id, ' У вас больше нет попыток чтобы проголосовать')
        return
    bot.send_message(
        message.chat.id, 'Наступила ночь, вы не сможете никого выгнать'
    )


'''
# Под?
@bot.message_handler(commands["kill"])
def kill_player(message):
    user_id = db.get_user_id(message.text.split(' ')[1])
    if not night:
        bot.send_message(message.chat.id, text='Сейчас не ночь!')
    elif not db.is_alive(user_id):
        bot.send_message(message.chat.id, text='Игрок уже мертв!')
    elif not db.is_mafia(message.from_user.id):
        bot.send_message(message.chat.id, text='У вас нет прав голосовать!')
    else:
        db.vote(user_id)
'''





















'''
string = '/kick Rahat Lukum'
string = string.split(' ')
print(string)                       ----->   username = ' '.join(message.text.split(' ')[1:])
print(string[1:])
print(' '.join(string[1:]))
'''

