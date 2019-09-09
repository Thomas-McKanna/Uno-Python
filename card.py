from animatable import Animatable


class Card(Animatable):
    """
    Represents a generic Uno card, which may be a color/value pair, or be a 
    special card.
    """

    def __init__(self, surface, x=0, y=0, hidden=False):
        """
        Initializes an Uno card for play.
        Parameters:
        -----------
        surface: an image asset in the form of a pygame.Surface
        """
        super(Card, self).__init__(surface, x, y, hidden)
