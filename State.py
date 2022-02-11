from CompressCard import CompressCard


class State:  # Creates
    def __init__(self, board, player, comp, bita, cards_in_deck, turn, attacker, play_num, koser, koser_card):
        self.compressed_board = self.build_board(board)
        self.player_hand = build_player_hand(player)
        self.comp_hand = self.build_comp_hand(comp)
        self.compressed_bita = self.build_bita(bita)
        self.turn = turn
        self.attacker = attacker
        self.play_num = play_num
        self.koser = koser
        self.koser_card = koser_card
        self.cards_in_deck = cards_in_deck

    @staticmethod
    def build_board(board):
        compressed_board = []
        for i in range(len(board)):
            compressed_board[i] = CompressCard(board[i].kind, board[i].value,
                                               board[i].origin, board[i].index)
        return compressed_board

    @staticmethod
    def build_comp_hand(comp):
        comp_hand = []
        for i in range(len(comp)):
            comp_hand[i] = CompressCard(comp[i].kind, comp[i].value,
                                        comp[i].origin, comp[i].index)
        return comp_hand

    @staticmethod
    def build_bita(bita):
        compressed_bita = []
        for i in range(len(bita)):
            compressed_bita[i] = CompressCard(bita[i].kind, bita[i].value,
                                              bita[i].origin, bita[i].index)
        return compressed_bita


def build_player_hand(player):
    player_hand = []
    for i in range(len(player)):
        player_hand[i] = CompressCard(player[i].kind, player[i].value,
                                      player[i].origin, player[i].index)
    return player_hand

