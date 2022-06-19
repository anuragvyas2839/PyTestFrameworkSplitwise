import uuid

class Transaction:
    def __init__(self, gpin, user_to_amount_map, transaction_name):
        self.gpin = gpin # primary key, we will need to extract all transactions of a group to settle balances
        self.tpin = uuid.uuid4() # secondary key, to segregate different transactions within the group
        self.user_to_amount_map = user_to_amount_map # dict containing only users involved in the split
        self.total = self.cal_total(user_to_amount_map)
        self.transaction_name = transaction_name

    def cal_total(self, user_to_amount_map):
        return sum(user_to_amount_map.values())
