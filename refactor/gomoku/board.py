import pygame as pg
from .colors import *

class GomokuBoard:
    size = 675
    interval = 45
    p1_score = 0
    p2_score = 0

    def __init__(self, onGame):
        self.title = "GOMOKU for 2 players"
        self.screen = pg.display.set_mode((900, GomokuBoard.size + 45))
        pg.display.set_caption(self.title)
        self.screen.fill(COLOR_BOARD)

        self.draw_board()
        self.draw_score()
        if not onGame:
            self.play_order = None
        elif onGame:
            self.stones = {}
            self.stones["white"], self.stones["black"] = [], []
            self.draw_text("NEXT GAME START", GomokuBoard.size//2, 30, COLOR_GREEN, 35)
            self.draw_text("PLAYER 1", 45 * 16 + 65, GomokuBoard.size // 2 - 90, COLOR_GRAY, 20)
            self.draw_text("PLAYER 2", 45 * 16 + 65, GomokuBoard.size // 2 + 20, COLOR_RED, 20)
            self.play_order = True

    # 오목판 그림.
    def draw_board(self, x=45, y=45):
        size = GomokuBoard.size
        for i in range(16):
            pg.draw.line(self.screen, COLOR_BLACK, (x + 45*i, y), (x + 45*i, size), 2)
            pg.draw.line(self.screen, COLOR_BLACK, (45, y + 45*i), (x + size, y + 45*i), 2)
        pg.draw.circle(self.screen, COLOR_BLACK, (45 * 8, 45 * 8), 8)

    # 점수 부분을 그림.
    def draw_score(self):
        size, interval = GomokuBoard.size, GomokuBoard.interval

        # 백돌 점수.
        self.draw_text("PLAYER 1", interval * 16 + 65, size // 2 - 90, (100, 100, 100), 20)
        pg.draw.circle(self.screen, COLOR_WHITE, (interval * 16 + 5, GomokuBoard.size // 2 - 90), interval // 5)
        pg.draw.rect(self.screen, COLOR_BOARD, (interval * 16 + 30, GomokuBoard.size // 2 - 70, 50, 60))
        self.draw_text(str(GomokuBoard.p1_score), interval * 16 + 65, size // 2 - 30, (100, 100, 100), interval)

        # 흑돌 점수.
        self.draw_text("PLAYER 2", 45 * 16 + 65, size // 2 + 20, COLOR_BLACK, 20)
        pg.draw.circle(self.screen, COLOR_BLACK, (interval * 16 + 5, size // 2 + 20), interval//5)
        pg.draw.rect(self.screen, COLOR_BOARD, (interval * 16 + 30, GomokuBoard.size // 2 + 40, 50, 60))
        self.draw_text(str(GomokuBoard.p2_score), 45 * 16 + 65, size // 2 + 80, COLOR_BLACK, interval)

    # Quit 버튼 눌렀을 때 종료처리
    def quit_pressed(self, x_pos, y_pos):
        x, y, w, h, size = GomokuBoard.interval*16, GomokuBoard.interval, 125, GomokuBoard.interval, GomokuBoard.size
        
        if x < x_pos < w + x and size - 90 < y_pos < size - 90 + h:
            pg.quit()
            quit()

    # New game, Next game, Quit 버튼에 대한 마우스 상호작용
    def board_button_interaction(self):
        x, y, w, h = GomokuBoard.interval*16, GomokuBoard.interval, 125, GomokuBoard.interval
        size = GomokuBoard.size
        button_color=COLOR_BUTTON
        ac_button_color=COLOR_AC_BUTTON

        # 아래 코드는 실시간 반응하는 버튼을 만듬.
        x_pos, y_pos = pg.mouse.get_pos()

        # New game 버튼.
        if x < x_pos < w + x and y < y_pos < y + h:
            pg.draw.rect(self.screen, ac_button_color, (x, y, w, h))
            self.draw_text("START", x + 59, y + 25, COLOR_RED, 20)

        # Next game 버튼.
        elif x < x_pos < w + x and y + 70 < y_pos < y + 70 + h:
            pg.draw.rect(self.screen, ac_button_color, (x, y + 70, w, h))
            self.draw_text("Next game", x + 62, y + 95, (0, 0, 225), 20)

        # Quit 버튼.
        elif x < x_pos < w + x and size - 90 < y_pos < size - 90 + h:
            pg.draw.rect(self.screen, ac_button_color, (x, size - 90, w, h))
            self.draw_text("Quit", x + 56, size-65, (225, 0, 225), 20)
            
        # 평상시 버튼 모습.
        else:
            pg.draw.rect(self.screen, button_color, (x, y, w, h))
            pg.draw.rect(self.screen, button_color, (x, y + 70, w, h))
            pg.draw.rect(self.screen, button_color, (x, size - 90, w, h))

            self.draw_text("NEW GAME", x + 59, y + 25, (200, 0, 0), 20)
            self.draw_text("NEXT GAME", x + 62, y + 95, (0, 0, 180), 20)
            self.draw_text("QUIT", x + 56, size - 65, (200, 0, 200), 20)

    # 텍스트 띄우는 내장함수
    def draw_text(self, text, x_pos, y_pos, font_color, font_size):
        ff = pg.font.Font(pg.font.get_default_font(), font_size)
        TextSurf, TextRect = self.text_objects(text, ff, font_color)
        TextRect.center = (x_pos, y_pos)
        self.screen.blit(TextSurf, TextRect)

    def text_objects(self, text, font, font_color):
        textSurface = font.render(text, True, font_color)
        return textSurface, textSurface.get_rect()

    # 돌을 그릴 기준 좌표를 구함.
    @staticmethod
    def get_stone_pos(x_pos, y_pos):
        if x_pos % 45 > 23:
            x_pos = (x_pos - x_pos % 45) + 45
        else:
            x_pos -= x_pos % 45

        if y_pos % 45 > 23:
            y_pos = (y_pos - y_pos % 45) + 45
        else:
            y_pos -= y_pos % 45

        return x_pos, y_pos

    # 색깔에 맞는 돌을 그림.
    def draw_stone(self, player_name, stone_color, x_pos, y_pos):
        x_pos, y_pos = GomokuBoard.get_stone_pos(x_pos, y_pos)
        stone = self.stones

        # 좌표가 이미 돌이 있는 곳이면 아무 작업도 하지 않음.
        if (x_pos, y_pos) in stone["white"] or (x_pos, y_pos) in stone["black"]:
            pass
        else:
            pg.draw.circle(self.screen, stone_color, (x_pos, y_pos), 45//2)
            stone[player_name].append((x_pos, y_pos))

            self.play_order = not self.play_order
            if self.play_order:
                self.draw_text("PLAYER 1", 45 * 16 + 65, GomokuBoard.size // 2 - 90, COLOR_GRAY, 20)
                self.draw_text("PLAYER 2", 45 * 16 + 65, GomokuBoard.size // 2 + 20, COLOR_RED, 20)   # 누구 차례인지를 표시.
                self.score("white")  # 이겼는지 판단.
            elif not self.play_order:
                self.draw_text("PLAYER 1", 45 * 16 + 65, GomokuBoard.size // 2 - 90, COLOR_RED, 20)
                self.draw_text("PLAYER 2", 45 * 16 + 65, GomokuBoard.size // 2 + 20, COLOR_BLACK, 20)
                self.score("black")  # 이겼는지 판단.

            if len(stone["white"]) + len(stone["black"]) == 225:    # 무승부 판단.
                self.draw_text("DRAW", 45 * 16 + 65, GomokuBoard.size // 2 + 120, (200, 0, 0), 45)
                self.play_order = None

    # 실제 승리 여부를 가르는 알고리즘.
    def score(self, color_name):
        stone = self.stones
        result = None
        if len(stone[color_name]) >= 5:
            stone_sort = sorted(stone[color_name])
            for x, y in stone_sort:
                cnt = 0
                for i in range(1, 5):
                    if (x, y + 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4:
                            self.play_order = None
                            result = True
                            break

                    else: break

                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y) in stone_sort:
                        cnt += 1
                        if cnt == 4:
                            self.play_order = None
                            result = True
                            break
                    else: break

                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y+45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4:
                            self.play_order = None
                            result = True
                            break
                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y - 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4:
                            self.play_order = None
                            result = True
                            break

        if result:
            if color_name == "white":
                self.draw_text("WIN", 45 * 16 + 65, GomokuBoard.size // 2 - 120,
                               (100, 100, 100), 45)
                GomokuBoard.p1_score += 1

            elif color_name == "black":
                self.draw_text("WIN", 45 * 16 + 65, GomokuBoard.size//2 + 120,
                               COLOR_BLACK, 45)
                GomokuBoard.p2_score += 1

            self.draw_score()