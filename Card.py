from kivy.uix.scatter import Scatter
from kivy.uix.image import Image


class Card(Scatter):
    def __init__(self, kind, value):
        Scatter.__init__(self)
        self.do_scale = False
        self.do_rotation = False
        self.rotation = 0
        self.scale = 3.2
        self.value = int(value)  # | 6-10 normal | 11 - Jack | 12 - Queen | 13 - King | 14 - Ace |
        self.kind = int(kind)  # | 0 - not set | 1 - heart | 2 - Spades | 3 - Clubs | 4 - Diamonds |
        self.y = 50
        self.x = 1275
        self.origin = 0  # | 0 - not set | 1 - player | 2 - board | 3 - computer |
        self.index = -1
        self.border = (0, 0, 0, 0)  # Fix for bug in kivy that distorts the image if border isn't set this way
        self.do_translation = True
        name = self.get_name()  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    def get_name(self):
        # produces the file name that is attached to this card by the combination of the kind and value
        if not self.value == 0:
            name = "Images/" + str(self.kind) + "_" + str(self.value) + ".png"
        else:
            name = "Images/" + str(self.kind) + ".png"
        return name

    def comp_card(self, y):
        self.hide_cards()
        self.y = y

    def hide_cards(self):  # hides the cards so that the player can't see them and locks them so he can't move them
        self.do_translation = False
        name = "Images/0.png"  # defines the file name that contains this card
        image = Image(source=name)
        # remove comment and place the 2 lines above in a comment to reveal the computers cards
        """name = "Images/" + str(self.kind) + "_" + str(
            self.value) + ".png"  # defines the file name that contains this card
        image = Image(source=name)"""
        self.add_widget(image)  # adding the image

    def unhide_cards(self):  # unhides the cards so that the player can see them
        self.do_translation = False
        name = "Images/" + str(self.kind) + "_" + str(
            self.value) + ".png"  # defines the file name that contains this card
        image = Image(source=name)
        self.add_widget(image)  # adding the image

    def on_touch_down(self, touch):
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):  # magnetizes cards to a specific location
        if self.kind != 0:
            if self.y > 300 and self.y != 1225 and self.origin == 1:
                self.parent.update(self.parent.player, self.parent.board, self.index, 50)
                self.parent.run()
            elif self.y < 300 and self.origin == 1:
                self.parent.update_loc(self.parent.player, 50)

        return super().on_touch_up(touch)
