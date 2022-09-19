import contextlib

with contextlib.redirect_stdout(None):
    import pygame
from client import Network
import os
from config import *
from typing import *

pygame.font.init()
NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)

players = {}
balls = []


# pretty time
def convert_time(t: int) -> str:
    if type(t) == str: return t
    if int(t) < 60:
        return str(t) + "s"
    else:
        s = str(t % 60)
        if int(s) < 10: s = "0" + s
        return str(t // 60) + ":" + s


# "clear" screen, redraw balls, redraw players, redraw scoreboard classification, redraw time, redraw score
def redraw_window(players: Dict, balls: List, game_time: int, score: int) -> None:
    global MY_WINDOW
    n = len(players)
    MY_WINDOW.fill((255, 255, 255))
    for ball in balls: pygame.draw.circle(MY_WINDOW, ball[2], (ball[0], ball[1]), BALL_RADIUS)

    for i in sorted(players, key=lambda player: players[player][SCORE]):
        player = players[i]
        pygame.draw.circle(MY_WINDOW, player["color"], (player["x"], player["y"]), PLAYER_RADIUS + round(player[SCORE]))
        nick = NAME_FONT.render(player["name"], True, (0, 0, 0))
        MY_WINDOW.blit(nick, (player["x"] - nick.get_width() / 2, player["y"] - nick.get_height() / 2))

    sort_players = list(reversed(sorted(players, key=lambda player: players[player][SCORE])))
    scoreboard = TIME_FONT.render("Scoreboard", True, (0, 0, 0))
    start_y = 40
    x = W - scoreboard.get_width() - 20
    MY_WINDOW.blit(scoreboard, (x, 5))

    three_or_less_players = min(n, 3)
    for place, player in enumerate(sort_players[:three_or_less_players]):
        time = SCORE_FONT.render(str(place + 1) + ". " + str(players[player]["name"]), True, (0, 0, 0))
        MY_WINDOW.blit(time, (x, start_y + place * 20))

    time = TIME_FONT.render("Time: " + convert_time(game_time), True, (0, 0, 0))
    MY_WINDOW.blit(time, (10, 10))
    time = TIME_FONT.render("Score: " + str(round(score)), True, (0, 0, 0))
    MY_WINDOW.blit(time, (10, 15 + time.get_height()))


def connect_and_move(nick: str, color:str) -> None:
    global players
    server = Network()
    current_id = server.connect(nick, color)
    balls, players, game_time = server.send("get")

    clock = pygame.time.Clock()
    flag = True
    while flag:
        clock.tick(30)
        player = players[current_id]
        speed = max(START_VEL - round(player[SCORE] / 10), 1)

        if pygame.key.get_pressed()[pygame.K_a]:
            if player["x"] - speed - PLAYER_RADIUS - player[SCORE] >= 0: player["x"] = player["x"] - speed
        if pygame.key.get_pressed()[pygame.K_d]:
            if player["x"] + speed + PLAYER_RADIUS + player[SCORE] <= W: player["x"] = player["x"] + speed
        if pygame.key.get_pressed()[pygame.K_w]:
            if player["y"] - speed - PLAYER_RADIUS - player[SCORE] >= 0: player["y"] = player["y"] - speed
        if pygame.key.get_pressed()[pygame.K_s]:
            if player["y"] + speed + PLAYER_RADIUS + player[SCORE] <= H: player["y"] = player["y"] + speed

        data = "move " + str(player["x"]) + " " + str(player["y"])

        balls, players, game_time = server.send(data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: flag = False

        redraw_window(players, balls, game_time, player[SCORE])
        pygame.display.update()

    server.disconnect()
    pygame.quit()
    quit()

MY_WINDOW = None
def start_new_game(nick: str, color:str=None) -> None:
    global MY_WINDOW
    MY_WINDOW = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Agar.io v2")
    if not color: color="null"
    connect_and_move(nick, color)
