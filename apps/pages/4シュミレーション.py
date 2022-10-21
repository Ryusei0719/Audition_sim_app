from turtle import textinput
import streamlit as st
from func import *
import main

st.header('シュミレーション')
st.text('札回しを選択してシュミレーションします')


aim_list = ['Vo','Vo','Vo','Vo','Vo']
critical_list =['p','p','p','p','p']
weapon_list = [None,None,None,None,None]

with st.form(key = 'sim_info'):
    audition_name = st.selectbox(
        'オーディション名',
        audition_df.index.tolist(),
        key = 'audition_name'
    )    
    
    trend = st.selectbox(
        '流行',
        ['VoDaVi','VoViDa','DaVoVi','DaViVo','ViVoDa','ViDaVo']
    )
    
    week = st.number_input(
            label='経過週',
            value = 29,
            key = 'week'
        )
    
    st.text('ステータス')
    status = {"Vo":None,"Da":None,"Vi":None,"Me":500,"name":"Myunit","P_idol":st.session_state.Pidol_name}
    col1,col2,col3 = st.columns(3)
    
    with col1:
        Vo = st.number_input(
            label='Vo',
            value = 500,
            key = 'Vo_status'
        )
        
    with col2:
        Da = st.number_input(
            label='Da',
            value = 500,
            key = 'Da_status'
        )
    with col3:
        Vi = st.number_input(
            label='Vi',
            value = 500,
            key = 'Vi_status'
        )       
    
    st.markdown('***')
    cols = st.columns(5)
    
    for i,col in enumerate(cols):
        with col:
            st.text(f'{i+1}ターン目')
            aim_list[i] = st.selectbox(
                '殴り先',
                ('Vo','Da','Vi'),
                key = f'aim{i}'
            )
            critical_list[i] = st.selectbox(
                '判定',
                ('Perfect','Good','Normal','Bad'),
                key = f'critical{i}'
            )
            weapon_list[i] = st.selectbox(
                '札',
                ('Perfect','Good','Normal','Bad'),
                key = f'weapon{i}'
            )
            
    sim_btn = st.form_submit_button('シュミレーション開始')
    
    if sim_btn:
        st.text('シュミレーション中')
        st.text('_'.join(aim_list))
        st.session_state.trend = [trend[x:x+2] for x in range(0, len(trend), 2)]
        st.session_state.aim_list = aim_list
        st.session_state.critical_list = [critical_dict[x] for x in critical_list]
        st.text(st.session_state)

# %%
