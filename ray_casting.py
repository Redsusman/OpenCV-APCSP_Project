import pygame as game
import numpy as np

game.init()

game.display.set_mode((200, 400))

while True:
    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()
    game.display.update()