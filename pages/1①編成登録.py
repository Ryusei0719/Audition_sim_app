import streamlit as st
from func import *

st.header('編成登録')
st.text('シュミレーションする編成を登録してください')

st.markdown("***")
st.subheader('プロデュースアイドル')
Pidol_name = st.selectbox(
    'アイドル名',
    idol_list
)
card_list = Pcard_df[Pcard_df['アイドル']==Pidol_name]['カード名'].tolist()


Pidol_index = st.selectbox(
    'カード名',
    card_list
)

st.markdown("***")
st.subheader('サポートアイドル')
Sidol_name_list = [None,None,None,None]
Sidol_card_list = [None,None,None,None]
Sidol_totu_list = [None,None,None,None]
Sidol_EX_list = [['','',''],['','',''],['','',''],['','','']]

cols = st.columns(4)
for i,col in enumerate(cols):
    with col:
        Sidol_name_list[i] =  st.selectbox(
            'アイドル名',
            idol_list,
            key = f'idolname{i}'
        )
       
        card_list = set(support_df[support_df['アイドル名']==Sidol_name_list[i]]['カード名'].tolist())
        Sidol_card_list[i] = st.selectbox(
            'カード名',
            card_list,
            key = f'idolcard{i}'
        )
        
        Sidol_totu_list[i] = st.selectbox(
            '凸数',
            ['4凸','3凸','2凸','1凸','0凸'],
            key = f'totu{i}'
        )
        
        Sidol_EX_list[i][0] = st.selectbox(
            'EX1',
            EX_df.index.tolist(),
            key = f'EX{i}1'
        )
        
        Sidol_EX_list[i][1] = st.selectbox(
            'EX2',
            EX_df.index.tolist(),
            key = f'EX{i}2'
        )
        Sidol_EX_list[i][2] = st.selectbox(
            'EX3',
            EX_df.index.tolist(),
            key = f'EX{i}3'
        )  

submit_btn = st.button('登録')

if submit_btn:
    st.session_state.support_list = [x+y+z for x,y,z in zip(Sidol_name_list,Sidol_card_list,Sidol_totu_list)]
    
    #EX周りをシュミレータの引数の形に成形
    EX_dict = {}
    for i,idol in enumerate(st.session_state.support_list):
        ret = {'Vo':0,'Da':0,'Vi':0}
        for EX in Sidol_EX_list[i]:
            dic = EX_df.loc[EX].to_dict()
            ret['Vo'] += dic['Vo']
            ret['Da'] += dic['Da']
            ret['Vi'] += dic['Vi']
        EX_dict[idol] = ret
    st.session_state.EX_dict = EX_dict
    st.session_state.Scard_index = Sidol_card_list
    st.session_state.Sidol_name_list = Sidol_name_list
    st.session_state.Pidol_name = Pidol_name
    st.session_state.Pidol_index = Pidol_index

    