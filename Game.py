import random
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from Card import Card
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock


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
        self.back_card = Card(0, 0)
        self.distribute_cards()
        self.set_koser()
        self.update_loc(self.player, 50)
        self.update_loc(self.comp, 1225)
        self.board = []  # list of cards that represents the cards on the board
        self.not_in_game = []  # cards that arent in the game
        self.create_buttons()
        self.upd = False  # has already been updated
        self.call_count = 0   # number of time the update function has been called in the past turn
        self.turn = True  # | True - player | False - computer |
        self.attacker = True  # | True - player | False - computer |
        self.adding = False  # allows the player to add cards after the computer has chosen to take the cards
        self.max_attack = 6
        self.added = 0
        self.game_starter()

    def create_buttons(self):
        bit = Button(text='Bita', font_size=45)
        bit.x = 250
        bit.y = 575
        bit.color = (0, 0, 0, 1)
        bit.background_normal = "Images/Green.png"
        bit.size = (150, 150)
        bit.border = (0, 0, 0, 0)
        tk = Button(text='Take', font_size=45)
        tk.x = 250
        tk.y = 815
        tk.color = (0, 0, 0, 1)
        tk.background_normal = "Images/Red.png"
        tk.size = (150, 150)
        bit.bind(on_press=self.bita_ply)
        tk.bind(on_press=self.take_ply)
        tk.border = (0, 0, 0, 0)
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
        self.back_card.x = 2400
        self.back_card.y = 600
        self.back_card.do_translation = False
        self.add_widget(self.back_card)
        self.disp_koser()

    def disp_koser(self):
        if self.koser == 1:
            koser_icon = Image(source="Images/Heart.png")
        elif self.koser == 2:
            koser_icon = Image(source="Images/Spade.png")
        elif self.koser == 3:
            koser_icon = Image(source="Images/Club.png")
        else:
            koser_icon = Image(source="Images/Diamond.png")
        koser_icon.x = 2510
        # koser_icon.y = 915
        koser_icon.y = 950
        koser_icon.opacity = 0.75
        self.add_widget(koser_icon)

    def game_starter(self):
        if not self.first_attacker():
            self.popup_comp_first()
            self.turn = False
            self.attacker = False
            self.run()
        else:
            self.popup_player_first()

    def first_attacker(self):
        lowest = 15
        tr_pl = True
        for i in range(6):
            if self.player[i].kind == self.koser:
                if self.player[i].value < lowest:
                    lowest = self.player[i].value
                    tr_pl = True
            if self.comp[i].kind == self.koser:
                if self.comp[i].value < lowest:
                    lowest = self.comp[i].value
                    tr_pl = False
        return tr_pl

    def move(self, cur_play, selected):  # executes the move that was made
        self.board.append(cur_play.pop(selected))
        self.board[-1].y = 600
        self.board[-1].origin = 2
        self.board[-1].index = len(self.board) - 1
        self.board[-1].unhide_cards()
        self.update_all_loc()

    def after_turn(self):  # distributes cards after the turn so that everyone has 6 cards or deck is empty
        if not self.turn:
            while len(self.player) < 6 and len(self.deck) > 1:  # player card fill up
                self.player.append(self.deck.pop(0))
                self.player[-1].y = 50
                self.player[-1].unhide_cards()
                self.player[-1].origin = 1
                self.player[-1].do_translation = True
                self.add_widget(self.player[-1])
            while len(self.comp) < 6 and len(self.deck) > 1:
                self.comp.append(self.deck.pop(0))
                self.comp[-1].y = 1225
                self.comp[-1].hide_cards()
                self.comp[-1].origin = 3
                self.add_widget(self.comp[-1])
            if len(self.player) < 6 and len(self.deck) == 1:
                self.player.append(self.deck.pop(0))
                self.player[-1].y = 50
                self.player[-1].unhide_cards()
                self.player[-1].origin = 1
                self.player[-1].do_translation = True
                self.player[-1].rotation = 0
                self.remove_widget(self.back_card)

            elif len(self.comp) < 6 and len(self.deck) == 1:
                self.comp.append(self.deck.pop(0))
                self.comp[-1].y = 1225
                self.comp[-1].hide_cards()
                self.comp[-1].origin = 3
                self.comp[-1].rotation = 0
                self.remove_widget(self.back_card)

        else:
            while len(self.comp) < 6 and len(self.deck) > 1:  # computer card fill up
                self.comp.append(self.deck.pop(0))
                self.comp[-1].y = 1225
                self.comp[-1].hide_cards()
                self.comp[-1].origin = 3
                self.add_widget(self.comp[-1])
            while len(self.player) < 6 and len(self.deck) > 1:
                self.player.append(self.deck.pop(0))
                self.player[-1].y = 50
                self.player[-1].unhide_cards()
                self.player[-1].origin = 1
                self.player[-1].do_translation = True
                self.add_widget(self.player[-1])

            if len(self.comp) < 6 and len(self.deck) == 1:
                self.comp.append(self.deck.pop(0))
                self.comp[-1].y = 1225
                self.comp[-1].hide_cards()
                self.comp[-1].origin = 3
                self.comp[-1].rotation = 0
                self.remove_widget(self.back_card)

            elif len(self.player) < 6 and len(self.deck) == 1:
                self.player.append(self.deck.pop(0))
                self.player[-1].y = 50
                self.player[-1].unhide_cards()
                self.player[-1].origin = 1
                self.player[-1].do_translation = True
                self.player[-1].rotation = 0
                self.remove_widget(self.back_card)

        self.update_loc(self.player, 50)
        self.update_loc(self.comp, 1225)

    def update_all_loc(self):
        self.update_loc(self.player, 50)
        self.update_board_loc()
        self.update_loc(self.comp, 1225)
        self.hide_comp()

    def hide_comp(self):
        for i in range(len(self.comp)):
            self.comp[i].hide_cards()

    def update_lists(self, org_list, new_list, index):  # updates the lists accordingly
        new_list.append(org_list.pop(index))
        self.update_index(new_list)
        self.update_index(org_list)
        if len(org_list) > 0:
            if org_list[0].y == 50:
                org_origin = 1
            elif org_list[0].y == 600 or org_list[0].y == 650 and org_list[0].y == 550:
                org_origin = 2
            elif org_list[0].y == 1225:
                org_origin = 3
            else:
                org_origin = 0
        else:
            if new_list[0].origin == 1:
                org_origin = 2
            else:
                org_origin = 1
        if len(new_list) > 1:
            if new_list[0].y == 50:
                new_origin = 1
            elif new_list[0].y == 600 or new_list[0].y == 650 or new_list[0].y == 550:
                new_origin = 2
            elif new_list[0].y == 1225:
                new_origin = 3
            else:
                new_origin = 0
        else:
            if org_origin == 1:
                new_origin = 2
            else:
                new_origin = 1
        self.update_origin(org_list, org_origin)
        self.update_origin(new_list, new_origin)

    @staticmethod
    def update_origin(lis, origin):
        for i in range(len(lis)):
            lis[i].origin = origin

    @staticmethod
    def update_index(lis):
        for i in range(len(lis)):
            lis[i].index = i

    def update(self, org_list, new_list, index, org_y, dest_y):
        if len(org_list) > index:
            self.update_lists(org_list, new_list, index)
            if len(org_list):
                self.update_loc(org_list, org_y)
            new_list[-1].y = dest_y
            self.update_loc(new_list, dest_y)

    def update_loc(self, lis, cor_y):
        if len(lis) > 0:
            first_c = self.first_card_loc(len(lis))
            dist = self.distance(len(lis))
            for i in range(len(lis)):
                lis[i].y = cor_y
                lis[i].x = first_c + i * dist
                self.remove_widget(lis[i])
                self.add_widget(lis[i])

    def update_board_loc(self):
        length = len(self.board)
        if length > 0:
            dist = 250
            pairs = length / 2
            if length % 2 != 0:
                pairs = pairs + 1
            starting_x = self.first_card_loc(pairs)
            for i in range(length):
                if i % 2 == 0:
                    self.board[i].x = starting_x + dist * int(i/2)
                    self.board[i].y = 650
                    self.board[i].origin = 2
                else:
                    self.board[i].x = starting_x + dist * int(i/2)
                    self.board[i].y = 550
                    self.board[i].origin = 2
                    self.remove_widget(self.board[i])
                    self.add_widget(self.board[i])

    def first_card_loc(self, length):
        if length > 0:
            end_x = int(2550)
            mid = int(end_x / 2)
            f_dist = self.distance(length)
            if int(length) % 2 == 0:
                mid = mid + f_dist / 2
            first_c = mid - f_dist * int(length / 2)
        else:
            end_x = int(2550)
            mid = int(end_x / 2)
            first_c = mid
        return first_c

    @staticmethod
    def distance(length):
        starting_x = 0
        end_x = int(2550)
        max_dist = int(210)
        dist = int(end_x - starting_x)
        dist = int(dist / length)
        if dist < max_dist:
            f_dist = int(dist)
        else:
            f_dist = int(max_dist)
        return f_dist

    def win(self):  # check if there is a winner | 0 - no winner | 1 - player won | 2 - computer won |
        if len(self.deck) == 0:
            if len(self.player) == 0:
                return 1
            elif len(self.comp) == 0:
                return 2
            else:
                return 0
        else:
            return 0

    def take_ply(self, touch):
        if not self.attacker:
            self.take(self.player, True, False)
            self.update_loc(self.player, 50)
            self.turn = False
            self.attacker = False
            self.after_turn()
            self.run()
        else:
            self.popup_invalid()

    def take(self, lis, pl, bit):
        if pl:  # allows the computer to add cards after the player has choosen to take
            selected = self.find_move()
            while selected != -1:
                self.move(self.comp, selected)
                self.update_all_loc()
                selected = self.find_move()
        elif not bit:
            self.instructions_popup()
            self.adding = True
            return
        elif bit:
            self.adding = False

        while len(self.board):
            lis.append(self.board.pop(0))
            lis[-1].origin = 1
            lis[-1].y = 1225
            if pl:
                lis[-1].do_translation = True
            else:
                lis[-1].hide_cards()
        if not pl:
            self.comp_take_popup()

        self.update_index(lis)
        self.update_loc(lis, 1225)
        self.after_turn()

        self.max_attack = len(self.comp)
        if len(self.player) < self.max_attack:
            self.max_attack = len(self.player)
        if self.max_attack > 6:
            self.max_attack = 6

    def bita_ply(self, touch):
        if self.attacker and self.adding:
            self.take(self.comp, False, True)
            self.added = 0
        elif self.attacker and not self.adding:
            self.bita()
        else:
            self.popup_invalid()

    def bita(self):
        if len(self.not_in_game) == 0 and len(self.board) > 0:
            self.not_in_game.append(self.board.pop(0))
            self.not_in_game[-1].y = 1100
            self.not_in_game[-1].x = 50
            self.not_in_game[-1].hide_cards()

        while len(self.board) > 0:
            self.not_in_game.append(self.board.pop(0))
            self.remove_widget(self.not_in_game[-1])

        if self.turn:
            self.turn = False
        else:
            self.turn = True

        if self.attacker:
            self.attacker = False
        else:
            self.attacker = True

        self.after_turn()

        self.max_attack = len(self.comp)
        if len(self.player) < self.max_attack:
            self.max_attack = len(self.player)
        if self.max_attack > 6:
            self.max_attack = 6

        if not self.attacker and not self.turn:
            self.run()

    def find_move(self):  # returns the index of the card that the computer plays or -1 if there is no option to play
        min_card = 15
        tmp = -1
        if self.attacker:
            for i in range(len(self.comp)):
                if self.comp[i].kind == self.board[-1].kind:
                    if self.comp[i].value > self.board[-1].value:
                        if self.comp[i].value < min_card:
                            min_card = self.comp[i].value
                            tmp = i
            if min_card == 15 and not self.board[-1].kind == self.koser:
                for i in range(len(self.comp)):
                    if self.comp[i].kind == self.koser and self.comp[i].value < min_card:
                        min_card = self.comp[i].value
                        tmp = i
        else:
            if len(self.board) == 0:
                for i in range(len(self.comp)):
                    if not self.comp[i].kind == self.koser:
                        if self.comp[i].value < min_card:
                            min_card = self.comp[i].value
                            tmp = i
                if tmp == -1:
                    for i in range(len(self.comp)):
                        if self.comp[i].value < min_card:
                            min_card = self.comp[i].value
                            tmp = i
            else:
                for i in range(len(self.comp)):
                    for j in range(len(self.board)):
                        if self.comp[i].value == self.board[j].value:
                            if self.comp[i].value < min_card:
                                min_card = self.comp[i].value
                                tmp = i
        return tmp

    def legal(self):
        if len(self.board) <= 12 and not self.adding:
            if len(self.board) == 1:
                return True
            elif len(self.board) % 2 == 0 and len(self.board) > 0:
                if self.board[-1].kind == self.board[-2].kind:
                    if self.board[-1].value > self.board[-2].value:
                        return True
                    else:
                        return False
                else:
                    if self.board[-1].kind == self.koser:
                        return True
                    else:
                        return False
            else:
                if len(self.board) > 0:
                    for i in range(len(self.board) - 1):
                        if self.board[-1].value == self.board[i].value:
                            return True
                    return False
                else:
                    return True
        elif self.adding:
            if len(self.board) > 0:
                if int((len(self.board) - self.added) / 2) + self.added + 1 <= self.max_attack:
                    for i in range(len(self.board) - 1):
                        if self.board[-1].value == self.board[i].value:
                            return True
                else:
                    print("!")
                return False

        else:
            return False

    def revert(self, lis, origin):
        if len(self.board) > 0:
            lis.append(self.board.pop(-1))
            lis[-1].index = len(lis) - 1
            lis[-1].origin = origin
            self.update_all_loc()
            if self.adding:
                self.added = self.added - 1

    @staticmethod
    def popup_invalid():

        print("Not a valid move, please try again")
        popup = Popup(title='                       Not a valid move',
                      content=Label(text='Not a valid move, please try again'),
                      size_hint=(None, None),
                      pos_hint={'right': .6, 'bottom': 1},
                      size=(600, 200))
        popup.open()
        Clock.schedule_once(popup.dismiss, 1.5)

    @staticmethod
    def popup_comp_first():
        print("The computer is making the first move")
        popup = Popup(title='                          The computer goes first',
                      content=Label(text='    He has the lowest Koser'),
                      size_hint=(None, None),
                      pos_hint={'right': .6, 'bottom': 1},
                      size=(600, 200))
        popup.open()
        Clock.schedule_once(popup.dismiss, 5)

    @staticmethod
    def popup_player_first():
        print("The computer is making the first move")
        popup = Popup(title='                           You go first',
                      content=Label(text='   You have the lowest Koser'),
                      size_hint=(None, None),
                      pos_hint={'right': .6, 'bottom': 1},
                      size=(600, 200))
        Clock.schedule_once(popup.open, 2)
        Clock.schedule_once(popup.dismiss, 5)

    @staticmethod
    def comp_take_popup():
        print("The computer took all the cards from the board")
        popup = Popup(title='                                  Take',
                      content=Label(text='   Computer choose to take'),
                      size_hint=(None, None),
                      pos_hint={'right': .6, 'bottom': 1},
                      size=(600, 200))
        Clock.schedule_once(popup.open, 5)
        Clock.schedule_once(popup.dismiss, 4)

    @staticmethod
    def comp_bita_popup():
        print("Computer choose bita")
        popup = Popup(title='                                  Bita',
                      content=Label(text='  Computer choose Bita'),
                      size_hint=(None, None),
                      pos_hint={'right': .6, 'bottom': 1},
                      size=(600, 200))
        popup.open()
        Clock.schedule_once(popup.dismiss, 1.5)

    @staticmethod
    def instructions_popup():
        print("Add cards as you like and press Bita when you are done ")
        popup = Popup(title='                                                Add cards',
                      content=Label(text='Add cards as you like and press Bita when you are done '),
                      size_hint=(None, None),
                      pos_hint={'right': .65, 'bottom': 0.5},
                      size=(900, 200))
        popup.open()
        Clock.schedule_once(popup.dismiss, 4.5)

    @staticmethod
    def comp_durak():
        print("Computer is the Durak")
        popup = Popup(title='                             Game over',
                      content=Label(text='   Computer is the Durak'),
                      size_hint=(None, None),
                      pos_hint={'right': .6, 'bottom': 1},
                      size=(600, 200))
        popup.open()
        Clock.schedule_once(exit, 7.5)

    @staticmethod
    def player_durak():
        print("Player is the Durak")
        popup = Popup(title='                             Game over',
                      content=Label(text='   Player is the Durak'),
                      size_hint=(None, None),
                      pos_hint={'right': .6, 'bottom': 1},
                      size=(600, 200))
        popup.open()
        Clock.schedule_once(exit, 7.5)

    @staticmethod
    def find_y_by_origin(origin):
        if origin == 1:
            return 50
        elif origin == 2:
            return 600
        elif origin == 3:
            return 1225

    def computer(self):
        selected = self.find_move()
        if selected == -1 and self.attacker:  # if the computer does not have an available move
            self.take(self.comp, False, False)
            self.update_loc(self.comp, 1225)

        elif selected == -1 and not self.attacker:  # the comp does not have an available move and turn is finished
            self.bita()
            self.update_loc(self.comp, 1225)

        else:
            self.move(self.comp, selected)
            while not self.legal():
                self.revert(self.comp, 3)
                print("Not a valid move please try again")
            self.update_all_loc()

    def run(self):  # runs the game
        if self.win() == 0:
            if self.adding:
                self.added = self.added + 1
            if self.turn:  # players turn
                if not self.legal():
                    self.popup_invalid()
                    self.revert(self.player, 1)
                else:
                    self.computer()
                    self.update_all_loc()

            elif not self.adding:  # computers turn
                if not self.legal():
                    self.revert(self.player, 1)
                    self.popup_invalid()
                    return
                selected = self.find_move()
                if selected == -1 and self.attacker:  # if the computer does not have an available move
                    self.take(self.comp, False, False)
                    self.update_all_loc()
                elif selected == -1 and not self.attacker:  # the comp does not have an available move and turn is over
                    self.bita()
                    self.comp_bita_popup()
                    self.attacker = True
                    self.turn = True
                    self.update_all_loc()
                else:
                    self.move(self.comp, selected)
                    while not self.legal():
                        self.revert(self.comp, 3)
                        self.popup_invalid()
        won = self.win()
        if won == 1:
            self.comp_durak()
        if won == 2:
            self.player_durak()


class DurakApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    DurakApp().run()
