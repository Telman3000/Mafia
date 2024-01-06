import sqlite3
from random import shuffle


def insert_player(player_id,username):
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"INSERT INTO players (player_id, username) VALUES ('{player_id}', '{username}')"
    cur.execute(sql)
    con.commit()
    con.close()

def players_amount():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"SELECT * FROM PLAYERS"
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return len(res)

def get_mafia_usernames():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"SELECT username FROM PLAYERS where role = 'mafia' "   
    cur.execute(sql)
    data = cur.fetchall()
    names = ''
    for row in data:
        name = row[0]
        names += name + '\n'
    con.close()
    return names

def get_players_roles():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"SELECT player_id, role From players"   
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data 

def get_all_alive():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    sql = f"SELECT username from players WHERE dead = 0"
    cur.execute(sql)
    data = cur.fetchall()
    data = [row[0] for row in data]                                                                     
    con.close()
    return data 

def set_roles():
    game_roles = ['citizen'] * players_amount
    mafias = int(players * 0.3)
    for i in range(mafias):
        game_roles[i] = 'mafia'
    random.shuffle(game_roles)
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"SELECT player_id FROM PLAYERS")
    player_ids_row = cur.fetchall()
    for role, players_id in zip(game_roles, player_ids):
        sql = f"UPDATE players SET role = '{role}' WHERE player_id = {row[0]}"
        cur.execute(sql)
    con.commit()
    con.close()

def vote(type, username, player_id):
    # type = 'mafia_vote, citizen_vote'
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(
        f"SELECT username FROM players WHERE player_id = {player_id} and dead = 0 and voted = 0")
    can_vote = cur.fetchone()
    if can_vote:  # если список не пустой, значит игрок сущевствует
        cur.execute(
            f"UPDATE players SET {type} = {type} +1 WHERE username = '{username}'"
        )
        cur.execute(
            f"UPDATE players SET voted = +1 WHERE usernaplayer_idme = '{player_id}'"
        )
        con.commit()
        con.close()
        return True
    con.close()
    return False


def mafia_kill():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    # Выбираем за кого больше всего голосов отдала мафия
    cur.execute(f"SELECT MAX(mafia_vote) FROM players")
    max_votes = cur.fetchone()[0]
    # Выбираем кол-во игроков за мафию, которых не убили
    cur.execute(
        f"SELECT COUNT(*) FROM players WHERE dead = '0' and role = 'mafia' "
    )
    mafia_alive = cur.fetchone()[0]
    username_killed = 'никого'
    # Максимальное кол-во голосов мафии должно равняться кол-ву мафий
    if set_roles == mafia_alive:
        # Получаем имя пользователя, за которого проголосовали
        cur.execute(f"SELECT username FROM players WHERE mafia_vote = {max_votes}")
        username_killed = cur.fetchone()[0]
        # Делаем update в БД что игрок мертв
        cur.execute(f"UPDATE players SET dead = 1 WHERE username = '{username_killed}' ")
        con.commit()
    con.close()
    return username_killed


def citizen_kill():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    # Выбираем за кого больше всего голосов отдали гороожане
    cur.execute(f"SELECT MAX(citizen_vote) FROM players")
    max_votes = cur.fetchone()[0]
    # Выбираем кол-во живых горожан
    cur.execute(f"SELECT COUNT(*) FROM players WHERE citizen_vote = {max_votes}")           
    max_votes_count = cur.fetchone()[0]                                                       
    username_killed = 'никого'
    # ПроверяемЮ что только 1 человек макс. кол-во голосов
    if max_votes_count == 1:
        cur.execute(f"SELECT username FROM players WHERE citizen_vote = {max_votes}")
        username_killed = cur.fetchone()[0]
        # Делаем update в БД что игрок мертв
        cur.execute(f"UPDATE players SET dead = 1 WHERE username = '{username_killed}' ")
        con.commit()
    con.close()
    return username_killed


def get_killed(night):
    if not night:
        username_killed = db.citizen_kill() # Если день, запрашиваем кого выгнали горожане
        return f"Горожане выгнали: {username_killed}"
    # Если ночь, получаем имя игрока кого убила мафия
    username_killed = db.mafia_kill()
    return f"Мафия уже убила: {username_killed}"


def clear(dead=False):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"UPDATE players SET citizen_vate = 0, mafia_vote = 0, voted = 0"
    # Добавим условие "оживления", для повторной игры 
    if dead:
        sql += ' , dead = 0'
    cur.execute(sql)
    con.commit()
    con.close()









''' 
new_data = []
for row in data:             Можно упростить
new_data.append(row[0])     ------->     data = [row[0] for row in data]
data = new_data 
'''
