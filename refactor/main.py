import pygame as pg

from gomoku.board import GomokuBoard
from gomoku.manager import MatchManager
from gomoku.colors import *

if __name__ == "__main__":
    pg.init()
    pg.font.init()
    
    # 게임을 초기화 합니다.
    game = GomokuBoard(None)
    manager = None
    size, k = GomokuBoard.size, GomokuBoard.interval
    x, y, w, h = k*16, k*2, 125, k

    while True:
        event = pg.event.poll()     # 행동을 하나 빼낸다.
        if event.type == pg.MOUSEBUTTONUP:  # 마우스 클릭 했을 때 행동
            # 클릭 위치 구함
            x_pos, y_pos = pg.mouse.get_pos()
            game.quit_pressed(x_pos, y_pos)

            # New game 버튼 누름. 모든 게임 초기화.
            if x < x_pos < w + x and y < y_pos < y + h:
                manager = MatchManager()
                game = GomokuBoard(manager)

            # Next game 버튼 누름. 스코어 제외 초기화.
            if x < x_pos < w + x and y + 70 < y_pos < y + 70 + h:
                if manager == None:
                    manager = MatchManager()
                else:
                    manager.new_game()
                game = GomokuBoard(manager)

            # play_order가 False이면 흰색 차례. True이면 검은 색 차례.
            if k-20 <= x_pos <= k+20 + size and k*2-20 <= y_pos <= k*2+20 + size:
                if manager.play_order is None: # 게임 중이 아니면 그냥 넘어간다.
                    pass
                elif not manager.play_order:   # 흰색 돌을 표시. (Player 1).
                    game.draw_stone("white", COLOR_WHITE, x_pos, y_pos)
                elif manager.play_order:   # 검은색 돌을 표시. (Player 2).
                    game.draw_stone("black", COLOR_BLACK, x_pos, y_pos)
        
        if event.type == pg.MOUSEMOTION:    # 마우스를 위로 올렸을 때 행동
            game.board_button_interaction()
        pg.display.update()
