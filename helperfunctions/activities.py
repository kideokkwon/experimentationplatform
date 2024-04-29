from helperfunctions.user import User
from helperfunctions.users import Users
from datetime import datetime, timedelta
import numpy as np

class Activities:
    def __init__(self, users, start_date, end_date):
        self.users = users
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.activities = self.simulate_activities()

    def simulate_activities(self):
        """ 
        Uses self.visit_probability for each user to decide independently on a given day if they will visit
        Uses self.action_lambda as the parameter for the poisson for those that do visit, how many times they commit the action
        """
        activities = {}
        current_date = self.start_date
        while current_date <= self.end_date:
            daily_activities = {}
            for user_id, user in self.users.items():
                if np.random.random() < user.visit_probability:  # Check if user visits
                    actions_count = np.random.poisson(user.action_lambda)
                    daily_activities[user_id] = actions_count
            activities[current_date.strftime('%Y-%m-%d')] = daily_activities
            current_date += timedelta(days=1)
        return activities

    def get_activities_on_date(self, date):
        return self.activities.get(date, {})
    
    def activities_as_nested_list(self):
        nested_list = []
        for date, daily_activities in self.activities.items():
            for user_id, actions_count in daily_activities.items():
                nested_list.append([date, user_id, actions_count])
        return nested_list
