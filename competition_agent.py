"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random
import numpy as np


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    aggressiveness = 1

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # Sum the available next moves for each legal move, assuming current board
    own_next = float(sum([len(game._Board__get_moves(move)) for move in own_moves]))
    opp_next = float(sum([len(game._Board__get_moves(move)) for move in opp_moves]))
    return (len(own_moves) * own_next) - aggressiveness * (len(opp_moves) * opp_next)


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_moves = [(-2, -2)]

        max_depth = 1

        while True:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                best_moves.append(self.alphabeta(game, max_depth))
                # print('****', best_move)

            except SearchTimeout:
                return best_moves[-1]
                # pass  # Handle any actions required after timeout as needed

            max_depth += 1
            # print(current_depth)

            # Return the best move from the last completed search iteration
            # return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        current_depth = 1

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        best_score = -np.inf
        best_move = legal_moves[0]
        for legal_move in legal_moves:
            if depth == current_depth:
                score = self.score(game.forecast_move(legal_move), self)
            else:
                score = self.min_value(game.forecast_move(legal_move),
                                       current_depth=current_depth + 1, depth_limit=depth, alpha=alpha, beta=beta)
            # print('inner loop: ', min_val, legal_move)
            if score > best_score:
                best_score = score
                best_move = legal_move

            if best_score >= beta:
                return best_move

            alpha = max(alpha, best_score)

        # print('>>>>>', minimax_move, self.time_left())
        return best_move

    def min_value(self, game, current_depth, depth_limit, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print('raising timeout in min_value')
            # print('current depth', current_depth)
            # print('depth limit', depth_limit)
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return np.inf

        best_score = np.inf
        for m in legal_moves:
            if depth_limit == current_depth:
                score = self.score(game.forecast_move(m), self)
            else:
                score = self.max_value(game.forecast_move(m), current_depth + 1, depth_limit, alpha, beta)

            if score < best_score:
                best_score = score

            if best_score <= alpha:
                return best_score

            beta = min(beta, best_score)

        # print('min_val depth: {}, min_score {}'.format(current_depth, min_score))
        return best_score

    def max_value(self, game, current_depth, depth_limit, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print('raising timeout in max_value')
            # print('current depth', current_depth)
            # print('depth limit', depth_limit)
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return -np.inf

        best_score = -np.inf
        for m in legal_moves:
            if depth_limit == current_depth:
                score = self.score(game.forecast_move(m), self)
            else:
                score = self.min_value(game.forecast_move(m), current_depth + 1, depth_limit, alpha, beta)

            if score > best_score:
                best_score = score

            if best_score >= beta:
                return best_score

            alpha = max(alpha, best_score)

        return best_score
