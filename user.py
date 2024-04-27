import uuid
import numpy as np
from datetime import datetime

class User:
    def __init__(self, registration_date):
        self.user_id = uuid.uuid4()
        self.gender = self.generate_gender()
        self.age = self.generate_age()
        self.registration_date = registration_date
        self.usertype = self.generate_usertype()
    
    @staticmethod 
    def generate_gender():
        return np.random.choice(['Male','Female','Nonbinary'], p=[0.48, 0.48, 0.04])
    
    @staticmethod
    def generate_age():
        # generate ages
        age = int(np.random.normal(loc=29, scale=5))
        return max(age, 18) # Ensure no one is below 18
    
    @staticmethod
    def generate_usertype():
        return np.random.choice(['Subscriber','Registrant'], p=[0.2, 0.8])
    
