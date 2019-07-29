#coding = utf-8
class Softner_by_chemical():  #化学软化
    def  __init__(self,i1,i2,i3,i4,i5):
        self.ca = int(i1)
        self.mg = int(i2)
        self.hco3 = int(i3)
        self.ph = i4
        pass
    def softner_cal_cana(self):
        pass
    def softner_cal_nana(self):
        pass
    def softner_cal_ca(self):
        pass

class Sofener_by_resin():  #树脂软化
    pass

class Heat_exchanger(): #换热器
    pass

class Inclined_plate():  #斜板沉淀池
    pass

class Sf():#砂滤器
    pass

class Cf():#活性炭滤器
    pass

class Uf():#超滤
    pass

class Ro():#RO
    def __init__(self,a):    #a进水流量，b进水Tds，c脱盐率，d水透过系数，e进水渗透压,f膜面积,p进水压力
        self.a = a[0]
        self.b = a[1]
        self.c = a[2]
        self.d = a[3]
        self.e = a[4]
        self.f = a[5]
        self.p = a[6]
        self.ro_one()
    def ro_one(self):
        self.ds_tds =round(self.b*(1-self.c),2)  #产水TDS
        self.ds_flow = round(self.d*self.f*((self.p-0.05)-1.1*self.e)/1000,2)  #0.05为淡水侧压力，1.2为浓差极化度。
        self.ns_flow =round( self.a - self.ds_flow,2)
        self.ns_tds = round((self.a*self.b-self.ds_tds*self.ds_flow)/self.ns_flow,2)
        print('进水流量%.2fm3/h,进水TDS%.0fmg/l,产水流量%.2fm3/h,产水TDS%.2fmg/l,浓水TDS%.2fTDS,浓水流量%.2fm3/h,'%(self.a,self.b,self.ds_flow,self.ds_tds,self.ns_tds,self.ns_flow))


class RO_press():
    def __init__(self,a,b,c,d):  #a是平均通量，b是水通过系数，c是进水渗透压，d是回收率
        self.ndp = a /b           #净推动压力为平均通量除以水通量
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def press(self):
        self.pf = self.ndp + 0.01 + (self.c + self.c / (1 - self.d)) / 2  # 进水压力为渗透压平均差+净推动压力+淡液渗透压
        return self.pf


class RO_design(Ro):
    def __init__(self,a,b):  #b是膜壳元件数,a进水流量，进水TDS,脱盐率，水通量，进水渗透压，膜面积，进水压力
        self.a = a
        self.b = b
    def design(self):
        self.j = 0
        for i in range(0,self.b) :
            self.f = Ro(self.a)
            self.c = self.f.ns_flow
            self.d = self.f.ns_tds
            self.j = self.j + self.f.ds_flow
            self.l = round(self.f.e*self.f.ns_tds/self.f.b,2)
            self.p = round(self.f.p-0.015,2)
            self.a = [self.c,self.d,self.a[2],self.a[3],self.l,self.a[5],self.p]    #进水流量，tds, 脱盐率，水通量，渗透压，膜面积，进水压力
            print( '渗透压%.2f mpa'
                  '给水压力%.2f mpa'%(self.a[4],self.a[6]))
        return [self.c,self.d,self.l,self.p,self.j]   #返回进水流量，TDS,渗透压，进水压力,产水流量

        print(self.j)    #产水量
        print('****************************************')


class RO_design_sys():
    def __init__(self,a,b):  #a第一段膜壳数，第二段膜壳数，第三段膜壳数，第四段膜壳数....
        # b            0进水流量，1进水TDS,2脱盐率，3水通量，4进水渗透压，5膜面积，6单位通量,7回收率
        self.a = a
        self.f = b[0]
        self.tds = b[1]
        self.press_shentou = b[4]
        self.press = RO_press(b[6],b[3],b[4],b[7]).press()
        # self.list1 = [f,b[1],b[2],b[3],b[4],b[5],self,press]
        print('运行压力是:   %.2f Mpa' %self.press)
        self.l = 0
        for i in  self.a :
            self.list1 = [self.f / i,self.tds, b[2], b[3], self.press_shentou, b[5], self.press]
            self.c = RO_design(self.list1,6).design()
            self.f = self.c[0]*i  #浓水汇总
            print(self.f)
            self.tds = self.c[1]
            self.press_shentou = self.c[2]
            self.press = self.c[3]
            self.l=self.l+self.c[4]
            print('------------------------------')
        print(self.l)    #产水量


class Edi():#电除盐
    pass

class Ed():#电渗析
    pass

class Mixed_bed():#混床
    pass

class Ozone():#臭氧
    def  __init__(self,a,b):  #输入a[0处理量，1COD进，2COD出]b[0臭氧停留时间，1活性炭停留时间，2加药比，3循环量，4催化剂高度，
        # 5氧化池高度，6氧化池数量，7催化池数量，8反洗时间，9反洗间隔，10气洗强度，11水洗强敌，12曝气强度]
        self.f = a[0]
        self.cod_in = a[1]
        self.cod_out = a[2]
        self.v_o3 = self.f*b[0]            #氧化池体积
        self.v_c = self.f*b[1]             #填料体积（活性炭）
        self.o3 = self.f*(self.cod_in - self.cod_out)*b[2]/1000     #臭氧耗用量
        self.f1 = self.f*b[3]                                #循环泵流量
        self.t_c = self.v_c*0.55                           #活性炭质量
        self.t_s =  self.v_c/b[4]*0.3*1.6                  #石英砂质量
        self.n_o3 = self.f/b[5]*2                          # 曝气盘数量（0.5m2/个）
        self.s_o3 = self.f/b[5]                              #氧化池面积
        self.s_c =  self.v_c/b[4]                            #活性炭池面积
        self.s_o3_n = self.s_o3/b[6]                        #单个氧化池面积
        self.s_c_n = self.s_c / b[7]                        #单个活性炭池面积
        self.v_bash_w = self.s_c_n*3.6*b[11]                 #反洗泵流量
        self.v_bash_g = self.s_c_n*3.6*b[10]/60              #反洗风机流量
        self.v_g = self.s_c * b[12]/60                      #曝气风机流量
        self.v_w = self.v_bash_w*b[8]/60/b[9]
        print('氧化池体积%.2f'%self.v_o3)
        print('活性炭体积%.2f'%self.v_c)
        print('臭氧量%.2f'%self.o3)
        print('循环泵流量%.2f'%self.f1)
        print('活性炭质量%.2f'%self.t_c)
        print('石英砂质量%.2f'%self.t_s)
        print('曝气盘数量%.2f'%self.n_o3)
        print('氧化池面积%.2f'%self.s_o3)
        print('活性炭池面积%.2f'%self.s_c)
        print('单个氧化池面积%.2f'%self.s_o3_n)
        print('单个碳池面积%.2f'%self.s_c_n)
        print('反洗泵流量%.2f'%self.v_bash_w)
        print('反洗风机流量%.2f'%self.v_bash_g)
        print('曝气风机流量%.2f'%self.v_g)
        print('反洗耗水量%.2f'%self.v_w)

if __name__ == '__main__':
   a = [6,3,1]#各段膜数量
   b =  (70,4000,0.97,60,0.3,37,15,0.75)
   RO_design_sys(a,b)

