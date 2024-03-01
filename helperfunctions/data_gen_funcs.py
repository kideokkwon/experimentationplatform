import numpy as np
import pandas as pd
import uuid
from datetime import datetime, timedelta

def create_user_dataset(num_users):
    """
    Create a pandas DataFrame with randomly generated user IDs.

    Parameters:
    - num_users (int): Number of users.

    Returns:
    - user_df (DataFrame): DataFrame with 'userid' column.
    """
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    user_df = pd.DataFrame({'userid': user_ids})
    return user_df

def generate_daily_data(date, user_data,param=2):
    """
    Generate daily data DataFrame with random values and corresponding user IDs.

    Parameters:
    - date (datetime): Date for the data.
    - user_data (DataFrame): DataFrame with 'userid' column.

    Returns:
    - daily_data_df (DataFrame): DataFrame with 'userid', 'data', and 'date' columns.
    """
    daily_data = np.random.poisson(param, size=np.random.randint(100, 200))
    daily_df = pd.DataFrame({
        'userid': np.random.choice(user_data['userid'], size=len(daily_data)),
        'action_count': daily_data,
        'date': date
    })
    return daily_df

def generate_main_dataframe(start_date, end_date, user_data,param=2):
    """
    Generate main DataFrame with daily data for a date range.

    Parameters:
    - start_date (datetime): Start date of the date range.
    - end_date (datetime): End date of the date range.
    - user_data (DataFrame): DataFrame with 'userid' column.

    Returns:
    - data_df (DataFrame): Main DataFrame with 'userid', 'data', and 'date' columns.
    """
    date_range = pd.date_range(start=start_date, end=end_date)
    data = []
    for date in date_range:
        daily_df = generate_daily_data(date, user_data,param)
        data.append(daily_df)
    data_df = pd.concat(data, ignore_index=True)
    return data_df