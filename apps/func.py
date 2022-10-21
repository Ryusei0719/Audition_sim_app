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
critical_dict = {"Perfect":1.5,"Good":1.1,"Normal":1.0,"Bad":0.5,"Memory":1.5}
appeal_name = {1.5:"Perfect",1.1:"Good",1.0:"Normal",0.5:"Bad"}

#%%
import pandas as pd
import random
import json
from passive import *
from Pweapon import *

Pcard_df = pd.ExcelFile('datas/ProduceCard_index.xlsx').parse(index_col=None)
Scard_df = pd.ExcelFile('datas/SupportCard_index.xlsx').parse(index_col=None)
EX_df = pd.ExcelFile('datas/EX_index.xlsx').parse(index_col=0)
audition_df = pd.ExcelFile('datas/Audition_index.xlsx').parse(index_col=0)
support_df = Scard_df
print(EX_df)
with open('datas/rival_move.json') as f:
    hantei_dict = json.load(f)
    
print(EX_df)

'''
def sumilate(
        status = {"Vo":300,"Da":500,"Vi":415,"Me":500,"name":"Myunit","P_idol":"櫻木真乃"},
        support_list = ["小宮果穂反撃の狼煙をあげよ！4凸","和泉愛依うち来る〜！？4凸","八宮めぐる花笑み咲匂う4凸","風野灯織水面を仰いで海の底4凸"],
        P_weapon = ["櫻木真乃花風smiley0凸","櫻木真乃花風smiley4凸","櫻木真乃水面仰いで海の底4凸","不使用"],
        Pweapon_dict = {"櫻木真乃花風smiley0凸":Pwaepon_template("櫻木真乃","花風smiley",0,hanakaze0),
                        "櫻木真乃花風smiley4凸":Pwaepon_template("櫻木真乃","花風smiley",4,hanakaze4),
                        "櫻木真乃水面仰いで海の底4凸":Pwaepon_template("櫻木真乃","水面仰いで海の底",4,umi4),
                        "不使用":Pwaepon_template("櫻木真乃","不使用",4,hoge),
                        },
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
        itr_num = 1000):
    
    result_list = [0,0,0,0,0,0]
    defeat18_num = 0
    support_df = support_df.loc[support_list]
    support_df.replace("",0,inplace=True)
    for support in support_list:
        for color in color_list:
            support_df.at[support,color+"_status"] += EX_dict[support][color]

    print("simurating")
    for i in tqdm(range(itr_num)):
    all_weapon = support_list + P_weapon
    hand_weapon = random.sample(all_weapon,3)
    weapon_hist = []
    passive_dict = get_passive_dict(taken_passive)
    skill_history = []
    buff_list = []
    passive_list = []
    LA_dict = {}
    score_df = pd.DataFrame({"Vo":0,"Da":0,"Vi":0,"star":0},
                            index=["Myunit","A","B","C","D","E"])
    judge_dict,rival_list = initialize(audition_name)
    Vo_judge_status,Da_judge_status,Vi_judge_status = judge_dict["Vo"],judge_dict["Da"],judge_dict["Vi"]
    turn_num = 0
    rival_critical = get_rival_critical()

    #フェス1回分のシュミレーション
    log = []
    all_log = []
    continue_flg = True
    while(continue_flg):
        continue_flg = one_turn_process(turn_num,critical_list[turn_num],continue_flg)
        turn_num += 1
        if turn_num > 4:
        continue_flg = False
    cal_result()
    log.append("======================")
    if "Myunit" in score_df.sort_values("star",ascending=False).index[0:2]:
        log.append("{0}ターン締め".format(turn_num))
        log_path = output_path+"/{0}turn_finish".format(turn_num)
        result_list[turn_num-1] += 1
    else:
        log.append("敗退")
        log_path = output_path+"/defeated"
        result_list[-1] += 1
        if score_df["star"]["Myunit"] >= 13:
        defeat18_num += 1

    #ログ出力
    if log_flg:
        f = open(log_path+"/{0}.txt".format(i), 'w')
        log.append("")
        log.extend(all_log)
        massage = '\n'.join(log)
        f.write(massage+"\n\n"+str(score_df))
        f.close

    print("\n"+audition_name)
    print("流行"+''.join(trend))
    for i,num in enumerate(result_list):
    if i<len(result_list)-1:
        print("{0}ターン締め:{1}%".format(i+1,100*num/itr_num))
    else:
        print("敗退:{0}%".format(100*num/itr_num))
    print("(18負け:{0}%)".format(100*defeat18_num/itr_num))
'''
# %%
