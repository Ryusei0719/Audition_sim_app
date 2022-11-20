unit_dict = {"イルミネーションスターズ":["櫻木真乃","風野灯織","八宮めぐる"],
             "アンティーカ":["月岡恋鐘","田中摩美々","白瀬咲耶","三峰結華","幽谷霧子"],
             "放課後クライマックスガールズ":["小宮果穂","園田智代子","西城樹里","杜野凛世","有栖川夏葉"],
             "アルストロメリア":["大崎甘奈","大崎甜花","桑山千雪"],
             "ストレイライト":["芹沢あさひ","黛冬優子","和泉愛依"],
             "ノクチル":["浅倉透","樋口円香","市川雛菜","福丸小糸"],
             "シーズ":["七草にちか","緋田美琴"]
             }

idol_list = ("櫻木真乃","風野灯織","八宮めぐる",
             "月岡恋鐘","田中摩美々","白瀬咲耶","三峰結華","幽谷霧子",
             "小宮果穂","園田智代子","西城樹里","杜野凛世","有栖川夏葉",
             "大崎甘奈","大崎甜花","桑山千雪",
             "芹沢あさひ","黛冬優子","和泉愛依",
             "浅倉透","樋口円香","市川雛菜","福丸小糸",
             "七草にちか","緋田美琴")

critical_dict = {"p":1.5,"g":1.1,"n":1.0,"b":0.5,"m":1.5}
color_list = ["Vo","Da","Vi"]
critical_full_name_dict = {"Perfect":1.5,"Good":1.1,"Normal":1.0,"Bad":0.5,"Memory":1.5}
appeal_name = {1.5:"Perfect",1.1:"Good",1.0:"Normal",0.5:"Bad"}

#%%
import pandas as pd
import random
import json
from passive import *
from Pweapon import *
import streamlit as st
import numpy as np

from google.oauth2 import service_account
import gspread
import pandas as pd
# スプレッドシートの認証
scopes = [ 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info( st.secrets["gcp_service_account"], scopes=scopes)
gc = gspread.authorize(credentials)
# スプレッドシートからデータ取得
SP_SHEET_KEY = '1_yC-107Od6CYlLbU_jtH_EUmZ3naQ5rmtG5tWQ5LJS4' # スプレッドシートのキー
sh = gc.open_by_key(SP_SHEET_KEY)
SP_SHEET = 'SupportCard_index' # シート名「シート1」を指定
worksheet = sh.worksheet(SP_SHEET)
data = worksheet.get_all_values() # シート内の全データを取得
support_df = pd.DataFrame(data[1:], columns=data[0]).fillna(0) # 取得したデータをデータフレームに変換

SP_SHEET = 'ProduceCard_index'
worksheet = sh.worksheet(SP_SHEET)
data = worksheet.get_all_values() 
Pcard_df = pd.DataFrame(data[1:], columns=data[0])


EX_df = pd.read_csv('datas/EX_index.csv',index_col=0,encoding="shift-jis")
audition_df = pd.read_csv('datas/Audition_index.csv',index_col=0,encoding="cp932")

with open('datas/rival_move.json') as f:
    hantei_dict = json.load(f)
    
def get_support_df():
      return support_df.set_index('検索キー')

def get_ATK(P_ATK,weapon,week,critical,support_list,skill_history,buff_list,aim,buff_add=True):
  #P_ATK:素のステータスdict,weapon:札の検索キー、week:経過週
  #critical:判定倍率、suport_list:サポートのリスト、aim:狙い先(白札で使用)
  ATK_dict = {}
  color_list = ["Vo","Da","Vi","Ex"]
  name = st.session_state.support_df["アイドル名"][weapon]
  link_flg = chk_link(skill_history,name)
  buff_dict = get_buff(buff_list)
  #各属性の攻撃力を計算
  for c in color_list:
    color = aim if c == "Ex" else c
    buff = buff_dict[color]
    #サポートのステ合計の算出
    S_status = 0
    for support in support_list:
      S_status += st.session_state.support_df.at[support,"{0}_status".format(color)]
    #攻撃力計算
    weapon_rate = float(st.session_state.support_df.at[weapon,"{0}_rate".format(c)])
    iS = st.session_state.support_df.at[weapon,"{0}_status".format(color)]
    ATK =int(int(int(P_ATK[color]*0.5 + (S_status + 3*iS) * (1 + 0.1*week) * 0.2)*buff*critical) * weapon_rate)
    #リンク処理
    if link_flg:
      #リンク倍率はPリストからあとで引っ張ってくる
      link_rate = 0 #p_df[][color]
      ATK += int(int(int(P_ATK[color]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical )*link_rate)
    ATK_dict[c] = ATK

    #バフの追加
    if c != "Ex" and buff_add:
      buff = st.session_state.support_df['{0}_buff'.format(color)][weapon]
      turn = st.session_state.support_df["{0}_buff_coT".format(color)][weapon]
      buff_pack = str(buff).split('&')
      turn_pack = str(turn).split("&")
      for (buff, turn) in zip(buff_pack, turn_pack):
        if int(float(buff))!=0:
          buff_list.append({"color":color,"buff":int(float(buff)),"turn":int(float(turn)),"name":weapon,"fanc":None})
  ATK_dict[aim] += ATK_dict["Ex"]
  del ATK_dict["Ex"]
  
  return "single",ATK_dict

def get_buff(buff_list):
  buffs={}
  for color in color_list:
    buff = 100
    #buff値の合算
    for buff_dict in buff_list:
      if buff_dict["color"] == color:
        buff += buff_dict["buff"]
    for passive in st.session_state.game_val['passive_list']:
      if passive["color"] == color:
        buff += passive["buff"]    
    buff /=100
    buffs[color] = buff
  return buffs

def choose_weapon(weapon_cnd,aim,P_ATK,week,critical,support_list,skill_history,buff_list,turn_num):
  buff_dict = get_buff(buff_list)

  #打つ順番固定のとき
  if st.session_state.weapon_list[turn_num] not in  ["*","+"]:
        return st.session_state.weapon_list[turn_num]
  #手札から選ぶとき
  else:
    if "櫻木真乃花風smiley4凸" in weapon_cnd and turn_num < 2:
      return "櫻木真乃花風smiley4凸"
    elif "櫻木真乃花風smiley0凸" in weapon_cnd and turn_num < 2:
      return "櫻木真乃花風smiley0凸"
    else:
      atk_cnd = 0
      for weapon in weapon_cnd:
        #思い出攻撃力計算
        if weapon == "memory":
          attack_type,ATK_dict = memory(st.session_state.memory_lv,P_ATK,week,support_list,skill_history,buff_list)
        #自札攻撃力計算
        elif weapon in list(st.session_state.Pweapon_dict.keys()):
          attack_type,ATK_dict = st.session_state.Pweapon_dict[weapon].get_ATK(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=False)
        #サポ札攻撃力計算
        else:
          attack_type,ATK_dict = get_ATK(P_ATK,weapon,week,critical,support_list,skill_history,buff_list,aim,buff_add=False)

        ATK = sum(ATK_dict.values()) + ATK_dict[aim]
        if st.session_state.weapon_list[turn_num] == "+":
          #全審査員に対する攻撃力計算
          tmp_dict = {"Vo":0,"Da":0,"Vi":0}
          for color in color_list:
            tmp_dict[color] = sum(ATK_dict.values()) + ATK_dict[color]
          ATK = sum(ATK_dict.values())

        if ATK > atk_cnd:
          cnd_weapon = weapon
          atk_cnd = ATK
      return cnd_weapon

def attack(aim,P_ATK,weapon,week,critical,support_list,skill_history,buff_list):
  color_list = ["Vo","Da","Vi"]
  if weapon in st.session_state.game_val['hand_weapon']:
    st.session_state.game_val['hand_weapon'].remove(weapon)
  st.session_state.game_val['weapon_hist'].append(weapon)
  #思い出攻撃力計算
  if weapon in ["memory","Memory"]:
    attack_type,ATK_dict = memory(st.session_state.memory_lv,P_ATK,week,support_list,skill_history,buff_list)
  #自札攻撃力計算
  elif weapon in list(st.session_state.Pweapon_dict.keys()):
    attack_type,ATK_dict = st.session_state.Pweapon_dict[weapon].get_ATK(P_ATK,week,critical,support_list,skill_history,buff_list)
  #サポ札攻撃力計算
  else:
    attack_type,ATK_dict = get_ATK(P_ATK,weapon,week,critical,support_list,skill_history,buff_list,aim)

  #単体アピール
  if attack_type == "single":
    ATK = min(sum(ATK_dict.values()) + ATK_dict[aim],st.session_state.game_val['judge_dict'][aim]["HP"])
    st.session_state.game_val['judge_dict'][aim]["HP"] -= ATK
    st.session_state.game_val['score_df'][aim][st.session_state.status["name"]] += ATK
    st.session_state.game_val['all_log'].append("to {0} by {1}".format(aim,ATK))

  #全体アピール
  if attack_type == "whole":
    for color in color_list:  
      ATK = min(sum(ATK_dict.values()) + ATK_dict[color],st.session_state.game_val['judge_dict'][color]["HP"])
      st.session_state.game_val['all_log'].append("to {0} by {1}".format(color,ATK))
      st.session_state.game_val['judge_dict'][color]["HP"] -= ATK
      st.session_state.game_val['score_df'][color][st.session_state.status["name"]] += ATK
  if weapon!="memory":
    st.session_state.game_config['all_weapon'].remove(weapon)

def initialize(audition_name):
  #オーディションの初期化
  colors = ["Vo","Da","Vi"]
  judges_dict = {}
  for color in colors:
    judge_dict ={"HP":audition_df["興味値"][audition_name],
                 "MAX_HP":audition_df["興味値"][audition_name],
                 "ATK":0,
                 "DEF":1,
                 "buff":[],
                 "exist_flg":True}
    judges_dict[color] = judge_dict

  rival_list =[]
  name_list =["A","B","C","D","E"]
  for name in name_list:
    if audition_df["{0}属性".format(name)][audition_name]!="NONE":
      rival_dict = {"name":name,
                    "color":audition_df["{0}属性".format(name)][audition_name],
                    "base_ATK":audition_df["基礎攻撃力"][audition_name],
                    "memory_ATK":audition_df["思い出火力"][audition_name],
                    "type":audition_df["{0}変遷種".format(name)][audition_name],
                    "sequence":str(audition_df["{0}変遷順".format(name)][audition_name]).split(','),
                    "Me":100000,
                    "buff":[],
                    "memory_flg":0
                    }
      rival_list.append(rival_dict)
  return judges_dict,rival_list

def show_judge(judge_list):
  l=[]
  for color in color_list:
    l.append(" "+color+":{0}".format(judge_list[color]["HP"]))
  return l

def show_passive_list(passive_list):
  l="PASSIVE:"
  name_list=[]
  for buff in passive_list:
    if buff["name"] not in name_list:
      name_list.append(buff["name"])
      l += (buff["name"] + " ")
  return l

def show_buff_list(buff_list):
  l="BUFF:"
  for buff in buff_list:
    l += buff["color"]+str(buff["buff"])+"%UP "
  return l


def chk_link(skill_history,idol):
  skill_history.append(idol)
  if len(skill_history)>5:
    del skill_history[0]
  out = False
  for unit in unit_dict.values():
    if idol in unit:
      if set(skill_history)>=set(unit):
        out = True
  return out

def rival_aim(rival,trend,turn):
  if rival["type"] == "s":
    aim_flg = True
    cnd = 0
    while(aim_flg):
      #i:殴り先の流行順位
      i = int(rival['sequence'][cnd])
      if st.session_state.game_val['judge_dict'][trend[i-1]]["HP"]>0:
        aim = trend[i-1]
        aim_flg = False
      else:
        cnd += 1
  if rival["type"] == "t":
    aim_flg = True
    cnd = turn + st.session_state.game_config['rival_list'][ord(rival["name"])-ord("A")]["memory_flg"]
    sequence = rival['sequence']
    while(aim_flg):
      aim = trend[int(sequence[cnd%3])-1]
      if st.session_state.game_val['judge_dict'][aim]["HP"]>0:
        aim_flg = False
      else:
        cnd += 1
  return aim

def own_aim(turn_num,aim_list,designate=False):
      #ターン毎に殴り先を指定する場合
  tmp_list = ["Vo","Da","Vi"]
  if designate:
    aim = aim_list[turn_num]
    flg = True
    while(flg):
      if st.session_state.game_val['judge_dict'][aim]["HP"]>0:
        flg = False
        return aim
      else:
         tmp_list.remove(aim)
         aim = tmp_list[0]
    return aim
  #１属性にスピアする場合
  else:
    for aim_cnd in aim_list:
      if st.session_state.game_val['judge_dict'][aim_cnd]["exist_flg"]:
        return aim_cnd

def buff_turn_process(buff_list,turn_num):
  #パッシブ判定に渡す盤面情報
  situation = {"status":st.session_state.status,
              "support_df":st.session_state.support_df,
              "buff_list":buff_list,
              "score_df":st.session_state.game_val['score_df'],
              "judge_dict":st.session_state.game_val['judge_dict'],
              "rival_list":st.session_state.game_config['rival_list'],
              "turn":turn_num,
              "skill_history":st.session_state.game_val['skill_history'],
               "passive_list":st.session_state.game_val['passive_list']
              }
  #ターン開始時の処理
  #前ターンのパッシブスキルの消去
  st.session_state.game_val['passive_list'].clear()
  #パッシブスキルを泣かせる
  for key,passive in st.session_state.game_config['passive_dict'].items():
    st.session_state.game_val['passive_list'] = passive.add_passive(situation,st.session_state.game_val['passive_list'])

  #バフターンを1小さくして0ならリストから消去
  remove_list = []
  for buff_dict in buff_list:
    if buff_dict["turn"]>0:
      buff_dict["turn"] -= 1
    if buff_dict["turn"] == 0:
      remove_list.append(buff_dict)
    #varuableなbuff値を決定
    if buff_dict["fanc"] != None:
      buff_dict["buff"] = buff_dict["fanc"](situation)
  for buff_dict in remove_list:
    buff_list.remove(buff_dict)

  #手札が2枚なら補充
  if len(set(st.session_state.game_val['hand_weapon'])-{"memory"}) < 3:
    st.session_state.game_val['hand_weapon'].append(random.choice(list(set(st.session_state.game_config['all_weapon'])-set(st.session_state.game_val['hand_weapon'])-set(st.session_state.game_val['weapon_hist']))))
  if turn_num == 2:
    st.session_state.game_val['hand_weapon'].append("memory")


def end_chk(idol):
  #ターン終了のチェック
  contenue_flg = True
  extict_flg = False
  colors = ["Vo","Da","Vi"]
  #LAの確認
  for color in colors:
    if st.session_state.game_val['judge_dict'][color]["exist_flg"] and st.session_state.game_val['judge_dict'][color]["HP"] <= 0:
      st.session_state.game_val['judge_dict'][color]["exist_flg"] = False
      st.session_state.game_val['LA_dict'][color] = idol["name"]
      st.session_state.game_val['judge_dict'][color]["HP"] = 0
    extict_flg = extict_flg or st.session_state.game_val['judge_dict'][color]["exist_flg"]
  if not extict_flg:
    contenue_flg = False
  return contenue_flg

def memory(lv,P_ATK,week,support_list,skill_history,buff_list):
  rate_list = [0,0.8,1.0,1.2,1.4,2.0]
  rate = rate_list[lv]
  flg = chk_link(skill_history,st.session_state.status["P_idol"])
  ATK_dict={}
  buff_dict = get_buff(buff_list)
  for color in color_list:
    buff = buff_dict[color]
    #サポートのステ合計の算出
    S_status = 0
    for support in support_list:
      S_status += st.session_state.support_df.at[support,"{0}_status".format(color)]
    #攻撃力計算
    ATK = int(int(int(P_ATK[color]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*1.5 )*rate)
    ATK_dict[color]=ATK
  return "whole",ATK_dict

def get_order(turn_num,critical,weapon):
  tmp_dict = {}
  if weapon == "memory":
    tmp_dict["Myunit"] = 5
  else: tmp_dict["Myunit"] = critical + 0.1
  for rival in st.session_state.game_config['rival_list']:
    tmp_dict[rival["name"]] = critical_dict[st.session_state.game_config['rival_critical'][rival["name"]][str(turn_num+1)+"T"]] + ord(rival["name"]) * 0.001
  Series= pd.Series(tmp_dict).sort_values(ascending=False)
  return(Series.index.tolist())



def one_turn_process(turn_num,aim_list,critical,continue_flg):
  #1ターンの処理 turn_numは0からスタート
  #バフのターン数を1つ小さくする
  buff_turn_process(st.session_state.game_val['buff_list'],turn_num)
  st.session_state.game_val['log'].append("{0}ターン目".format(turn_num+1))
  st.session_state.game_val['all_log'].append("{0}ターン目".format(turn_num+1))
  st.session_state.game_val['log'].append(show_buff_list(st.session_state.game_val['buff_list']))
  st.session_state.game_val['log'].append(show_passive_list(st.session_state.game_val['passive_list']))
  st.session_state.game_val['log'].append("HAND: {0}".format(", ".join(st.session_state.game_val['hand_weapon'])))
  st.session_state.game_val['all_log'].append("buff")

  #自分の攻撃
  hand_weapon = st.session_state.game_val['hand_weapon']
  status = st.session_state.status
  week = st.session_state.week

  #aim = own_aim(turn_num,aim_list,designate=True)
  aim = aim_list[turn_num]
  weapon = choose_weapon(hand_weapon,aim,status,week,critical,st.session_state.support_list,st.session_state.game_val['skill_history'],st.session_state.game_val['buff_list'],turn_num)
  order_list = get_order(turn_num,critical,weapon)
  for idol in order_list:
    if idol == "Myunit":
      attack(aim,status,weapon,week,critical,st.session_state.support_list,st.session_state.game_val['skill_history'],st.session_state.game_val['buff_list'])
      st.session_state.game_val['log'].append(weapon+"Apeal! to"+aim)
      st.session_state.game_val['all_log'].append(weapon+"Apeal!")
      continue_flg = end_chk(status)
      if not continue_flg:
        return continue_flg
      st.session_state.game_val['all_log'].extend(show_judge(st.session_state.game_val['judge_dict']))
      st.session_state.game_val['log'].append("=========================")

    #ライバルの攻撃
    else:
      rival = [k for k in st.session_state.game_config['rival_list'] if idol == k["name"]][0]
      aim = rival_aim(rival,st.session_state.trend,turn_num)
      base_ATK = int(rival["base_ATK"] * mys_rate(turn_num))
      #ライバルの思い出アピール
      if st.session_state.game_config['rival_critical'][idol][str(turn_num+1)+"T"] == "m":
        for color in color_list:
          ATK = min(rival["memory_ATK"],st.session_state.game_val['judge_dict'][color]["HP"])
          st.session_state.game_val['judge_dict'][color]["HP"] -= ATK
          st.session_state.game_val['score_df'][color][rival["name"]] += ATK
          st.session_state.game_config['rival_list'][ord(idol)-ord("A")]["memory_flg"]
        st.session_state.game_val['all_log'].append("rival {0} Memory Apeal by {1} ".format(rival["name"],ATK))
      #通常攻撃
      else:
        if aim==rival["color"]:
          base_ATK *= 2
        critical = critical_dict[st.session_state.game_config['rival_critical'][rival["name"]][str(turn_num+1)+"T"]]
        buff = 1
        ATK = min(int(base_ATK * critical * buff),st.session_state.game_val['judge_dict'][aim]["HP"])
        st.session_state.game_val['judge_dict'][aim]["HP"] -= ATK
        st.session_state.game_val['score_df'][aim][rival["name"]] += ATK
        st.session_state.game_val['all_log'].append("rival {0} {1}Apeal on {2} by {3} ".format(rival["name"],appeal_name[critical],aim,ATK))
      continue_flg = end_chk(rival)
      if not continue_flg:
        return continue_flg
      st.session_state.game_val['all_log'].extend(show_judge(st.session_state.game_val['judge_dict']))
      st.session_state.game_val['all_log'].append("------------------------------")
  return continue_flg

def cal_result(score,trend,judge_dict,LA_dict):
  score_df = score
  LA_point = [8,6,4]
  TA_point = [20,15,10]
  three_rate = [4,3,2]
  for i,color in enumerate(trend):
    #TAの計算
    score_df["star"][score_df.idxmax()[color]] += TA_point[i]
    #LAの計算
    if color in LA_dict.keys():
      score_df["star"][LA_dict[color]] += LA_point[i]
    #3割星の計算
    for idol in score_df.index:
      if score_df[color][idol] > judge_dict[color]["MAX_HP"] * 0.3:
        score_df["star"][idol] += three_rate[i]
      if score_df[color][idol] > judge_dict[color]["MAX_HP"] * 0.6:
        score_df["star"][idol] += three_rate[i]
      if score_df[color][idol] > judge_dict[color]["MAX_HP"] * 0.9:
        score_df["star"][idol] += three_rate[i]
  return score_df

def get_rival_critical():
  #判定を決める
  rival_mamory = {}
  idol_list = ["A","B","C","D","E"]
  for idol in idol_list:
    #思い出ターン決定
    rival_hantei_dict = hantei_dict[idol]
    tmp=[]
    for turn in rival_hantei_dict.keys():
      if "m" in rival_hantei_dict[turn].keys():
        tmp.append(rival_hantei_dict[turn]["m"])
      else:
        tmp.append(0)
    rival_mamory[idol] = str(random.choices(range(len(tmp)),weights=tmp)[0]+1) + "T"

  #各アイドルの判定決定
  rival_critical = {}
  for idol in idol_list:
    tmp = {}
    for turn,critical_dict in rival_hantei_dict.items():
      keys = [k for k, v in critical_dict.items() if k in ["p","g","n","b"]]
      values = [v for k, v in critical_dict.items() if k in ["p","g","n","b"]]
      tmp[turn] = random.choices(keys,weights=values)[0]
    tmp[rival_mamory[idol]] = "m"
    rival_critical[idol] = tmp
  return rival_critical

#謎バフ倍率
def mys_rate(turn_num):
  p = 0.4
  r = random.random()
  if turn_num<3 or r > p:
    return 1.0
  elif st.session_state.audition_name == "歌姫楽宴":
    st.session_state.game_val['all_log'].append("(謎バフ)")
    return 1.33
  else: 
    st.session_state.game_val['all_log'].append("(謎バフ)")
    return 1.25
    



def sumilate():
    '''
    status = {"Vo":300,"Da":500,"Vi":415,"Me":500,"name":"Myunit","P_idol":"櫻木真乃"},
    support_list = ["小宮果穂反撃の狼煙をあげよ！4凸","和泉愛依うち来る〜！？4凸","八宮めぐる花笑み咲匂う4凸","風野灯織水面を仰いで海の底4凸"],
    P_weapon = ["櫻木真乃花風smiley0凸","櫻木真乃花風smiley4凸","櫻木真乃水面仰いで海の底4凸","不使用"],

    taken_passive = ["花風smiley金1","花風smiley金2","花風smiley白","水面を仰いで海の底金"],
    EX_dict = {"小宮果穂反撃の狼煙をあげよ！4凸":{"Vo":0,"Da":120,"Vi":120},
            "和泉愛依うち来る〜！？4凸":{"Vo":0,"Da":120,"Vi":120},
            "八宮めぐる花笑み咲匂う4凸":{"Vo":0,"Da":120,"Vi":120},
            "風野灯織水面を仰いで海の底4凸":{"Vo":0,"Da":120,"Vi":120}},
    weapon_list = ["*","*","*","*","*"],
    week = 29,
    Memory_lv = 2,
    critical_list = [1.5,1.5,1.5,1.5,1.5,1.5],
    trend = ["Da","Vi","Vo"],
    audition_name = "歌姫楽宴",
    aim_list = ["Da","Vi","Vo"],
    #aim_list = ["Da","Da","Vi","Vi","Da"],
    itr_num = 1000
    '''
  #data_input
    support_list = st.session_state.support_list
    P_weapon = list(st.session_state.Pweapon_dict.keys())
    taken_passive = st.session_state.passive_list
    EX_dict = st.session_state.EX_dict
    audition_name = st.session_state.audition_name
    critical_list = st.session_state.critical_list
    aim_list = st.session_state.aim_list
    trend = st.session_state.trend
    itr_num = st.session_state.itr_num
  
    log_dict = {
      '1ターン締め':[],
      '2ターン締め':[],
      '3ターン締め':[],
      '4ターン締め':[],
      '5ターン締め':[],
      '敗退':[],
      '18負け':[]
    }
    result_list = [0,0,0,0,0,0]
    defeat18_num = 0
    support_df = get_support_df().loc[support_list]
    support_df = support_df.replace("",int(0))
    support_df = support_df.drop_duplicates()
    for support in support_list:
        for color in color_list:
            support_df.at[support,color+"_status"] = int(support_df.at[support,color+"_status"])+EX_dict[support][color]
    st.session_state.support_df = support_df
    print("simurating")
    for i in range(itr_num):
        if aim_list != st.session_state.aim_list:
              st.write('caution')
        st.session_state.game_config = {
          'all_weapon':support_list + P_weapon, #選べる全アピール
          'passive_dict':st.session_state.passive_dict, #全パッシブ
          'rival_list' :initialize(audition_name)[1], #対面の情報
          'rival_critical':get_rival_critical() #対面の判定
        }
        for key,val in st.session_state.game_config['passive_dict'].items():
              val._times = val._max_times
 
        st.session_state.game_val = {
          'hand_weapon':random.sample(st.session_state.game_config['all_weapon'],3), #手札
          'buff_list' :[], #今鳴いているバフ
          'passive_list':[], #今鳴いているパッシブ
          'skill_history':[], #今まで打った札(アイドル)の履歴
          'weapon_hist':[], #今まで打った札名の履歴
          'LA_dict':{}, #誰がLAをとったかの情報
          'score_df':pd.DataFrame(np.zeros([6,4]),
                                index=["Myunit","A","B","C","D","E"],
                                columns=['Vo','Da','Vi','star']),  #星の取得情報
          'judge_dict' : initialize(audition_name)[0], #審査員情報
          'log':[],
          'all_log':[],
        }
        turn_num = 0
        continue_flg = True
        #フェス1回分のシュミレーション
        while(continue_flg):
            if turn_num > 4:
                  turn_num = 4
                  break
            else:
              continue_flg = one_turn_process(turn_num,aim_list,critical_list[turn_num],continue_flg)
            turn_num += 1
        st.session_state.game_val['score_df'] = cal_result(st.session_state.game_val['score_df'],trend,st.session_state.game_val['judge_dict'],st.session_state.game_val['LA_dict'])
        st.session_state.game_val['log'].append("======================")
        
        log = st.session_state.game_val['log']
        log.extend(st.session_state.game_val['all_log'])
        log.append("======================\n\n")
        log.append(str(st.session_state.game_val['score_df'])) 
        message = '\n'.join(log)
        

        
        if "Myunit" in st.session_state.game_val['score_df'].sort_values("star",ascending=False).index[0:2].to_list() and not continue_flg:
            st.session_state.game_val['log'].append("{0}ターン締め".format(turn_num))
            result_list[turn_num-1] += 1
            log_dict[f'{turn_num}ターン締め'].append(message)
        else:
            st.session_state.game_val['log'].append("敗退")
            result_list[-1] += 1
            log_dict['敗退'].append(message)
            if st.session_state.game_val['score_df']["star"]["Myunit"] >= 13 and not continue_flg:
                defeat18_num += 1
                log_dict['18負け'].append(message)
                
    st.session_state.simulate_log = log_dict
    ret_dict = {}
    for i,num in enumerate(result_list):
        if i<len(result_list)-1:
            ret_dict[f"{i+1}ターン締め"] = f"{100*num/itr_num}%"
        else:
              ret_dict['敗退'] = f"{100*num/itr_num}%"
        ret_dict["(18負け)"] = f'{100*defeat18_num/itr_num}%'
    return ret_dict
# %%
