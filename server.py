import socket
from _thread import *
import _pickle as pickle
import time
import random
import math
from config import *
from typing import *

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e) + "\n" + "Event: Server could not start")
    exit()
S.listen()
print(f"Event: Server started")

players = {}
balls = []

# how many players are connected
connections = 0

# id of player
id = 0

game_started = False
stat_time = 0
game_time = "Starting Soon"
nxt = 1


def release_mass(players: Dict) -> None:
    for player in players:
        player_score = players[player]
        if player_score[SCORE] > 8:
            player_score[SCORE] = math.floor(player_score[SCORE] * 0.9)


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# new player eat power of spot
def check_collision(players: Dict, balls: List) -> None:
    for player in players:
        p = players[player]
        x = p["x"]
        y = p["y"]
        for ball in balls:
            if dist(x, y, ball[0], ball[1]) <= START_RADIUS + p[SCORE]:
                p[SCORE] = p[SCORE] + 0.5
                balls.remove(ball)


# players eat each other
def player_collision(players: Dict) -> None:
    # for conveniance which player will eat another
    sorted_players = sorted(players, key=lambda x: players[x]["SCORE"])

    for i in range(len(sorted_players)):
        one = sorted_players[i]
        for j in range(i + 1, len(sorted_players)):
            two = sorted_players[j]
            one_x = players[one]["x"];
            one_y = players[one]["y"]
            two_x = players[two]["x"];
            two_y = players[two]["y"]

            # one player eat another
            if dist(one_x, one_y, two_x, two_y) < players[two][SCORE] - players[one][SCORE] * 0.8:
                players[two][SCORE] += players[one][SCORE]
                players[one][SCORE] = 0
                players[one]["x"], players[one]["y"] = get_new_spot_for_player(players)
                print(f"Event " + players[two]["name"] + " ATE " + players[one]["name"])


def create_balls(balls: List, n: int) -> None:
    for i in range(n):
        while True:
            flag = True
            x = random.randrange(0, W)
            y = random.randrange(0, H)
            for player in players:
                p = players[player]
                dis = math.sqrt((x - p["x"]) ** 2 + (y - p["y"]) ** 2)
                if dis <= START_RADIUS + p[SCORE]:
                    flag = False
            if flag: break

        balls.append((x, y, random.choice(colors)))


# search a spot for new player
def get_new_spot_for_player(players: Dict) -> Tuple[int, int]:
    while True:
        flag = True
        x = random.randrange(0, W)
        y = random.randrange(0, H)
        for key in players:
            player = players[key]
            # players overlap
            if dist(x, y, player["x"], player["y"]) <= START_RADIUS + player[SCORE]:
                flag = False
                break
        if flag: break
    return x, y


def new_thread_for_client(conn: str, id: int) -> None:
    global connections, players, balls, game_time, nxt, game_started
    curr_id = id
    # receive name and color
    data = conn.recv(40)
    my_data = data.decode("utf-8")
    nick, color = my_data.split(";")
    print("Event:", nick, "connected")
    if color != "null":
        color = color_change[color]
    else:
        color = colors[curr_id]

    x, y = get_new_spot_for_player(players)
    players[curr_id] = {"x": x, "y": y, "color": color, SCORE: 0, "name": nick}

    conn.send(str.encode(str(curr_id)))
    while True:

        if game_started:
            game_time = round(time.time() - game_started_time)
            if game_time >= ROUND_TIME:
                game_started = False
            else:
                if game_time // MASS_LOSS_TIME == nxt:
                    nxt += 1
                    release_mass(players)
                    print(f"Event {nick}'s mass was reduced")
        try:
            data = conn.recv(32)

            if not data:
                break

            data = data.decode("utf-8")
            if data.split(" ")[0] == "move":
                split_data = data.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                players[curr_id]["x"] = x
                players[curr_id]["y"] = y

                if game_started:
                    check_collision(players, balls)
                    player_collision(players)

                if len(balls) < 120:
                    create_balls(balls, random.randrange(80, 120))
                    print("Event: Creating more balls")

                send_data = pickle.dumps((balls, players, game_time))

            elif data.split(" ")[0] == "id":
                send_data = str.encode(str(curr_id))

            elif data.split(" ")[0] == "jump":
                send_data = pickle.dumps((balls, players, game_time))
            else:
                send_data = pickle.dumps((balls, players, game_time))

            conn.send(send_data)

        except Exception as e:
            str(e)
            break

        time.sleep(0.001)

    print(f"Event: {nick} [{curr_id}] disconnected")

    connections -= 1
    del players[curr_id]
    conn.close()


create_balls(balls, random.randrange(200, 250))
print("Event: Waiting for connections")

while True:
    host, addr = S.accept()
    print(host, addr)
    print(f"Event: {addr} connected")

    if addr[0] == SERVER_IP and not game_started:
        game_started = True
        game_started_time = time.time()
        print("Event: Game Started")
    connections += 1
    start_new_thread(new_thread_for_client, (host, id))
    id += 1
