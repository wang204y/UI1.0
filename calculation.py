#coding = utf-8
from  math  import *
from cal_tool import *
class Softner_by_chemical():  #化学软化
    def __init__(self,i1,i2,i3,i4,i5,i6):   #钙含量，镁含量，碳酸氢根含量，目标钙，目标镁，水量
        self.m_ca = (i1-i4)/40
        self.m_mg = (i2-i5)/24
        self.m_hco3 = i3/61
        self.l = i6
        pass
    def softner_cal_cana(self):  #石灰碳钠软化
        cao = self.m_hco3*28  #暂时硬度消耗的氧化钙
        solid_1 = self.m_hco3*100 #暂时硬度产生的泥量
        solid_2 = (self.m_ca- self.m_hco3/2)*100+self.m_mg*58  #永久硬度产生的泥量
        na2co3 = (self.m_ca+self.m_mg- self.m_hco3/2)*106   #碳酸钠用量
        hcl = 100 / 60 * 36.5 + 0.001 * 36.5 * 1000  # 过量100mg/l的碳酸钠及PH11调至中性需要氯化氢量
        m_cao = cao*self.l/1000/0.9   #需要90%氢氧化钠质量  kg
        m_na2co3  = na2co3*self.l/1000/0.99  #需要99%碳酸钠质量 kg
        m_hcl = hcl*self.l/1000/0.31    #需要31%盐酸量   kg
        m_solid = (solid_1+solid_2)*self.l/1000/0.5  #50%含水污泥量  kg
        c1 = Cost('氧化钙',m_cao)
        c2 = Cost('碳酸钠', m_na2co3)
        c3 = Cost('盐酸', m_hcl)
        c_all= c1.a +c2.a+c3.a
        c_cost = c_all/self.l
        self.cost = [cao,na2co3,hcl,m_cao,m_na2co3,m_hcl,c_all,c_cost,m_solid]
        print(self.cost)
        pass
    def softner_cal_nana(self):   #两碱法软化
        naoh = self.m_mg*2*40+  self.m_hco3*40 #氢氧化钠用量
        na2co3 = self.m_ca *106 - self.m_hco3*106 #碳酸钠用量
        solid = self.m_ca*100+self.m_mg*58
        hcl = 100/60*36.5 +0.001*36.5*1000   #过量100mg/l的碳酸钠及PH11调至中性需要氯化氢量
        if na2co3 <0:
            na2co3 = 0
        m_naoh = naoh*self.l/1000/0.3   #需要30%氢氧化钠质量  kg
        m_na2co3  = na2co3*self.l/1000/0.99  #需要99%碳酸钠质量 kg
        m_hcl = hcl*self.l/1000/0.31    #需要31%盐酸量   kg
        m_solid = solid*self.l/1000/0.5  #50%含水污泥量  kg
        c1 = Cost('氢氧化钠',m_naoh)
        c2 = Cost('碳酸钠', m_na2co3)
        c3 = Cost('盐酸', m_hcl)
        c_all= c1.a +c2.a+c3.a
        c_cost = c_all/self.l
        self.cost = [naoh,na2co3,hcl,m_naoh,m_na2co3,m_hcl,c_all,c_cost,m_solid]
        print(self.cost)
    def softner_cal_ca(self):     #石灰软化
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

class Uf_sys():#超滤
    def __init__(self,a,b,c):  #a膜参数（0膜面积，1运行时间min，2冲洗时间s，3反洗流量lpm，4气洗流量
        # ,5清洗流量，6CEB药剂（酸碱次钠周期），7CIP药剂（酸碱次钠周期）,8单支清洗用量，
        # b设计参数（0设计通量，1设计膜堆数量,2设计进水泵数量）,c设计处理量
        self.a = a
        self.b = b
        self.c = c
    def uf_cal(self):
        m_mj = self.a[0] #膜面积
        m_tl = self.b[0] #设计通量
        m_h = self.a[1]+self.a[2]/60 #每周期用时min
        n_yx = 24*60/m_h  #每天运行周期
        m_h1 = 24*self.a[1]/m_h#日实际运行时间
        m_h2 = 24-m_h1   #反洗消耗时间
        f = self.c / m_h1 #实际运行流量 m3/h
        n_mj = f*1000/self.b[0]/self.a[0]  #计算膜数量
        n_mdj = n_mj/self.b[1]   #计算单膜堆的膜数量
        n_mds = ceil(n_mdj/4)    #4排向上取整,实际膜对（4排）
        n_ms = n_mds*4*self.b[1]  #实际膜数量
        n_ms_dt = n_mds*4
        s_ms = n_ms*self.a[0]
        f_ms = f*1000/self.a[0]/n_ms #校正运行流量
        f_fx = self.a[3]*n_mds*4*self.a[0]/1000   #反洗流量
        v_fx =  f_fx*60/3600*n_yx #反洗耗水量
        v_zx =  f *30/3600*n_yx  #正洗耗水量
        v_fs = v_fx+v_zx  #废水量
        v_js = self.c - v_fs #净产水量
        k_hs  = v_js/self.c  #回收率
        p_js  = f/self.b[2]   #进水泵流量
        p_fj = self.a[4]*n_mds*4/60  #空压机nm3/min
        p_qx = self.a[5]*n_mds*4  #CIP泵流量
        p_fx = f_fx    #反洗泵流量
        v_cqg = p_fj/2/4 #气洗储气罐30S用气，压力4bar
        p_hcl =self.a[6][0] *f_fx/0.31*10              #CEB  用0.1%盐酸计量泵L/h
        p_naoh =self.a[6][1]*f_fx /0.3*10              #CEB  用0.05%碱计量泵L/h
        p_naclo =self.a[6][2] *f_fx/0.1*10            #CEB  用0.1%次钠计量泵L/h
        v_hcl = self.a[7][0]*self.a[8]/0.31        #CIP 用0.2%盐酸计量泵    m3/次
        v_naoh = self.a[7][1] * self.a[8]/0.3       #CIP  用0.1%碱计量泵    m3/次
        v_naclo = self.a[7][2] * self.a[8]/0.1       #CIP  用0.2%次钠计量泵 m3/次
        v_hcl_year = p_hcl/60*(8000/self.a[6][3])+v_hcl*8000/self.a[7][3]         #年盐酸耗用
        v_naoh_year = p_naoh / 60 * (8000 / self.a[6][3]) + v_naoh * 8000 / self.a[7][3] #年氢氧化钠耗用
        v_naclo_year = p_naclo / 60 * (8000 / self.a[6][3]) + v_naclo * 8000 / self.a[7][3]  #年次钠耗用
        p_1 = Pump_power(p_js,2.5,0.7)  #进水泵功率计算
        p_2 = Pump_power(p_fx,2,0.7)  #反洗泵
        p_3 = Pump_power(p_qx, 2, 0.7) #清洗泵
        p_4 = Pump_power(p_fj, 4.7, 0.7)  #空压机 (7bar是，k是4.71，8bar时K是5.07,6bar时是4.31）
        if p_4.pp[1] < 7.5:
            p_4.pp[1] = 7.5
        p1_all = p_1.pp[0]*self.b[2]*m_h1+p_2.pp[0]*m_h2*0.5+p_3.pp[0]*0.1+p_4.pp[0]*m_h2*0.25+1.11      #日运行功率
        p2_all = p_1.pp[1] * self.b[2] + p_2.pp[1] + p_3.pp[1] + p_4.pp[1]+1.11  #装机功率之和
        c_1 = Cost('盐酸',v_hcl_year)
        c_2 = Cost('氢氧化钠', v_naoh)
        c_3 = Cost('次氯酸钠', v_naclo_year)
        c_all = c_1.a+c_2.a+c_3.a       #年药剂费用之和
        p_water = p1_all*0.7/self.c  #吨水电耗  （以0.7元/kwh计，8000小时，330天运行计算）
        c_all = c_all/self.c/330    #吨水药耗
        costs_all = p_water + c_all  #吨水直接运行费用
        self.list_1 = [p_1.pp,p_2.pp,p_3.pp,p_4.pp,p1_all,p2_all,p_water,c_all,costs_all]  #0 进料泵轴功装功，1反洗泵轴功装功
        #  2清洗泵轴功装机3空压机轴功装机，4日运行功率,5装机功率 6 吨水电耗，7吨水药耗 8直接运行费用
        self.list =[n_ms,s_ms,self.b[1],n_ms_dt,f_ms,self.c,v_fs,v_js ,k_hs,p_js,p_fx,p_fj,p_hcl,p_naoh,p_naclo,p_qx,v_cqg,v_hcl_year,v_naoh_year,v_naclo_year]
        #0膜总数量,1膜总面积，2膜套数，3单套膜数量，4矫正运行通量，5进水量，6废水量，7净产水量，
        # 8回收率，9进水泵，10反洗泵，11空压机，12盐酸加药泵，13碱加药泵，14次钠加药泵，15清洗泵，16储气罐，17盐酸年耗用量，18碱年耗用量，19次钠年耗用量
        print(self.list)
        print('1、膜总数量: %d支  \n2、膜总面积:  %d m2\n3、膜套数:  %d 套\n4、单套膜数量:  %d 支\n5、运行通量:  %f l/m2.h\n6、进水量:  %f m3/h'
              '\n7、废水量:  %f m3/d\n8、净产水量:  %f m3/d\n9、回收率:  %f \n10、进水泵:  %f m3/h\n11、反洗泵:  %f m3/h'
              '\n12、空压机:  %f nm3/min\n13、盐酸加药泵:  %f kg/h\n14、碱加药泵:  %f kg/h\n15、次钠加药泵:  %f kg/h'
              '\n16、清洗泵:  %f m3/h\n17、储气罐:  %f m3\n18、盐酸年耗用:  %f kg/y\n19、碱年耗用:  %f kg/y'
              '\n20、次钠年耗用:  %f kg/y'%(self.list[0],self.list[1],self.list[2],self.list[3],self.list[4],self.list[5],self.list[6]
                                                    , self.list[7],self.list[8],self.list[9],self.list[10],self.list[11],self.list[12]
                                                    , self.list[13],self.list[14],self.list[15],self.list[16],self.list[17],self.list[18],self.list[19]))
        print(self.list_1)


class Ro():#单支RO计算
    def __init__(self,a):    #a进水流量，b进水Tds，c脱盐率，d水透过系数，e进水渗透压,f膜面积,p进水压力,nc浓差极化度
        self.a = a[0]
        self.b = a[1]
        self.c = a[2]
        self.d = a[3]
        self.e = a[4]
        self.f = a[5]
        self.p = round(a[6],2)
        self.nc = a[7]
        self.ro_one()
    def ro_one(self):
        self.ds_tds =round(self.b*(1-self.c),2)  #产水TDS
        self.ds_flow = round(self.d*self.f*((self.p-0.01)-self.nc*self.e)/1000,2)  #0.01为淡水侧压力。
        self.ds_yhl = self.ds_tds*self.ds_flow    #淡水盐含量等于淡水流量乘以淡水TDS
        self.ns_flow =round( self.a - self.ds_flow,2)
        self.ns_tds = round((self.a*self.b-self.ds_yhl)/self.ns_flow,2)
        self.list = [self.p,self.a,self.b,self.ds_flow,self.ds_tds,self.ns_tds,self.ns_flow,self.ds_yhl]  #进水压力，进水流量，进水电导，产水流量，产水电导，浓水电导，浓水流量，淡水含盐质量
        print('进水流量%.2fm3/h,进水TDS%.0fmg/l,产水流量%.2fm3/h,产水TDS%.2fmg/l,浓水TDS%.2fTDS,浓水流量%.2fm3/h,'%(self.a,self.b,self.ds_flow,self.ds_tds,self.ns_tds,self.ns_flow))


class RO_press():  #初始压力计算
    def __init__(self,a,b,c,d):  #a是平均通量，b是水通过系数，c是进水渗透压，d是回收率
        self.ndp = a /b           #净推动压力为平均通量除以水通量
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def press(self):
        self.pf = self.ndp  + (self.c + self.c / (1 - self.d)) / 2 -0.1 # 进水压力为渗透压平均差+净推动压力
        return self.pf


class RO_design():   ##单支膜管设计计算
    def __init__(self,a,b,c):  #c是压差系数，b是膜壳元件数,a进水流量，进水TDS,脱盐率，水通量，进水渗透压，膜面积，进水压力 浓差极化度
        self.a = a   #包含浓差极化度
        self.b = b
        self.c_m = c #压差系数
        self.ty = a[2]
    def design(self):
        self.j = 0
        self.list = []
        self.ds_yhl = 0
        for i in range(0,self.b) :
            print(self.a)
            self.f = Ro(self.a)           #单支RO膜计算并输出结果
            self.ds_yhl  += self.f.ds_yhl
            self.c = self.f.ns_flow       #浓水流量变更为下支膜进水流量
            self.tyl = self.ty*(0.9930+0.0007*self.c)
            self.d = self.f.ns_tds        #浓水TDS变更为下支膜进水TDS
            self.j = self.j + self.f.ds_flow     #淡水流量累加值
            self.l = round(self.f.e*self.f.ns_tds/self.f.b,2)  #进水渗透压*浓水TDS/进水TDS
            self.k = (self.c*self.c / 64)  * self.c_m           #差压系数根据浓液流量变化
            self.p = round(self.f.p-0.02*self.k,2)          #下段浓水压力
            self.a = [self.c,self.d,self.tyl,self.a[3],self.l,self.a[5],self.p,self.a[7]]
            #进水流量，tds, 脱盐率，水通量，渗透压，膜面积，进水压力,浓差极化度（输入条件重新复制）
            self.list.append(self.f.list)
            print( '渗透压%.2f mpa'
                  '浓水压力%.2f mpa'%(self.a[4],self.a[6]))
            print('****************************************')
        print(self.list)
        return [self.c,self.d,self.l,self.p,self.j]   #返回进水流量，浓水TDS,浓水渗透压，进水压力,产水流量


class RO_design_sys():
    def __init__(self,a,b,c,d,e,f1,f2):  #a第一段膜壳数，第二段膜壳数，第三段膜壳数，第四段膜壳数....
        # b            0进水流量，1进水TDS,2脱盐率，3水通量，4进水渗透压，5膜面积，6单位通量,7回收率
        # c      单支膜壳内元件数量   d是膜压差系数，e是水浓差极化度
        self.d = d  #膜压差系数
        self.e_e = e  #浓差极化度
        self.a = a   #膜壳列表
        self.f = b[0]   #进水流量
        self.tds = b[1]   #进水tds
        self.m_n = c       #膜壳内元件数
        self.ls = self.f*b[7]   #淡水流量
        self.ns = self.f - self.ls
        self.press_shentou = b[4]    #进水渗透压
        self.press = RO_press(b[6],b[3],b[4],b[7]).press()   #进水压力初步估算值
        self.m_add = f1
        self.p_add = f2
        # self.list1 = [f,b[1],b[2],b[3],b[4],b[5],self,press]
        print('初始运行压力是:   %.2f Mpa' %self.press)       #打印初次进水压力
        n = 0
        self.l = 0                                         #初始累计流量
        while(self.l < self.ls):                          #判断累计流量与淡水设计通量比较
            self.f = b[0]           #赋值进水流量重新
            self.tds =b[1]           #进水tds重新赋值
            self.press_shentou = b[4]   #进水渗透压重新赋值
            self.l = 0                  #累计流量重新赋值
            self.press = RO_press(b[6], b[3], b[4], b[7]).press()+0.01*n
            print('更新运行压力是:   %.2f Mpa' % self.press)          #打印运行压力
            m = 0
            self.list = []     #膜数据清单定义
            self.ds_yhl = 0
            for i in  self.a :   #获取列表中膜壳排列
                self.list1 = [round(self.f / i,2),self.tds, b[2], b[3], self.press_shentou, b[5], self.press,self.e_e]#清单1流量，2TDS,3脱盐率4水通量5渗透压6膜面积7进水压力8浓差极化度
                print(self.list1)
                self.c1 = RO_design(self.list1,self.m_n,self.d)  #输入列表，膜壳元件数，压差系数
                self.c = self.c1.design()  #获取设计列表，#1返回进水流量，2浓水TDS,3浓水渗透压，4进水压力,5产水流量
                self.p = self.c1.p  #下支膜进水压力
                self.f = self.c[0]*i  #浓水汇总
                self.tds = self.c[1]   #浓水的TDS
                self.press_shentou = self.c[2]  #浓水的渗透压
                self.press = self.c[3]     #进水压力
                self.l=round(self.l+self.c[4]*i,2)    #产水流量汇总
                m = m+1
                if m == self.m_add:
                    self.press = self.press +self.p_add
                    self.p_add = 0
                    print(self.press)
                    print('****')
                self.list.append(self.c1.list) #添加入数据清单
                self.ds_yhl = self.ds_yhl+self.c1.ds_yhl*i   #淡水盐含量
            self.ns_tds = self.tds   #浓水TDS
            n = n+1
            print('%d 段总产水量是%.2f   m3/h'%(m,self.l))
            print('------------------------------------------------------------------------------')
        self.ds_tds = round(self.ds_yhl/self.l,2)
        self.ns_l =round(b[0]-self.l,2)
        self.list_1 = [b[0],self.ns_l,self.l,b[1],self.ns_tds,self.ds_tds,self.list[0][0][0],self.p,0.01]
        print(self.list_1)
        #进水流量，浓水流量，产水流量，进水TDS，浓水TDS，产水TDS，进水压力，浓缩压力，产水压力
        print(self.list)  #输出集合列表[[[]]]
        print('总产水量为%.2f m3/h' %self.l)    #产水量
        print('产水TDS为%.2f mg/l' %self.ds_tds)


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
        print('氧化池体积%.2f m3'%self.v_o3)
        print('活性炭体积%.2f m3'%self.v_c)
        print('臭氧量%.2f kg/h'%self.o3)
        print('循环泵流量%.2f m3/h'%self.f1)
        print('活性炭质量%.2f 吨'%self.t_c)
        print('石英砂质量%.2f 吨'%self.t_s)
        print('φ180曝气盘数量%.2f 个'%self.n_o3)
        print('氧化池面积%.2f  m2'%self.s_o3)
        print('活性炭池面积%.2f m2'%self.s_c)
        print('单个氧化池面积%.2f m2'%self.s_o3_n)
        print('单个碳池面积%.2f m2'%self.s_c_n)
        print('反洗泵流量%.2f m3/h'%self.v_bash_w)
        print('单池反洗风机流量%.2f Nm3/min'%self.v_bash_g)
        print('曝气风机流量%.2f Nm3/min'%self.v_g)
        print('单池反洗耗水量%.2f t/d'%self.v_w)

if __name__ == '__main__':
   # a = [3,1]#各段膜数量
   # b =  (20,10000,0.99,45,0.6,37,20,0.5) #进水流量，进水TDS，脱盐率，水通量，进水渗透压，膜面积，设计通量，回收率
   # RO_design_sys(a,b,6,1.1,1.1)
   # print('**********************')
   # c = [150,60,20]  #处理量，cod进，COD出
   # d = [1,2.5,1.5,0.4,2.5,6.5,2,2,8,1,12,5,3]              #臭氧设计技术常数,[0臭氧停留时间，1活性炭停留时间，2加药比，3循环量，4催化剂高度，
   #      # 5氧化池高度，6氧化池数量，7催化池数量，8反洗时间，9反洗间隔，10气洗强度，11水洗强敌，12曝气强度],
   # Ozone(c,d)
   a = [70,45,140,80,8,2,[0.1,0.05,0.1,24],[0.2,0.1,0.2,720],75]
   b = [40,2,2]
   c = 5000  #a膜参数（0膜面积，1运行时间min，2冲洗时间s，3反洗流量lpm，4气洗流量nm3/h/支
        # ,5清洗流量，6CEB药剂（酸碱次钠周期），7CIP药剂（酸碱次钠周期）,8单支清洗用量，
        # b设计参数（0设计通量，1设计膜堆数量,2设计进水泵数量）,
        # c设计处理量
   d= Uf_sys(a,b,c)
   d.uf_cal()
   # 0膜总数量,1膜总面积，2膜套数，3单套膜数量，4矫正运行通量，5进水量，6废水量，7净产水量，
   # 8回收率，9进水泵，10反洗泵，11空压机，12盐酸加药泵，13碱加药泵，14次钠加药泵，15清洗泵，16储气罐，17盐酸年耗用量，18碱年耗用量，19次钠年耗用量


    # a = Softner_by_chemical(2000,2000,1000,20,20,100)
    # a.softner_cal_cana()
    # print(a.cost)