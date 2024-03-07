import numpy as np
import pandas as pd
import streamlit as st
import uuid
from datetime import datetime, timedelta
import helperfunctions.data_gen_funcs as gen_funcs
from scipy import stats


##############################################################################################################

# Title and Introduction (Keep it Brief!)

##############################################################################################################
st.set_page_config(
    page_title="Exp / Home Page",
    page_icon="👁",
)

st.write("# Experimentation Platform Simulation")
st.markdown(
    """
A simulated experimentation platform that allows you to perform experiments on simulated user data. 
Includes various standard A/B test vendor functionalities as well as 
other popular features implemented in modern A/B testing tools, 
described in texts such as ([Larsen et al., 2023](https://arxiv.org/pdf/2212.11366.pdf)) and 
([Kohavi, Tang and Xu, 2019](https://www.researchgate.net/publication/339914315_Trustworthy_Online_Controlled_Experiments_A_Practical_Guide_to_AB_Testing)).
"""
)

##############################################################################################################

# Table of Contents

##############################################################################################################

st.write('## Table of Contents / Layout')

st.markdown(
    """
    1. **Quick Demo** (in this page): a quick example of an A/B test
    2. **Run A Test** (page 2): Run your experiments here
    3. **Appendix: Data Generation** (page 2): explains the structure of the simulated data and the userpool
    4. **Appendix: Sequential Testing** (page 3): the rationale as well as an example implementation
    5. **Work in Progress**:


"""
)
##############################################################################################################

# Quick Demo Intro

##############################################################################################################

st.write('## Quick Demo')
st.markdown(
    """
The below is a quick example of running a typical A/B test.
"""
)
##############################################################################################################

# Quick Demo Intro

##############################################################################################################
st.write('### Sample Events')
st.markdown(
    """
A sample of events, with `action_count` representing some arbitrary count metric. 
"""
)
param = 2
num_users = 100000 # number of total registrants
user_data = gen_funcs.create_user_dataset(num_users) # generates userid's for each user
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
data_df = gen_funcs.generate_main_dataframe(start_date, end_date, user_data,param=param) # creates random event data
st.write(data_df.head(3))

##############################################################################################################

# Outputs sample mean and sample variance

##############################################################################################################
st.write('### Sample Mean and Sample Variance')
st.markdown(
    """
At a user level. The average `action_count` per user is our primary metric that we are testing. 
"""
)
weeks = pd.DataFrame({'weeks': [i for i in range(1, 51)]})
option1 = st.selectbox('How many weeks do we look over to compute our sample mean/variance?',weeks['weeks'])
st.write('Notice how as the time period gets larger, the metric on average goes up. We explain this in page 2.')

# Group data by userid and calculate the sum of action_count for each user
start_date = '2023-01-01'
end_date = pd.to_datetime(start_date) + pd.Timedelta(days=option1*7)

user_data_sum = data_df[(data_df['date'] >= start_date) & (data_df['date'] < end_date)].groupby('userid')['action_count'].sum()

# Calculate the sample mean and sample variance and output
st.write("Sample Mean:", round(user_data_sum.mean(),2))
st.write("Sample Variance:", round(np.var(user_data_sum,ddof=1),2))


##############################################################################################################

# Choose Approximate True Effect

##############################################################################################################
st.write('### The True Effect we will Simulate in this Simulation')
st.markdown(
    """
This is an approximation because how you gather the data (e.g., how long you run the test) can change the metric of interest.
More info of this in the Data Generation page.
"""
)
trueeffect = st.slider('x (%)',value=10) 
st.write('The secret approximate relative lift of ',trueeffect, '%')

##############################################################################################################

# State Null and Alt. Hypothesis

##############################################################################################################
st.write('### Our hypothesis')
st.write('Here we use the typical .8 power and .05 alpha')

st.latex(r'''
    H_0: \bar{X}_C = \bar{X}_T
    ''')
st.latex(r'''
    H_1: \bar{X}_C\neq \bar{X}_T
    ''')

##############################################################################################################

# van Belle's Sample Size Calculator

##############################################################################################################
st.write('### Calculate Sample Size Needed')
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

# Run t-test

##############################################################################################################
st.write('### Post-Experiment Analysis')
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
trueeffectmod = param*(1+(trueeffect/100))

## Run Test for specified number of days
start_date_new = datetime(2024, 1, 1)
end_date_new = start_date_new + timedelta(days=daysrun)

data_df_control = gen_funcs.generate_main_dataframe(start_date_new, end_date_new, user_data,param=param)
data_df_treat = gen_funcs.generate_main_dataframe(start_date_new, end_date_new, user_data,param=trueeffectmod)

## 6. Display Welch's T-Test
user_data_sums_control = data_df_control.groupby('userid')['action_count'].sum()
user_data_sums_treat = data_df_treat.groupby('userid')['action_count'].sum()

st.write("Control:", round(user_data_sums_control.mean(),2),"Treatment:", round(user_data_sums_treat.mean(),2))
st.write("Relative Lift: ",round((user_data_sums_treat.mean()- user_data_sums_control.mean())/user_data_sums_control.mean(),2))

# Perform Welch's t-test
t_stat, p_value = stats.ttest_ind(user_data_sums_treat,user_data_sums_control, equal_var=False)

# Print the results
##st.write("Welch's t-statistic:", round(t_stat,2))
st.write("p-value:", round(p_value,6))

st.markdown(
    """
Our decision criteria as mentioned earlier is to reject the null hypothesis if the p-value is below 0.05. 

Note that it is not recommended to compute the post-experiment power despite some websites with significance testing doing so 
[(Kohavi et al., 2022)](https://drive.google.com/file/d/1oK2HpKKXeQLX6gQeQpfEaCGZtNr2kR76/view?usp=sharing)
"""
)




