from CompressCard import CompressCard


class State:  # Creates a state of the game
    def __init__(self, board, player, comp, bita, deck, turn, attacker, koser, koser_card):
        self.compressed_board = self.build_board(board)
        self.player_hand = self.build_player_hand(player)
        self.comp_hand = self.build_comp_hand(comp)
        self.compressed_bita = self.build_bita(bita)
        self.turn = turn
        self.attacker = attacker
        self.koser = koser
        self.koser_card = self.create_koser_card(koser_card)
        self.deck = deck

    @staticmethod
    def create_koser_card(koser_card):
        return CompressCard(koser_card.kind, koser_card.value, 0, 0)

    @staticmethod
    def build_board(board):
        compressed_board = []
        for i in range(len(board)):
            compressed_board.append(CompressCard(board[i].kind, board[i].value, board[i].origin, board[i].index))
        return compressed_board

    @staticmethod
    def build_comp_hand(comp):
        comp_hand = []
        for i in range(len(comp)):
            comp_hand.append(CompressCard(comp[i].kind, comp[i].value, comp[i].origin, comp[i].index))
        return comp_hand

    @staticmethod
    def build_bita(bita):
        compressed_bita = []
        for i in range(len(bita)):
            compressed_bita.append(CompressCard(bita[i].kind, bita[i].value, bita[i].origin, bita[i].index))
        return compressed_bita

    @staticmethod
    def build_player_hand(player):
        player_hand = []
        for i in range(len(player)):
            player_hand.append(CompressCard(player[i].kind, player[i].value, player[i].origin, player[i].index))
        return player_hand

