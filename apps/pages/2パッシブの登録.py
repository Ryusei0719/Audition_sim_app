from multiprocessing import allow_connection_pickling
import streamlit as st
from passive import *
from func import *

st.header('パッシブの登録')

st.session_state.Scard_index = ['水面を仰いで海の底', '反撃の狼煙をあげよ！', 'kimagure全力ビート！', 'こころ、えんにならんで']

@st.cache(allow_output_mutation=True)
def cache_list():
    return []
@st.cache(allow_output_mutation=True)
def cache_dict():
    return {}

passive_list = cache_list()
passive_dict = cache_dict()

name = ''
buffs = [["Vo",0],["Da",0],["Vi",0],['At',0],['Av',0]]
val = None
times = 0
p = 0
condition_func = no_requirement


passive_candidate = []
for Scard_name in st.session_state.Scard_index:
    for passive_name in all_passive_dict.keys():
        if Scard_name in passive_name:
            passive_candidate.append(passive_name)

if 'Pidol_index' in st.session_state:
    passive_candidate.append(st.session_state.Pidol_index)

st.markdown("***")
st.text('取得するパッシブの情報を入力し、「取得」ボタンで登録してください')

tab1, tab2 = st.tabs(["パッシブ情報を自分で入力する", "データベース内のパッシブを検索する"])
with tab1:
    name = st.text_input(
        '登録するパッシブの表示名を入力',
        '(例:LATE金,海白など)'
    )
    
    cl1,cl2,cl3 = st.columns(3)
    st.text('バフ倍率(%)を入力')
    with cl1:
        buffs[0][1] = st.number_input('Vo',value=0)
        buffs[1][1] = st.number_input('Da',value=0)
        buffs[2][1] = st.number_input('Vi',value=0)
        with st.expander("その他"):
            buffs[3][1] = st.number_input('注目度',value=0)
            buffs[4][1] = st.number_input('回避率',value=0)
        
    
    with cl2:
        condition_name = st.selectbox(
            '発動条件',condition_name_dict.keys()
        )
        condition_func = condition_name_dict[condition_name]
        if condition_func == buff_requirement:
            color = st.selectbox(
            '(属性)',buff_icon_dict.values()
            )
            val = {v:k for k,v in buff_icon_dict.items()}[color]
            
        if condition_func == before_turn_requirement:
           turn = st.number_input('(N)',value=0)
           val = turn
        
        if condition_func == after_turn_requirement:
            turn = st.number_input('(N)',value=0)
            val = turn
               
        if condition_func == history_requirement:
            idols = st.multiselect(
                '(アイドル)',
                idol_list
            )
            val = idols
            st.text(val)
            
    with cl3:
        times = st.number_input('最大発動回数',value=0)
        p = st.number_input('発動確率',value=0)

    buffs = [buff for buff in buffs if buff[1]>0]
    passive = Passive_template(name,times,p,condition_func,buffs,val)

    st.markdown("***")
    st.text(passive.get_text())
    regist = st.button('このパッシブを登録する',key = 'own_passive_regi')
    if regist:
        passive_list.append(name)
        passive_dict[name]=passive

with tab2:
    passive_name = st.selectbox(
        '登録されているパッシブから選択する',
        passive_candidate
    )
    passive  = all_passive_dict[passive_name]
    
    st.markdown("***")
    st.subheader('パッシブ内容')
    st.text(passive.get_text())
    regist = st.button('このパッシブを登録する',key = 'templete_pasive_regi')
    if regist:
        passive_list.append(passive_name)
        passive_dict[passive_name]=passive
        
st.markdown("***")
st.subheader('登録されているパッシブスキル')
with st.form('passive_regi'):
    for name,passive in passive_dict.items():
        st.text(name)
        st.caption(passive.get_text())
    with st.expander("登録パッシブを消去する"):
        delete = st.selectbox(
            're',
            passive_list,
            label_visibility='hidden'
        )
        del_btn = st.form_submit_button('このパッシブを消去する')
        if del_btn:
            passive_list.remove(delete)
            del passive_dict[delete]
    
    submitted = st.form_submit_button("このパッシブで決定する")
    if submitted:
        st.session_state.passive_list =passive_list
        st.session_state.passive_dict=passive_dict
        


    
