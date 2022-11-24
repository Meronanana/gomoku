import pygame as pg

from gomoku.board import GomokuBoard
from gomoku.manager import GameManager
from gomoku.colors import *

if __name__ == "__main__":
    pg.init()
    pg.font.init()
    
    # 게임을 초기화 합니다.
    stone = {}
    stone["white"], stone["black"] = [], []
    game = GomokuBoard()
    game.draw_board()
    game.draw_score()

    play_order = None

    while True:
        event = pg.event.poll()
        if event.type == pg.MOUSEBUTTONUP:

            # 클릭 위치 구함
            x_pos, y_pos = pg.mouse.get_pos()
            game.quit_pressed(x_pos, y_pos)

            # New game 버튼 누름. 모든 게임 초기화.
            if 45*16 < x_pos < 45*16 + 125 and 45 < y_pos < 90:
                stone["white"], stone["black"] = [], []
                player1_score, player2_score = 0, 0 # 요고 유무 차이
                game = GomokuBoard()
                game.draw_board()
                game.draw_score()
                game.draw_text("GAME START", GomokuBoard.size//2, 30, COLOR_GREEN, 35)
                play_order = True

            # Next game 버튼 누름. 스코어 제외 초기화.
            if 45*16 < x_pos < 45*16 + 125 and 115 < y_pos < 160:
                stone["white"], stone["black"] = [], []
                game = GomokuBoard()
                game.draw_board()
                game.draw_score()
                game.draw_text("NEXT GAME START", GomokuBoard.size//2, 30, COLOR_GREEN, 35)
                play_order = True

            # 흰색 돌을 표시. (Player 1).
            if play_order is None:  # play_order가 False이면 흰색 차례. True이면 검은 색 차례.
                pass
            elif not play_order:
                # 누구 차례인지를 표시
                game.draw_text("PLAYER 1", 45 * 16 + 65, GomokuBoard.size // 2 - 90,
                               COLOR_RED, 20)
                game.draw_text("PLAYER 2", 45 * 16 + 65, GomokuBoard.size // 2 + 20,
                               COLOR_BLACK, 20)
                if 45 <= x_pos <= GomokuBoard.size and 45 <= y_pos <= GomokuBoard.size:
                    x_pos, y_pos = GomokuBoard.get_stone_pos(x_pos, y_pos)   # 돌을 그릴 좌표 가져옴
                    stone, play_order = game.play_draw_stone(
                        stone, play_order, "white", COLOR_WHITE,
                        x_pos, y_pos)   # 흰돌을 그린다.
                    game.draw_text("PLAYER 1", 45 * 16 + 65, GomokuBoard.size // 2 - 90,
                                   COLOR_GRAY, 20)
                    game.draw_text("PLAYER 2", 45 * 16 + 65, GomokuBoard.size // 2 + 20,
                                   COLOR_RED, 20)   # 누구 차례인지를 표시.
                    play_order = game.score(
                        stone, "white", play_order)  # 이겼는지 판단.
                    if len(stone["white"]) + len(stone["black"]) == 225:    # 무승부 판단.
                        game.draw_text("DRAW", 45 * 16 + 65, GomokuBoard.size // 2 + 120,
                                       (200, 0, 0), 45)
                        play_order = None

            # 검은색 돌을 표시. (Player 2).
            elif play_order:
                game.draw_text("PLAYER 1", 45 * 16 + 65, GomokuBoard.size // 2 - 90,
                               COLOR_GRAY, 20)
                game.draw_text("PLAYER 2", 45 * 16 + 65, GomokuBoard.size // 2 + 20,
                               COLOR_RED, 20)
                if 45 <= x_pos <= GomokuBoard.size and 45 <= y_pos <= GomokuBoard.size:
                    x_pos, y_pos = GomokuBoard.get_stone_pos(x_pos, y_pos)
                    stone, play_order = game.play_draw_stone(
                        stone, play_order, "black", COLOR_BLACK, x_pos, y_pos)
                    game.draw_text("PLAYER 1", 45 * 16 + 65, GomokuBoard.size // 2 - 90,
                                   COLOR_RED, 20)
                    game.draw_text("PLAYER 2", 45 * 16 + 65, GomokuBoard.size // 2 + 20,
                                   COLOR_BLACK, 20)
                    play_order = game.score(
                        stone, "black", play_order)
                    if len(stone["white"]) + len(stone["black"]) == 225:
                        game.draw_text("DRAW", 45 * 16 + 65, GomokuBoard.size//2 + 120,
                                       (200, 0, 0), 45)
                        play_order = None
        
        if event.type == pg.MOUSEMOTION:
            game.board_button_interaction()
        pg.display.update()
