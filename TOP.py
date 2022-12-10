import streamlit as st
from func import *
from passive import *
from Pweapon import *
import datahandler as DH
import pandas as pd
from deta import Deta
import hashlib

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
    
if 'login' not in st.session_state:
    st.session_state.login = False
    
if 'totu_list' not in st.session_state:
    st.session_state.totu_list = ['4凸','4凸','4凸','4凸']

st.set_page_config(
    page_title="オーディションシミュレータ",
    initial_sidebar_state="expanded",
)


st.title('オーディションシミュレータ(1.1.0)')
st.write('これは編成と札回しを登録することでオデの勝率をシュミレーションできるアプリです。')

st.write('左のスライドバーから順番に条件を設定することで、その条件での勝率や何ターンで締まるのかをシュミレーションすることができます。')


with st.form('form'):
    st.write('ログイン')
    st.caption('ログインすることで編成を登録し，いつでも呼び出せるようになります。')
    name = st.text_input("ユーザ名")
    password = st.text_input('パスワード',type='password')
    log_in = st.form_submit_button("ログイン")
    with st.expander('新規登録'):
        new_name = st.text_input("ユーザ名",key = 'new_name')
        new_password = st.text_input('パスワード',key = 'new_pass',type='password')
        sign_up = st.form_submit_button("新規登録")

deta = Deta(st.secrets["deta_key"])

#新規登録
if sign_up:
    db = deta.Base("user_db")
    if new_password == None:
        st.error('パスワードを入力してください')
    db_content = db.fetch().items
    if new_name in [x['name'] for x in db_content]:
        st.error('そのユーザ名は使用されています')
    else:
        db.put({"name": new_name, "password": hashlib.sha256(str.encode(new_password)).hexdigest()})
        st.success('登録完了しました。ログインしてください')

if log_in:
    db = deta.Base("user_db")
    all_record = db.fetch().items
    flg = True
    for record in all_record:
        if record['name'] == name and record['password'] == hashlib.sha256(str.encode(password)).hexdigest():
            st.session_state.user_name = name
            st.session_state.login = True
            st.success('ログインしました')
            flg = False
            break
    if flg:
        st.error('ログイン失敗')
        
DH.side_info()

    
        
    

st.markdown('***')
st.markdown('バグ報告や仕様の質問はこちらから：[お問い合わせページ](https://docs.google.com/forms/d/e/1FAIpQLSezsZWwtLLn3mfla98NMoXGE9t9E1aDlN1txtjPPEb8VjAm8g/viewform?usp=sf_link)')
#st.write(st.session_state)

st.write('note記事：https://note.com/sakuragikonomi/n/n9ed6a5abbb01' )
st.write('もとになったGoogle Colab版シミュレータ：https://note.com/sakuragikonomi/n/n70944644c4f3' )

#st.write(support_df)