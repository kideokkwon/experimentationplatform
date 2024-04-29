import numpy as np
import pandas as pd
import streamlit as st
import helperfunctions as hf

##############################################################################################################

# Title and Introduction (Keep it Brief!)

##############################################################################################################
st.set_page_config(
    page_title="Exp / Generate Users",
    page_icon="👁",
)

st.write("# Generate Users")
st.markdown(
    """
Based on the parameters below, generate your userpool to be used for the simulation.
Unless parameters are modified, users will be cached for the duration of the session.
"""
)

# pick how many users to generate

