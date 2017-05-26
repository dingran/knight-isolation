# Helper Functions for Evaluators
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


# Evaluator Functions
def evaluator_aggresively_chase_opponent(game, player):
    """The "Aggresively Chase Opponent" evaluation function outputs a
        score equal to the difference in the number of moves available to the player
        and twice the numbers of moves available to the opponent

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : hashable
            One of the objects registered by the game object as a valid player.
            (i.e., `player` should be either game.__player_1__ or
            game.__player_2__).

        Returns
        ----------
        float
            The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(abs(own_moves - 2 * opp_moves))


def evaluator_check_near_walls(game, player):
    """The "Check Near Walls" evaluation function calculates a cumulative score based on the moves
    and their positions.
    A cumulative score is calculated for both the players.
    A positive score is added to the cumulative score for the player if the board is less than 50% occupied and
    the moves lie on the walls, in case the board is between 50% and 85% occupied a higher score is subtracted from the sum.
    If the occupancy is greater than 85% even more higher score is subtracted
    The process is negated in case of the opponent.
    The difference between both the player cumulative scores is added to the number difference of non-corners move for both players
    and the value returned

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : hashable
            One of the objects registered by the game object as a valid player.
            (i.e., `player` should be either game.__player_1__ or
            game.__player_2__).

        Returns
        ----------
        float
            The heuristic value of the current game state
    """
    walls = [
        [(0, i) for i in range(game.width)],
        [(i, 0) for i in range(game.height)],
        [(game.width - 1, i) for i in range(game.width)],
        [(i, game.height - 1) for i in range(game.height)]
    ]
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    own_cum_score = 0
    opp_cum_score = 0

    own_moves_left = 0
    opp_moves_left = 0
    for move in own_moves:
        if is_near_walls(move, walls) and percent_occupied(game) < 50:
            own_cum_score += 10
        elif is_near_walls(move, walls) and percent_occupied(game) > 50 and percent_occupied(game) < 85:
            own_cum_score -= 20
        elif is_near_walls(move, walls) and percent_occupied(game) > 85:
            own_cum_score -= 30
        else:
            own_moves_left += 5

    for move in opp_moves:
        if is_near_walls(move, walls) and percent_occupied(game) < 50:
            opp_cum_score += 10
        elif is_near_walls(move, walls) and percent_occupied(game) > 50 and percent_occupied(game) < 85:
            opp_cum_score -= 20
        elif is_near_walls(move, walls) and percent_occupied(game) > 85:
            opp_cum_score -= 30
        else:
            opp_moves_left += 5

    return float(own_cum_score - opp_cum_score) + float(own_moves_left - opp_moves_left)


def evaluator_check_in_corners(game, player):
    """The "Check In Corners" evaluation function calculates a cumulative score based on the moves
        and their positions.
        A cumulative score is calculated for both the players.
        A positive score is added to the cumulative score for the player if the board is less than 60% occupied and
        the moves lie in the corners, in case the board is more than 60% occupied a higher score is subtracted from the sum.
        The process is negated in case of the opponent.
        The difference between both the player cumulative scores is added to the number difference of non-corners move for both players
        and the value returned

                Parameters
                ----------
                game : `isolation.Board`
                    An instance of `isolation.Board` encoding the current state of the
                    game (e.g., player locations and blocked cells).

                player : hashable
                    One of the objects registered by the game object as a valid player.
                    (i.e., `player` should be either game.__player_1__ or
                    game.__player_2__).

                Returns
                ----------
                float
                    The heuristic value of the current game state
                """
    corners = [(0, 0), (0, game.width - 1), (game.height - 1, 0), (game.height - 1, game.width - 1)]

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    own_cum_score = 0
    opp_cum_score = 0
    own_moves_left = 0
    opp_moves_left = 0
    for move in own_moves:
        if is_in_corners(move, corners) and percent_occupied(game) < 60:
            own_cum_score += 15
        elif is_in_corners(move, corners) and percent_occupied(game) > 60:
            own_cum_score -= 40
        else:
            own_moves_left += 10

    for move in opp_moves:
        if is_in_corners(move, corners) and percent_occupied(game) < 60:
            opp_cum_score += 15
        elif is_in_corners(move, corners) and percent_occupied(game) > 60:
            opp_cum_score -= 40
        else:
            opp_moves_left += 10

    return float(own_cum_score - opp_cum_score) + float(own_moves_left - opp_moves_left)


def evaluator_check_near_walls_and_corners(game, player):
    """The "Check Near Walls And Corners" evaluation function calculates a cumulative score based on the moves
            and their positions.
            A cumulative score is calculated for both the players.
            The method calculates the score for corners using 'evaluator_check_in_corners',
            and the score for walls using 'evaluator_check_near_walls'. The walls score is multiplied by 0.3 and
            corners score is multiplied y 0.7 and their sum is returned.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    walls_score = evaluator_check_near_walls(game, player)
    corners_score = evaluator_check_in_corners(game, player)
    return float(0.3 * walls_score + 0.7 * corners_score)