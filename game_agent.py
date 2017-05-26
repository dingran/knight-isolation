"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import numpy as np


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def percent_occupied(game):
    """
            Checks if a move is in the corners of the board

            Parameters
            ----------
            game : `isolation.Board`
                The game board

            Returns
            -------
            int
                The percentage of occupied space in the board
        """
    blank_spaces = game.get_blank_spaces()
    return int((len(blank_spaces) / (game.width * game.height)) * 100)


def is_near_walls(move, walls):
    """
    Checks if a move is on near the edges of the board

    Parameters
    ----------
    move : (int, int)
        The input move on the board

    walls : list(list(tuples))
        A nested list of tuples for each edge of the board

    Returns
    -------
    bool
        Returns True if a move lies along the edges else False
    """
    for wall in walls:
        if move in wall:
            return True
    return False


def is_in_corners(move, corners):
    """
        Checks if a move is in the corners of the board

        Parameters
        ----------
        move : (int, int)
            The input move on the board

        corners : list(tuples)
            A list of tuples for each corner of the board

        Returns
        -------
        bool
            Returns True if a move lies in a corner of the board else False
    """
    return move in corners


def score_differential_open_move(game, player, aggressiveness=1.0):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # print('aggressiveness: {}'.format(aggressiveness))
    score = float(own_moves - aggressiveness * opp_moves)

    return score


def score_time_variant_differential_open_move(game, player, var=1):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = float(len(game.get_legal_moves(player)))
    opp_moves = float(len(game.get_legal_moves(game.get_opponent(player))))

    pct = percent_occupied(game)

    if var == 1:
        if pct < 50:
            score = own_moves - 2.5 * opp_moves

        else:
            score = own_moves - 0.5 * opp_moves
    else:
        if pct < 50:
            score = own_moves - 0.5 * opp_moves

        else:
            score = own_moves - 2.5 * opp_moves

    return score


def score_look_ahead_differential_move(game, player, aggressiveness=1.0):
    """ Improved score weighted on available moves of legal moves """
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


def score_look_ahead_agg(game, player):
    """ Improved score weighted on available moves of legal moves """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # Sum the available next moves for each legal move, assuming current board
    opp_next = float(sum([len(game._Board__get_moves(move)) for move in opp_moves]))
    return - (len(opp_moves) * opp_next)


def score_wall_corner_aware_differential_open_move(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    walls = [
        [(0, i) for i in range(game.width)],
        [(i, 0) for i in range(game.height)],
        [(game.width - 1, i) for i in range(game.width)],
        [(i, game.height - 1) for i in range(game.height)]
    ]

    corners = [(0, 0), (0, game.width - 1), (game.height - 1, 0), (game.height - 1, game.width - 1)]

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    own_cum_score_wall = 0
    opp_cum_score_wall = 0
    wall_score_inc_early = 10
    wall_score_inc_mid = -20
    wall_score_inc_late = -30

    own_cum_score_corner = 0
    opp_cum_score_corner = 0
    corner_score_inc_early = 15
    corner_score_inc_late = -40

    own_moves_left = 0
    opp_moves_left = 0

    move_left_score_inc = 10

    for move in own_moves:
        if is_near_walls(move, walls):
            if percent_occupied(game) < 30:
                own_cum_score_wall += wall_score_inc_early
            elif 30 <= percent_occupied(game) < 60:
                own_cum_score_wall += wall_score_inc_mid
            else:
                own_cum_score_wall += wall_score_inc_late

        elif is_in_corners(move, corners):
            if percent_occupied(game) < 60:
                own_cum_score_corner += corner_score_inc_early
            else:
                own_cum_score_corner += corner_score_inc_late
        else:  # not in corners or near wall
            own_moves_left += move_left_score_inc

    for move in opp_moves:
        if is_near_walls(move, walls):
            if percent_occupied(game) < 30:
                opp_cum_score_wall += wall_score_inc_early
            elif 30 <= percent_occupied(game) < 60:
                opp_cum_score_wall += wall_score_inc_mid
            else:
                opp_cum_score_wall += wall_score_inc_late

        elif is_in_corners(move, corners):
            if percent_occupied(game) < 60:
                opp_cum_score_corner += corner_score_inc_early
            else:
                opp_cum_score_corner += corner_score_inc_late
        else:  # not in corners or near wall
            opp_moves_left += move_left_score_inc

    wall_score = float(own_cum_score_wall - opp_cum_score_wall)
    corner_score = float(own_cum_score_corner - opp_cum_score_corner)
    open_move_score = float(own_moves_left - opp_moves_left)

    overall_score = 0.3 * wall_score + 0.7 * corner_score + 1.0 * open_move_score

    return overall_score


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    return score_differential_open_move(game, player, aggressiveness=1.0)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    return score_differential_open_move(game, player, aggressiveness=0.5)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    return score_differential_open_move(game, player, aggressiveness=2.5)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

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
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            # print('SearchTimeout raised')
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

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
                                       current_depth=current_depth + 1, depth_limit=depth)
            # print('inner loop: ', min_val, legal_move)
            if score > best_score:
                best_score = score
                best_move = legal_move

        # print('>>>>>', minimax_move, self.time_left())
        return best_move

    def min_value(self, game, current_depth, depth_limit):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print('raising timeout in min_value')
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return np.inf

        best_score = np.inf
        for m in legal_moves:
            if depth_limit == current_depth:
                score = self.score(game.forecast_move(m), self)
            else:
                score = self.max_value(game.forecast_move(m), current_depth + 1, depth_limit)

            if score < best_score:
                best_score = score
        # print('min_val depth: {}, min_score {}'.format(current_depth, min_score))
        return best_score

    def max_value(self, game, current_depth, depth_limit):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print('raising timeout in max_value')
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return -np.inf

        best_score = -np.inf
        for m in legal_moves:
            if depth_limit == current_depth:
                score = self.score(game.forecast_move(m), self)
            else:
                score = self.min_value(game.forecast_move(m), current_depth + 1, depth_limit)

            if score > best_score:
                best_score = score

        return best_score


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

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
        if self.time_left() < self.TIMER_THRESHOLD * 1.5:
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
        if self.time_left() < self.TIMER_THRESHOLD * 1.5:
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
