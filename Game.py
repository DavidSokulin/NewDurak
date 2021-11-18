import random
from kivy.uix.layout import Layout
from Card import Card
from Place import Place
from kivy.core.window import Window
from kivy.app import App


class Game(Layout):
    def __init__(self, **kwargs):
        Window.system_size = (1450, 800)
        super().__init__(**kwargs)
        """dk = Image(source="0.png")
        dk.size = (2000, 2000)
        dk.pos
        self.add_widget(dk)"""
        self.card_list = []  # empty list of integers in the length of 36
        self.create_cards()
        self.deck = []  # list of cards that represents the deck
        self.create_deck()
        self.player = []  # list of cards that represents the players cards
        self.comp = []  # list of cards that represents the computers cards
        # | 0 - not set | 1 - heart | 2 - Spades | 3 - Clubs | 4 - Diamonds |
        self.koser = 0  # integer that represents the kind of the koser
        self.bottom_card = Card(0, 0)  # card that is flipped at the bottom of the deck (determines koser kind)
        self.distribute_cards()
        self.board = []  # list of cards that represents the cards on the board
        self.not_in_game = []  # cards that arent in the game
        self.run()

    def create_cards(self):  # creates random card deck
        for i in range(1, 4+1):
            for j in range(6, 9+6):
                self.card_list.append(Card(i, j))

    def create_deck(self):  # creates random card deck
        index_list = []
        for i in range(36):
            index_list.append(i)

        for i in range(36):
            x = random.randint(0, i)
            if not index_list[x] == 1000:
                self.deck.append(self.card_list[index_list[x]])
                index_list[x] = 1000

    def distribute_cards(self):  # distributes 6 cards to each player
        for i in range(6):
            self.player.append(self.deck[0])  # adding card to player
            if len(self.player) > 1:  # changing graphic characteristics
                self.player[-1].x = self.player[-2].x + 200
            self.add_widget(self.player[-1])
            self.deck.pop(0)  # removing the added card from the deck
            self.comp.append(self.deck[0])  # adding card to computer
            self.comp[0].y = 1225  # changing graphic characteristics
            self.comp[0].hide_cards()  # chiding the card in the ui
            self.comp[0].do_translation = False
            if len(self.comp) > 1:  # changing graphic characteristics
                self.comp[-1].x = self.comp[-2].x + 200
                self.comp[-1].y = 1225
                self.comp[-1].hide_cards()  # chiding the card in the ui
                self.comp[-1].do_translation = False
            self.add_widget(self.comp[-1])
            self.deck.pop(0)

            """self.add_widget(Place(450, 650))
            self.add_widget(Place(450, 425))
            #self.add_widget(Place(450, 800))
            self.add_widget(Place(450, 200))
            self.add_widget(Place(450, -25))
            self.add_widget(Place(450, 875))"""

        # adding and displaying the bottom card and the deck
        self.koser = self.deck[0].kind
        self.bottom_card = self.deck[0]
        self.deck.pop(0)
        self.bottom_card.do_translation = False
        self.deck.append(self.bottom_card)
        self.bottom_card.x = 2250
        self.bottom_card.y = 600
        self.bottom_card.rotation = 90
        self.add_widget(self.bottom_card)
        back_card = Card(0, 0)
        back_card.x = 2400
        back_card.y = 600
        back_card.do_translation = False
        self.add_widget(back_card)

    def move(self, cur_play, selected):  # executes the move that was made
        self.board.append(cur_play[selected])
        cur_play.pop(selected)

    def after_turn(self, cur_play):  # distributes cards after the turn so that everyone has 6 cards or deck is empty
        while len(cur_play) < 6 and len(self.deck) > 0:  # player card fill up
            cur_play.append(self.deck[0])
            self.deck.pop(0)

    def valid_move(self, selected, cur_play):  # checks to see if the move that was made by the player is valid
        if len(self.board) > 0 and len(cur_play) > 0 and selected >= 0:
            if cur_play[selected].kind == self.board[-1].kind:  # if the kind of the cards is the same
                if cur_play[selected].value > self.board[len(self.board)-1].value:  # defending card is higher in value
                    return True
                else:
                    return False
            elif cur_play[selected].kind == self.koser:  # if the card is a koser then it is better then a non koser
                return True
            else:
                return False
        else:
            return True

    def win(self):  # check if there is a winner
        if len(self.deck) == 0:
            if len(self.player) == 0:
                return True
            elif len(self.comp) == 0:
                return True
            else:
                return False

    def take(self, lis_play):
        while len(self.board):
            lis_play.append(self.board[0])
            self.board.pop(0)

    def bita(self):
        while len(self.board) > 0:
            self.not_in_game.append(self.board[0])
            self.board.pop(0)

    def find_move(self):  # returns the index of the card that the computer plays or -1 if there is no option to play
        min_card = 15
        tmp = -1
        for i in range(len(self.comp)):
            if self.comp[i].kind == self.board[len(self.board)-1].kind:
                if self.comp[i].value > self.board[len(self.board)-1].value:
                    if self.comp[i].value < min_card:
                        min_card = self.comp[i].value
                        tmp = i
        if min_card == 15 and not self.board[len(self.board) - 1].kind == self.koser:
            for i in range(len(self.comp)):
                if self.comp[i].kind == self.koser and self.comp[i].value < min_card:
                    min_card = self.comp[i].value
                    tmp = i
        return tmp

    def run(self):  # runs the game
        selected = 0
        player_turn = True
        attacker = True
        while not self.win():  # runs the game until someone wins
            if player_turn:  # players turn
                self.move(self.player, selected)
                self.valid_move(selected, self.player)
                self.after_turn(self.player)

            else:  # computers turn
                selected = self.find_move()
                if selected == -1 and attacker:  # if the computer does not have an available move
                    self.take(self.comp)
                elif selected == -1 and not attacker:  # the comp does not have an available move and turn is finished
                    self.bita()
                else:
                    self.move(self.comp, selected)
                    self.valid_move(selected, self.comp)
                    self.after_turn(self.comp)


class DurakApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    DurakApp().run()
