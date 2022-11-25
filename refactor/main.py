import pygame as pg

from gomoku.board import GomokuBoard
from gomoku.manager import GameManager
from gomoku.colors import *

if __name__ == "__main__":
    pg.init()
    pg.font.init()
    
    # 게임을 초기화 합니다.
    game = GomokuBoard(False)

    while True:
        event = pg.event.poll()     # 행동을 하나 빼낸다.
        if event.type == pg.MOUSEBUTTONUP:  # 마우스 클릭 했을 때 행동
            # 클릭 위치 구함
            x_pos, y_pos = pg.mouse.get_pos()
            game.quit_pressed(x_pos, y_pos)

            # New game 버튼 누름. 모든 게임 초기화.
            if 45*16 < x_pos < 45*16 + 125 and 45 < y_pos < 90:
                GomokuBoard.p1_score, GomokuBoard.p2_score = 0, 0 # 요고 유무 차이
                game = GomokuBoard(True)

            # Next game 버튼 누름. 스코어 제외 초기화.
            if 45*16 < x_pos < 45*16 + 125 and 115 < y_pos < 160:
                game = GomokuBoard(True)


            # 게임 중이 아니면 그냥 넘어간다.
            if game.play_order is None:  # play_order가 False이면 흰색 차례. True이면 검은 색 차례.
                pass

            # 흰색 돌을 표시. (Player 1).
            elif not game.play_order:
                if 45 <= x_pos <= 45 + GomokuBoard.size and 45 <= y_pos <= 45 + GomokuBoard.size:
                    game.draw_stone("white", COLOR_WHITE, x_pos, y_pos)   # 흰돌을 그린다.
            # 검은색 돌을 표시. (Player 2).
            elif game.play_order:
                if 45 <= x_pos <= 45 + GomokuBoard.size and 45 <= y_pos <= 45 + GomokuBoard.size:
                    game.draw_stone("black", COLOR_BLACK, x_pos, y_pos)
        
        if event.type == pg.MOUSEMOTION:    # 마우스를 위로 올렸을 때 행동
            game.board_button_interaction()
        pg.display.update()
