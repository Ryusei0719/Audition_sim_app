import streamlit as st
from func import *
from passive import *
from Pweapon import *
import pandas as pd
from deta import Deta

def check_dup_deckname(all_record,username,deckname):
    flag = False
    for record in all_record:
        if record['name']==username and record['deck_name'] == deckname:
            flag = True
            break
    if flag:
        return -1,'既に同じ編成名が登録されています。別の編成名で登録してください'
    else:
        return 1,'success'

#SS:st.session_state
def push_deck(username,deck_name,SS):
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("Idol-db")

    #プロデュースアイドル登録
    push_dict = {
        'name':username,
        'deck_name':deck_name,
        'idol_name':SS.Pidol_name,
        'card_name':SS.Pidol_index,
        'card_type':'P',
        'totu':0,
        'Vo_EX':0,
        'Da_EX':0,
        'Vi_EX':0
    }
    db.put(push_dict)
    #サポートアイドル登録
    push_dict = {}
    for idol,card,totu,Ex in zip(SS.Sidol_name_list,SS.Scard_index,SS.totu_list,SS.EX_dict.values()):
        push_dict = {
        'name':username,
        'deck_name':deck_name,
        'idol_name':idol,
        'card_name':card,
        'card_type':'S',
        'totu':totu,
        'Vo_EX':Ex['Vo'],
        'Da_EX':Ex['Da'],
        'Vi_EX':Ex['Vi']
        }
        db.put(push_dict)
    return 1,'success'

def fetch_deck(user_name,deck_name,SS):
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("Idol-db")
    all_record = db.fetch({'name':user_name,'deck_name':deck_name}).items
    Sidol_name_list = []
    Scard_index = []
    totu_list = []
    support_list = []
    EX_dict = {}
    for record in all_record:
        if record['card_type'] == 'P':
            SS.Pidol_name = record['idol_name']
            SS.Pidol_index = record['card_name']
        elif record['card_type'] == 'S':
            Sidol_name_list.append(record['idol_name'])
            Scard_index.append(record['card_name'])
            totu_list.append(record['totu'])
            support_name = record['idol_name']+record['card_name']+record['totu']
            support_list.append(support_name)
            Ex = {'Vo':record['Vo_EX'],'Da':record['Da_EX'],'Vi':record['Vi_EX']}
            EX_dict[support_name] = Ex
        else:
            return -1,'type_error'
    if len(Sidol_name_list) != 4:
        return -1,'number of Scard invalid'
    else:
        SS.Sidol_name_list = Sidol_name_list
        SS.Scard_index = Scard_index
        SS.totu_list = totu_list
        SS.support_list = support_list
        SS.EX_dict = EX_dict
        return 1,'success'
        
def push_passive(username,deckname,SS):
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("Passive-db")
    for passive in SS.passive_dict.values():
        info = passive.get_DB_info()
        info['name'] = username
        info['deck_name'] = deckname
        db.put(info)
    return 1,'success'
        
def fetch_passive(username,deckname,SS):
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("Passive-db")
    all_record = db.fetch({'name':username,'deck_name':deckname}).items
    passive_dict = {}
    for record in all_record:
        buffs = []
        for color in ['Vo','Da','Vi']:
            if record[color] > 0:
                buffs.append([color,record[color]])
        if record['Otherbuff'] != None:
            buffs.append([record['Otherbuff'],record['Otherrate']])
        val = record['args']
        passive_dict[record['passive_name']] = Passive_template(
            record['passive_name'],
            record['times'],
            record['p'],
            condition_name_dict[record['requirement']],
            buffs,
            val
        )
    SS.passive_dict = passive_dict
    return 1,'success'

def push_Pweapon(username,deckname,SS):
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("Pweapon-db")
    for weapon in SS.Pweapon_dict.values():
        push_dict = {
            'name':username,
            'deck_name':deckname,
            'weapon_name':weapon._name,
            'idol':weapon._idol,
            'info_dict':weapon.info
        }
        db.put(push_dict)
    return 1,'success'

def fetch_Pweapon(username,deckname,SS):
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("Pweapon-db")
    all_record = db.fetch({'name':username,'deck_name':deckname}).items
    Pweapon_dict = {}
    for record in all_record:
        weapon = Pweapon_template(record['idol'],record['weapon_name'],record['info_dict'])
        Pweapon_dict[record['weapon_name']] = weapon
    SS.Pweapon_dict = Pweapon_dict
    return 1,'success'

def push_all_info(username,deckname,SS):
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("Idol-db")
    #編成名がかぶってないかチェック
    all_record = db.fetch({'name':username,'deck_name':deckname}).items
    if len(all_record)>0:
        return -2,'既に同じ編成名が登録されています。別の名前で登録するか，既に登録されている編成を消してから登録してください。'

    else:
        ret = push_deck(username,deckname,SS)
        if ret[0]<0:
            return ret
        ret = push_passive(username,deckname,SS)
        if ret[0]<0:
            return ret
        ret = push_Pweapon(username,deckname,SS)
        if ret[0]<0:
            return ret
        return 1,'success'
    
def fetch_all_info(username,deckname,SS):
    ret = fetch_deck(username,deckname,SS)
    if ret[0]<0:
        return ret
    ret = fetch_passive(username,deckname,SS)
    if ret[0]<0:
        return ret
    ret = fetch_Pweapon(username,deckname,SS)
    if ret[0]<0:
        return ret
    return 1,'success'

def get_deckname(username):
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("Idol-db")
    all_record = db.fetch().items
    deck_list = []
    for record in all_record:
        if record['name'] == username:
            if record['deck_name'] not in deck_list:
                deck_list.append(record['deck_name'])
    return deck_list

def side_info():
    if st.session_state.login:
        with st.sidebar:
            st.write(f'お疲れさまです　{st.session_state.user_name}P!')
            st.write('登録されている編成▽')
            deck_list = get_deckname(st.session_state.user_name)
            for deckname in deck_list:
                st.text('・'+deckname)
                
def delete_info(username,deckname):
    deta = Deta(st.secrets["deta_key"])
    db_names = ['Idol-db','Passive-db','Pweapon-db']
    for db_name in db_names:
        db = deta.Base(db_name)
        all_record = db.fetch({'name':username,'deck_name':deckname}).items
        for record in all_record:
            db.delete(record['key'])
        