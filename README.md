
# Build a Game-playing Agent

![Example game of isolation](viz.gif)

## Submission content

* Heuristics comparison: [heuristic_analysis.md](heuristic_analysis.md)
* Alpha Go paper review: [research_review.pdf](research_review.pdf)
* Source code:
    * [game_agent.py](game_agent.py): source code for implementing minimax and alpha-beta pruning as well as various heuristics
    * [tournament.py](tournament.py): The `tournament.py` script is used to evaluate the effectiveness of custom heuristics.


----


Quote from original readme file ([README_original.md](README_original.md)) below:

## Synopsis

In this project, students will develop an adversarial search agent to play the game "Isolation".  Isolation is a deterministic, two-player game of perfect information in which the players alternate turns moving a single piece from one cell to another on a board.  Whenever either player occupies a cell, that cell becomes blocked for the remainder of the game.  The first player with no remaining legal moves loses, and the opponent is declared the winner.  These rules are implemented in the `isolation.Board` class provided in the repository. 

This project uses a version of Isolation where each agent is restricted to L-shaped movements (like a knight in chess) on a rectangular grid (like a chess or checkerboard).  The agents can move to any open cell on the board that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. Movements are blocked at the edges of the board (the board does not wrap around), however, the player can "jump" blocked or occupied spaces (just like a knight in chess).

Additionally, agents will have a fixed time limit each turn to search for the best move and respond.  If the time limit expires during a player's turn, that player forfeits the match, and the opponent wins.

Students only need to modify code in the `game_agent.py` file to complete the project.  Additional files include example Player and evaluation functions, the game board class, and a template to develop local unit tests.  

## Instructions

In order to complete the Isolation project, students must submit code that passes all test cases for the required functions in `game_agent.py` and complete a report as specified in the rubric.  Students can submit using the [Udacity Project Assistant]() command line utility.  Students will receive feedback on test case success/failure after each submission.

Students must implement the following functions:

- `MinimaxPlayer.minimax()`: implement minimax search
- `AlphaBetaPlayer.alphabeta()`: implement minimax search with alpha-beta pruning
- `AlphaBetaPlayer.get_move()`: implement iterative deepening search
- `custom_score()`: implement your own best position evaluation heuristic
- `custom_score_2()`: implement your own alternate position evaluation heuristic
- `custom_score_3()`: implement your own alternate position evaluation heuristic

You may write or modify code within each file (but you must maintain compatibility with the function signatures provided).  You may add other classes, functions, etc., as needed, but it is not required.

The Project Assistant sandbox for this project places some restrictions on the modules available and blocks calls to some of the standard library functions.  In general, standard library functions that introspect code running in the sandbox are blocked, and the PA only allows the following modules `random`, `numpy`, `scipy`, `sklearn`, `itertools`, `math`, `heapq`, `collections`, `array`, `copy`, and `operator`. (Modules within these packages are also allowed, e.g., `numpy.random`.)

### Tournament

The `tournament.py` script is used to evaluate the effectiveness of your custom heuristics.  The script measures relative performance of your agent (named "Student" in the tournament) in a round-robin tournament against several other pre-defined agents.  The Student agent uses time-limited Iterative Deepening along with your custom heuristics.

The performance of time-limited iterative deepening search is hardware dependent (faster hardware is expected to search deeper than slower hardware in the same amount of time).  The script controls for these effects by also measuring the baseline performance of an agent called "ID_Improved" that uses Iterative Deepening and the improved_score heuristic defined in `sample_players.py`.  Your goal is to develop a heuristic such that Student outperforms ID_Improved. (NOTE: This can be _very_ challenging!)


