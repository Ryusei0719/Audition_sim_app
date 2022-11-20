import random
import func

class Passive_template:
    #name:バフ名,times:鳴く回数(最大),p:条件を満たしたときに鳴く確率,request:バフ条件
    #situation:盤面条件dict{"status","support_df","buff_list","score_df","judge_dict","rival_list"}
    #buffs:鳴くバフ キュンコメ[["Vi",120],["Da",80],["Vo",80]]みたいに2次元配列を渡す
    def __init__(self,name,times,p,request,buffs,*args):
        self._name = name
        self._times = times
        self._max_times = times
        self._p = p
        self._request = request
        self._buffs = buffs
        self._args = args

    def add_passive(self,situation,passive_list):
        if self._times >0:
          Pup = 0
          for buff in situation["buff_list"]:
              if buff["color"] == "PASSIVEpr":
                  Pup += buff["buff"]
          if self._request(situation,self._args) and random.random()<((self._p + Pup)/100):
              self._times -= 1
              for buff in self._buffs:
                  passive_list.append({"color":buff[0],"buff":int(buff[1]),"name":self._name})
        return passive_list
                
    def get_text(self):
      txt = self._name + '\n'
      for buff in self._buffs:
        txt += buff_icon_dict[buff[0]]
        txt += str(buff[1])
        txt += "%UP/"
      txt += '\n'
      txt += f'[条件:{get_condition_name(self._request,self._args)}]\n'
      txt += f'[確率:{self._p}%]\n'
      txt += f'[最大:{self._max_times}回]'
      return txt
     
def get_condition_name(func,val):
  if func == no_requirement:
        return '無条件'
  elif func == three_color_requirement:
        return 'VoDaViUPすべてが付与されている場合'
  elif func == buff_requirement:
        return f'{buff_icon_dict[val[0]]}UPが付与されている場合'
  elif func == after_turn_requirement:
        return f'{val[0]}ターン以降'
  elif func == before_turn_requirement:
        return f'{val[0]}ターン以前'
  elif func == history_requirement:
        return '履歴に'+",".join(val[0])+'がある場合'
  elif func == possibility_requirement:
    return f'{val[0]}の確率で発動'


      

#無条件バフ
def no_requirement(situation,val):                
  return True

#3色バフ条件
def three_color_requirement(situation,val):
  buff_list = situation["buff_list"]
  color_list =[]
  for buff in buff_list:
    color_list.append(buff["color"])
  return {"Vo","Da","Vi"} <= set(color_list)

#1色バフ条件
def buff_requirement(situation,val):
  buff_list = situation["buff_list"]
  flg = False
  for buff in buff_list:
    if val == buff["color"]:
      flg = True
  return flg

#ターン以降条件
def after_turn_requirement(situation,val):
  return situation["turn"]+1 >= int(val[0])

#ターン以前条件
def before_turn_requirement(situation,val):
  return situation["turn"] < int(val[0])

#確率近似条件
def possibility_requirement(situation,val):
  r = random.random()
  turn_num = situation['turn']
  return r < val[0][turn_num]

#履歴条件
def history_requirement(situation,val):
  set(val[0]) <= set(situation["skill_history"])
  

  
condition_name_dict = {
  '無条件':no_requirement,
  '3色バフ条件':three_color_requirement,
  '(属性)UPが付与されている場合':buff_requirement,
  '(N)ターン以前':before_turn_requirement,
  '(N)ターン以後':after_turn_requirement,
  '履歴に(アイドル)がある場合':history_requirement,
  'それ以外':possibility_requirement
}
  
buff_icon_dict ={
  'Vo':'Vocal',
  'Da':'Dance',
  'Vi':'Visual',
  'At':'注目度',
  'Av':'回避率',
  'PASSIVEpr':'発動率UP'
}

all_passive_dict = {"花風Smiley金1":Passive_template("花風金1",3,30,no_requirement,[["Da",75]]),
            "花風Smiley白":Passive_template("花風白1",3,30,three_color_requirement,[["Vo",50],["Da",50],["Vi",50]]),
            "花風Smiley金2":Passive_template("花風金2",3,30,three_color_requirement,[["Vo",100],["Da",100],["Vi",100]]),
            "水面を仰いで海の底金":Passive_template("海金",3,10,after_turn_requirement,[["Da",60],["Vi",30]],3),
            "水面を仰いで海の底白":Passive_template("海白1",3,10,no_requirement,[["Da",40],["Vi",20]]),
            "反撃の狼煙をあげよ！金":Passive_template("狼煙金",3,20,after_turn_requirement,[["Vo",50],["Da",50],["Vi",50]],3),
            "反撃の狼煙をあげよ！白":Passive_template("狼煙白",3,20,before_turn_requirement,[["Vo",30],["Da",30],["Vi",30]],3),
            "駅線上の日常金":Passive_template("駅金",3,10,after_turn_requirement,[["Da",65],["Vi",65]],3),
            "駅線上の日常白":Passive_template("駅白",3,10,before_turn_requirement,[["Da",30],["Vi",30]],6),
            "kimagure全力ビート！金":Passive_template("バンド金",3,10,no_requirement,[["Vo",40],["Da",40],["Vi",40]]),
            "kimagure全力ビート！白":Passive_template("バンド白",3,10,no_requirement,[["Vo",25],["Da",25],["Vi",25]]),
            "スプリング・フィッシュ金":Passive_template("釣り金",3,10,no_requirement,[["Vo",40],["Da",40],["Vi",40]]),
            "スプリング・フィッシュ白":Passive_template("釣り白",3,10,no_requirement,[["Vo",25],["Da",25],["Vi",25]]),
            "祝唄-hogiuta-金":Passive_template("ホギウタ金",3,10,no_requirement,[["Vo",40],["Da",40],["Vi",40]]),
            "祝唄-hogiuta-白":Passive_template("ホギウタ白",3,10,no_requirement,[["Vo",25],["Da",25],["Vi",25]]),
            "ワン・デー金":Passive_template("ワンデー金",2,20,before_turn_requirement,[["Vo",30],["Da",50],["Vi",30]],3),
            "ワン・デー白":Passive_template("ワンデー白",1,5,no_requirement,[["Da",15]]),
            "チョコレー党白":Passive_template("チョコレー党白",2,20,before_turn_requirement,[["Da",50]],3),
            "チョコレー党金":Passive_template("チョコレー党白",2,20,before_turn_requirement,[["Da",80]],3),
            "ピトス・エルピス白":Passive_template("ピトス白",2,35,before_turn_requirement,[["Vi",30],["Av",30]],2),
            "LATE白":Passive_template("LATE白",1,20,before_turn_requirement,[["Vi",50]],3),
            "LATE金1":Passive_template("LATE金1",1,20,no_requirement,[["Vi",120]]),
            "LATE金2":Passive_template("LATE金2",2,20,possibility_requirement,[["Vi",100]],[0,0,10/32,58/512,0,0]),
            "ちょー早い金":Passive_template("ちょー早い金",3,30,no_requirement,[["Vi",60]]),
            "ちょー早い白":Passive_template("ちょー早い金",2,20,no_requirement,[["Vi",50]]),
            "シャッターチャンス金":Passive_template("シャッター金",3,30,buff_requirement,[["Vo",75]],"Vo"),
            "永遠の方程式金":Passive_template("方程式金",1,30,possibility_requirement,[["Vo",80],["Da",80],["Vi",80]],[0,0.7,1,1,0]),
            "きゅんコメ金":Passive_template("きゅんコメ",3,40,history_requirement,[["Vi",75]],["櫻木真乃","風野灯織"])
            }