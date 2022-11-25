import pygame as pg

from .manager import MatchManager
from .colors import *

class GomokuBoard:
    size = 630
    interval = 45

    def __init__(self, manager):
        self.title = "GOMOKU for 2 players"
        self.screen = pg.display.set_mode((900, self.size + self.interval*3))
        pg.display.set_caption(self.title)
        self.screen.fill(COLOR_BOARD)

        self.draw_board()

        if manager != None:
            self.manager = manager
            self.draw_score()
            
            text = "GAME " + str(self.manager.game_count) + " START"
            self.draw_text(text, self.interval*9, self.interval, COLOR_BLACK, 35)
            self.draw_text("PLAYER 1", self.interval * 16 + 65, self.size // 2 - self.interval+20, COLOR_WHITE, 20)
            self.draw_text("PLAYER 2", self.interval * 16 + 65, self.size // 2 + self.interval+40, COLOR_RED, 20)

    # 오목판 그림.
    def draw_board(self):
        size = GomokuBoard.size
        k = self.interval
        x, y = k, k*2
        for i in range(15):
            pg.draw.line(self.screen, COLOR_BLACK, (x + k*i, y), (x + k*i, y + size), 2)
            pg.draw.line(self.screen, COLOR_BLACK, (k, y + k*i), (x + size, y + k*i), 2)
        pg.draw.circle(self.screen, COLOR_BLACK, (k * 8, k * 9), 8)

        # 버튼 부분
        x, y, w, h = k*16, k*2, 125, k

        pg.draw.rect(self.screen, COLOR_BUTTON, (x, y, w, h))
        pg.draw.rect(self.screen, COLOR_BUTTON, (x, y + 70, w, h))
        pg.draw.rect(self.screen, COLOR_BUTTON, (x, size, w, h))

        self.draw_text("NEW GAME", x + 59, y + 25, COLOR_DEEP_RED, 20)
        self.draw_text("NEXT GAME", x + 62, y + 95, COLOR_DEEP_BLUE, 20)
        self.draw_text("QUIT?", x + 56, size + 25, COLOR_DEEP_BLUE, 20)

    # 점수 부분을 그림.
    def draw_score(self):
        # 게임 매니저가 없으면 그리지 않음.
        if self.manager == None:
            return
        
        size, k = GomokuBoard.size, GomokuBoard.interval

        # 백돌 점수.
        self.draw_text("PLAYER 1", k * 16 + 65, size // 2 - k + 20, COLOR_WHITE, 20)
        pg.draw.circle(self.screen, COLOR_WHITE, (k * 16 + 5, GomokuBoard.size // 2 - k + 20), k // 5)
        pg.draw.rect(self.screen, COLOR_BOARD, (k * 16 + 30, k*7, 50, 60))
        self.draw_text(str(self.manager.p1_score), k * 16 + 65, size // 2 - 10+k, COLOR_WHITE, k)

        # 흑돌 점수.
        self.draw_text("PLAYER 2", k * 16 + 65, size // 2 + k+40, COLOR_BLACK, 20)
        pg.draw.circle(self.screen, COLOR_BLACK, (k * 16 + 5, size // 2 + k+40), k//5)
        pg.draw.rect(self.screen, COLOR_BOARD, (k * 16 + 30, GomokuBoard.size // 2 + k+60, 50, 60))
        self.draw_text(str(self.manager.p2_score), k * 16 + 65, size // 2 + k+100, COLOR_BLACK, k)

    # Quit 버튼 눌렀을 때 종료처리
    def quit_pressed(self, x_pos, y_pos):
        size, k = GomokuBoard.size, GomokuBoard.interval
        x, y, w, h = k*16, k*2, 125, k
        if x < x_pos < w + x and size < y_pos < size + h:
            pg.quit()
            quit()

    # New game, Next game, Quit 버튼에 대한 마우스 상호작용
    def board_button_interaction(self):
        size, k = GomokuBoard.size, GomokuBoard.interval
        x, y, w, h = k*16, k*2, 125, k
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
            self.draw_text("START", x + 62, y + 95, COLOR_BLUE, 20)

        # Quit 버튼.
        elif x < x_pos < w + x and size < y_pos < size + h:
            pg.draw.rect(self.screen, ac_button_color, (x, size, w, h))
            self.draw_text("EXIT", x + 56, size + 25, COLOR_BLUE, 20)
            
        # 평상시 버튼 모습.
        else:
            pg.draw.rect(self.screen, button_color, (x, y, w, h))
            pg.draw.rect(self.screen, button_color, (x, y + 70, w, h))
            pg.draw.rect(self.screen, button_color, (x, size, w, h))

            self.draw_text("NEW GAME", x + 59, y + 25, COLOR_DEEP_RED, 20)
            self.draw_text("NEXT GAME", x + 62, y + 95, COLOR_DEEP_BLUE, 20)
            self.draw_text("QUIT?", x + 56, size + 25, COLOR_DEEP_BLUE, 20)

    # 텍스트 띄우는 내장함수
    def draw_text(self, text, x_pos, y_pos, font_color, font_size):
        ff = pg.font.Font(pg.font.get_default_font(), font_size)
        TextSurf = ff.render(text, True, font_color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (x_pos, y_pos)
        self.screen.blit(TextSurf, TextRect)

    # 색깔에 맞는 돌을 그림.
    def draw_stone(self, player_name, stone_color, x_pos, y_pos):
        size, k = GomokuBoard.size, GomokuBoard.interval

        x_pos, y_pos = self.get_stone_pos(x_pos, y_pos)
        print("Position on board :", x_pos, y_pos)
        if self.manager.is_positionable(self.interval, self.interval*2, x_pos, y_pos, player_name):
            pg.draw.circle(self.screen, stone_color, (x_pos, y_pos), 45//2)
            self.manager.turn_change()
            if self.manager.play_order:
                self.draw_text("PLAYER 1", k * 16 + 65, size // 2 - k+20, COLOR_WHITE, 20)
                self.draw_text("PLAYER 2", k * 16 + 65, size // 2 + k+40, COLOR_RED, 20)  # 누구 차례인지를 표시.
                if self.manager.is_win("white"):  # 이겼는지 판단.
                    self.draw_text("WIN", k * 16 + 65, k*5+25, COLOR_WHITE, 45)
                    self.draw_score()
            elif not self.manager.play_order:
                self.draw_text("PLAYER 1", k * 16 + 65, size // 2 - k+20, COLOR_RED, 20)
                self.draw_text("PLAYER 2", k * 16 + 65, size // 2 + k+40, COLOR_BLACK, 20)  # 누구 차례인지를 표시.
                if self.manager.is_win("black"):  # 이겼는지 판단.
                    self.draw_text("WIN", k * 16 + 65, k*11+20, COLOR_BLACK, 45)
                    self.draw_score()
            if self.manager.is_draw():    # 무승부 판단.
                self.draw_text("DRAW", 45 * 16 + 65, GomokuBoard.size // 2 + 120, (200, 0, 0), 45)

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
    
