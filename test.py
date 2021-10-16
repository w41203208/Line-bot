class Test():
    def __init__(self):
        self.weight = None
        self.high = None

    def set_number(self, w):
        self.weight = w

    def set_password(self, h):
        self.high = h

    def get_info(self):

        if self.weight != None and self.high != None:
            return True
        else:
            return False