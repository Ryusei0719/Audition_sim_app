from func import *
#自札の登録
class Pwaepon_template:
  def __init__(self,idol,card_name,totsu,ATK_fanc):
    self._idol = idol
    self._card_name = card_name
    self._key = idol + card_name + str(totsu) + "凸"
    self.get_ATK = ATK_fanc

#花風smiley0凸
def hanakaze0(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add =True):
  ATK_dict = {}
  link_flg = chk_link(skill_history,"櫻木真乃")
  weapon_rate={"Vo":0.5,"Da":2.5,"Vi":0.5}
  buff_dict = get_buff(buff_list)
  for color in color_list:
    buff = buff_dict[color]
    S_status = 0
    for support in support_list:
      S_status += support_df.at[support,"{0}_status".format(color)]
    if link_flg:
      if not color == "Da":
        weapon_rate[color] += 1
    ATK = int(int(int(P_ATK[color]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical )*weapon_rate[color])
    ATK_dict[color] = ATK
    if buff_add:
      buff_list.append({"color":color,"buff":10,"turn":3,"name":"櫻木真乃花風smiley0凸","fanc":None})
  return "whole",ATK_dict

#花風smiley4凸
def hanakaze4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  link_flg = chk_link(skill_history,"櫻木真乃")
  weapon_rate={"Vo":1,"Da":4,"Vi":1}
  buff_dict = get_buff(buff_list)
  for color in color_list:
    buff = buff_dict[color]
    S_status = 0
    for support in support_list:
      S_status += support_df.at[support,"{0}_status".format(color)]
    if link_flg:
      if not color == "Da":
        weapon_rate[color] += 1
    ATK = int(int(int(P_ATK[color]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical )*weapon_rate[color])
    ATK_dict[color] = ATK
    if buff_add:
      buff_list.append({"color":color,"buff":30,"turn":3,"name":"櫻木真乃花風smiley4凸","fanc":None})
  return "whole",ATK_dict

#ちょー速い0凸
def hayai0(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  link_flg = chk_link(skill_history,"和泉愛依")
  weapon_rate = 3.5
  if link_flg:
    weapon_rate = 5
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Vi"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Vi")]
  ATK = int(int(int(P_ATK["Vi"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff * critical )*weapon_rate)
  ATK_dict["Vi"] = ATK
  ATK_dict["Da"]=0
  ATK_dict["Vo"]=0
  if buff_add:
    buff_list.append({"color":"Vi","buff":20,"turn":4,"name":"ちょー速い0凸","fanc":None})
    buff_list.append({"color":"Vi","buff":5,"turn":7,"name":"ちょー速い0凸","fanc":None})
  return "single",ATK_dict

#ちょー速い4凸
def hayai4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  link_flg = chk_link(skill_history,"和泉愛依")
  weapon_rate = 5
  if link_flg:
    weapon_rate = 6.5
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Vi"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Vi")]
  ATK = int(int(int(P_ATK["Vi"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff * critical )*weapon_rate)
  ATK_dict["Vi"] = ATK
  ATK_dict["Da"]=0
  ATK_dict["Vo"]=0
  if buff_add:
    buff_list.append({"color":"Vi","buff":40,"turn":4,"name":"ちょー速い0凸","fanc":None})
    buff_list.append({"color":"Vi","buff":10,"turn":7,"name":"ちょー速い0凸","fanc":None})
  return "single",ATK_dict

#シャッターチャンス4凸
def shutter4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  link_flg = chk_link(skill_history,"和泉愛依")
  weapon_rate = 5
  if link_flg:
    weapon_rate = 6
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Vo"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Vo")]
  ATK = int(int(int(P_ATK["Vo"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff * critical )*weapon_rate)
  ATK_dict["Vo"] = ATK
  ATK_dict["Da"]=0
  ATK_dict["Vi"]=0
  if buff_add:
    buff_list.append({"color":"Vo","buff":30,"turn":3,"name":"シャッター4凸","fanc":None})
    buff_list.append({"color":"Vo","buff":30,"turn":5,"name":"シャッター4凸","fanc":None})
    buff_list.append({"color":"Da","buff":30,"turn":5,"name":"シャッター4凸","fanc":None})
    buff_list.append({"color":"Vi","buff":30,"turn":5,"name":"シャッター4凸","fanc":None})
  return "single",ATK_dict

#海4凸(取得札)
def umi4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  link_flg = chk_link(skill_history,P_ATK["P_idol"])
  weapon_rate = [3,1.5]
  buff_rate = []
  buff_dict = get_buff(buff_list)
  for i,color in enumerate(["Da","Vi"]):
    buff = buff_dict[color]
    S_status = 0
    for support in support_list:
      S_status += support_df.at[support,"{0}_status".format(color)]
    ATK = int(int(int(P_ATK[color]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical )*weapon_rate[i])
    ATK_dict[color] = ATK
    if buff_add:
      buff_list.append({"color":color,"buff":30,"turn":3,"name":P_ATK["P_idol"]+"水面仰いで海の底4凸","fanc":None})
  ATK_dict["Vo"] = 0
  return "single",ATK_dict

#駅4凸
def eki4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  link_flg = chk_link(skill_history,P_ATK["P_idol"])
  weapon_rate = [2,2]
  buff_rate = []
  buff_dict = get_buff(buff_list)
  for i,color in enumerate(["Da","Vi"]):
    buff = buff_dict[color]
    S_status = 0
    for support in support_list:
      S_status += support_df.at[support,"{0}_status".format(color)]
    ATK = int(int(int(P_ATK[color]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical )*weapon_rate[i])
    ATK_dict[color] = ATK
    if buff_add:
      buff_list.append({"color":color,"buff":20,"turn":3,"name":P_ATK["P_idol"]+"駅線上の日常4凸","fanc":None})
  ATK_dict["Vo"] = 0
  return "single",ATK_dict

#ワンデー4凸
def oneday4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  weapon_rate = 3
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Da"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Da")]
  ATK = int(int(int(P_ATK["Da"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff * critical )*weapon_rate)
  ATK_dict["Da"] = ATK
  ATK_dict["Vi"]=0
  ATK_dict["Vo"]=0
  if buff_add:
    buff_list.append({"color":"Vo","buff":15,"turn":3,"name":"ワンデー4凸","fanc":None})
    buff_list.append({"color":"Da","buff":30,"turn":3,"name":"ワンデー4凸","fanc":None})
    buff_list.append({"color":"Vi","buff":15,"turn":3,"name":"ワンデー4凸","fanc":None})
  return "single",ATK_dict

#ピトス4凸
def pitosu4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  link_flg = chk_link(skill_history,P_ATK["P_idol"])
  weapon_rate = 4
  buff_rate = []
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Vi"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Vi")]
  ATK = int(int(int(P_ATK["Vi"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical)*weapon_rate)
  ATK_dict["Vi"] = ATK
  if buff_add:
    buff_list.append({"color":"Vi","buff":0,"turn":3,"name":"ピトス","fanc":pitosu_buff})
    buff_list.append({"color":"Av","buff":10,"turn":4,"name":"ピトス","fanc":None})
  ATK_dict["Vo"] = 0
  ATK_dict["Da"] = 0
  return "whole",ATK_dict

def pitosu_buff(situation):
  avoid = 0
  for buff_dict in situation["buff_list"]+situation["passive_list"]:
    if buff_dict["color"] == "Av":
      avoid += buff_dict["buff"]/100
  return random.choices([80,160,240,0],weights=[3*avoid/8,3*avoid/8,1*avoid/8,1-7*avoid/8])[0]

#LATE4凸
def LATE4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  ATK_dict = {}
  weapon_rate = 3.5
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Vi"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Vi")]
  ATK = int(int(int(P_ATK["Vi"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff * critical )*weapon_rate)
  ATK_dict["Vi"] = ATK
  ATK_dict["Da"]=0
  ATK_dict["Vo"]=0
  if buff_add:
    buff_list.append({"color":"Vi","buff":20,"turn":4,"name":"LATE4凸","fanc":None})
  return "single",ATK_dict
  

#不使用札
def hoge(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  return_dict = {"Vo":0,"Da":0,"Vi":0}
  return "single",return_dict

#Da2.5倍アピール
def Da25(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  weapon_rate = 2.5
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Da"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Da")]
  ATK = int(int(int(P_ATK["Da"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical)*weapon_rate)
  ATK_dict = {"Vo":0,"Da":ATK,"Vi":0}
  return "single",ATK_dict

#Vi2.5倍アピール
def Vi25(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  weapon_rate = 2.5
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Vi"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Vi")]
  ATK = int(int(int(P_ATK["Vi"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical)*weapon_rate)
  ATK_dict = {"Vo":0,"Da":0,"Vi":ATK}
  return "single",ATK_dict

#巫女真乃0凸
def mikomano0(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  weapon_rate = 2.5
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Vi"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Vi")]
  ATK = int(int(int(P_ATK["Vi"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical)*weapon_rate)
  ATK_dict = {"Vo":0,"Da":0,"Vi":ATK}
  if buff_add:
    buff_list.append({"color":"PASSIVEpr","buff":10,"turn":3,"name":"春日影、さんならび0凸","fanc":None})
  return "single",ATK_dict 

#巫女真乃4凸
def mikomano4(P_ATK,week,critical,support_list,skill_history,buff_list,buff_add=True):
  weapon_rate = 3.5
  buff_dict = get_buff(buff_list)
  buff = buff_dict["Vi"]
  S_status = 0
  for support in support_list:
    S_status += support_df.at[support,"{0}_status".format("Vi")]
  ATK = int(int(int(P_ATK["Vi"]*2 + S_status * 0.2 * (1 + 0.1*week)) * buff*critical)*weapon_rate)
  ATK_dict = {"Vo":0,"Da":0,"Vi":ATK}
  if buff_add:
    buff_list.append({"color":"PASSIVEpr","buff":20,"turn":3,"name":"春日影、さんならび4凸","fanc":None})
  return "single",ATK_dict 
