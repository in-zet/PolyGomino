# -*- coding: utf-8 -*-
# PolyGomino by in_zet
# 2024/03/22 ~
# 2024/04/08 v0.1.0

import sys
import pygame
import os
from shapes import *
import json
from pygame.locals import *
import random
import time
import copy


pygame.init()


def block_turn_right():
    global current_block_shape, current_block_position
    if current_block_shape:

        selection_call(0)

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

        block_map()
        selection_call(2, isinitiallize=False)

    button_turnright.event_call("button_turnright_press", None)


def block_turn_left():
    global current_block_shape, current_block_position
    if current_block_shape:

        selection_call(0)

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

        block_map()
        selection_call(2, isinitiallize=False)

    button_turnleft.event_call("button_turnleft_press", None)


def block_flip_front():
    global current_block_shape
    if current_block_shape:
        selection_call(0)

        current_block_shape = current_block_shape[-2::-1] + [current_block_shape[-1]]

        block_map()
        selection_call(2, isinitiallize=False)

    button_flipfront.event_call("button_flipfront_press", None)


def block_flip_side():
    global current_block_shape
    if current_block_shape:
        selection_call(0)

        current_block_shape = [i[::-1] for i in current_block_shape[:-1]] + [current_block_shape[-1]]

        block_map()
        selection_call(2, isinitiallize=False)

    button_flipside.event_call("button_flipside_press", None)


def block_move_up():
    global current_block_shape, current_block_position
    if current_block_shape:
        if current_block_position[0] != 0:
            current_block_position = [current_block_position[0] - 1, current_block_position[1]]
            block_map()
            selection_call(4)

    button_up.event_call("button_up_press", None)


def block_move_down():
    global current_block_shape, current_block_position
    if current_block_shape:
        if current_block_position[0] + current_block_shape[-1][0] < 6:
            current_block_position = [current_block_position[0] + 1, current_block_position[1]]
            block_map()
            selection_call(3)

    button_down.event_call("button_down_press", None)


def block_move_right():
    global current_block_shape, current_block_position
    if current_block_shape:
        if current_block_position[1] + current_block_shape[-1][1] < 6:
            current_block_position = [current_block_position[0], current_block_position[1] + 1]
            block_map()
            selection_call(6)

    button_right.event_call("button_right_press", None)


def block_move_left():
    global current_block_shape, current_block_position
    if current_block_shape:
        if current_block_position[1] != 0:
            current_block_position = [current_block_position[0], current_block_position[1] - 1]
            block_map()
            selection_call(5)

    button_left.event_call("button_left_press", None)


def block_move_to(block_position_moveto: list):
    global current_block_shape, current_block_position
    if current_block_shape:
        if block_position_moveto[0] + current_block_shape[-1][0] < 6 and \
                block_position_moveto[1] + current_block_shape[-1][1] < 6:
            tmp_pos = current_block_position
            current_block_position = block_position_moveto

            block_map()

            if tmp_pos[0] == block_position_moveto[0]:
                if tmp_pos[1] == block_position_moveto[1]:
                    pass
                elif tmp_pos[1] > block_position_moveto[1]:
                    selection_call(5)
                else:
                    selection_call(6)
            elif tmp_pos[0] > block_position_moveto[0]:
                if tmp_pos[1] == block_position_moveto[1]:
                    selection_call(4)
                elif tmp_pos[1] > block_position_moveto[1]:
                    selection_call(9)
                else:
                    selection_call(10)
            else:
                if tmp_pos[1] == block_position_moveto[1]:
                    selection_call(3)
                elif tmp_pos[1] > block_position_moveto[1]:
                    selection_call(7)
                else:
                    selection_call(8)


# def block_drop_check() -> bool:
#     # if current_block_shape != ():
#     #     block_info = current_block_shape[-1]
#     #     for i in range(block_info[0]):
#     #         for j in range(block_info[1]):
#     #             if current_block_shape[i][j]:
#     #                 if board[current_block_position[0] + i][current_block_position[1] + j]:
#     #                     return False
#     #     return True
#     for i in current_block_shape[:-1]:
#         if 2 in i:
#             return False
#     return True


def block_map():
    # 1: not overlapped / 2: overlapped

    global current_block_shape

    for i in range(current_block_shape[-1][0]):
        for j in range(current_block_shape[-1][1]):
            if current_block_shape[i][j]:
                if board[i + current_block_position[0]][j + current_block_position[1]]:
                    current_block_shape[i][j] = 2
                else:
                    current_block_shape[i][j] = 1


def block_drop() -> bool:
    global board, current_block_shape, current_block_position, deck_selected

    button_place.event_call("button_place_press", None)

    if not current_block_shape:
        return False

    for i in current_block_shape[:-1]:
        if 2 in i:
            return False

    selection_call(0)

    block_info = current_block_shape[-1]
    for i in range(block_info[0]):
        for j in range(block_info[1]):
            if current_block_shape[i][j]:
                board[current_block_position[0] + i][current_block_position[1] + j] = 1
                stones.event_call("stone_fall", "stone_stand",
                                  [current_block_position[0] + i, current_block_position[1] + j])

    block_pick(deck_selected)
    cards.event_call("card_delete", ["card_emerge", "card_non_picked"], deck_selected - 1)
    deck_selected = 0

    current_block_shape = []
    return True


def block_delete_check():
    global board, num_var
    block_delete_target = []
    target_tmp = []
    del_line_count = 0

    # Horizontal

    for i in range(6):
        if board[i][0] == 1:
            target_tmp.append([i, 0])
            for j in range(1, 5):
                if board[i][j] == 1:
                    target_tmp.append([i, j])
                else:
                    target_tmp = []
                    break

                if j == 4:
                    if board[i][5] == 1:
                        target_tmp.append([i, 5])
                    block_delete(target_tmp, del_line_count + 1)
                    block_delete_target += target_tmp
                    del_line_count += 1
                    target_tmp = []

        else:
            for j in range(1, 6)[::-1]:
                if board[i][j] == 1:
                    target_tmp.append([i, j])
                else:
                    target_tmp = []
                    break

                if j == 1:
                    block_delete(target_tmp, del_line_count + 1)
                    block_delete_target += target_tmp
                    del_line_count += 1
                    target_tmp = []

    # Vertical

    for i in range(6):
        if board[0][i] == 1:
            target_tmp.append([0, i])
            for j in range(1, 5):
                if board[j][i] == 1:
                    target_tmp.append([j, i])
                else:
                    target_tmp = []
                    break

                if j == 4:
                    if board[5][i] == 1:
                        target_tmp.append([5, i])
                    block_delete(target_tmp, del_line_count + 1)
                    block_delete_target += target_tmp
                    del_line_count += 1
                    target_tmp = []

        else:
            for j in range(1, 6)[::-1]:
                if board[j][i] == 1:
                    target_tmp.append([j, i])
                else:
                    target_tmp = []
                    break

                if j == 1:
                    block_delete(target_tmp, del_line_count + 1)
                    block_delete_target += target_tmp
                    del_line_count += 1
                    target_tmp = []

    # Diagonal_5

    diag_5_start = [(0, 1), (1, 0), (4, 0), (5, 1)]

    for i in range(4):

        if i <= 1:
            modf = 1
        else:
            modf = -1

        for j in range(5):
            if board[diag_5_start[i][0] + j * modf][diag_5_start[i][1] + j] == 1:
                target_tmp.append([diag_5_start[i][0] + j * modf, diag_5_start[i][1] + j])
            else:
                target_tmp = []
                break

            if j == 4:
                block_delete(target_tmp, del_line_count + 1)
                block_delete_target += target_tmp
                del_line_count += 1
                target_tmp = []

    # Diagonal_6_down

    if board[0][0] == 1:
        target_tmp.append([0, 0])
        for j in range(1, 5):
            if board[j][j] == 1:
                target_tmp.append([j, j])
            else:
                target_tmp = []
                break

            if j == 4:
                if board[5][5] == 1:
                    target_tmp.append([5, 5])
                block_delete(target_tmp, del_line_count + 1)
                block_delete_target += target_tmp
                del_line_count += 1
                target_tmp = []

    else:
        for j in range(1, 6)[::-1]:
            if board[j][j] == 1:
                target_tmp.append([j, j])
            else:
                target_tmp = []
                break

            if j == 1:
                block_delete(target_tmp, del_line_count + 1)
                block_delete_target += target_tmp
                del_line_count += 1
                target_tmp = []

    # Diagonal_6_up

    if board[5][0] == 1:
        target_tmp.append([5, 0])
        for j in range(1, 5):
            if board[5 - j][j] == 1:
                target_tmp.append([5 - j, j])
            else:
                # target_tmp = []
                break

            if j == 4:
                if board[0][5] == 1:
                    target_tmp.append([0, 5])
                block_delete(target_tmp, del_line_count+ 1)
                block_delete_target += target_tmp
                del_line_count += 1
                target_tmp = []

    else:
        for j in range(1, 6)[::-1]:
            if board[5 - j][j] == 1:
                target_tmp.append([5 - j, j])
            else:
                # target_tmp = []
                break

            if j == 1:
                block_delete(target_tmp, del_line_count + 1)
                block_delete_target += target_tmp
                del_line_count += 1
                target_tmp = []

    # if block_delete_target:
    #     return block_delete_target
    # return False

    for i in block_delete_target:
        board[i[0]][i[1]] = 0

    if del_line_count:
        number_call(0, (2 * del_line_count + 4) * animation_delay, isstop=True)

    return del_line_count


def block_delete(block_delete_target, delay):
    global board, num_var

    for i in block_delete_target:
        isoverlap = 0

        for j in range(len(stones.queue)):
            if i in stones.queue[j]:
                # if stones.queue[j][2] == "stone_delete":
                #     stones.event_call(None, [["stone_stand", (2 * delay - 4)], None],
                #                       i, force_duration=4, isappend=True)

                if stones.queue[j][0] == "stone_fall" and stones.queue[j][2]:
                    stones.queue[j][2] = None
                    if delay - 1:
                        stones.event_call(None, [["stone_stand", (2 * delay - 2)], "stone_delete"], i,
                                          force_duration=4, isappend=True)
                    else:
                        stones.event_call(None, "stone_delete", i,
                                          force_duration=4, isappend=True)

                    isoverlap = 1
                    break

                elif stones.queue[j][0] != "stone_fall" and stones.queue[j][1] != -1:
                    stones.event_call(None, "stone_delete", i,
                                      force_duration=(2 * delay + 2), isappend=True)

                    isoverlap = 1
                    break

        if not isoverlap:
            stones.event_call("stone_stand", "stone_delete", i,
                              force_duration=(2 * delay + 2))

    num_var["score"] += 10 * len(block_delete_target)
    if delay == 1:
        number_call(0, (2 * delay + 2), isclear=True, noappend=True)

    else:
        number_call(0, (2 * delay + 2), isclear=True)


def block_pick(slot: int):
    # slot = position + 1

    global deck
    shape_num = 0
    for i in range(len(inflection)):
        if num_var["turn"] <= inflection[i]:
            shape_num = random.choices([0, 1, 2, 3, 4], difficulties[i])[0]
            break
    if num_var["turn"] > inflection[-1]:
        shape_num = random.choices([0, 1, 2, 3, 4], difficulties[-1])[0]

    tmp_shape_num = random.randint(0, len(llist_shape[shape_num]) - 1)
    deck[slot - 1] = [list(i) for i in llist_shape[shape_num][tmp_shape_num]]

    tmp_shape_size = deck[slot - 1][-1]

    tmp_ministone_size = (6 - tmp_shape_size[0] - (tmp_shape_size[1] // tmp_shape_size[0]))

    deck_ministone[slot - 1] = [
                                [
                                 [
                                  4 * ((ministone_size_pixel[tmp_ministone_size] + 1) * [j, i][k] +
                                       ministone_preset[tuple(tmp_shape_size)][k])
                                  for k in range(2)
                                 ],
                                 ministone_images[tmp_ministone_size][deck[slot - 1][i][j]]
                                ]
                                for i in range(tmp_shape_size[0]) for j in range(tmp_shape_size[1])
                               ]


def block_load(slot: int):
    # slot = position + 1

    global deck, deck_selected, current_block_position, current_block_shape
    deck_selected = slot
    current_block_position = [0, 0]
    current_block_shape = deck[slot - 1]
    block_map()
    selection_call(1)

    cards.event_call("card_pickup", "card_picked", slot - 1)


def block_unload():
    global deck_selected, current_block_shape
    selection_call(0)
    cards.event_call("card_pickdown", "card_non_picked", deck_selected - 1)

    deck_selected = 0
    current_block_shape = []


slc_animation_list = ["lockoff", "lockon", "waitlockon", "movedown", "moveup", "moveleft", "moveright",
                      "movedownleft", "movedownright", "moveupleft", "moveupright"]
slc_color_list = ["blue", "red"]


def selection_call(animation_shape: int, isinitiallize: bool = True):
    # 0: lock off, 1: lock on, 2: wait lock on
    # 3: down 4: up 5: left 6: right
    # 7: downleft 8: downright 9: upleft 10: upright

    if isinitiallize:
        selections.event_delete()

    if animation_shape:
        for i in range(len(current_block_shape) - 1):
            for j in range(len(current_block_shape[i])):
                if current_block_shape[i][j]:
                    selections.event_call(
                        f'selection_{slc_color_list[current_block_shape[i][j] - 1]}_{slc_animation_list[animation_shape]}',
                        f'selection_{slc_color_list[current_block_shape[i][j] - 1]}_stand',
                        [i + current_block_position[0], j + current_block_position[1]], isappend=True)

    else:
        for i in range(len(current_block_shape) - 1):
            for j in range(len(current_block_shape[i])):
                if current_block_shape[i][j]:
                    selections.event_call(
                        f'selection_{slc_color_list[current_block_shape[i][j] - 1]}_{slc_animation_list[animation_shape]}',
                        None, [i + current_block_position[0], j + current_block_position[1]],
                        isappend=True)


num_var_list = ["score", "turn"]


def number_call(isscore_isturn: int, wait: int = 0,
                isclear: bool = False, isstop: bool = False, noappend: bool = False):  # WIP
    # 0: score 1: turn

    tmp_num = str(num_var[num_var_list[isscore_isturn]])
    tmp_num_len = len(tmp_num)
    tmp_num_queue = copy.deepcopy(numbers.queue)

    if isstop:
        for i in range(tmp_num_len):
            numbers.event_call(None, f'number_{tmp_num[i]}',
                               [isscore_isturn, 5 - tmp_num_len + i], isappend=True, force_duration=wait)

    if not wait:
        for i in range(tmp_num_len):
            numbers.event_call(f'number_{tmp_num[i]}_scoreup', f'number_{tmp_num[i]}',
                               [isscore_isturn, 5 - tmp_num_len + i])
    else:
        for i in range(tmp_num_len):
            tmp_pos = [isscore_isturn, 5 - tmp_num_len + i]
            for j in tmp_num_queue:
                if j[3] == tmp_pos:
                    if isclear:
                        if noappend:
                            numbers.event_call(j[0], f'number_{tmp_num[i]}_scoreup',
                                               tmp_pos, force_duration=wait)
                        else:
                            numbers.event_call(j[0], f'number_{tmp_num[i]}_scoreup',
                                               tmp_pos, isappend=True, force_duration=wait)
                    else:
                        numbers.event_call(j[0],
                                           [f'number_{tmp_num[i]}_scoreup', f'number_{tmp_num[i]}'],
                                           tmp_pos, force_duration=wait)


def pos(tileset_position: list | int, sprite_type: int = 0) -> list[int]:
    # tileset_position: row, column (if sprite_type != 0;)
    # sprite type // 0: x4 1: stone 2: selection 3: card 4: score/turn

    if sprite_type == 0:
        return [tileset_position[0] * 4, tileset_position[1] * 4]
    elif sprite_type == 1:
        return [17 * tileset_position[1], 17 * tileset_position[0]]
    elif sprite_type == 2:
        return [17 * tileset_position[1], 17 * tileset_position[0]]
    elif sprite_type == 3:
        return [34 * tileset_position, 0]
    elif sprite_type == 4:
        return [8 * tileset_position[1], 15 * tileset_position[0]]


class AnimatedSprite:
    def __init__(self, size: tuple[int, int], init_pos: tuple[int, int], sprite_type: int, *directorys: str):

        self.sprite_type = sprite_type
        self.size = size
        self.images = dict()
        self.queue = []
        self.init_pos = init_pos

        for directory in directorys:
            temp_file_list = list(filter(os.path.isfile, [f'{directory}/{i}' for i in os.listdir(directory)]))
            folder_list = list(filter(os.path.isdir, [f'{directory}/{i}' for i in os.listdir(directory)]))
            for i in temp_file_list:
                self.images[i.split("/")[-1].split(".")[0]] = pygame.image.load(i).convert_alpha()

            for i in folder_list:
                temp_file_list = sorted(list(filter(os.path.isfile, [f'{i}/{j}' for j in os.listdir(i)])))
                self.images[i.split("/")[-1]] = [pygame.image.load(j).convert_alpha() for j in temp_file_list]

    # def add_animation(self, directory: str, name: str):
    #     file_list = sorted(list(filter(os.path.isfile, os.listdir(directory))))
    #     self.images[name] \
    #         = [pygame.image.load(f'{directory}/{file_list[i]}').convert_alpha() for i in range(len(file_list))]
    #
    # def add_images(self, directory: str):
    #     file_list = list(filter(os.path.isfile, os.listdir(directory)))
    #     for i in file_list:
    #         self.images[i.split(".")[0]] = pygame.image.load(f'{directory}/{i}').convert_alpha()

    def add_positioned_animation(self, target_image: str, name: str, position: list[list[int]]):
        self.images[name] \
            = position + [self.images[target_image], "PA"]

    def event_call(self, current_event: str | None, next_event: str | None | list[list | str | None],
                   position: list[int] | int = [0, 0], isappend: bool = False, force_duration: int = 0,
                   isinsert: bool = False):

        if current_event:
            temp_target = self.images[current_event]

            if isinstance(temp_target, list):

                if temp_target[-1] == "PA":

                    if len(temp_target) == 3:
                        duration = -1
                    else:
                        duration = (len(temp_target) - 2) * animation_delay

                else:
                    duration = len(temp_target) * animation_delay

            else:
                if not force_duration:
                    duration = -1
                else:
                    duration = force_duration * animation_delay
        else:
            duration = force_duration * animation_delay

        if self.queue and not isappend:
            del_list = []
            for i in range(len(self.queue)):
                if self.queue[i][3] == position:
                    del_list.append(i)
            for i in range(len(del_list)):
                del self.queue[del_list[i]]
                del_list = list(map(lambda x: x - 1, del_list))

            if isinsert:
                self.queue.insert(0, [current_event, duration, next_event, position])
            else:
                self.queue.append([current_event, duration, next_event, position])
            return len(del_list)

        else:
            if isinsert:
                self.queue.insert(0, [current_event, duration, next_event, position])
            else:
                self.queue.append([current_event, duration, next_event, position])

    def event_check(self):

        # del_list = []
        # it = 0
        # it_obj = len(self.queue)
        # while it < it_obj:
        #     if self.queue[it][1] >= 0:
        #         self.queue[it][1] -= 1
        #         if self.queue[it][1] == 0:
        #             if not self.queue[it][2]:
        #                 del_list.append(it)
        #             else:
        #                 if isinstance(self.queue[it][2], list):
        #                     tmp_num = self.event_call(self.queue[it][2][0], self.queue[it][2][1:],
        #                                     self.queue[it][3])
        #                 else:
        #                     tmp_num = self.event_call(self.queue[it][2], None, self.queue[it][3])
        #                 it -= tmp_num
        #                 it_obj -= tmp_num
        #     it += 1

        for i in self.queue:
            if i[1] > 0:
                i[1] -= 1

        tmp_queue = copy.deepcopy(self.queue)

        for i in range(len(self.queue)):
            if tmp_queue[i][1] == 0:
                if tmp_queue[i][2]:
                    if isinstance(tmp_queue[i][2], list):
                        if isinstance(tmp_queue[i][2][0], list):
                            self.event_call(tmp_queue[i][2][0][0], tmp_queue[i][2][1:],
                                            tmp_queue[i][3],
                                            isappend=True, force_duration=tmp_queue[i][2][0][1])
                        else:
                            self.event_call(tmp_queue[i][2][0], tmp_queue[i][2][1:],
                                            tmp_queue[i][3], isappend=True)
                    else:
                        self.event_call(tmp_queue[i][2], None,
                                        tmp_queue[i][3], isappend=True)

        it = 0
        it_obj = len(self.queue)
        while it < it_obj:
            if not self.queue[it][1]:
                del self.queue[it]
                it -= 1
                it_obj -= 1
            it += 1

    def event_delete(self):
        self.queue = []

    def draw(self):
        for i in self.queue:

            if not i[0]:
                continue

            temp_target = self.images[i[0]]
            temp_trans_pos = pos(i[3], self.sprite_type)

            if isinstance(temp_target, list):

                if temp_target[-1] == "PA":
                    if i[1] == -1:
                        animation_number = 0
                    else:
                        animation_number = len(temp_target) - 2 - (i[1] + animation_delay - 1) // animation_delay

                    temp_position = tuple(pos([self.init_pos[j] + temp_trans_pos[j] + temp_target[animation_number][j]
                                               for j in range(2)]))

                    screen.blit(temp_target[-2], temp_position)

                else:
                    animation_number = len(temp_target) - (i[1] + animation_delay - 1) // animation_delay
                    temp_position = tuple(pos([self.init_pos[j] + temp_trans_pos[j] for j in range(2)]))

                    screen.blit(temp_target[animation_number], temp_position)

            else:
                temp_position = tuple(pos([self.init_pos[j] + temp_trans_pos[j] for j in range(2)]))
                screen.blit(temp_target, temp_position)

            if self == cards and i[0] != "card_delete":
                temp_ministone = deck_ministone[i[3]]
                for j in temp_ministone:
                    n_temp_position = tuple([temp_position[k] + j[0][k] for k in range(2)])
                    screen.blit(j[1], n_temp_position)


class ListFuncQueue(list):
    def w_append(self, func, args: tuple, duration: int):
        self.append([func, args, duration * animation_delay])

    def run_check(self):
        for i in self:
            if not i[-1]:
                i[0](i[1])
            else:
                i[-1] -= 1


########################################################################################################################

window_size = [1024, 600]
screen = pygame.display.set_mode(window_size)

title = "PolyGomino"
pygame.display.set_caption(title)

fps = 30
frame = 0
animation_delay = 3
run = 1

cannot_operate = 0

########################################################################################################################

board = [[0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]

deck = [[], [], []]
deck_ministone = [[], [], []]
deck_selected = 0  # 1,2,3 / 0 : not selected
current_block_shape = []  # [] : not selected
current_block_position = []  # row, column / [] : not selected
num_var = {"score": 0, "turn": 0}

# func_queue = ListFuncQueue()

with open('difficulty.json') as f:
    json_object = json.load(f)

inflection = json_object['inflection']
difficulties = json_object['difficulties']

button_place = AnimatedSprite((80, 20), (168, 128), 0,
                              "resources/buttons/button_place")
button_place.event_call("button_place_stand", None)

button_down = AnimatedSprite((38, 24), (189, 102), 0,
                             "resources/buttons/button_down")
button_down.event_call("button_down_stand", None)

button_up = AnimatedSprite((38, 24), (189, 80), 0,
                           "resources/buttons/button_up")
button_up.event_call("button_up_stand", None)

button_left = AnimatedSprite((20, 46), (168, 80), 0,
                             "resources/buttons/button_left")
button_left.event_call("button_left_stand", None)

button_right = AnimatedSprite((20, 46), (228, 80), 0,
                              "resources/buttons/button_right")
button_right.event_call("button_right_stand", None)

button_flipfront = AnimatedSprite((40, 20), (167, 58), 0,
                                  "resources/buttons/button_flipfront")
button_flipfront.event_call("button_flipfront_stand", None)

button_flipside = AnimatedSprite((40, 20), (209, 58), 0,
                                 "resources/buttons/button_flipside")
button_flipside.event_call("button_flipside_stand", None)

button_turnleft = AnimatedSprite((40, 20), (167, 40), 0,
                                 "resources/buttons/button_turnleft")
button_turnleft.event_call("button_turnleft_stand", None)

button_turnright = AnimatedSprite((40, 20), (209, 40), 0,
                                  "resources/buttons/button_turnright")
button_turnright.event_call("button_turnright_stand", None)

cards = AnimatedSprite((28, 39), (61, 111), 3, "resources/cards")
cards.add_positioned_animation("card_picked", "card_non_picked", [[0, 8]])
cards.add_positioned_animation("card_picked", "card_pickup", [[0, 1], [0, 0]])
cards.add_positioned_animation("card_picked", "card_pickdown", [[0, 7], [0, 8]])
cards.add_positioned_animation("card_picked", "card_emerge",
                               [[0, 40], [0, 40], [0, 28], [0, 18], [0, 13], [0, 10]])

numbers = AnimatedSprite((7, 11), (212, 6), 4, "resources/numbers")

numbers.add_positioned_animation("number_0", "number_0_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_1", "number_1_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_2", "number_2_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_3", "number_3_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_4", "number_4_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_5", "number_5_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_6", "number_6_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_7", "number_7_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_8", "number_8_scoreup", [[0, -2], [0, -1]])
numbers.add_positioned_animation("number_9", "number_9_scoreup", [[0, -2], [0, -1]])

stones = AnimatedSprite((18, 23), (57, 1), 1, "resources/stones")
selections = AnimatedSprite((22, 22), (55, 4), 2,
                            "resources/selections/selection_blue",
                            "resources/selections/selection_red")

asp_list = [button_place, button_down, button_up, button_left, button_right, button_flipfront, button_flipside,
            button_turnleft, button_turnright, cards, numbers, stones, selections][::-1]

main_ui = pygame.image.load("resources/basic_gui.png").convert_alpha()

ministone_preset = {(1, 1): (9, 12), (2, 2): (6, 9), (2, 1): (9, 7), (3, 3): (5, 8),
                    (3, 2): (6, 5), (3, 1): (10, 5), (4, 4): (4, 7), (4, 3): (5, 5),
                    (4, 2): (8, 5), (4, 1): (11, 5), (5, 5): (4, 7), (5, 4): (4, 5),
                    (5, 3): (6, 5), (5, 2): (9, 5), (5, 1): (11, 5), (6, 5): (4, 5),
                    (6, 4): (6, 5), (6, 3): (8, 5), (6, 2): (10, 5), (6, 1): (12, 5)}
ministone_images = [[pygame.image.load("resources/ministones/ministone_verybig.png").convert_alpha(),
                     pygame.image.load("resources/ministones/ministone_verybig.png").convert_alpha()],
                    [pygame.image.load("resources/ministones/ministone_big_empty.png").convert_alpha(),
                     pygame.image.load("resources/ministones/ministone_big.png").convert_alpha()],
                    [pygame.image.load("resources/ministones/ministone_medium_empty.png").convert_alpha(),
                     pygame.image.load("resources/ministones/ministone_medium.png").convert_alpha()],
                    [pygame.image.load("resources/ministones/ministone_small_empty.png").convert_alpha(),
                     pygame.image.load("resources/ministones/ministone_small.png").convert_alpha()],
                    [pygame.image.load("resources/ministones/ministone_verysmall_empty.png").convert_alpha(),
                     pygame.image.load("resources/ministones/ministone_verysmall.png").convert_alpha()]][::-1]
ministone_size_pixel = [3, 4, 5, 7, 9]

for card_num in range(3):
    block_pick(card_num + 1)
    cards.event_call("card_emerge", "card_non_picked", card_num)

for inumpos in range(2):
    for jnumpos in range(5):
        numbers.event_call("number_0_scoreup", "number_0", [inumpos, jnumpos])

########################################################################################################################


def main_loop():
    global frame, cannot_operate
    while run == 1:
        frame += 1

        screen.blit(main_ui, (0, 0))

        for animated_sprites in asp_list:
            animated_sprites.draw()
            animated_sprites.event_check()

        pygame.display.flip()

        # events = pygame.event.get()
        # pygame.event.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if not cannot_operate:

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        if block_drop():
                            num_var["turn"] += 1
                            number_call(1, (2 * block_delete_check() + 4) * animation_delay)
                    if event.key == pygame.K_DOWN:
                        block_move_down()
                    if event.key == pygame.K_UP:
                        block_move_up()
                    if event.key == pygame.K_LEFT:
                        block_move_left()
                    if event.key == pygame.K_RIGHT:
                        block_move_right()
                    if event.key == pygame.K_PERIOD:
                        block_flip_front()
                    if event.key == pygame.K_SLASH:
                        block_flip_side()
                    if event.key == pygame.K_SEMICOLON:
                        block_turn_left()
                    if event.key == pygame.K_QUOTE:
                        block_turn_right()
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        if not deck_selected:
                            block_load(1)
                        else:
                            if deck_selected == 1:
                                block_unload()
                            else:
                                block_unload()
                                block_load(1)
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        if not deck_selected:
                            block_load(2)
                        else:
                            if deck_selected == 2:
                                block_unload()
                            else:
                                block_unload()
                                block_load(2)
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        if not deck_selected:
                            block_load(3)
                        else:
                            if deck_selected == 3:
                                block_unload()
                            else:
                                block_unload()
                                block_load(3)
                    if event.key == pygame.K_r:
                        print(current_block_shape, current_block_position)
                        print(cards.queue, "\n\n", stones.queue)

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_RETURN:
                        button_place.event_call("button_place_detach", "button_place_stand")
                    if event.key == pygame.K_DOWN:
                        button_down.event_call("button_down_detach", "button_down_stand")
                    if event.key == pygame.K_UP:
                        button_up.event_call("button_up_detach", "button_up_stand")
                    if event.key == pygame.K_LEFT:
                        button_left.event_call("button_left_detach", "button_left_stand")
                    if event.key == pygame.K_RIGHT:
                        button_right.event_call("button_right_detach", "button_right_stand")
                    if event.key == pygame.K_PERIOD:
                        button_flipfront.event_call("button_flipfront_detach",
                                                    "button_flipfront_stand")
                    if event.key == pygame.K_SLASH:
                        button_flipside.event_call("button_flipside_detach",
                                                   "button_flipside_stand")
                    if event.key == pygame.K_SEMICOLON:
                        button_turnleft.event_call("button_turnleft_detach",
                                                   "button_turnleft_stand")
                    if event.key == pygame.K_QUOTE:
                        button_turnright.event_call("button_turnright_detach",
                                                    "button_turnright_stand")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

        pygame.time.Clock().tick(fps)

        if cannot_operate > 0:
            cannot_operate -= 1


if __name__ == "__main__":
    main_loop()
