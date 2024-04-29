from helperfunctions.user import User

class Users:

    def __init__(self, number_of_users):
        self.users = {}
        for _ in range(number_of_users):
            user = User()
            self.users[user.user_id] = user

    def __repr__(self):
        return f"UserPool({len(self.users)} users)"
    
    def get_user(self, user_id):
        return self.users.get(user_id, "User not found")

    def all_users(self):
        return self.users.values()
    
    def users_in_list_form(self):
        return [x.attributes_in_list_form() for x in self.users.values()]
    
    def get_visit_probabilities(self):
        return [user.visit_probability for user in self.users.values()]
    
    def get_action_lambdas(self):
        return [user.action_lambda for user in self.users.values()]
        