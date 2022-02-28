import copy
import time


class AI:

    @staticmethod
    def possible_moves(game_state):
        if game_state.attacker:  # player is the attacker
            pos_moves = [[0, -1], [3, -1]]  # defend or take
        elif len(game_state.compressed_board) > 0:  # computer is the attacker
            pos_moves = [[1, -1], [2, -1]]  # attack or bita
        else:
            pos_moves = [[1, -1], [1, -1]]  # attack
        return pos_moves

    @staticmethod
    def get_available_moves(game_state):  # returns all free spaces in form of (x, y) index
        moves = []
        for i in range(len(game_state.comp_hand)):
            if game_state.comp_hand[i].kind == game_state.board[-1].kind:
                if game_state.comp_hand[i].value > game_state.board[-1].value:
                    moves.append(game_state.comp_hand[i])
            elif game_state.player[i].kind == game_state.koser:
                moves.append(game_state.comp_hand[i])
        return moves

    @staticmethod
    def next_state(game_state, move, turn):  # returns a copy of the board after the move that was given was simulated
        new_state = copy.deepcopy(AI.update_state(game_state, move))
        new_state[move[0]] = turn
        return new_state

    @staticmethod
    def update_state(game_state, move):  # updates the state of the game
        if move >= 0:
            game_state.compressed_board.append(game_state.comp_hand.pop(move))
        elif move == -1:
            for i in range(len(game_state.compressed_board)):
                game_state.compressed_bita.append(game_state.compressed_board.pop(-1))
            bn = True
            while bn and len(game_state.deck) > 0:
                if len(game_state.comp_hand) < 6:
                    game_state.comp_hand.append(game_state.deck.pop(-1))
                else:
                    bn = False
                if len(game_state.player_hand) < 6 and len(game_state.deck) > 0:
                    game_state.player_hand.append(game_state.deck.pop(-1))
                    bn = True
        elif move == -2:
            for i in range(len(game_state.compressed_board)):
                game_state.comp_hand.append(game_state.compressed_board.pop(-1))
        return game_state

    @staticmethod
    def won(game_state, turn, bn):  # checks if the player that was given won
        if len(game_state.deck) == 0:
            if len(game_state.player) == 0:
                return 1
            elif len(game_state.comp_hand) == 0:
                return 2
            else:
                return 0
        else:
            return 0

    @staticmethod
    def evaluate(game_state):  # evaluates a board
        if AI.won(game_state, -1, False) == 1:  # human won
            return -1
        elif AI.won(game_state, 1, False) == 2:  # computer won
            return 1
        else:  # tie
            return 0

    @staticmethod
    def minimax(game_state, level):  # first call- computer player
        start_time = time.time()
        moves = AI.get_available_moves(game_state)
        best_move = copy.deepcopy(moves[0])
        best_score = float('-inf')
        for move in moves:
            clone = copy.deepcopy(AI.next_state(game_state, move, 1))
            score = AI.min_play(clone, level - 1)
            if score > best_score:
                best_move = move
                best_score = score
            print(move, score)
        end_time = time.time()
        print()
        time_lapsed = end_time - start_time
        print(time_lapsed)
        return best_move

    @staticmethod
    def min_play(game_state, level):  # human player
        turn = -1
        if AI.won(game_state, 1, True) or level == 0:
            return AI.evaluate(game_state)
        moves = copy.deepcopy(AI.get_available_moves(game_state))
        best_score = float('inf')
        for move in moves:
            clone = copy.deepcopy(AI.next_state(game_state, move, turn))
            score = AI.max_play(clone, level - 1)
            if score < best_score:
                best_move = copy.deepcopy(move)
                best_score = score
        return best_score

    @staticmethod
    def max_play(game_state, level):  # computer
        turn = 1
        if AI.won(game_state, -1, True) or level == 0:
            return AI.evaluate(game_state)
        moves = copy.deepcopy(AI.get_available_moves(game_state))
        best_score = float('-inf')
        for move in moves:
            clone = copy.deepcopy(AI.next_state(game_state, move, turn))
            score = AI.min_play(clone, level - 1)
            if score > best_score:
                best_move = copy.deepcopy(move)
                best_score = score
        return best_score
