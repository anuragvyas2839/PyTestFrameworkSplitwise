import uuid

class Group:
    def __init__(self, data=None):
        self.gpin = uuid.uuid4()
        self.users = data.get('users')
        self.transactions = data.get('transations')
        self.group_name = data.get('name')
