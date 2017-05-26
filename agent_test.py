"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players

from importlib import reload
import timeit


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)


class MinimaxPlayerTest(unittest.TestCase):
    """Unit tests for MinimaxPlayer agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = sample_players.RandomPlayer()
        self.player2 = game_agent.MinimaxPlayer()
        # self.player2 = game_agent.AlphaBetaPlayer()
        self.game = isolation.Board(self.player1, self.player2)

    def test_output_single_step_minimax(self):

        # self.player2.search_depth = 100
        print('\n')
        time_millis = lambda: 1000 * timeit.default_timer()
        time_limit = 150

        self.game.apply_move((2, 3))
        print(self.game.to_string())

        assert (self.player2 == self.game.active_player)

        legal_player_moves = self.game.get_legal_moves()

        move_start = time_millis()
        time_left = lambda: time_limit - (time_millis() - move_start)
        print(time_left())
        curr_move = self.game._active_player.get_move(self.game, time_left)
        print(time_left())

        self.game.apply_move(curr_move)

        print(self.game.to_string())
        # self.assertTrue(curr_move in legal_player_moves)
        print(curr_move)

    # def test_gameplay_minimax(self):
    #     move_history = []
    #
    #     time_millis = lambda: 1000 * timeit.default_timer()
    #     time_limit = 150
    #
    #     while True:
    #         print('\n')
    #         print(self.game.active_player)
    #         legal_player_moves = self.game.get_legal_moves()
    #
    #         move_start = time_millis()
    #         time_left = lambda : time_limit - (time_millis() - move_start)
    #         print(time_left())
    #         curr_move = self.game._active_player.get_move(self.game, time_left)
    #         move_end = time_left()
    #         print(time_left())
    #         print(curr_move)
    #
    #         if move_end < 0:
    #             result = self.game._inactive_player, move_history, "timeout"
    #             print(result)
    #             return
    #
    #         if curr_move not in legal_player_moves:
    #             if len(legal_player_moves) > 0:
    #                 print(legal_player_moves)
    #                 result = self.game._inactive_player, move_history, "forfeit"
    #                 print(result)
    #                 return
    #             result = self.game._inactive_player, move_history, "illegal move"
    #             print(result)
    #             return
    #
    #         move_history.append(list(curr_move))
    #
    #         self.game.apply_move(curr_move)
    #         print(self.game.to_string())


if __name__ == '__main__':
    unittest.main()
