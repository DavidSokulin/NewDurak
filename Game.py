import random
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from Card import Card
from kivy.core.window import Window
from kivy.app import App


class Game(Layout):
    def __init__(self, **kwargs):
        Window.system_size = (1450, 800)
        super().__init__(**kwargs)
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
        self.set_koser()
        self.update_loc(self.player, 50)
        self.update_loc(self.comp, 1225)
        self.board = []  # list of cards that represents the cards on the board
        self.not_in_game = []  # cards that arent in the game
        self.create_buttons()
        self.upd = False  # has already been updated
        self.call_count = 0   # number of time the update function has been called in the past turn
        #self.run()
        print()

    def create_buttons(self):
        bit = Button(text='Bita', font_size=50)
        bit.x = 250
        bit.y = 575
        bit.color = (1, 1, 1, 1)
        bit.background_color = (0, 0, 0, 0)
        tk = Button(text='Take', font_size=50)
        tk.x = 250
        tk.y = 775
        tk.color = (1, 1, 1, 1)
        tk.background_color = (0, 0, 0, 0)
        bit.bind(on_press=self.bita)
        tk.bind(on_press=self.take_pl)
        self.add_widget(bit)
        self.add_widget(tk)

    def create_cards(self):  # creates random card deck
        for i in range(1, 4+1):
            for j in range(6, 9+6):
                self.card_list.append(Card(i, j))

    def create_deck(self):  # creates random card deck
        index_list = []
        for i in range(36):
            index_list.append(i)

        for i in range(36):
            x = random.randint(0, 35)
            while index_list[x] == 1000:
                x = random.randint(0, 35)
            self.deck.append(self.card_list[index_list[x]])
            index_list[x] = 1000

    def distribute_cards(self):  # distributes 6 cards to each player
        self.comp.append(self.deck[0])  # adding card to computer
        self.comp[0].comp_card(1225)
        self.add_widget(self.comp[0])
        self.comp[0].index = 0
        self.comp[0].origin = 3
        self.deck.pop(0)  # removing the added card from the deck

        self.player.append(self.deck[0])  # adding card to player
        self.add_widget(self.player[0])
        self.player[0].index = 0
        self.player[-1].origin = 1
        self.deck.pop(0)  # removing the added card from the deck

        for i in range(1, 6):
            self.player.append(self.deck[0])  # adding card to player
            self.player[-1].x = self.player[-2].x + 200
            self.player[-1].index = i
            self.player[-1].origin = 1
            self.add_widget(self.player[-1])
            self.deck.pop(0)  # removing the added card from the deck

            self.comp.append(self.deck[0])  # adding card to computer
            self.comp[-1].x = self.comp[-2].x + 200
            self.comp[-1].comp_card(1225)
            self.comp[-1].index = i
            self.comp[-1].origin = 3
            self.add_widget(self.comp[-1])
            self.deck.pop(0)

    def set_koser(self):
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

    def update_lists(self, org_list, new_list, index):
        new_list.append(org_list.pop(index))
        self.update_index(new_list)
        self.update_index(org_list)
        if len(org_list) > 0:
            if org_list[0].y == 50:
                org_origin = 1
            elif org_list[0].y == 600:
                org_origin = 2
            elif org_list[0].y == 1225:
                org_origin = 3
        else:
            if new_list[0].origin == 1:
                org_origin = 2
            else:
                org_origin = 1
        if len(new_list) > 1:
            if new_list[0].y == 50:
                new_origin = 1
            elif new_list[0].y == 600:
                new_origin = 2
            elif new_list[0].y == 1225:
                new_origin = 3
        else:
            if org_origin == 1:
                new_origin = 2
            else:
                new_origin = 1
        self.update_origin(org_list, org_origin)
        self.update_origin(new_list, new_origin)

    def update_origin(self, list, origin):
        for i in range(len(list)):
            list[i].origin = origin

    def update_index(self, list):
        for i in range(len(list)):
            list[i].index = i

    def update(self, org_list, new_list, index, org_y, dest_y):
        self.call_count = self.call_count + 1
        if len(org_list) > index:
            self.update_lists(org_list, new_list, index)
            if len(org_list):
                self.update_loc(org_list, org_y)
            new_list[-1].y = dest_y
            self.update_loc(new_list, dest_y)
            self.upd = True
        if self.call_count == 2:
            self.call_count = 0
            self.upd = False

    def update_loc(self, list, cor_y):
        first_c = self.distance_between(len(list))
        for i in range(len(list)):
            list[i].y = cor_y
            list[i].x = first_c + i * 200

    def distance_between(self, length):
        if length > 0:
            starting_x = 0
            end_x = int(2550)
            mid = int(end_x / 2)
            max_dist = int(200)
            dist = int(end_x - starting_x)
            dist = int(dist / length)
            if dist < max_dist:
                f_dist = int(dist)
            else:
                f_dist = int(max_dist)
            if int(length) % 2 == 0:
                mid = mid + f_dist / 2
            first_c = mid - f_dist * int(length / 2)
        else:
            end_x = int(2550)
            mid = int(end_x / 2)
            first_c = mid
        return first_c

    """def update(self, list, layer):
        length = len(list)
        if length > 0:
            starting_x = 0
            end_x = int(2550)
            mid = int(end_x/2)
            max_dist = int(200)
            dist = int(end_x - starting_x)
            dist = int(dist / length)
            if dist < max_dist:
                f_dist = int(dist)
            else:
                f_dist = int(max_dist)
            if int(length) % 2 == 0:
                mid = mid + f_dist/2
            first_c = mid - f_dist * int(length/2)

            if layer == 1:
                loc_y = 50
            elif layer == 2:
                loc_y = 600
            else:
                loc_y = 1225
            i = 0
            while i < length:
                list[i].x = first_c + i * f_dist
                print("Before" + str(list[i].x))
                if list[i].y != 50 and list[i].y != 600 and list[i].y != 1225:
                    list[i].y = loc_y
                    if layer == 2:
                        self.board.append(list[i])
                    elif layer == 1:
                        self.player.append(list[i])
                    elif layer == 3:
                        self.comp.append(list[i])
                    print("After" + str(list[i].x))
                    list.pop(i)
                length = len(list)
                i = i + 1
            #def update_board(slef):
        #elif layer == 1:"""

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

    def take_pl(self, touch):
        while len(self.board):
            self.player.append(self.board[0])
            self.board.pop(0)

    def take_cp(self):
        while len(self.board):
            self.comp.append(self.board[0])
            self.board.pop(0)

    def bita(self, touch):
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
                    self.bita(1)
                else:
                    self.move(self.comp, selected)
                    self.valid_move(selected, self.comp)
                    self.after_turn(self.comp)


class DurakApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    DurakApp().run()
