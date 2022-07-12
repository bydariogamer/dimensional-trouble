import csv  # ? Why is this here?


class Level:

    def __init__(self, path):
        self.path = path
        self.foreground = None
        self.background = None
        self.actorlayer = None
        self.solidlayer = None

        try:
            ...

        except FileNotFoundError:
            ...
