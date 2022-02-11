
class EarlyGame:
    def __init__(self, state, ):
        self.state = state
        self.pos_moves = self.possible_moves()  # | 0 - defend | 1 - attack | 2 - bita | 3 - take |
        self.pos_plays = self.possible_plays()  # | -2 - take | -1 - bita | other numbers - index of card for move |
        self.best_move = self.determine_best_move()  # | 0 - defend | 1 - attack | 2 - bita | 3 - take |

    def possible_moves(self):
        if self.state.attacker:  # player is the attacker
            pos_moves = [0, 3]  # defend or take
        else:  # computer is the attacker
            pos_moves = [1, 2]  # attack or bita
        return pos_moves

    def possible_plays(self):  # finds all possible plays
        first = self.pos_moves[0]
        second = self.pos_moves[1]
        if first == 0:  # defend
            first_val = self.defend_value()
        else:  # attack
            first_val = self.attack_value()
        if second == 2:  # bita
            second_val = self.bita_value()
        else:  # take
            second_val = self.take_value()
        return [first_val, second_val]

    def determine_best_move(self):  # returns the best kind of move to make
        if self.pos_plays[0] > self.pos_plays[1]:
            return self.pos_moves[0]
        else:
            return self.pos_moves[1]

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
            state.board[-1] = state.comp_hand.pop(move)
        elif move == -1:
            for i in range(len(state.board)):
                state.compressed_bita.append(state.board.pop(-1))
            bn = True
            while bn:
                if len(state.comp_hand) < 6:
                    state.comp_hand.append(state.deck.pop(-1))
                else:
                    bn = False
                if len(state.player_hand) < 6:
                    state.player_hand.append(state.deck.pop(-1))
                    bn = True
        elif move == -2:
            for i in range(len(state.board)):
                state.comp_hand.append(state.board.pop(-1))
        return state

    def defend_move(self):  # returns the move to defend
        state = self.state
        hand = state.comp_hand()
        value = state.board[-1].value
        kind = state.board[-1].kind
        min_value = 15
        index = -1
        for i in range(len(hand)):
            if hand[i].kind == state.board[-1].kind:
                if hand[i].value > state.board[-1].value:
                    if hand[i].value < min_value:
                        min_value = hand[i].value
                        index = i
        if min_value == 15 and not state.board[-1].kind == state.koser:
            for i in range(len(hand)):
                if hand[i].kind == state.koser and hand[i].value < min_value:
                    min_value = hand[i].value
                    index = i
        return index

    def attack_move(self):  # returns the move to attack
        state = self.state
        hand = state.comp_hand()
        value = state.board[-1].value
        kind = state.board[-1].kind
        min_value = 15
        index = -1

        if len(state.board) == 0:
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
            for i in range(len(hand)):
                for j in range(len(state.board)):
                    if hand[i].kind != state.koser and hand[i].value == state.board[j].value:
                        if hand[i].value < min_value:
                            min_value = hand[i].value
                            index = i
        if index == -1:
            for i in range(len(hand)):
                for j in range(len(state.board)):
                    if hand[i].value == state.board[j].value:
                        if hand[i].value < min_value:
                            min_value = hand[i].value
                            index = i
        return index

    @staticmethod
    def hand_value(state):  # returns the value of the hand
        hand = state.comp_hand()
        value = 0
        if len(hand) > 6:
            value = -2*(len(hand) - 6)
        for i in range(len(hand)):
            if hand[i].kind == state.koser:
                value += 3
            if hand[i].value >= 10:
                value += (1 + 0.5*(hand[i].value - 10))
            elif hand[i].kind != state.koser:
                value += 0.5*(hand[i].value - 10)
        return value
