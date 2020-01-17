#coding = utf-8
from math import *

class Datebase():
    def __init__(self):
        self.water = {'超滤产水':[1.05],'RO产水':[1],'地表水':[1.2],'砂滤微滤产水':[1.1],'海水':[1.05]}
        self.ufmem = {'TUF8080':[70,45,140,80,8,2,[0.1,0.05,0.1,24],[0.2,0.1,0.2,720],75],'TUF8040':[40,45,140,80,8,2,[0.1,0.05,0.1,24],[0.2,0.1,0.2,720],75],
        '2880':[77,45,140,80,8,2,[0.1,0.05,0.1,24],[0.2,0.1,0.2,720],75],'2860':[51,45,140,80,8,2,[0.1,0.05,0.1,24],[0.2,0.1,0.2,720],75]}
        self.romem ={'EM8040-400':[98,37,25,1.1],'LP8040-400':[97,37,35,1.1],'EM4040':[98,7,25,1.1],'BW30-400':[99,37,30,1.05],'BW30FR-400':[99.1,37,27,1],'SW30HRLE-400':[99.7,37,9,1]}
        self.price = [0.7,0.7,0.7,4,40,45,2,30,12,2,0.4]
            #0盐酸，1氢氧化钠，2次氯酸钠，3亚硫酸氢钠,4阻垢剂，5非氧杀菌剂6PAC,7PAM 8EDTA 9碳酸钠，10石灰
        self.k = [800,1200,3000,1500]   #0列管水-水，1列管水-蒸汽，2板换，3螺旋板


    def check(self,a,b,c):  #a是大类，b是小类，c是编号
        if a == 'water' and b in self.water.keys():
            self.value = float(self.water.get(b,c)[c])
        elif a == 'ufmem' and b in self.ufmem.keys():
            self.value = float(self.ufmem.get(b,c)[c])
        elif a == 'romem' and b in self.romem.keys():
            self.value = float(self.romem.get(b,c)[c])
        else:
            self.value =1
        print(self.value)

    def check_uf(self,a):
        self.uf_value = self.ufmem[a]


class Mem_choose():
    def __init__(self,a):
        self.a = a
        if a < 350:
           self.out = '建议使用苦咸水膜'
        elif a < 70 and a >35:
            self.out  ='建议使用海水淡化膜'
        elif a>70 and  a<110:
            self.out = '建议使用超高压浓缩膜'
        else :
            self.out = '建议使用蒸发浓缩方式'



class Pip_diameter():  #管径计算
    def __init__(self,flow,speed):      #输入进水流量t/h和设定流速m/s，计算获取管径和实际流速
        self.flow = flow
        self.speed = speed

        self.p_d = sqrt(self.flow*4/self.speed/3.14/3600)*1000
        print('计算管径值为:   %.2fmm' %self.p_d)
        dn_list = [10,15,20,25,32,40,50,65,80,100,125,150,200,250,300,350,400]
        for i in dn_list:
            if i > self.p_d:
                self.dn = i
                self.f_speed = round(self.flow*4*1000*1000/3600/3.14/self.dn/self.dn,2)
                print('设计流速为:   %.2fm3/h' %self.f_speed)
                print('设计管径为:   %dmm' % self.dn)
                break
        self.pip = [self.dn,self.f_speed]


class Pump_power():  #功率计算
    def __init__(self,flow,press,eff):      #输入进水流量t/h和设定压力m，计算轴功率和电机功率
        self.flow = flow
        self.press = press
        self.eff = eff
        self.power = self.flow*self.press*9.8/367/self.eff
        dn_list = [0.55,0.75,1.1,2.2,3,4,5.5,7.5,11,15,18.5,22,30,45,55,75,90,110,132,160,185,200,220,250]
        for i in dn_list:
            if i > self.power*1.1:
                self.power_1 = i
                print('设计轴功率为:   %.2fkw' %self.power)
                print('设计电机功率为:   %.2fkw' % self.power_1)
                break
        self.pp = [self.power,self.power_1]

class Lsi():  #计算朗格里尔指数
    def __init__(self,a,b,c,d,e):     #a为TDS，B为钙浓度，C为碱度,d为温度，e为ph  均以mg/l
        a1 = 0.0418*log(a)-0.0942     #TDS系数
        b1 = 0.4335 * log(b+1) - 0.3923  #钙换算
        c1 = 0.4346 * log(c) - 0.0003   #碱换算
        d1 =  2.5547-0.0222*d           #温度换算
        phs = 9.3+ a1 + d1 -b1-c1 #a1为含盐量矫正值，d1为温度校正值，b1为钙值，c1为碱值
        self.lsi = round(e - phs,2)
        self.rsi = round(2*phs-e,2)
        if self.lsi < 0:
            print('Lsi为%f,Rsi为%f'%(self.lsi,self.rsi))
            print('碳酸钙不结垢.')
        else:
            print('Lsi为%f,Rsi为%f'%(self.lsi,self.rsi))
            print('请加阻垢剂或调节pH以防止结垢.')

class Scaling_cal():  #计算结垢

  def  __init__(self,a):   #阻垢计算，传入离子列表列表中依次为（TDS,回收率，钠，钙，镁，钾，氨氮，铁，钡，氯，硫酸根，氟，碳酸氢根，硝酸根，磷酸根，系统脱盐率,碱度，温度，ph,二氧化硅）
     self.ee_list = a
     c_cl = int(self.ee_list[9])/35.5/1000
     c_so4 = int(self.ee_list[10])/96/1000
     c_no3 = int(self.ee_list[13]) / 62/1000
     c_f  = int(self.ee_list[11]) / 19/1000
     c_ca = int(self.ee_list[3]) / 40/1000
     c_mg = int(self.ee_list[4]) / 24/1000
     c_nh4 = int(self.ee_list[6]) / 18/1000
     c_hco3 =int(self.ee_list[12]) / 61/1000
     c_na = int(self.ee_list[2]) / 23/1000
     c_k  = int(self.ee_list[5])/39/1000
     c_fe = int(self.ee_list[7]) / 56/1000
     c_ba = int(self.ee_list[8])/ 137/1000
     c_po4 = int(self.ee_list[14]) / 95/1000
     huishou_lv = int(self.ee_list[1])
     x_tuoyan = int(self.ee_list[15])


     self.cc = (1-(1 - x_tuoyan /100) * huishou_lv/100) / (1 - huishou_lv/100) #浓缩倍数
     self.tds = self.ee_list[0]   #进水TDS
     self.tds_out = self.tds*self.cc                                                                       #浓水渗透压
     self.ca_out = int(self.ee_list[3]) * self.cc
     self.hco3_out =int(self.ee_list[12]) * self.cc

     self.press_in = (c_cl + c_so4+ c_no3 + c_hco3 + c_f + c_ca + c_mg + c_na+c_k+c_fe+c_ba+c_po4+c_nh4) / 100*8.314*298          #进水渗透压
     self.press_out = self.press_in*self.cc                                           #出水渗透压
     self.strength = 0.5*(c_cl+c_so4*4+c_no3+c_f+c_ca*4+c_mg*4+c_nh4+c_hco3+c_na+c_k+c_fe*4+c_ba*4+c_po4*9)*self.cc
     #浓缩液中的离子强度
     print('此浓缩液的离子强度为%.3f'%self.strength)
     if self.strength <0.01:
        ksp_caso4 = 4.36*e-5
     elif self.strength <0.05:
        ksp_caso4 = (self.strength*3.9 + 0.01) * 0.001
     elif self.strength < 0.1:
        ksp_caso4 = (self.strength*2 + 0.1) * 0.001
     elif self.strength < 0.2:
        ksp_caso4 = (self.strength*2 + 0.1) * 0.001
     elif self.strength < 0.5:
        ksp_caso4 = (self.strength*0.66 + 0.17) * 0.001
     elif self.strength < 1.0:
        ksp_caso4 = (self.strength*1.6 + 0.2) * 0.001
     elif self.strength < 2.0:
        ksp_caso4 = (self.strength+0.8)*0.001
     else:
        ksp_caso4 = (self.strength + 0.8) * 0.001
     ksp_caso4_out = c_ca*c_so4*self.cc*self.cc   #浓缩液中硫酸钙的离子积
     self.ksp_caso4 = ksp_caso4_out/ksp_caso4

     print('原水渗透压为%.2fbar'%self.press_in)
     print('浓水的渗透压是%.2fbar'%self.press_out)
     print('原水的TDS为%.2fmg/l'%self.tds)
     print('浓水离子积%.5f'%ksp_caso4_out)
     print('浓水溶度积%.5f'%ksp_caso4)
     if ksp_caso4 > ksp_caso4_out:                                              #判断溶度积大于离子积
        print(
                    '\n\n浓缩液溶度积为%.2f,离子积为%f，结垢计算硫酸钙为未饱和,'%(ksp_caso4,ksp_caso4_out))


        print('硫酸钙未饱和')
     else:
        print(
                    '\n\n浓缩液溶度积为%f,离子积为%f，结垢计算硫酸钙饱和,请降低回收率或除钙软化'%(ksp_caso4,ksp_caso4_out))
        print('硫酸钙饱和')

     self.ksp_caco3 = Lsi(self.tds,int(self.ee_list[3]),int(self.ee_list[16]),int(self.ee_list[17]), float(self.ee_list[18]))  #a为TDS，B为钙浓度，C为碱度,d为温度，e为ph
     self.ksp_caco3_out = Lsi(self.tds*self.cc, int(self.ee_list[3])*self.cc, int(self.ee_list[16])*self.cc, int(self.ee_list[17])*self.cc, float(self.ee_list[18]))
     self.lsi = self.ksp_caco3_out.lsi
     self.rsi = self.ksp_caco3_out.rsi
     print(
                     '\n浓水中的LSI值为%f,小于O为溶解趋势，大于0为结垢趋势' %self.lsi)
     self.ksp_fca = c_ca*c_f*c_f/(5.3e-9)
     self.ksp_fba = c_ba*c_f*c_f/(1.84e-7)
     self.ksp_baso4 =c_ba*c_so4/(1.1e-10)
     self.ksp_sio2 = int(self.ee_list[19])*self.cc/100

class Ex_hot():  #计算换热
    def __init__(self, a,b,c,d,e,f):  # 输入（热进，热出，冷进，冷出，热水流量，传热系数）
        t1 = a -d
        t2 = b -c
        t3 = t1/t2   #热介质进出口温差和冷介质进出口温差之比
        t4 = (t1-t2)/log(t1/t2) #平均对数温差
        t5 = (t1+t2)/2          #算数平均温差
        f1 = e
        k1 = f
        self.f2 = f1*(a - b) / (d - c)
        if t3>1.7:
            t = t4
            self.s= f1*1000*(a-b)*4.2/3.6/t/k1
        else:
            t = t5
            self.s = f1 * 1000 * (a - b) * 4.2 / 3.6 / t / k1
        print('所需冷媒流量为%.2ft/h,所需换热器面积为%.2fm2'%(self.f2,self.s))

class Ex_ion():
    # def init(self):
    #     pass
    def na(self,a):
        a  = a/23
        return a
    def ca(self,a):
        a  = a/20
        return a
    def mg(self,a):
        a  = a/12
        return a
    def k(self,a):
        a  = a/39
        return a
    def nh3(self,a):
        a  = a/14
        return a
    def fe(self, a):
        a = a / 28
        return a
    def ba(self, a):
        a = a / 68.5
        return a
    def cl(self, a):
        a = a / 35.5
        return a
    def so4(self, a):
        a = a / 48
        return a
    def f(self, a):
        a = a / 14
        return a
    def hco3(self, a):
        a = a / 61
        return a
    def no3(self, a):
        a = a / 62
        return a
    def po4(self, a):
        a = a / 32
        return a

class Cost():   #费用计算
    def __init__(self, a, b):  # 输入（项目，用量kg）   #0盐酸，1氢氧化钠，2次氯酸钠，3亚硫酸氢钠,4阻垢剂，5非氧杀菌剂6PAC,7PAM 8EDTA
        p = Datebase()
        price = p.price
        self.a = a
        if a == '盐酸':
            self.a = round(price[0] * b,0)
        elif a == '氢氧化钠':
            self.a = round(price[1] * b,0)
        elif a == '次氯酸钠':
            self.a = round(price[2] * b,0)
        elif a == '亚硫酸氢钠':
            self.a = round(price[3] * b,0)
        elif a == '阻垢剂':
            self.a = round(price[4] * b,0)
        elif a == '非氧杀菌剂':
            self.a = round(price[5] * b,0)
        elif a == 'PAC':
            self.a = round(price[6] * b,0)
        elif a == 'PAM':
            self.a = round(price[7] * b,0)
        elif a == 'EDTA':
            self.a = round(price[8] * b,0)
        elif a == '碳酸钠':
            self.a = round(price[9] * b,0)
        elif a == '氧化钙':
            self.a = round(price[10] * b,0)
        else:
            self.a = 0.00000001



if __name__ == '__main__':
     a = Lsi(1076,500,280,35,7)
     print(a.lsi)