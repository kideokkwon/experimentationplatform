import uuid
import numpy as np
# from datetime import datetime

class User:
    # def __init__(self, registration_date):
    def __init__(self):
        # base user attributes
        self.user_id = str(uuid.uuid4())
        self.gender = np.random.choice(['Male', 'Female', 'Nonbinary'], p=[0.48, 0.48, 0.04])
        self.age = max(int(np.random.normal(loc=29, scale=5)), 18)  # Normal distribution, minimum age 18
        self.registration_date = '2023-01-01' # fixed date for now
        self.usertype = np.random.choice(['Subscriber','Registrant'], p=[0.2, 0.8])
        
        # propensities
        self.visit_probability = self.calculate_visit_probability()
        self.action_lambda = self.calculate_action_lambda()
    
    def __repr__(self):
        return (f"User(ID={self.user_id}, Gender={self.gender}, Age={self.age}, UserType = {self.usertype} "
                f"Visit Prob={self.visit_probability:.2f}, Actions λ={self.action_lambda:.2f})")
    
    def calculate_visit_probability(self):
        # Example calculation, can be modified based on deeper analysis
        age_factor = 0.6 - (self.age - 18) * 0.01  # Older users have lower propensity
        gender_factor = 0.5 if self.gender == 'Male' else 0.6 if self.gender == 'Female' else 0.55
        type_factor = 0.6 if self.usertype == 'Subscriber' else 0.4
        return max(min(age_factor + gender_factor + type_factor, 0.6), 0.3)
    
    def calculate_action_lambda(self):
        # Example calculation, can be modified based on deeper analysis
        age_factor = 1 + (30 - self.age) * 0.1  # Younger users perform more actions
        gender_factor = 1.5 if self.gender == 'Female' else 1 if self.gender == 'Male' else 1.25
        type_factor = 1.5 if self.usertype == 'Subscriber' else 1
        return age_factor + gender_factor + type_factor
    
    def attributes_in_list_form(self):
        return [self.user_id, self.gender, self.age, self.usertype, np.round(self.visit_probability,2), np.round(self.action_lambda,2)]
    
