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


def start_test(days, rl, param=2, num_users=100000):
    """
    Starts the A/B Test starting in 2024-01-01 for a set number of days

    Input: 
    - days: number of days
    - rl: relative lift
    - param: default param for control
    - num_users: # of subs that may eventually enter the test
    """
    # start time is 2024-01-01
    start_date = datetime(2024, 1, 1)
    end_date = start_date + timedelta(days=days)

    # generate users
    user_data = create_user_dataset(num_users)

    # generate events for control and test groups
    df_c = generate_main_dataframe(start_date, end_date, user_data, param)
    df_t = generate_main_dataframe(start_date, end_date, user_data, param * (1 + rl))

    # Initialize lists to store daily snapshots
    snapshot_c = []
    snapshot_t = []

    for day in range(1, days + 1):
        # Slice the dataframes to get data up to the current day
        df_c_slice = df_c[df_c['date'] <= start_date + timedelta(days=day)]
        df_t_slice = df_t[df_t['date'] <= start_date + timedelta(days=day)]

        # Aggregate by user for control and test groups
        userdata_c = df_c_slice.groupby('userid')['action_count'].sum().reset_index()
        userdata_t = df_t_slice.groupby('userid')['action_count'].sum().reset_index()

        # Add snapshot column
        userdata_c['snapshot'] = day
        userdata_t['snapshot'] = day

        # Append to snapshot lists
        snapshot_c.append(userdata_c)
        snapshot_t.append(userdata_t)

    # Concatenate the snapshots to create final dataframes
    userdata_c = pd.concat(snapshot_c, ignore_index=True)
    userdata_t = pd.concat(snapshot_t, ignore_index=True)

    return userdata_c, userdata_t
