class Balances:
    def __init__(self, gpin, owed, owes, amount):
        self.gpin = gpin # primary key
        self.user_owed = owed # secondary key
        self.user_owes = owes # secondary key
        self.amount = amount