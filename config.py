PORT = 5555
BALL_RADIUS = 5
START_RADIUS = 7
ROUND_TIME = 300
MASS_LOSS_TIME = 5
W, H = 1600, 830
SCORE = "SCORE"


rgb = [0,128,255]
colors = [(a,b,c) for a in rgb for b in rgb for c in rgb]
colors.remove((255,255,255))
colors.remove((0,0,0))

color_change = {"red":(255, 0,0), "green":(0,255,0), "blue":(0,0,255)}

SERVER_IP = "192.168.232.240"
HOST = "192.168.232.240"

PLAYER_RADIUS = 10
START_VEL = 9