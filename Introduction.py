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
    1. **Run A Test** (page 2): Run your experiments here
    2. **Appendix: Data Generation** (page 2): explains the structure of the simulated data and the userpool
    3. **Appendix: Sequential Testing** (page 3): the rationale as well as an example implementation
    4. **Appendix: Future Work** (page 4): What will be added in the near future
"""
)
