import streamlit as st
from func import *
from passive import *
from Pweapon import *
import pandas as pd

#session_state初期化
if  'Pidol_name' not in st.session_state:
    st.session_state.Pidol_name = '櫻木真乃'

if 'Pidol_index' not in st.session_state:
    st.session_state.Pidol_index = ''

if 'Sidol_name_list' not in st.session_state:
    st.session_state.Sidol_name_list = []

if 'Scard_index' not in st.session_state:
    st.session_state.Scard_index = []

if 'support_list' not in st.session_state:
    st.session_state.support_list = ["小宮果穂反撃の狼煙をあげよ！4凸","和泉愛依うち来る〜！？4凸","八宮めぐる花笑み咲匂う4凸","風野灯織水面を仰いで海の底4凸"]

if 'Pweapon_dict' not in st.session_state:
    st.session_state.Pweapon_dict = get_default_weapon_dict(st.session_state.Pidol_name)

if 'passive_list' not in st.session_state:
    st.session_state.passive_list = []

if 'passive_dict' not in st.session_state:
    st.session_state.passive_dict = {}

if 'EX_dict' not in st.session_state:
    st.session_state.EX_dict = {"小宮果穂反撃の狼煙をあげよ！4凸":{"Vo":0,"Da":120,"Vi":120},
            "和泉愛依うち来る〜！？4凸":{"Vo":0,"Da":120,"Vi":120},
            "八宮めぐる花笑み咲匂う4凸":{"Vo":0,"Da":120,"Vi":120},
            "風野灯織水面を仰いで海の底4凸":{"Vo":0,"Da":120,"Vi":120}}

if 'status' not in st.session_state:
    st.session_state.status = {}

if 'aim_list' not in st.session_state:
    st.session_state.aim_list = []

if 'critical_list' not in st.session_state:
    st.session_state.critical_list = []

if 'weapon_list' not in st.session_state:
    st.session_state.weapon_list = ["*","*","*","*","*"]

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title('オーディションシュミレータ(1.0.0)')
st.write('これは編成と札回しを登録することでオデの勝率をシュミレーションできるアプリです。')

st.write('左のスライドバーから順番に条件を設定することで、その条件での勝率や何ターンで締まるのかをシュミレーションすることができます。')

st.markdown('バグ報告や仕様の質問はこちらから：[お問い合わせページ](https://docs.google.com/forms/d/e/1FAIpQLSezsZWwtLLn3mfla98NMoXGE9t9E1aDlN1txtjPPEb8VjAm8g/viewform?usp=sf_link)')
#st.write(st.session_state)

#st.write('note記事：[リンク](%s)' % )
st.write('もとになったGoogle Colab版シュミレータ：https://note.com/sakuragikonomi/n/n70944644c4f3' )
