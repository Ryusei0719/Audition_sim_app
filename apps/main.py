import streamlit as st
from func import *
from Pweapon import *
from passive import *
import pandas as pd

#session_state初期化
if  'Pidol_name' not in st.session_state:
    st.session_state.Pidol_name = ''

if 'Pidol_index' not in st.session_state:
    st.session_state.Pidol_index = ''

if 'Sidol_name_list' not in st.session_state:
    st.session_state.Sidol_name_list = []

if 'Scard_index' not in st.session_state:
    st.session_state.Scard_index = []

if 'support_list' not in st.session_state:
    st.session_state.support_list = ["小宮果穂反撃の狼煙をあげよ！4凸","和泉愛依うち来る〜！？4凸","八宮めぐる花笑み咲匂う4凸","風野灯織水面を仰いで海の底4凸"]

if 'Pweapon_dict' not in st.session_state:
    st.session_state.Pweapon_dict = {}

if 'passive_list' not in st.session_state:
    st.session_state.passive_list = []

if 'passive_dict' not in st.session_state:
    st.session_state.passive_dict = {}

if 'EX_dict' not in st.session_state:
    st.session_state.EX_dict = {}

if 'status' not in st.session_state:
    st.session_state.status = {}

if 'aim_list' not in st.session_state:
    st.session_state.aim_list = []

if 'critical_list' not in st.session_state:
    st.session_state.critical_list = []

if 'weapon_list' not in st.session_state:
    st.session_state.weapon_list = ["*","*","*","*","*"]




st.title('オーディションシュミレータ')
st.caption('これは編成と札回しを登録することでオデの勝率をシュミレーションできるアプリです。')

st.write(st.session_state)
