import pygame as pg

from gomoku.gomoku import Gomoku
from gomoku.colors import *

if __name__ == "__main__":
    pg.init()
    pg.font.init()
    
    # 게임을 초기화 합니다.
    stone = {}
    stone["white"], stone["black"] = [], []
    player1_score, player2_score = 0, 0
    game = Gomoku()
    game.draw_main()
    game.draw_score(player1_score, player2_score)

    play_order = None

    while True:
        event = pg.event.poll()
        if event.type == pg.MOUSEBUTTONDOWN:

            x_stone, y_stone = game.play_get_pos()

            # New game 버튼 누름. 모든 게임 초기화.
            if (125 + 45 * 16) > x_stone > 45 * 16 and 90 > y_stone > 45:
                stone["white"], stone["black"] = [], []
                player1_score, player2_score = 0, 0 # 요고 유무 차이
                game = Gomoku()
                game.draw_main()
                game.draw_score(player1_score, player2_score)
                game.text_draw("GAME START", game.w_h//2, 30, COLOR_GREEN, 35)
                play_order = True

            # Next game 버튼 누름. 스코어 제외 초기화.
            if (125 + 45 * 16) > x_stone > 45 * 16 and 160 > y_stone > 115:
                stone["white"], stone["black"] = [], []
                game = Gomoku()
                game.draw_main()
                game.draw_score(player1_score, player2_score)
                game.text_draw("NEXT GAME START", game.w_h//2, 30, COLOR_GREEN, 35)
                play_order = True

            # 흰색 돌을 표시. (Player 1).
            if play_order is None:  # play_order가 False이면 흰색 차례. True이면 검은 색 차례.
                pass
            elif not play_order:
                # 누구 차례인지를 표시
                game.text_draw("PLAYER 1", 45 * 16 + 65, game.w_h // 2 - 90,
                               COLOR_RED, 20)
                game.text_draw("PLAYER 2", 45 * 16 + 65, game.w_h // 2 + 20,
                               COLOR_BLACK, 20)
                if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:
                    x_stone, y_stone = game.play_draw_stone_pos()   # 마우스 좌표 가져옴.
                    stone, play_order = game.play_draw_stone(
                        stone, play_order, "white", COLOR_WHITE,
                        x_stone, y_stone)   # 흰돌을 그린다.
                    game.text_draw("PLAYER 1", 45 * 16 + 65, game.w_h // 2 - 90,
                                   COLOR_GRAY, 20)
                    game.text_draw("PLAYER 2", 45 * 16 + 65, game.w_h // 2 + 20,
                                   COLOR_RED, 20)   # 누구 차례인지를 표시.
                    player1_score, play_order = game.score(
                        stone, "white", player1_score, play_order)  # 이겼는지 판단.
                    if len(stone["white"]) + len(stone["black"]) == 225:    # 무승부 판단.
                        game.text_draw("DRAW", 45 * 16 + 65, game.w_h // 2 + 120,
                                       (200, 0, 0), 45)
                        play_order = None

            # 검은색 돌을 표시. (Player 2).
            elif play_order:
                game.text_draw("PLAYER 1", 45 * 16 + 65, game.w_h // 2 - 90,
                               COLOR_GRAY, 20)
                game.text_draw("PLAYER 2", 45 * 16 + 65, game.w_h // 2 + 20,
                               COLOR_RED, 20)
                if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:
                    x_stone, y_stone = game.play_draw_stone_pos()
                    stone, play_order = game.play_draw_stone(
                        stone, play_order, "black", COLOR_BLACK, x_stone, y_stone)
                    game.text_draw("PLAYER 1", 45 * 16 + 65, game.w_h // 2 - 90,
                                   COLOR_RED, 20)
                    game.text_draw("PLAYER 2", 45 * 16 + 65, game.w_h // 2 + 20,
                                   COLOR_BLACK, 20)
                    player2_score, play_order = game.score(
                        stone, "black", player2_score, play_order)
                    if len(stone["white"]) + len(stone["black"]) == 225:
                        game.text_draw("DRAW", 45 * 16 + 65, game.w_h//2 + 120,
                                       (200, 0, 0), 45)
                        play_order = None
        game.interactive_button()
        pg.display.update()
