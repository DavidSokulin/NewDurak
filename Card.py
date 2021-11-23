from kivy.uix.scatter import Scatter
from kivy.uix.image import Image


class Card(Scatter):
    def __init__(self, kind, value):
        Scatter.__init__(self)
        self.do_scale = False
        self.do_rotation = False
        self.rotation = 0
        self.scale = 3.2
        # self.on_touch_down(self.parent.take_cards())
        self.value = int(value)  # | 6-10 normal | 11 - Jack | 12 - Queen | 13 - King | 14 - Ace |
        self.kind = int(kind)  # | 0 - not set | 1 - heart | 2 - Spades | 3 - Clubs | 4 - Diamonds |
        self.y = 50
        self.x = 675
        self.distance = self.dist()
        self.cards_in_deck = 1
        self.board_loc = []
        #self.create_board_loc()
        self.player_loc = []
        #self.create_player_loc()
        self.do_translation = True
        name = self.get_name()  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    def dist(self):
        starting_x = 200
        end_x = 2750
        max_dist = 200
        dist = end_x - starting_x
        dist = dist/self.cards_in_deck
        if dist < max_dist:
            f_dist = dist
        else:
            f_dist = max_dist
        return dist
        #for i in range(self.cards_in_deck):
        #self.board_loc[i] = (x_loc, y_loc)
        """ def create_player_loc(self):
            self."""
        
    def get_name(self):
        if not self.value == 0:
            name = "Images/" + str(self.kind) + "_" + str(self.value) + ".png"
        else:
            name = "Images/" + str(self.kind) + ".png"
        return name

    def hide_cards(self):
        name = "Images/0.png"  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    def on_touch_down(self, touch):
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):  # magnitizes cards to a specific location
        if touch.y < 550:
            if self.do_translation and self.y < 450:
                self.y = 50
                if 0 < self.x < 750:
                    self.x = 675
                if 750 < self.x < 950:
                    self.x = 875
                if 950 < self.x < 1150:
                    self.x = 1075
                if 1150 < self.x < 1350:
                    self.x = 1275
                if 1350 < self.x < 1600:
                    self.x = 1475
                if 1600 < self.x < 2200:
                    self.x = 1675
        print(touch.x)

        if self.do_translation and 400 < self.y < 950:
            self.y = 600
            if 0 < self.x < 750:
                self.x = 600
            if 750 < self.x < 950:
                self.x = 825
            if 950 < self.x < 1150:
                self.x = 1050
            if 1150 < self.x < 1350:
                self.x = 1275
            if 1350 < self.x < 1600:
                self.x = 1500
            if 1600 < self.x < 2200:
                self.x = 1725
        return super().on_touch_up(touch)
