import streamlit as st

st.set_page_config(
    page_title="Exp / Appendix: Future Work",
    page_icon="👁",
)

st.write("# Future Work")
st.markdown(
    """
The following are a list of features to be added to this platform (in progress)
"""
)
st.write("## CUPED")
st.markdown(
    """
CUPED is a popular variance reduction method proposed by 
([Deng et al., 2013](https://exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf)).

With the right infrastructure (to support the method), CUPED promises to reduce the variance of your effect estimates significantly
using historical data. 

Conceptually, it is very similar to one purpose of g-computation in a doubly robust matching framework, 
and CUPED is also referred to as "Regression Adjustment".
"""
)

st.write("## Multiple Testing")
st.markdown(
    """
As it is with all A/B test platforms, the platform should allow for multiple metrics to be used as decision metrics.
"""
)

st.write("## Make Data More Realistic: Weekly Seasonality")
st.markdown(
    """
Many engagement data follow weekly seasonality, and is one reason that A/B tests are recommended to run at least 7 days, even if
the sample size calculator says you need less. To make this more clear, we can add weekly seasonality to our simulated user data
"""
)

st.write("## More to Come!")
st.markdown(
    """
Stay tuned~
"""
)