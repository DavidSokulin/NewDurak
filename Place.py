from kivy.uix.image import Image
from kivy.uix.scatter import Scatter


class Place(Scatter):
    def __init__(self):
        Scatter.__init__(self)
        self.do_scale = False
        self.do_rotation = False
        self.rotation = 0
        # self.on_touch_down(self.parent.take_cards())
        self.y = 50
        self.x = 125
        self.scale = 3
        self.do_translation = False
        name = "Border.png"  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    def __init__(self, x, y):
        Scatter.__init__(self)
        self.do_scale = False
        self.do_rotation = False
        self.rotation = 0
        self.scale = 3
        # self.on_touch_down(self.parent.take_cards())
        self.y = int(x)  # | 6-10 normal | 11 - Jack | 12 - Queen | 13 - King | 14 - Ace |
        self.x = int(y)  # | 0 - not set | 1 - heart | 2 - Spades | 3 - Clubs | 4 - Diamonds |
        self.do_translation = False
        name = "Border.png"  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image


