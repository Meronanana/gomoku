import pygame as pg
from .colors import *

class GameManager:
    def __init__(self):
        self.w_h = 675
        self.title = "GOMOKU for 2 players"
        self.screen = pg.display.set_mode((900, self.w_h + 45))
        pg.display.set_caption(self.title)
        self.screen.fill(COLOR_BOARD)

    # 오목판 그림.
    def draw_main(self, x=45*16, y=45, w=125, h=45,
                  button_color=COLOR_BUTTON, ac_button_color=COLOR_AC_BUTTON):

        # Gomoku board.
        for i in range(1, 16):
            pg.draw.line(self.screen, COLOR_BLACK, (45 * i, 45), (45 * i, self.w_h), 2)
            pg.draw.line(self.screen, COLOR_BLACK, (45, 45 * i), (self.w_h, 45 * i), 2)
        pg.draw.circle(self.screen, COLOR_BLACK, (45 * 8, 45 * 8), 8)

    # 점수 부분을 그림.
    def draw_score(self, player1_score, player2_score):
        self.player1_score, self.player2_score = player1_score, player2_score
        # Score.
        self.text_draw("PLAYER 1", 45 * 16 + 65, self.w_h // 2 - 90,
                       (100, 100, 100), 20)
        pg.draw.circle(self.screen, COLOR_WHITE,
                           (45 * 16 + 5, self.w_h // 2 - 90), 45 // 5)
        self.text_draw(str(self.player1_score), 45 * 16 + 65, self.w_h // 2 - 30,
                       (100, 100, 100), 45)
        self.text_draw("PLAYER 2", 45 * 16 + 65, self.w_h // 2 + 20,
                       COLOR_BLACK, 20)
        pg.draw.circle(self.screen, COLOR_BLACK,
                           (45 * 16 + 5, self.w_h // 2 + 20), 45//5)
        self.text_draw(str(self.player2_score), 45 * 16 + 65,
                       self.w_h // 2 + 80, COLOR_BLACK, 45)

    # New game, Next game, Quit 버튼에 대한 마우스 상호작용
    def interactive_button(self, x=45*16, y=45, w=125, h=45,
                           button_color=COLOR_BUTTON,
                           ac_button_color=COLOR_AC_BUTTON):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.button_color = button_color
        self.ac_button_color = ac_button_color

        # Draw buttons.
        pg.draw.rect(self.screen, self.button_color, (self.x, self.y, w, h))
        pg.draw.rect(self.screen, self.button_color, (self.x, self.y + 70, w, h))
        pg.draw.rect(self.screen, self.button_color, (self.x, self.w_h - 90, w, h))
        # Draw text on buttons.
        self.text_draw("NEW GAME", self.x + 59, self.y + 25, (200, 0, 0), 20)
        self.text_draw("NEXT GAME", self.x + 62, self.y + 95, (0, 0, 180), 20)
        self.text_draw("QUIT", self.x + 56, self.w_h - 65, (200, 0, 200), 20)
        # To make interactive buttons.
        mouse = pg.mouse.get_pos()
        # New game.
        if self.w + self.x > mouse[0] > self.x and \
                self.y + self.h > mouse[1] > self.y:
            pg.draw.rect(self.screen, self.ac_button_color,
                             (self.x, self.y, self.w, self.h))
            self.text_draw("START", self.x+59, self.y + 25, COLOR_RED, 20)

        # Next game.
        if self.w + self.x > mouse[0] > self.x and \
                self.y + 70 + self.h > mouse[1] > self.y + 70:
            pg.draw.rect(self.screen, self.ac_button_color,
                             (self.x, self.y + 70, self.w, self.h))
            self.text_draw("Next game", self.x + 62, self.y + 95, (0, 0, 225), 20)

        # Quit.
        if self.w + self.x > mouse[0] > self.x and \
                self.w_h - 90 + self.h > mouse[1] > self.w_h - 90:
            pg.draw.rect(self.screen, self.ac_button_color,
                             (self.x, self.w_h - 90, self.w, self.h))
            self.text_draw("Quit", self.x + 56, self.w_h-65, (225, 0, 225), 20)
            if pg.mouse.get_pressed()[0] == 1:
                pg.quit()
                quit()

    # ???????
    def text_draw(self, text, x_pos, y_pos, font_color, font_size):
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        ff = pg.font.Font(pg.font.get_default_font(), self.font_size)
        TextSurf, TextRect = self.text_objects(self.text, ff, self.font_color)
        TextRect.center = (x_pos, y_pos)
        self.screen.blit(TextSurf, TextRect)

    def text_objects(self, text, font, font_color):
        textSurface = font.render(text, True, font_color)
        return textSurface, textSurface.get_rect()

    # 마우스 좌표 구함.
    def play_get_pos(self):
        self.x_stone, self.y_stone = pg.mouse.get_pos()

        return self.x_stone, self.y_stone

    # 돌을 그릴 기준 좌표를 구함.
    def play_draw_stone_pos(self):
        if self.x_stone % 45 > 23:
            self.x_stone = (self.x_stone - self.x_stone % 45) + 45
        else:
            self.x_stone -= self.x_stone % 45

        if self.y_stone % 45 > 23:
            self.y_stone = (self.y_stone - self.y_stone % 45) + 45
        else:
            self.y_stone -= self.y_stone % 45

        return self.x_stone, self.y_stone

    # 색깔에 맞는 돌을 그림.
    def play_draw_stone(self, stone, play_order, color_name, stone_color, x_stone, y_stone):
        self.stone, self.play_order, self.color_name = stone, play_order, color_name
        self.stone_color, self.x_stone, self.y_stone = stone_color, x_stone, y_stone

        if (self.x_stone, self.y_stone) in self.stone["white"]:
            pass
        elif (self.x_stone, self.y_stone) in self.stone["black"]:
            pass
        else:
            pg.draw.circle(self.screen, self.stone_color,
                               (self.x_stone, self.y_stone), 45//2)
            self.stone[self.color_name].append((self.x_stone, self.y_stone))
            if self.play_order: self.play_order = False
            else: self.play_order = True
        return self.stone, self.play_order

    # 실제 승리 여부를 가르는 알고리즘.
    def score(self, stone, color_name, player_score, play_order):
        self.stone, self.color_name, self.player_score = stone, color_name, player_score
        self.play_order = play_order
        self.result = None
        if len(self.stone[self.color_name]) >= 5:

            stone_sort = sorted(self.stone[self.color_name])

            for x, y in stone_sort:
                cnt = 0
                for i in range(1, 5):
                    if (x, y + 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4:
                            self.player_score += 1
                            self.play_order = None
                            self.result = True
                            break

                    else: break

                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y) in stone_sort:
                        cnt += 1
                        if cnt == 4:
                            self.player_score += 1
                            self.play_order = None
                            self.result = True
                            break
                    else: break

                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y+45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4:
                            self.player_score += 1
                            self.play_order = None
                            self.result = True
                            break
                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y - 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4:
                            self.player_score += 1
                            self.play_order = None
                            self.result = True
                            break

        if self.result:
            if self.color_name == "white":
                self.text_draw("WIN", 45 * 16 + 65, self.w_h // 2 - 120,
                               (100, 100, 100), 45)

            elif self.color_name == "black":
                self.text_draw("WIN", 45 * 16 + 65, self.w_h//2 + 120,
                               COLOR_BLACK, 45)

        return self.player_score, self.play_order
