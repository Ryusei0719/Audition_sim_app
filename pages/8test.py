import streamlit as st
from deta import Deta
import datahandler as DH
import func




#st.write(st.session_state)
# Data to be written to Deta Base


link = '[TOPへ](/)'
st.markdown(link, unsafe_allow_html=True)
st.write(func.get_support_df())
