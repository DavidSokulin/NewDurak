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
        #self.x = 675
        self.x = 1275
        self.index = 0
        self.cards_in_deck = 1
        self.board_loc = []
        self.player_loc = []
        self.do_translation = True
        name = self.get_name()  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    def get_name(self):
        if not self.value == 0:
            name = "Images/" + str(self.kind) + "_" + str(self.value) + ".png"
        else:
            name = "Images/" + str(self.kind) + ".png"
        return name

    def comp_card(self, y):
        self.hide_cards()
        self.y = y

    def hide_cards(self):
        self.do_translation = False
        name = "Images/0.png"  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    def on_touch_down(self, touch):
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):  # magnitizes cards to a specific location
        if self.kind != 0:
            if self.y > 500:
                self.parent.update(self.parent.player, 2)
            else:
                self.parent.update(self.parent.board, 1)
        return super().on_touch_up(touch)
