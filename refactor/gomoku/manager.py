import pygame as pg
from .colors import *

class MatchManager:
    def __init__(self):
        self.p1_score = 0
        self.p2_score = 0
        self.game_count = 0
        self.play_order = None

        self.new_game()

    # 새 게임을 시작.
    def new_game(self):
        self.stones = {}
        self.stones["white"], self.stones["black"] = [], []
        self.play_order = True
        self.game_count += 1

    # 턴 넘기기.
    def turn_change(self):
        self.play_order = not self.play_order

    # 돌을 둘 수 있는지 판단.
    def is_positionable(self, x, y, x_pos, y_pos, player_name):
        x_pos, y_pos = x_pos - x, y_pos - y
        x_i, y_i = y_pos // 45, x_pos // 45
        print("In database :", x_i, y_i)

        # 좌표가 이미 돌이 있는 곳이면 두지 못한다.
        if (x_i, y_i) in self.stones["white"] or (x_i, y_i) in self.stones["black"]:
            return False
        else:
            self.stones[player_name].append((x_i, y_i))
            return True

    # 무승부 판단.
    def is_draw(self):
        if len(self.stones["white"]) + len(self.stones["black"]) == 225:
            self.play_order = None
            return True
        else:
            return False

    # 실제 승리 여부를 가르는 알고리즘.
    def is_win(self, color_name):
        stone = self.stones
        dx, dy = (1, 1, 1, 0), (-1, 0, 1, 1)
        result = False
        if len(stone[color_name]) >= 5:
            stone_sort = sorted(stone[color_name])
            print(stone_sort)
            for x, y in stone_sort:
                for i in range(4):
                    cnt = 0
                    for j in range(1, 5):
                        if (x + j*dx[i], y + j*dy[i]) in stone_sort:
                            cnt += 1
                            if cnt == 4:
                                self.play_order = None
                                result = True
                                break
                        else:
                            break

        if result:
            if color_name == "white":
                self.p1_score += 1

            elif color_name == "black":
                self.p2_score += 1
                
        return result
            
    