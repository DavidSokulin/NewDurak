import random
from kivy.uix.layout import Layout
from kivy.uix.button import Button
from Card import Card
from EarlyGame import EarlyGame
from MinMax import AI
from State import State
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
        self.board = []  # list of cards that represents the cards on the board
        self.not_in_game = []  # cards that arent in the game
        self.update_all_loc()
        self.create_buttons()
        self.create_instructions_button()
        self.upd = False  # has already been updated
        self.call_count = 0   # number of time the update function has been called in the past turn
        self.turn = True  # | True - player | False - computer |
        self.attacker = True  # | True - player | False - computer |
        self.adding = False  # allows the player to add cards after the computer has chosen to take the cards
        self.max_attack = 6
        self.added = 0
        self.game_starter()

    def create_buttons(self):
        # Creates two buttons - Bita and take, they are displayed on the left side of the screen
        bit = Button(text='Bita', font_size=45)
        bit.x = 250  # x coordinate of the button
        bit.y = 575  # y coordinate of the button
        bit.color = (0, 0, 0, 1)  # color of the button
        bit.background_normal = "Images/Green.png"  # Green Bita button
        bit.size = (150, 150)  # size of the button
        bit.border = (0, 0, 0, 0)  # Fix for bug in kivy that distorts the image if border isn't set this way
        tk = Button(text='Take', font_size=45)  # Take button
        tk.x = 250
        tk.y = 815
        tk.color = (0, 0, 0, 1)
        tk.background_normal = "Images/Red.png"  # Red Take button
        tk.size = (150, 150)
        bit.bind(on_press=self.bita_ply)
        tk.bind(on_press=self.take_ply)
        tk.border = (0, 0, 0, 0)  # Fix for bug in kivy that distorts the image if border isn't set this way
        self.add_widget(bit)
        self.add_widget(tk)

    def create_instructions_button(self):
        # Creates two buttons - Bita and take, they are displayed on the left side of the screen
        inst = Button(text='Instructions', font_size=20)
        inst.x = 2490  # x coordinate of the button
        inst.y = 1300  # y coordinate of the button
        inst.color = (0, 0, 0, 1)  # color of the button
        inst.background_normal = "Images/Red.png"  # Green Bita button
        inst.size = (150, 150)  # size of the button
        inst.border = (0, 0, 0, 0)  # Fix for bug in kivy that distorts the image if border isn't set this way
        inst.bind(on_press=self.popup_start)
        self.add_widget(inst)

    def create_cards(self):  # creates 36 cards (all the cards that will be used in the game)
        for i in range(1, 4+1):  # goes throw each kind of cards that there is from 1 to 4
            for j in range(6, 9+6):  # goes throw each value of cards that there is from 6 to 14
                self.card_list.append(Card(i, j))

    def create_deck(self):  # creates random card deck
        index_list = []
        for i in range(36):  # creating a index list that is used to randomize the card deck
            index_list.append(False)

        for i in range(36):  # creating a randomized card deck
            x = random.randint(0, 35)  # random number between 0 and 35 for the index list
            while index_list[x]:  # finds a index that hasn't been used yet
                x = random.randint(0, 35)
            self.deck.append(self.card_list[x])  # adds the random card to the deck
            index_list[x] = True  # marking the index as used

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
            self.player[-1].index = i
            self.player[-1].origin = 1
            self.add_widget(self.player[-1])
            self.deck.pop(0)  # removing the added card from the deck

            self.comp.append(self.deck[0])  # adding card to computer
            self.comp[-1].comp_card(1225)
            self.comp[-1].index = i
            self.comp[-1].origin = 3
            self.add_widget(self.comp[-1])
            self.deck.pop(0)  # removing the added card from the deck

    def set_koser(self):
        # adding and displaying the bottom (Koser) card and the deck
        self.koser = self.deck[0].kind  # extracting the Koser
        self.bottom_card = self.deck[0]
        self.deck.pop(0)  # removing card from the deck
        self.deck.append(self.bottom_card)  # adding the Koser back to the end of the deck as the last card

        # Graphical aspects for the bottom card (Koser)
        self.bottom_card.x = 2250
        self.bottom_card.y = 600
        self.bottom_card.rotation = 90
        self.bottom_card.do_translation = False
        self.add_widget(self.bottom_card)

        # Graphical aspects for the deck
        self.back_card.x = 2400
        self.back_card.y = 600
        self.back_card.do_translation = False
        self.add_widget(self.back_card)
        self.disp_koser()  # Displaying the current Koser above the deck

    def disp_koser(self):
        # Displays the current Koser above the deck so that the player will know what the koser is throughout the game
        # Choosing what Koser to display
        if self.koser == 1:
            koser_icon = Image(source="Images/Heart.png")
        elif self.koser == 2:
            koser_icon = Image(source="Images/Spade.png")
        elif self.koser == 3:
            koser_icon = Image(source="Images/Club.png")
        else:
            koser_icon = Image(source="Images/Diamond.png")

        # Graphical aspects for the Koser icon
        koser_icon.x = 2510
        koser_icon.y = 950
        koser_icon.opacity = 0.75
        self.add_widget(koser_icon)

    def game_starter(self):
        # starts the game by deciding who goes first
        if not self.first_attacker():  # if the function returns that the computer goes first
            self.popup_comp_first()
            self.turn = False
            self.attacker = False
            self.run()
        else:
            self.popup_player_first()

    def first_attacker(self):
        # Checks who should start the game by finding the player with lowest Koser
        lowest = 15
        tr_pl = True  # | True - player goes first | False - Computer goes first |
        for i in range(6):  # checks all the player and computer cards to find lowest Koser
            if self.player[i].kind == self.koser:
                if self.player[i].value < lowest:
                    lowest = self.player[i].value
                    tr_pl = True
            if self.comp[i].kind == self.koser:
                if self.comp[i].value < lowest:
                    lowest = self.comp[i].value
                    tr_pl = False
        return tr_pl

    def move(self, cur_play, selected):  # executes the move that was chosen
        self.board.append(cur_play.pop(selected))  # adds the card to the board
        self.board[-1].origin = 2
        self.board[-1].index = len(self.board) - 1
        self.board[-1].unhide_cards()  # makes the card visible to the player
        self.update_all_loc()

    def after_turn(self):  # Distribute cards after the turn so that everyone has at least 6 cards or deck is empty
        if not self.attacker:  # If the player should receive the cards first
            self.player_after_turn()
        else:
            self.comp_after_turn()

        self.max_attack_update()
        self.update_all_loc()

    def comp_after_turn(self):  # Distribute cards after the turn so that everyone has at least 6 cards or deck is empty
        while len(self.comp) < 6 and len(self.deck) > 1:  # computer first card fill up
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

    def player_after_turn(self):  # Distribute cards after the turn so that everyone has at least 6 cards or deck is empty
        while len(self.player) < 6 and len(self.deck) > 1:  # player first card fill up
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

    def update_all_loc(self):
        # updates all the cards location on the board
        self.sort()
        self.hide_comp()
        self.update_loc(self.player, 50)
        self.update_board_loc()
        self.update_loc(self.comp, 1225)

    def sort(self):  # sorts the cards so that they appear in ascending order
        self.player.sort(key=lambda x: x.value)
        self.comp.sort(key=lambda x: x.value)
        self.update_index(self.player)
        self.update_index(self.comp)

    def hide_comp(self):  # hides all the computers cards so that the player doesn't see them
        for i in range(len(self.comp)):
            self.comp[i].hide_cards()

    def update_lists(self, org_list, new_list, index):  # updates the lists accordingly
        new_list.append(org_list.pop(index))
        # updating all the indexes
        self.update_index(new_list)
        self.update_index(org_list)
        if len(org_list) > 0:
            org_origin = self.find_origin_by_y(org_list[0].y)
        else:
            if new_list[0].origin == 1:
                org_origin = 2
            else:
                org_origin = 1
        if len(new_list) > 1:
            new_origin = self.find_origin_by_y(new_list[0].y)
        else:
            if org_origin == 1:
                new_origin = 2
            else:
                new_origin = 1

        # update all the origins
        self.update_origin(org_list, org_origin)
        self.update_origin(new_list, new_origin)

    @staticmethod
    def update_origin(lis, origin):  # updates the origin of a whole list
        for i in range(len(lis)):
            lis[i].origin = origin

    @staticmethod
    def update_index(lis):  # updates all the indexes of the list
        for i in range(len(lis)):
            lis[i].index = i

    def update(self, org_list, new_list, index, org_y):  # updates everything that needs to be updated
        dest_y = self.find_y_by_origin(2, len(self.board)+1)
        if len(org_list) > index:
            self.update_lists(org_list, new_list, index)
            if len(org_list):
                self.update_loc(org_list, org_y)
            new_list[-1].y = dest_y
            self.update_loc(new_list, dest_y)

    def update_loc(self, lis, cor_y):  # updates location for player or computer
        if len(lis) > 0:
            first_c = self.first_card_loc(len(lis))
            dist = self.distance(len(lis))
            for i in range(len(lis)):
                lis[i].y = cor_y
                lis[i].x = first_c + i * dist
                self.remove_widget(lis[i])
                self.add_widget(lis[i])

    def update_board_loc(self):  # updates card location for the board
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

    def first_card_loc(self, length):  # finds where the first card should go
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
    def distance(length):  # finds the distance that should be between each card
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

    def take_ply(self, touch):  # tied to the take button so only the player can call this function
        if not self.attacker:  # checks to see if the move the player is making is valid
            self.take(self.player, True, False)
            self.turn = False
            self.attacker = False
            self.after_turn()
            self.run()
        else:
            self.popup_invalid()

    def take(self, lis, pl, bit):
        if pl:  # allows the computer to add cards after the player has chosen to take
            selected = self.find_move()  # finds a card to add
            while selected != -1:  # adds cards as long as it has more to add
                self.move(self.comp, selected)
                selected = self.find_move()
            self.update_all_loc()
        elif not bit:  # if the computer chooses to take, so this allows the player to add cards
            self.instructions_popup()
            self.adding = True
            return
        elif bit:
            self.adding = False

        while len(self.board):  # moves all the cards to the player that took the cards
            lis.append(self.board.pop(0))
            if pl:
                lis[-1].origin = 1
                lis[-1].do_translation = True
            else:
                lis[-1].origin = 3
                lis[-1].hide_cards()

        self.update_index(lis)
        self.after_turn()

    def max_attack_update(self):  # updates the max attack value
        self.max_attack = len(self.comp)
        if len(self.player) < self.max_attack:
            self.max_attack = len(self.player)
        if self.max_attack > 6:
            self.max_attack = 6

    def bita_ply(self, touch):  # tied to the Bita button so only the player can call this function
        if self.attacker and self.adding:  # if the computer decided to take and the player finished adding cards
            self.take(self.comp, False, True)
            self.added = 0
        elif self.attacker and not self.adding:  # if the player decides to Bita
            self.bita()
        else:
            self.popup_invalid()

    def bita(self):
        # creates the not in game card graphical side
        if len(self.not_in_game) == 0 and len(self.board) > 0:
            self.not_in_game.append(self.board.pop(0))
            self.not_in_game[-1].y = 1100
            self.not_in_game[-1].x = 50
            self.not_in_game[-1].hide_cards()

        # removes the cards from the board and moves them to the not in game deck
        while len(self.board) > 0:
            self.not_in_game.append(self.board.pop(0))
            self.remove_widget(self.not_in_game[-1])

        self.change_turn()
        self.after_turn()
        self.max_attack_update()

        if not self.attacker and not self.turn:
            self.run()

    def change_turn(self):  # changes the turn
        if self.turn:
            self.turn = False
        else:
            self.turn = True

        if self.attacker:
            self.attacker = False
        else:
            self.attacker = True

    def find_move(self):  # returns the index of the card that the computer plays or -1 if there is no option to play
        current_state = State(self.board, self.player, self.comp, self.not_in_game, self.deck,
                              self.turn, self.attacker, self.koser, self.bottom_card)
        if len(self.deck) > 0:
            best_move = EarlyGame(current_state)
            index = -1
            if best_move.best_move[0] == -1:
                self.bita()
            elif best_move.best_move[0] == -2:
                self.take(self.comp, False, True)
            else:
                index = best_move.best_move[1]
            return index
        else:
            best_move = AI.minimax(current_state, 15)
            index = -1
            if best_move.index == -1:
                self.bita()
            elif best_move.index == -2:
                self.take(self.comp, False, True)
            else:
                index = best_move.index
            return index

    def legal(self):
        # checks to see if the move that was made is legal by the game rules
        if len(self.board) == 0:
            return True

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
                return False
            else:
                return True
        else:
            return False

    def revert(self, lis, origin):
        # reverts the players move by undoing it
        if len(self.board) > 0:
            lis.append(self.board.pop(-1))
            lis[-1].index = len(lis) - 1
            lis[-1].origin = origin
            self.update_all_loc()
            if self.adding:
                self.added = self.added - 1

    @staticmethod
    def popup_start(touch):

        popup = Popup(title='Instructions',
                      content=Label(text="Card Rank: \nHighest to lowest - A, K, Q, J, 10, 9, 8, 7, 6 \n \n"
                      "Objective: \nThe objective of the game is to avoid being the last player with cards. \n \n"
                      "Losing: \nThe last player still with cards is the loser \n \n"
                      "Playing: \nDrag the card you want to use to the center of the board and release it\n\n"
                      "Rules: \nDefending cards must be higher than the attacking card with the same symbol\nor it can "
                      "be a koser with any value as ling as the attacking card isn't a koser if it "
                      "is the first rule applies\n\n"
                      "Attacking cards should be with the same value as one of the cards that are already on the board"
                      "\nif there aren't any cards on the board, any card can be placed on the board\n\n"
                      "Bita:\nThe attacking  player can choose bita if he doesn't want or can add any more cards\n\n"
                      "Take:\nThe defending player can choose take if he doesn't want or can defebd against the attack"
                      "\n\nKoser:\nKoser is the symbol that appears on the card bellow the deck,\n"
                      "it can also be found above the deck through out the whole game,\nany card that has the same"
                      " symbol as the koser is higher in value then non koser cards\nso it can beat any non koser card"
                      "\n\nTo close instructions click anywhere on the screen that isn't the popup"
                                    ),
                      size_hint=(None, None),
                      pos_hint={'right': .735, 'bottom': 1},
                      size=(1400, 1300))
        popup.open()  #After turn: \n"
                      #"After an attack, players will draw cards to return their hands to at least six cards\n"
                      #"The original attacker draws first, then the defender if needed

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
        print("The player is making the first move")
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
        popup.open()
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
        popup = Popup(title='                                       Computer chose to take',
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
    def find_y_by_origin(origin, index):  # finds y coordinate from origin
        if origin == 1:
            return 50
        elif origin == 2:
            if index % 2 == 0:
                return 650
            else:
                return 550
        elif origin == 3:
            return 1225

    @staticmethod
    def find_origin_by_y(y):  # finds the origin by y coordinate
        if y == 50:
            origin = 1
        elif y == 600 or y == 650 and y == 550:
            origin = 2
        elif y == 1225:
            origin = 3
        else:
            origin = 0
        return origin

    def computer(self):
        # decides what the computers move will be
        selected = self.find_move()
        if selected == -1 and self.attacker:  # if the computer does not have an available move
            self.take(self.comp, False, False)

        elif selected == -1 and not self.attacker:  # the comp does not have an available move and turn is finished
            self.bita()

        else:  # the computer found a valid move that it can make and it makes it
            self.move(self.comp, selected)

    def run(self):  # runs the game

        if self.adding:
            self.added = self.added + 1
        if self.turn:  # players turn
            won = self.win()
            if not self.legal():
                self.popup_invalid()
                self.revert(self.player, 1)

            elif won == 0:
                if not self.adding:  # computer defending
                    self.computer()
                    self.update_all_loc()
                    won = self.win()
                    if won == 1:
                        self.comp_durak()
                    elif won == 2:
                        self.player_durak()
            elif won == 1:
                self.comp_durak()
            elif won == 2:
                self.player_durak()

        elif not self.adding:  # computers turn
            if not self.legal():
                self.revert(self.player, 1)
                self.popup_invalid()
                return
            selected = self.find_move()
            if selected == -1 and self.attacker:  # if the computer does not have an available move
                self.take(self.comp, False, False)
                self.update_all_loc()
                won = self.win()
                if won == 1:
                    self.comp_durak()
                elif won == 2:
                    self.player_durak()
            elif selected == -1 and not self.attacker:  # the comp does not have an available move and turn is over
                won = self.win()
                if won == 1:
                    self.comp_durak()
                elif won == 2:
                    self.player_durak()
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
                won = self.win()  #
                if won == 1:  # if the computer lost
                    self.comp_durak()
                elif won == 2:  # if the player lost
                    self.player_durak()
        

class DurakApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    DurakApp().run()
