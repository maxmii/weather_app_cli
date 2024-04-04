class Style:
    """Styling class for weather app to use"""

    def __init__(self):
        self.RED = "\033[1;31m"
        self.BLUE = "\033[1;34m"
        self.CYAN = "\033[1;36m"
        self.GREEN = "\033[0;32m"
        self.YELLOW = "\033[33m"
        self.WHITE = "\033[37m"
        self.PADDING = 20
        self.REVERSE = "\033[;7m"
        self.RESET = "\033[0m"

    def change_colour(self, colour):
        print(colour, end="")
