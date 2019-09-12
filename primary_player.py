from player import Player
from hand import Hand

class PrimaryPlayer(Player):
    """
    Represent the player in this Uno game who is playing against opponent
    players.
    """
    def __init__(self, name):
        super(PrimaryPlayer, self).__init__(name)
