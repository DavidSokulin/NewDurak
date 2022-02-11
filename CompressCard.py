

class CompressCard:
    def __init__(self, kind, value, origin, index):
        self.rotation = 0
        self.value = int(value)  # | 6-10 normal | 11 - Jack | 12 - Queen | 13 - King | 14 - Ace |
        self.kind = int(kind)  # | 0 - not set | 1 - heart | 2 - Spades | 3 - Clubs | 4 - Diamonds |
        self.origin = origin  # | 0 - not set | 1 - player | 2 - board | 3 - computer |
        self.index = index  # | -1 - not set | 0 - first | 1 - second | 2 - third | 3 - fourth |
