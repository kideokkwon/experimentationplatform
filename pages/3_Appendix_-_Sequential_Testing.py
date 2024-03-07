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
Here is an example of an A/A Test - we track how the confidence interval fluctates over time
"""
)

# run an A/A Test
control, treat = gen_funcs.start_test(days=14, rl=0)

# for each day, collect criteria
x = control['snapshot'].unique()
y_fh_l = []; y_fh_h = []
y_st_l = []; y_st_h = []


for i in range(1,np.max(x)+1):
    temp_c = control[control['snapshot'] == i]['action_count']
    temp_t = treat[treat['snapshot'] == i]['action_count'] 
    st_l, st_h = st_funcs.msprt(0.05, temp_c, temp_t)
    fh_l, fh_h = st_funcs.fixedttest(0.05, temp_c, temp_t)
    y_fh_l.append(fh_l)
    y_fh_h.append(fh_h)
    y_st_l.append(st_l)
    y_st_h.append(st_h)

chart_data = pd.DataFrame(np.array([y_fh_l, y_fh_h, y_st_l, y_st_h]).T, columns=['Lower (Regular)','Upper (Regular)','Lower (mSPRT)','Upper (mSPRT)'])
st.line_chart(chart_data,color=['#FF0000','#0000FF','#FF0000','#0000FF'])

st.write("### The FPR and Power")
st.markdown(
    """
The "False Positive Rate" is the rate of "*falsely* thinking the test is *positive*". 
We can check this rate by simulating a lot of A/A tests and seeing how often the two methods conclude that the test is positive

On the other hand, the "power" can be easily checked by simulating A/B tests where there is a difference and seeing what percent of them
are rejected.

Feel free to check out my Simulation here: [Link](https://github.com/kideokkwon/experimentation-simulation-and-text-notes/blob/main/simulation/topic_03_sequential_testing.ipynb)

For one with more detail and insights (but no replication code): ([Stewart, 2023](https://www.statsig.com/blog/sequential-testing-on-statsig))

The results indicate that the Sequential helps protect from inflated FPR, but the tradeoff is that the Power is going to be a little lower
than a standard fixed horizon test. This is why Sequential Testing is not the default - because when it is not necessary to perform a Sequential Test,
it is more powerful to perform a regular fixed horizon test.
"""
)











