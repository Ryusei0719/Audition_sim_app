import streamlit as st
from Pweapon import *

func.session_init()

st.header('取得札の登録')
st.write('パネルを開けて獲得するアピール札の情報を登録してください。')


tab1, tab2 = st.tabs(["札情報を自分で入力する", "データベース内の札を使用する"])
with tab1:
    st.subheader("アイドル情報")
    cl1,cl2 = st.columns(2)
    with cl1:
        idol_name = st.selectbox(
            'アイドル名',
            [st.session_state.Pidol_name]+st.session_state.Sidol_name_list
        )

    with cl2:
        card_name = st.text_input(
            '識別できる名前',
            '海4凸,花風smiley0凸など'
        )

    with st.form("P_rate_form"):

        st.subheader('アピール倍率')
        cl1,cl2,cl3,cl4,cl5 = st.columns([4,5,3,2,3])
        with cl1:
            way= st.radio(
                "スピアか全体札か",
                ('観客１人に', '全観客に'),
                label_visibility='hidden'
                )
        with cl2:
            color =st.selectbox(
                'メイン',
                ('Vocal','Dance','Visual','Vocal&Dance','Dance&Visual','Visual&Vocal','Vocal&Danec&Visual','Excellent'),
                label_visibility='hidden'
            )
        
        with cl3:
            rate = st.number_input(
                '倍率',value=0.0,step=0.5,min_value=0.0,label_visibility='hidden'
            )

        with cl4:
            st.subheader('')
            st.text('倍アピール')

        with cl5:
            st.subheader('')
            rate_btn = st.form_submit_button("追加")
            st.session_state.init = False
            if rate_btn:
                for color in color_dict[color]:
                    st.session_state.weapon_info['weapon_rate'][color] += rate
                if way == '全観客に':
                    st.session_state.weapon_info['type'] = 'whole'
                else:
                    st.session_state.weapon_info['type'] = 'single'



    with st.form("P_buff_form"):
        st.subheader('追加されるバフ')
        cl1,cl2,cl3,cl4,cl5 = st.columns(5)
        with cl1:
            buff_icon =st.selectbox(
                'バフ内容',
                ('Vocal','Dance','Visual','Vocal&Dance','Dance&Visual','Visual&Vocal','Vocal&Danec&Visual','注目度','回避率','パッシブ発動率'),
            )

        with cl2:
            buff_rate = st.number_input(
                '倍率',value=0,step=10,label_visibility='hidden'
            )
        
        with cl3:
            st.subheader('')
            st.text('%UP')

        with cl4:
            turns = st.number_input(
                'バフ継続ターン',value=0
            )

        with cl5:
            st.subheader('')
            buff_btn = st.form_submit_button("追加")
            if buff_btn:
                st.session_state.ini = False
                for color in color_dict[buff_icon]:
                    buff_parts = {}
                    buff_parts["color"] = color
                    buff_parts['buff'] = buff_rate
                    buff_parts['turn'] = turns
                    buff_parts['name'] = idol_name+card_name
                    buff_parts['fanc'] = None
                    st.session_state.weapon_info['buff'].append(buff_parts)

    is_link = (idol_name == st.session_state.Pidol_name)

    if is_link:
            st.subheader('リンクアピール')
            cl1,cl2,cl3,cl4,cl5 = st.columns(5)
            
            with cl1:
                link_way = st.radio(
                    "バフか追撃か",
                    ('追撃', 'バフ追加'),
                    label_visibility='hidden'
                    )
            if link_way =='追撃':
                with cl2:
                    link_color =st.selectbox(
                        'メイン',
                        ('Vocal','Dance','Visual','Vocal&Dance','Dance&Visual','Visual&Vocal','Vocal&Danec&Visual'),
                        label_visibility='hidden'
                    )
                with cl3:
                    link_rate = st.number_input(
                        '倍率',value=0.0,step=0.5,min_value=0.0,label_visibility='hidden'
                    )

                with cl4:
                    st.subheader('')
                    st.text('倍追撃')

            if link_way == 'バフ追加':
                with cl2:
                    link_buff_icon =st.selectbox(
                        'バフ内容',
                        ('Vocal','Dance','Visual','Vocal&Dance','Dance&Visual','Visual&Vocal','Vocal&Danec&Visual'),
                    )

                with cl3:
                    link_buff_rate = st.number_input(
                        '倍率(%UP)',value=0,step=10
                    )

                with cl4:
                    link_turns = st.number_input(
                        'バフ継続ターン',value=0
                    )

            with cl5:
                st.subheader('')
                link_btn = st.button("追加")
                if link_btn:
                    if link_way == '追撃':
                        st.session_state.weapon_info['link'][0] = "ATK"
                        st.session_state.weapon_info['link'][1] = {'Vo':0,"Da":0,"Vi":0}
                        for color in color_dict[link_color]:
                            st.session_state.weapon_info['link'][1][color] += link_rate
                    else:
                        st.session_state.weapon_info['link'][0] = "buff"
                        st.session_state.weapon_info['link'][1] = []
                        for color in color_dict[link_buff_icon]:
                            buff_parts = {}
                            buff_parts["color"] = color
                            buff_parts['buff'] = link_buff_rate
                            buff_parts['turn'] = link_turns
                            buff_parts['name'] = idol_name+card_name
                            buff_parts['fanc'] = None
                            st.session_state.weapon_info['link'][1].append(buff_parts)

    weapon = Pweapon_template(idol_name,card_name,st.session_state.weapon_info)




    st.markdown('***')
    st.subheader('作成中の札')
    st.text(idol_name+card_name)
    st.text(weapon.get_text())

    cl1,cl2 = st.columns(2)
    with cl1: 
        clear_btn = st.button("札内容を消去")
        if clear_btn:
            st.session_state.weapon_info = info_init()
    with cl2:
        add_btn = st.button("札内容を登録")
        if add_btn:
            if len(st.session_state.get_weapon_list)<4:
                st.session_state.get_weapon_list.append(weapon)
                st.session_state.Pweapon_dict[weapon._idol+weapon._name]=weapon
                st.session_state.weapon_info = info_init()
            else:
                st.warning('既に4つ札が登録されています', icon="⚠️")


with tab2:
    tmp_dict ={}
    for card in [st.session_state.Pidol_index]+st.session_state.Scard_index:
        if card in all_weapon_dict.keys():
            tmp_dict[card] = all_weapon_dict[card]
    selected_idol_index=st.selectbox(
        '取得する札を持つカード名',
        tmp_dict.keys()
    )
    if selected_idol_index != None:
        weapon = tmp_dict[selected_idol_index]
        if weapon._idol =='P':
            weapon._idol = st.session_state.Pidol_name
    add_btn = st.button("札内容を登録",key='addFromDB')
    if add_btn:
        if len(st.session_state.get_weapon_list)<4:
            st.session_state.get_weapon_list.append(weapon)
            st.session_state.Pweapon_dict[weapon._idol+weapon._name]=weapon
        else:
            st.warning('既に4つ札が登録されています', icon="⚠️")

    
    

st.markdown('***')
st.subheader('登録されている札')
for i,weapon in enumerate(st.session_state.get_weapon_list):
    st.text(str(i+1)+' : '+weapon._name)
    st.caption(weapon.get_text())


clear_weapon = st.selectbox(
    '札を消去する',
    st.session_state.Pweapon_dict.keys()
)
clear_weapon_btn = st.button("消去")
if clear_weapon_btn and len(st.session_state.get_weapon_list)>0:
    st.session_state.get_weapon_list.remove(st.session_state.Pweapon_dict[clear_weapon])
    del st.session_state.Pweapon_dict[clear_weapon]
    st.experimental_rerun()
next_btn = st.button("この札で次に進む")









