import numpy as np
import pandas as pd
import streamlit as st
import uuid
from datetime import datetime, timedelta
import helperfunctions.data_gen_funcs as gen_funcs
from scipy import stats
import matplotlib.pyplot as plt

##############################################################################################################

# Title and Introduction (Keep it Brief!)

##############################################################################################################
st.set_page_config(
    page_title="Exp / Appendix: Sequential Testing",
    page_icon="👁",
)

st.write("# Appendix: Sequential Testing")
st.markdown(
    """
'Peeking' is a dangerous source of inflated false positives in an A/B test. However, the desire to 'know results early' 
is not always a bad one - 
for example, when a significant loss may be incurred by delaying an experiment decision, 
such as launching a new feature ahead of a major event ([More Examples Here](https://docs.statsig.com/experiments-plus/sequential-testing)).
Sequential Testing is the body of work that develops and recommends
methods in which A/B Test practicioners can, under controlled settings, 'peak' and make earlier decisions as necessary. 

A nice review of the current state of the literature of Sequential Stopping can be found at 
([Larsen et al., 2023](https://arxiv.org/pdf/2212.11366.pdf)). There is also a nice high level overview by Spotify 
([Schultzberg and Ankargren, 2023](https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions/)).
Note that the Spotify article's comment on StatSig's implementation is outdated - like many other companies, StatSig has switched to the mSPRT 
methodology described in ([Zhao et al., 2019](https://arxiv.org/pdf/1905.10493.pdf)). 
More on StatSig's implementation at ([Stewart, 2023](https://www.statsig.com/blog/sequential-testing-on-statsig))
"""
)

##############################################################################################################

# Simulate an A/A Test where there is no effect - see how often the p-value dips

##############################################################################################################

st.write("### A Demonstration")
st.markdown(
    """
Here is an example of an A/A Test - we track how the p-value fluctates over time
"""
)

## Run Test for specified number of days
start_date_new = datetime(2024, 1, 1)
end_date_new = start_date_new + timedelta(days=14)

# generate users
param = 2
num_users = 100000 # number of total registrants
user_data = gen_funcs.create_user_dataset(num_users) # generates userid's for each user

data_df_control = gen_funcs.generate_main_dataframe(start_date_new, end_date_new, user_data,param=param)
data_df_treat = gen_funcs.generate_main_dataframe(start_date_new, end_date_new, user_data,param=param)

user_data_sums_control = data_df_control.groupby('userid')['action_count'].sum()
user_data_sums_treat = data_df_treat.groupby('userid')['action_count'].sum()

pvals = []
for i in range(2,len(user_data_sums_control)+1):
    t_stat, p_value = stats.ttest_ind(user_data_sums_treat[:i],user_data_sums_control[:i], equal_var=False)
    pvals.append(p_value)
int_list = list(range(2,len(user_data_sums_control)+1))

fig, ax = plt.subplots()
ax.plot(int_list,pvals); ax.set_ylabel('p-value'); ax.set_xlabel('samples')
ax.set_title('example of p-value fluctuation as test runs')
st.pyplot(fig)

st.markdown(
    """
While the above result just shows an example of fluctation over time for one A/A test, examples of aggregate simulation results can be found at
([Stewart, 2023](https://www.statsig.com/blog/sequential-testing-on-statsig)) for even further intuition.

The point is that an experiment, when design assumptions are met, caps the false positive rate at the alpha level, typically 5%.
However, "peeking" will inflate this rate, but we still want a method for some scenarios where even when peeking, the FPR is controlled.


"""
)

