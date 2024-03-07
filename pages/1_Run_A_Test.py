import numpy as np
import pandas as pd
import streamlit as st
import uuid
from datetime import datetime, timedelta
import helperfunctions.data_gen_funcs as gen_funcs
import helperfunctions.statistical_tests as st_funcs
from scipy import stats
import matplotlib.pyplot as plt

##############################################################################################################

# Title and Introduction (Keep it Brief!)

##############################################################################################################
st.set_page_config(
    page_title="Exp / Run A Test",
    page_icon="👁",
)

st.write("# Run A Test")
st.markdown(
    """
Use the UI below to run an A/B Test
"""
)
##############################################################################################################

# Generate Users

##############################################################################################################
st.write("## Registrants")
st.markdown(
    """
Number of Registrants on Website to simulate
"""
)
usercount = st.slider('User Count', min_value=50000, max_value=100000,value=75000)
users = gen_funcs.create_user_dataset(usercount)

##############################################################################################################

# Generate Events

##############################################################################################################

st.markdown(
    """
set minimum DAU
"""
)
min_users = st.slider('minimum DAU', min_value=100, max_value=usercount,value=100)
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
data_df = gen_funcs.generate_main_dataframe(start_date, end_date, users,param=2,min_per_day=min_users)


##############################################################################################################

# Select Metrics

##############################################################################################################

st.markdown(
    """
## Select Metrics
"""
)

option1 = pd.DataFrame({'metrics': ['action_count']})
metric_option = st.selectbox('Select a Metric',option1['metrics'])

##############################################################################################################

# Sequential Test?

##############################################################################################################

st.markdown(
    """
## Sequential Test?

Sequential Tests typically have less power than a regular test (given all else equal), but is useful for when there is prior justification that
the ability to make an earlier decision would be valuable for the feature. 

Examples can be found here: https://docs.statsig.com/experiments-plus/sequential-testing

The type of Sequential Test implemented here is mSPRT ([Zhao et al., 2019](https://arxiv.org/pdf/1905.10493.pdf))
"""
)

option2 = pd.DataFrame({'Test Type': ['Fixed Horizon Test','Sequential Test (mSPRT)']})
flg_st = st.selectbox('Select a Specification',option2['Test Type'])

##############################################################################################################

# Outputs sample mean and sample variance

##############################################################################################################
st.write('## Sample Mean and Sample Variance')
st.markdown(
    """
At a user level of the metric(s) of our choice
"""
)
weeks = pd.DataFrame({'weeks': [i for i in range(1, 51)]})
option3 = st.selectbox('How many weeks do we look over to compute our sample mean/variance?',weeks['weeks'])
st.write('Notice how as the time period gets larger, the metric on average goes up. We explain this in the Appendix.')

# Group data by userid and calculate the sum of action_count for each user
start_date = '2023-01-01'
end_date = pd.to_datetime(start_date) + pd.Timedelta(days=int(option3*7))

user_data_sum = data_df[(data_df['date'] >= start_date) & (data_df['date'] < end_date)].groupby('userid')[metric_option].sum()

# Calculate the sample mean and sample variance and output
st.write("Sample Mean:", round(user_data_sum.mean(),2))
st.write("Sample Variance:", round(np.var(user_data_sum,ddof=1),2))

##############################################################################################################

# Choose Approximate True Effect

##############################################################################################################
st.write('## The True Effect we will Simulate in this Simulation')
st.markdown(
    """
This is an approximation because how you gather the data (e.g., how long you run the test) can change the metric of interest.
More info of this in the Data Generation page.

In a real A/B test, you will not know this!
"""
)
trueeffect = st.slider('x (%)',value=10) 
st.write('The secret approximate relative lift of ',trueeffect, '%')

##############################################################################################################

# State Null and Alt. Hypothesis

##############################################################################################################
st.write('## Our hypothesis')
st.write('We will test this with the typical .8 power and .05 alpha')

st.latex(r'''
    H_0: \mu_C = \mu_T
    ''')
st.latex(r'''
    H_1: \mu_C\neq \mu_T
    ''')


##############################################################################################################

# Sample Size Calculator

##############################################################################################################

st.write('## Calculate Sample Size Needed')
st.markdown(
    """
van Belle ([2002](http://vanbelle.org/chapters%5Cwebchapter2.pdf))'s sample size calculator shortcut for .8 power and .05 alpha. 
The sigma squared is the sample variance and delta is the minimum amount of change you want to detect. n is the number of users
in each variant and assumes equal size
"""
)


st.latex(r'''
    n=\frac{16\sigma^2}{\delta^2}
    ''')

st.write('The delta, or minimum detectable effect (MDE), is the change you want to be able to detect.')
mde = st.slider('MDE (%)', min_value=1, max_value=10,value=5)
n = round((16*np.var(user_data_sum,ddof=1))/(np.mean(user_data_sum)*(mde/100))**2)
st.write('Given the above configurations, we need: ', n, ' users per variant')

##############################################################################################################

# Plots the # of unique users over time to see how long the test must be run

##############################################################################################################
# Group by date and count unique users
# Sort the dataframe by date
data_df = data_df.sort_values(by='date')

# Create a new column for days_from_experiment_start
data_df['days_from_experiment_start'] = (data_df['date'] - data_df['date'].min()).dt.days + 1

# Group by days_from_experiment_start and count unique users
daily_unique_users = data_df.groupby('days_from_experiment_start')['userid'].nunique().cumsum().reset_index()

# Plot
daily_unique_users_capped = daily_unique_users[daily_unique_users['userid'] <= (n*2)] # bug: needs to round up, not round down
# Rename the column
daily_unique_users_capped = daily_unique_users_capped.rename(columns={'userid': 'unique_users'})
st.line_chart(data = daily_unique_users_capped,x='days_from_experiment_start',y='unique_users')
st.write('In practice, this chart may look more logarithmic, since repeat users are excluded from the unique user count')

daysrun = np.max(daily_unique_users_capped['days_from_experiment_start'])
st.write('It looks like we need about ',daysrun,' days to reach our sample size')
st.markdown("""Note that if it takes less than 7 days to reach our sample size, we should still run the test for at least a week 
                to capture weekly seasonality ([Larsen et al., 2023](https://arxiv.org/pdf/2212.11366.pdf))
                """)

# minimum of 7 days
daysrun = max(daysrun, 7)


##############################################################################################################

# Run statistical test

##############################################################################################################
st.write('## Post-Experiment Analysis')

param = 2
trueeffectmod = param*(1+(trueeffect/100))

## Run Test for specified number of days
start_date_new = datetime(2024, 1, 1)
end_date_new = start_date_new + timedelta(days=int(daysrun))

data_df_control = gen_funcs.generate_main_dataframe(start_date_new, end_date_new, users,param=param)
data_df_treat = gen_funcs.generate_main_dataframe(start_date_new, end_date_new, users,param=trueeffectmod)


if flg_st == 'Sequential Test (mSPRT)':
    st.markdown(
    """
    Now, we run mSPRT. We use the Confidence Interval Method here, which has equivalence with the p-value method. 
    Here, we reject the null if the interval does not include 0. 
    """
    )
    result, day, ci_l, ci_u, e = st_funcs.msprt_ci(data_df_control, data_df_treat)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean Difference", round(e,2), "")
    col2.metric("Days Run", day, "")
    col3.metric("Lower CI Bound", round(ci_l,4), "")
    col4.metric('Upper CI Bound', round(ci_u,4), "")


else:
    st.markdown(
        """
    Now that the experiment duration has been reached, we perform Welch's t-test. For our non-proportions data, it is most common to run
    a Welch's t-test, which is a unequal variance robust variation of the t-test. It is not recommended to test for equal variances and then choose
    the variation of the t-test. Instead, it is recommended to just use Welch's t-test anyways. 

    There are some scenarios where one should rely on a permutation test if the sample is not large enough to mitigate the skewness of the underlying
    distribution. In the case of two sample t-tests, because you are looking at the difference of the two variables with similar distributions, 
    the number of samples needed for the normality assumption to be plausible tends to be fewer, 
    especially if the traffic allocation is the same ([Kohavi, Tang and Xu, 2019](https://www.researchgate.net/publication/339914315_Trustworthy_Online_Controlled_Experiments_A_Practical_Guide_to_AB_Testing)). 
    Perhaps in a future iteration of this streamlit application, we will explore that nuance further. 
    """
    )

    ## 6. Display Welch's T-Test
    mean_c, mean_t, relative_lift, p_value = st_funcs.welchtest(data_df_control, data_df_treat, alpha=0.05)

    col1, col2, col3 = st.columns(3)
    col1.metric("Control", mean_c, "")
    col2.metric("Treatment", mean_t, relative_lift)
    col3.metric("p-value", round(p_value,6), "")