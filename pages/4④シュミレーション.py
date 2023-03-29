import streamlit as st
from func import *
from datahandler import *

st.header('シュミレーション')
st.text('札回しを選択してシュミレーションします')


aim_list = ['Vo','Vo','Vo','Vo','Vo']
critical_list =['p','p','p','p','p']
weapon_list = [None,None,None,None,None]

side_info()
if st.session_state.login and 'user_name' in st.session_state:
    st.markdown('***')
    cl1,cl2 = st.columns(2)
    with cl1:
        deck_name = st.selectbox(
            '登録した編成を呼び出す',
            get_deckname(st.session_state.user_name)
        )
    with cl2:
        st.write('')
        st.write('')
        if st.button('呼び出す'):
            fetch_all_info(st.session_state.user_name,deck_name,st.session_state)
            
    with st.expander("今の編成"):
        st.text('プロデュースアイドル：'+st.session_state.Pidol_name+st.session_state.Pidol_index)
        for i,Sidol in enumerate(st.session_state.support_list):
            st.text(f'サポートアイドル{i+1}：'+Sidol)
            tmp = [key+str(val) for key,val in st.session_state.EX_dict[Sidol].items()]
            st.caption('--EXの上昇量：'+','.join(tmp))
            
        st.text('所得したパッシブ：')
        for name,passive in st.session_state.passive_dict.items():
            st.caption(passive.get_text())
            
        st.text('取得した札：')
        for name,weapon in st.session_state.Pweapon_dict.items():
            st.text(name+':'+weapon.get_text())

with st.form(key = 'sim_info'):
    cl1,cl2 = st.columns(2)
    
    with cl1:
        audition_name = st.selectbox(
            'オーディション名',
            audition_df.index.tolist()
        )    
        
        trend = st.selectbox(
            '流行',
            ['VoDaVi','VoViDa','DaVoVi','DaViVo','ViVoDa','ViDaVo']
        )
        
    with cl2:
        week = st.number_input(
                label='経過週',
                value = 29,
                key = 'week'
            )
        memory_lv = st.number_input(
            label = '思い出レベル',
            step = 1,
            min_value = 0,
            max_value = 5,
            key = 'memory_lv'
        )
    
    st.text('ステータス')
    status = {"Vo":None,"Da":None,"Vi":None,"Me":500,"name":"Myunit","P_idol":st.session_state.Pidol_name}
    col1,col2,col3 = st.columns(3)
    
    with col1:
        status['Vo'] = st.number_input(
            label='Vo',
            value = 500,
            step = 10,
            key = 'Vo_status'
        )
        
    with col2:
        status['Da'] = st.number_input(
            label='Da',
            value = 500,
            step = 10,
            key = 'Da_status'
        )
    with col3:
        status['Vi'] = st.number_input(
            label='Vi',
            value = 500,
            step = 10,
            key = 'Vi_status'
        )       
    
    st.markdown('***')

    
    for i in range(5):
        st.text(f'{i+1}ターン目')
        cl1,cl2 = st.columns(2)
        with cl1:
            aim_list[i] = st.selectbox(
                '殴り先',
                ('Vo','Da','Vi','ランダム'),
                key = f'aim{i}'
            )
        with cl2:
            critical_list[i] = st.selectbox(
                '判定',
                ('Perfect','Good','Normal','Bad','ランダム'),
                key = f'critical{i}'
            )
        weapon_list[i] = st.selectbox(
            '札',
            ['おまかせ(殴り先に最も高いアピールをする札を切る)','おまかせ(全観客に与えるアピール値の総和が最も大きい札を切る)','memory']+list(st.session_state.Pweapon_dict.keys())+st.session_state.support_list,
            key = f'weapon{i}'
        )
        
    st.markdown("****")
    cl1,cl2 = st.columns(2)
    with cl1:
        itr_num = st.number_input(
            label='シュミレーション回数',
            value = 1000,
            step = 100,
            key = 'itr_num'
        )       
    with cl2:
        st.write('')
        sim_btn = st.form_submit_button('シュミレーション開始')
    
    if sim_btn:
        st.session_state.audition_name = audition_name
        st.session_state.status = status
        aim_list = [random.choice(['Vo','Da','Vi']) for x in aim_list if x == 'ランダム']
        st.session_state.trend = [trend[x:x+2] for x in range(0, len(trend), 2)]
        st.session_state.aim_list = aim_list
        for i,x in enumerate(weapon_list):
            if x == 'おまかせ(殴り先に最も高いアピールをする札を切る)':
                weapon_list[i] = '*'
            elif x == 'おまかせ(全観客に与えるアピール値の総和が最も大きい札を切る)':
                weapon_list[i] = '+'
            elif x == 'ランダム':
                weapon_list[i] = [random.choice(['Perfect','Good','Normal'])]
        st.session_state.weapon_list = weapon_list
        st.session_state.critical_list = [critical_full_name_dict[x] for x in critical_list]
        finish_flg = False
        with st.spinner('シュミレーション中'):
            out = sumilate()
            finish_flg = True
        
        if finish_flg:
            st.subheader('シュミレーション結果')
            for key,val in out.items():
                if not key == '(18負け)':
                    st.text(key+':'+val)
            st.text('(18負け)：'+out['(18負け)'])

    #st.write([x.get_text() for x in st.session_state.get_weapon_list])
    #st.write([x.get_text() for x in st.session_state.Pweapon_dict.values()])
    #st.write(support_df)
# %%
