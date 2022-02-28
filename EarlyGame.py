
class EarlyGame:
    def __init__(self, state):
        self.index = -1  # index of card to attack with (-1 - not set)
        self.state = state
        self.pos_moves = self.possible_moves()  # | 0 - defend | 1 - attack | 2 - bita | 3 - take |
        self.pos_plays = self.possible_plays()  # | -2 - take | -1 - bita | other numbers - index of card for move |
        self.best_move = self.determine_best_move()  # | -1 - bita | -2 - take | other number - index of card for move |

    def possible_moves(self):
        if self.state.attacker:  # player is the attacker
            pos_moves = [[0, -1], [3, -1]]  # defend or take
        elif len(self.state.compressed_board) > 0:  # computer is the attacker
            pos_moves = [[1, -1], [2, -1]]  # attack or bita
        else:
            pos_moves = [[1, -1], [1, -1]]  # attack
        return pos_moves

    def possible_plays(self):  # finds all possible plays
        first = self.pos_moves[0]
        second = self.pos_moves[1]
        if first[0] == 0:  # defend
            first_val = self.defend_value()
        else:  # attack
            first_val = self.attack_value()
        if second[0] != 1:
            if second[0] == 2:  # bita
                second_val = self.bita_value()
            else:  # take
                second_val = self.take_value()
        else:
            second_val = first_val - 10
        return [first_val, second_val]

    def determine_best_move(self):  # returns the best kind of move to make
        if self.pos_plays[0] > self.pos_plays[1]:
            return self.pos_moves[0]  # defend or attack (0 or 1)
        else:
            return self.pos_moves[1]  # take or bita (3 or 2)

    def defend_value(self):  # returns the value of defend move
        move = self.defend_move()
        state = self.update_state(move)
        value = self.hand_value(state)
        return value

    def attack_value(self):  # returns the value of attack move
        move = self.attack_move()
        state = self.update_state(move)
        value = self.hand_value(state)
        return value

    def bita_value(self):  # returns the value of bita move
        state = self.update_state(-1)
        value = self.hand_value(state)
        return value

    def take_value(self):  # returns the value of take move
        state = self.update_state(-2)
        value = self.hand_value(state)
        return value

    def update_state(self, move):  # updates the state of the game
        state = self.state
        if move >= 0:
            state.compressed_board.append(state.comp_hand.pop(move))
        elif move == -1:
            for i in range(len(state.compressed_board)):
                state.compressed_bita.append(state.compressed_board.pop(-1))
            bn = True
            while bn and len(state.deck) > 0:
                if len(state.comp_hand) < 6:
                    state.comp_hand.append(state.deck.pop(-1))
                else:
                    bn = False
                if len(state.player_hand) < 6 and len(state.deck) > 0:
                    state.player_hand.append(state.deck.pop(-1))
                    bn = True
        elif move == -2:
            for i in range(len(state.compressed_board)):
                state.comp_hand.append(state.compressed_board.pop(-1))
        return state

    def defend_move(self):  # returns the move to defend
        state = self.state
        hand = state.comp_hand
        value = state.compressed_board[-1].value
        kind = state.compressed_board[-1].kind
        min_value = 15
        index = -1
        for i in range(len(hand)):
            if hand[i].kind == state.compressed_board[-1].kind:
                if hand[i].value > state.compressed_board[-1].value:
                    if hand[i].value < min_value:
                        min_value = hand[i].value
                        index = i
        if min_value == 15 and not state.compressed_board[-1].kind == state.koser:
            for i in range(len(hand)):
                if hand[i].kind == state.koser and hand[i].value < min_value:
                    min_value = hand[i].value
                    index = i
        self.index = index
        self.pos_moves[0][1] = index
        return index

    def attack_move(self):  # returns the move to attack
        state = self.state
        hand = state.comp_hand

        min_value = 15
        index = -1

        if len(state.compressed_board) == 0:
            for i in range(len(hand)):
                if not hand[i].kind == state.koser:
                    if hand[i].value < min_value:
                        min_value = hand[i].value
                        index = i
            if index == -1:
                for i in range(len(hand)):
                    if hand[i].value < min_value:
                        min_value = hand[i].value
                        index = i
        else:
            value = state.compressed_board[-1].value
            kind = state.compressed_board[-1].kind
            for i in range(len(hand)):
                for j in range(len(state.compressed_board)):
                    if hand[i].kind != state.koser and hand[i].value == state.compressed_board[j].value:
                        if hand[i].value < min_value:
                            min_value = hand[i].value
                            index = i
        if index == -1:
            for i in range(len(hand)):
                for j in range(len(state.compressed_board)):
                    if hand[i].value == state.compressed_board[j].value:
                        if hand[i].value < min_value:
                            min_value = hand[i].value
                            index = i
        self.index = index
        self.pos_moves[0][1] = index
        return index

    @staticmethod
    def hand_value(state):  # returns the value of the hand
        hand = state.comp_hand
        value = 0
        if len(hand) > 6:
            value = (-2)*(len(hand) - 6)
        if len(hand) < 6:
            value = 0.5*(6 - len(hand))
        for i in range(len(hand)):
            if hand[i].kind == state.koser:
                value += 5
                value += (hand[i].value - 6) * 0.5

        return value
