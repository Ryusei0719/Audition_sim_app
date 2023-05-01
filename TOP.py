import streamlit as st
from func import *
from passive import *
from Pweapon import *
import datahandler as DH
import pandas as pd
from deta import Deta
import hashlib

session_init()

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