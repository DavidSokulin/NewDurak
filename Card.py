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
        self.x = 800
        self.do_translation = True
        name = self.get_name()  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    """def __init__(self):
        Scatter.__init__(self)
        self.do_scale = False  # so that the card doesn't change scale
        self.do_rotation = False  # so that the card doesn't change scale
        self.value = int(0)  # | 0 - not set | 6-10 normal | 11 - Jack | 12 - Queen | 13 - King | 14 - Ace |
        self.kind = int(0)  # | 0 - not set | 1 - heart | 2 - Spades | 3 - Clubs | 4 - Diamonds |
        name = str(self.kind), ".png"  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image (a back of a card)"""

    def get_name(self):
        if not self.value == 0:
            name = str(self.kind) + "_" + str(self.value) + ".png"
        else:
            name = str(self.kind) + ".png"
        return name

    def hide_cards(self):
        name = "0.png"  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    def on_touch_down(self, touch):
        # if self.collide_point(*touch.pos):
        print("touch x:" + str(touch.x))
        print("touch y:" + str(touch.y))
        print(self.pos)
        return super().on_touch_down(touch)
