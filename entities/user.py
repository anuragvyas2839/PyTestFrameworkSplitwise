import uuid

class User:
    def __init__(self, details):
        self.upin = uuid.uuid4()
        self.username = details['username']
        self.first_name = details['first_name']
        self.last_name = details['last_name']
        self.dob = details['dob']
        self.country = details.get('country') #optional attribute hence using .get() to avoid key not found error
        self.groups = details.get('groups') #optional for initialization, if a user directly joins by invite to a group


class UserBalances(User):
    def __init__(self, details):
        User.__init__(self, details['user_details'])
        self.amount_owed_to_user = details['total_amount_owed_to_user'] # dict of contact users (who owe the user) to amount owed
        self.debt = details['total_amount_owed_by_user'] # dict of contact users (whom the user owes) to amount owed