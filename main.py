# -*- coding: utf-8 -*-
# PolyGomino by in_zet
# 2024/3/22 ~

import pygame
import os
from shapes import *
import json
from pygame.locals import *
import random
import time
import copy


def block_turn_right():
    global current_block_shape, current_block_position
    if current_block_shape:
        block_info = current_block_shape[-1]
        new_shape = []

        for i in range(block_info[1]):
            new_shape.append([j[i] for j in current_block_shape[-2::-1]])
        new_shape.append(block_info[::-1])

        current_block_shape = new_shape

        if block_info[0] > block_info[1]:
            final_position = current_block_position[1] + block_info[0]
            if final_position >= 7:
                current_block_position[1] -= final_position - 6
        elif block_info[0] < block_info[1]:
            final_position = current_block_position[0] + block_info[1]
            if final_position >= 7:
                current_block_position[0] -= final_position - 6


def block_turn_left():
    global current_block_shape, current_block_position
    if current_block_shape:
        block_info = current_block_shape[-1]
        new_shape = []

        for i in range(block_info[1])[::-1]:
            new_shape.append([j[i] for j in current_block_shape[:-1]])
        new_shape.append(block_info[::-1])

        current_block_shape = new_shape

        if block_info[0] > block_info[1]:
            final_position = current_block_position[1] + block_info[0]
            if final_position >= 7:
                current_block_position[1] -= final_position - 6
        elif block_info[0] < block_info[1]:
            final_position = current_block_position[0] + block_info[1]
            if final_position >= 7:
                current_block_position[0] -= final_position - 6


def block_flip_front():
    global current_block_shape
    if current_block_shape:
        current_block_shape = current_block_shape[-2::-1] + current_block_shape[-1]


def block_flip_side():
    global current_block_shape
    if current_block_shape:
        current_block_shape = [i[::-1] for i in current_block_shape[:-1]] + current_block_shape[-1]


def block_move_up():
    global current_block_shape, current_block_position
    if current_block_shape:
        if current_block_position[0] != 0:
            current_block_position = [current_block_position[0] - 1, current_block_position[1]]


def block_move_down():
    global current_block_shape, current_block_position
    if current_block_shape:
        if current_block_position[0] + current_block_shape[-1][0] < 6:
            current_block_position = [current_block_position[0] + 1, current_block_position[1]]


def block_move_right():
    global current_block_shape, current_block_position
    if current_block_shape:
        if current_block_position[1] != 0:
            current_block_position = [current_block_position[0], current_block_position[1] - 1]


def block_move_left():
    global current_block_shape, current_block_position
    if current_block_shape:
        if current_block_position[1] + current_block_shape[-1][1] < 6:
            current_block_position = [current_block_position[0], current_block_position[1] + 1]


def block_move_to(block_position_moveto: list):
    global current_block_shape, current_block_position
    if current_block_shape:
        if block_position_moveto[0] + current_block_shape[-1][0] < 6 and \
                block_position_moveto[1] + current_block_shape[-1][1] < 6:
            current_block_position = block_position_moveto


def block_drop_check() -> bool:
    # if current_block_shape != ():
    #     block_info = current_block_shape[-1]
    #     for i in range(block_info[0]):
    #         for j in range(block_info[1]):
    #             if current_block_shape[i][j]:
    #                 if board[current_block_position[0] + i][current_block_position[1] + j]:
    #                     return False
    #     return True
    for i in current_block_shape[:-1]:
        if 2 in i:
            return False
    return True


def block_map():
    global current_block_shape
    for i in range(current_block_shape[-1][0]):
        for j in range(current_block_shape[-1][1]):
            if current_block_shape[i][j]:
                if board[i + current_block_position[0]][j + current_block_position[1]]:
                    current_block_shape[i][j] = 2
                else:
                    current_block_shape[i][j] = 1


def block_drop():
    global board, current_block_shape, current_block_position, deck_selected, turn
    block_info = current_block_shape[-1]
    for i in range(block_info[0]):
        for j in range(block_info[1]):
            if current_block_shape[i][j]:
                board[current_block_position[0] + i][current_block_position[1] + j] = 1
    deck_selected = 0
    current_block_shape = []
    turn += 1


def block_delete_check() -> list | bool:
    global board
    block_delete_target = []
    target_tmp = []

    # Horizontal

    for i in range(6):
        if board[i][0] == 1:
            target_tmp.append((i, 0))
            for j in range(1, 6):
                if board[i][j] == 1:
                    target_tmp.append((i, j))
                else:
                    target_tmp = []
                    break

                if j >= 4:
                    block_delete_target += target_tmp
                    target_tmp = []

        else:
            for j in range(1, 6)[::-1]:
                if board[i][j] == 1:
                    target_tmp.append((i, j))
                else:
                    target_tmp = []
                    break

                if j == 1:
                    block_delete_target += target_tmp
                    target_tmp = []

    # Vertical

    for i in range(6):
        if board[0][i] == 1:
            target_tmp.append((0, i))
            for j in range(1, 6):
                if board[j][i] == 1:
                    target_tmp.append((j, i))
                else:
                    target_tmp = []
                    break

                if j >= 4:
                    block_delete_target += target_tmp
                    target_tmp = []

        else:
            for j in range(1, 6)[::-1]:
                if board[j][i] == 1:
                    target_tmp.append((j, i))
                else:
                    target_tmp = []
                    break

                if j == 1:
                    block_delete_target += target_tmp
                    target_tmp = []

    # Diagonal_5

    diag_5_start = [(0, 1), (1, 0), (4, 0), (5, 1)]

    for i in range(3):

        if i <= 1:
            modf = 1
        else:
            modf = -1

        for j in range(5):
            if board[diag_5_start[i][0] + j * modf][diag_5_start[i][1] + j] == 1:
                target_tmp.append((diag_5_start[i][0] + j * modf, diag_5_start[i][1] + j))
            else:
                target_tmp = []
                break

            if j == 4:
                block_delete_target += target_tmp
                target_tmp = []

    # Diagonal_6_down

    if board[0][0] == 1:
        target_tmp.append((0, 0))
        for j in range(1, 6):
            if board[j][j] == 1:
                target_tmp.append((j, j))
            else:
                target_tmp = []
                break

            if j >= 4:
                block_delete_target += target_tmp
                target_tmp = []

    else:
        for j in range(1, 6)[::-1]:
            if board[j][j] == 1:
                target_tmp.append((j, j))
            else:
                target_tmp = []
                break

            if j == 1:
                block_delete_target += target_tmp
                target_tmp = []

    # Diagonal_6_up

    if board[5][0] == 1:
        target_tmp.append((5, 0))
        for j in range(1, 6):
            if board[5 - j][j] == 1:
                target_tmp.append((5 - j, j))
            else:
                target_tmp = []
                break

            if j >= 4:
                block_delete_target += target_tmp
                target_tmp = []

    else:
        for j in range(1, 6)[::-1]:
            if board[5 - j][j] == 1:
                target_tmp.append((5 - j, j))
            else:
                target_tmp = []
                break

            if j == 1:
                block_delete_target += target_tmp
                target_tmp = []

    if block_delete_target:
        return block_delete_target
    return False


def block_delete(block_delete_target):
    global board, score
    for i in block_delete_target:
        board[i[0]][i[1]] = 0
    score += 10 * len(block_delete_target)


def block_pick(slot: int):
    global turn, deck
    shape_num = 0
    for i in range(len(inflection)):
        if turn <= inflection[i]:
            shape_num = random.choices([0, 1, 2, 3, 4], difficulties[i])
            break
    if turn > inflection[-1]:
        shape_num = random.choices([0, 1, 2, 3, 4], difficulties[-1])

    deck[slot] = [shape_num, random.randint(0, len(llist_shape[shape_num]) - 1)]


def block_load(slot: int):
    global deck, deck_selected, current_block_position, current_block_shape
    deck_selected = slot
    current_block_position = [0, 0]
    current_block_shape = [list(i) for i in llist_shape[deck[slot][0]][deck[slot][1]]]


def block_unload():
    global deck_selected, current_block_shape
    deck_selected = 0
    current_block_shape = []


def ministone_draw():
    pass


def pos(tileset_position: list | int, sprite_type: int = 0):
    # sprite type // 0: x4 1: stone 2: selection 3: card 4: score 5: turn

    if sprite_type == 0:
        return [tileset_position[0] * 4, tileset_position[1] * 4]
    elif sprite_type == 1:
        return [4 * 17 * tileset_position[1], 4 * 17 * tileset_position[0]]
    elif sprite_type == 2:
        return [4 * 17 * tileset_position[1], 4 * 17 * tileset_position[0]]
    elif sprite_type == 3:
        return [4 * 34 * tileset_position, 0]
    elif sprite_type == 4:
        return [4 * 8 * tileset_position, 0]
    elif sprite_type == 5:
        return [4 * 8 * tileset_position, 15]


class AnimatedSprite:
    def __init__(self, size: tuple[int, int], init_pos: tuple, *directorys):

        self.size = size
        self.images = dict()
        self.queue = []
        self.init_pos = init_pos

        for directory in directorys:
            temp_file_list = list(filter(os.path.isfile, [f'{directory}\\{i}' for i in os.listdir(directory)]))
            folder_list = list(filter(os.path.isdir, [f'{directory}\\{i}' for i in os.listdir(directory)]))
            for i in temp_file_list:
                self.images[i.split("\\")[-1].split(".")[0]] = pygame.image.load(i).convert_alpha()

            for i in folder_list:
                temp_file_list = sorted(list(filter(os.path.isfile, [f'{i}\\{j}' for j in os.listdir(i)])))
                self.images[i.split("\\")[-1]] = [pygame.image.load(j).convert_alpha() for j in temp_file_list]

    # def add_animation(self, directory: str, name: str):
    #     file_list = sorted(list(filter(os.path.isfile, os.listdir(directory))))
    #     self.images[name] \
    #         = [pygame.image.load(f'{directory}\\{file_list[i]}').convert_alpha() for i in range(len(file_list))]
    #
    # def add_images(self, directory: str):
    #     file_list = list(filter(os.path.isfile, os.listdir(directory)))
    #     for i in file_list:
    #         self.images[i.split(".")[0]] = pygame.image.load(f'{directory}\\{i}').convert_alpha()

    def add_positioned_animation(self, target_image: str, name: str, position: list[list, int]):
        self.images[name] \
            = position + [self.images[target_image], "PA"]

    def event_call(self, current_event: str, duration: int, next_event: str, position: list[int, int]):
        self.queue.append([current_event, duration, next_event, position])

    def event_check(self):
        for i in range(len(self.queue)):
            if self.queue[i][1] != 0:
                self.queue[i][1] -= 1
                if self.queue[i][1] == 0:
                    if self.queue[i][2] is None:
                        del self.queue[i]
                    else:
                        self.queue[i][0] = self.queue[i][2]
                        self.queue[i][2] = None

    # def event_delete(self):
    #     self.queue = []

    def draw(self):
        for i in self.queue:
            temp_target = self.images[i[0]]

            if isinstance(temp_target, list):

                if temp_target[-1] == "PA":
                    animation_number = len(temp_target) - 2 - (i[1] + animation_delay - 1) // animation_delay
                    temp_position = tuple([pos(self.init_pos[j] + pos(i[3])[j] + temp_target[animation_number])
                                           for j in range(2)])

                    screen.blit(temp_target[-2], temp_position)

                else:
                    animation_number = len(temp_target) - (i[1] + animation_delay - 1) // animation_delay
                    temp_position = tuple([pos(self.init_pos[j] + pos(i[3])[j]) for j in range(2)])

                    screen.blit(temp_target[animation_number], temp_position)

            else:
                screen.blit(temp_target, pos(i[3]))


board = [[0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]

deck = [[], [], []]
deck_selected = 0  # 1,2,3 / 0 : not selected
current_block_shape = []  # [] : not selected
current_block_position = []  # row, column / [] : not selected
turn = 0
score = 0

with open('difficulty.json') as f:
    json_object = json.load(f)

inflection = json_object['inflection']
difficulties = json_object['difficulties']

button_place = AnimatedSprite((80, 20), (168, 128),
                              ".\\resources\\buttons\\button_place")
button_down = AnimatedSprite((38, 24), (189, 102),
                             ".\\resources\\buttons\\button_down")
button_up = AnimatedSprite((38, 24), (189, 80),
                           ".\\resources\\buttons\\button_up")
button_left = AnimatedSprite((20, 46), (168, 80),
                             ".\\resources\\buttons\\button_left")
button_right = AnimatedSprite((20, 46), (228, 80),
                              ".\\resources\\buttons\\button_right")
button_flipfront = AnimatedSprite((40, 20), (167, 58),
                                  ".\\resources\\buttons\\button_flipfront")
button_flipside = AnimatedSprite((40, 20), (209, 58),
                                 ".\\resources\\buttons\\button_flipside")
button_turnleft = AnimatedSprite((40, 20), (167, 40),
                                 ".\\resources\\buttons\\button_turnleft")
button_turnright = AnimatedSprite((40, 20), (209, 40),
                                  ".\\resources\\buttons\\button_turnright")

cards = AnimatedSprite((28, 39), (61, 111), ".\\resources\\cards")
cards.add_positioned_animation()

numbers = AnimatedSprite((7, 11), (212, 6), ".\\resources\\numbers")
numbers.add_positioned_animation()

stones = AnimatedSprite((18, 23), (57, 1), ".\\resources\\stones")
selections = AnimatedSprite((22, 22), (55, 4),
                            ".\\resources\\selections\\selection_blue",
                            ".\\resources\\selections\\selection_red")

asp_list = [button_place, button_down, button_up, button_left, button_right, button_flipfront, button_flipside,
            button_turnleft, button_turnright, cards, numbers, stones]

####################

pygame.init()

window_size = [1024, 600]
screen = pygame.display.set_mode(window_size)

title = "PolyGomino"
pygame.display.set_caption(title)

fps = 10
frame = 0
animation_delay = 1
run = 1


def main_loop():
    global frame
    while run == 1:
        frame += 1
        pygame.time.Clock().tick(fps)

        pygame.display.flip()


main_loop()
