class Ordini:

    def __init__(self):
        self.ordini = {}

    def add_ordine(self, user: str,  pizza_name: str):
        self.ordini[user] = pizza_name

    def rem_ordine(self, user: str):
        self.ordini.pop(user, None)

    def get_ordini(self):
        return self.ordini

    def clean(self):
        self.ordini.clear()
