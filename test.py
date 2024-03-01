import numpy as np
import pandas as pd
import streamlit as st
import uuid
from datetime import datetime, timedelta

st.title('Simulated Experimentation Platform')

"""
# The Userbase
Our simulated Product has about a 500k unique users, here's a sample:
"""

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

df = create_user_dataset(100)
st.write(df.head())

"""
# Events
We also have event data, here's a sample:
"""
def generate_daily_data(date, user_data):
    """
    Generate daily data DataFrame with random values and corresponding user IDs.

    Parameters:
    - date (datetime): Date for the data.
    - user_data (DataFrame): DataFrame with 'userid' column.

    Returns:
    - daily_data_df (DataFrame): DataFrame with 'userid', 'data', and 'date' columns.
    """
    daily_data = np.random.poisson(2, size=np.random.randint(8000, 12000))
    daily_df = pd.DataFrame({
        'userid': np.random.choice(user_data['userid'], size=len(daily_data)),
        'action_count': daily_data,
        'date': date
    })
    return daily_df

def generate_main_dataframe(start_date, end_date, user_data):
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
        daily_df = generate_daily_data(date, user_data)
        data.append(daily_df)
    data_df = pd.concat(data, ignore_index=True)
    return data_df

# Example usage:
num_users = 100
user_data = create_user_dataset(num_users)
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
data_df = generate_main_dataframe(start_date, end_date, user_data)
st.write(data_df.head(20))

"""
# Data over time
We can compute the daily average over time:
"""
st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)