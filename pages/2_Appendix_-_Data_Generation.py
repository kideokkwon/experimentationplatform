import numpy as np
import pandas as pd
import streamlit as st
import uuid
from datetime import datetime, timedelta
import helperfunctions.data_gen_funcs as gen_funcs
from scipy import stats
import plotly.figure_factory as ff
import matplotlib.pyplot as plt


##############################################################################################################

# Title and Introduction (Keep it Brief!)

##############################################################################################################
st.set_page_config(
    page_title="Exp / Appendix: Data Generation",
    page_icon="👁",
)

st.write("# Appendix: Data Generation")
st.markdown(
    """
This section clarifies the structure of the simulated data.
"""
)

##############################################################################################################

# Registrants

##############################################################################################################
st.write("### Registrants")
st.markdown(
    """
We have a list of users:
"""
)

param = 2
num_users = 100000 # number of total registrants
user_data = gen_funcs.create_user_dataset(num_users) # generates userid's for each user
st.write(user_data.head())

##############################################################################################################

# Events Table

##############################################################################################################
st.write("### Events Table")
st.markdown(
    """
On each day, a random number of users from the userpool commit a number of actions, as seen below.
Each day, data is sampled from some statistical distribution and each row is assigned a user. This is repeated for each day of 2023.
"""
)

start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
data_df = gen_funcs.generate_main_dataframe(start_date, end_date, user_data,param=param) # creates random event data
st.write(data_df.head(5))

st.markdown(
    """
There are a few implications with this approach. The most notable one is that the metric of "Average Action Count Per User" will differ from the
population Average, as each day, users who came the previous day can come back. What this means is that, 
based on how we are generating the data, as the difference between 
the size of the registrant base and DAU increases, the value of the metric converges with the population mean. 

Interestingly, the question of "How many days does it take for every user to get sampled at least once" given the data generation above
is a solved combinatorics problem with well-known asymptotic properties. This was first solved in (Stadje, 1990) and is known as 
a generalization of the Coupon Collector's problem, which you can read more about in ([Ferrante, 2012](https://arxiv.org/pdf/1209.2667.pdf))
"""
)

##############################################################################################################

# Distribution of Action Count

##############################################################################################################
st.write("### Distribution of Sample (with varying parameters)")
st.markdown(
    """
The below is an example distribution of the sample paired with another distribution with a slightly different parameter
"""
)
trueeffect = st.slider('true difference (%)',value=10)
param = 2 
param_mod = param*(1+(trueeffect/100))

# https://docs.streamlit.io/library/api-reference/charts/st.pyplot
# Add histogram data
x1 = np.random.poisson(param, size=10000)
x2 = np.random.poisson(param_mod, size=10000)

# Group data together
hist_data = [x1, x2]
labels = ['Control', 'Hypothetical Treatment']

fig, ax = plt.subplots()
ax.hist(hist_data,label=labels); ax.set_ylabel('# of users'); ax.set_xlabel('action count'); ax.legend()
ax.set_title('events data (histogram)')
st.pyplot(fig)

##############################################################################################################

# Distribution of Sample Mean

##############################################################################################################
st.write("### Distribution of Sample Mean")
# Parameters
num_samples = 1000
sample_size = 1000
lambda_1 = 2
lambda_2 = 2.1

# Generate samples from two Poisson distributions
samples_1 = np.random.poisson(param, size=(num_samples, sample_size))
samples_2 = np.random.poisson(param_mod, size=(num_samples, sample_size))

# Calculate sample means
sample_means_1 = np.mean(samples_1, axis=1)
sample_means_2 = np.mean(samples_2, axis=1)

# Plot histograms for the distributions of sample means
fig, ax = plt.subplots()
ax.hist(sample_means_1, bins=30, alpha=0.5, label='Control', density=True)
ax.hist(sample_means_2, bins=30, alpha=0.5, label='Hypothetical Treatment', density=True)
ax.set_xlabel('Sample Mean')
ax.set_ylabel('Density')
ax.set_title('Distribution of Sample Means')
ax.legend()
st.pyplot(fig)
