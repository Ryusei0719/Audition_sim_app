import streamlit as st
from deta import Deta
import datahandler as DH



if st.button('test_push'):
    DH.push_Pweapon('test','test_deck',st.session_state)
    
if st.button('test_fetch'):
    DH.fetch_Pweapon('test','test_deck',st.session_state)

st.write(st.session_state)
# Data to be written to Deta Base


link = '[TOPへ](/)'
st.markdown(link, unsafe_allow_html=True)
