import copy
import time
from CompressCard import CompressCard


class AI:

    @staticmethod
    def possible_moves(gamestate):
        if gamestate.attacker:  # player is the attacker
            pos_moves = [[0, -1], [3, -1]]  # defend or take
        elif len(gamestate.compressed_board) > 0:  # computer is the attacker
            pos_moves = [[1, -1], [2, -1]]  # attack or bita
        else:
            pos_moves = [[1, -1], [1, -1]]  # attack
        return pos_moves

    @staticmethod
    def get_available_moves_comp(gamestate, turn):  # finds all possible moves for the computer
        moves = []
        for i in range(len(gamestate.comp_hand)):
            if len(gamestate.comp_hand) and len(gamestate.compressed_board) > 0:
                if gamestate.comp_hand[i].kind == gamestate.compressed_board[-1].kind:
                    if gamestate.comp_hand[i].value > gamestate.compressed_board[-1].value:
                        moves.append(gamestate.comp_hand[i])
                        moves[-1].index = i
                elif gamestate.comp_hand[i].kind == gamestate.koser:
                    moves.append(gamestate.comp_hand[i])
                    moves[-1].index = i
            elif len(gamestate.compressed_board) == 0:
                moves.append(gamestate.comp_hand[i])
                moves[-1].index = i

        if not turn:
            moves.append(CompressCard(0, 0, 0, -1))
        else:
            moves.append(CompressCard(0, 0, 0, -2))
        return moves

    @staticmethod
    def get_available_moves_player(gamestate, turn):  # returns all free spaces in form of (x, y) index
        moves = []
        for i in range(len(gamestate.player_hand)):
            if len(gamestate.player_hand) and len(gamestate.compressed_board) > 0:
                if gamestate.player_hand[i].kind == gamestate.compressed_board[-1].kind:
                    if gamestate.player_hand[i].value > gamestate.compressed_board[-1].value:
                        moves.append(gamestate.player_hand[i])
                        moves[-1].index = i
                elif gamestate.player_hand[i].kind == gamestate.koser:
                    moves.append(gamestate.player_hand[i])
                    moves[-1].index = i

            elif len(gamestate.compressed_board) == 0:
                moves.append(gamestate.player_hand[i])
                moves[-1].index = i
        if turn:
            moves.append(CompressCard(0, 0, 0, -1))
        else:
            moves.append(CompressCard(0, 0, 0, -2))
        return moves

    @staticmethod
    def next_state_comp(gamestate, move):  # returns a copy of the board after the move that was given was simulated
        new_state = gamestate
        new_state = AI.update_state_comp(new_state, move)
        return new_state

    @staticmethod
    def next_state_player(gamestate, move):  # returns a copy of the board after the move that was given was simulated
        new_state = gamestate
        new_state = AI.update_state_player(new_state, move)
        return new_state

    @staticmethod
    def update_state_comp(gamestate, move):  # updates the state of the game
        if 0 <= move.index < len(gamestate.comp_hand):
            gamestate.compressed_board.append(gamestate.comp_hand.pop(move.index))
        elif move.index == -1:
            for i in range(len(gamestate.compressed_board)):
                gamestate.compressed_bita.append(gamestate.compressed_board.pop(-1))
            bn = True
            while bn and len(gamestate.deck) > 0:
                if len(gamestate.comp_hand) < 6:
                    gamestate.comp_hand.append(gamestate.deck.pop(-1))
                else:
                    bn = False
                if len(gamestate.player_hand) < 6 and len(gamestate.deck) > 0:
                    gamestate.player_hand.append(gamestate.deck.pop(-1))
                    bn = True
        elif move.index == -2:
            for i in range(len(gamestate.compressed_board)):
                gamestate.comp_hand.append(gamestate.compressed_board.pop(-1))
        return gamestate

    @staticmethod
    def update_state_player(gamestate, move):  # updates the state of the game
        if 0 <= move.index < len(gamestate.player_hand):
            gamestate.compressed_board.append(gamestate.player_hand.pop(move.index))
        elif move.index == -1:
            for i in range(len(gamestate.compressed_board)):
                gamestate.compressed_bita.append(gamestate.compressed_board.pop(-1))
            bn = True
            while bn and len(gamestate.deck) > 0:
                if len(gamestate.player_hand) < 6:
                    gamestate.player_hand.append(gamestate.deck.pop(-1))
                else:
                    bn = False
                if len(gamestate.comp_hand) < 6 and len(gamestate.deck) > 0:
                    gamestate.comp_hand.append(gamestate.deck.pop(-1))
                    bn = True
        elif move.index == -2:
            for i in range(len(gamestate.compressed_board)):
                gamestate.player_hand.append(gamestate.compressed_board.pop(-1))
        return gamestate

    @staticmethod
    def won(gamestate):  # checks if the player that was given won
        if len(gamestate.deck) == 0:
            if len(gamestate.player_hand) == 0:
                return True
            elif len(gamestate.comp_hand) == 0:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def minimax(gamestate):  # first call- computer
        start_time = time.time()
        moves = AI.get_available_moves_comp(gamestate, True)
        if len(moves) == 0:
            return CompressCard(0, 0, 0, -2)
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = AI.next_state_comp(gamestate, move)
            score = AI.min_play(clone)
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
    def min_play(gamestate):  # human player
        turn = False
        if AI.won(gamestate):
            return 1
        moves = AI.get_available_moves_player(gamestate, turn)
        best_score = float('inf')
        for move in moves:
            clone = copy.deepcopy(AI.next_state_player(gamestate, move))
            score = AI.max_play(clone)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    @staticmethod
    def max_play(gamestate):  # computer
        turn = True
        if AI.won(gamestate):
            return -1
        moves = AI.get_available_moves_comp(gamestate, turn)
        best_score = float('-inf')
        for move in moves:
            clone = copy.deepcopy(AI.next_state_comp(gamestate, move))
            score = AI.min_play(clone)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score
