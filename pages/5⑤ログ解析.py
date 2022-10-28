import streamlit as st

st.header('ログの解析')

with st.expander("使用した編成"):
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

tab_name = ["1ターン締め", "2ターン締め", "3ターン締め",'4ターン締め','5ターン締め','敗退','18負け']
tabs = st.tabs(tab_name)
for i,tab in enumerate(tabs):
    with tab:
        cl1,cl2 = st.columns([1,5])
        with cl1:
            case_num = len(st.session_state.simulate_log[tab_name[i]])
            if case_num>0:
                case = st.radio("case",range(case_num),
                        label_visibility='hidden',
                        key = tab_name[i])
        with cl2:
            if case_num > 0:
                st.text(st.session_state.simulate_log[tab_name[i]][case])

