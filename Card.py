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
        if self.do_translation and 400 < self.y < 850:
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
