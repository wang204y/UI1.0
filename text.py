# coding = utf-8
from math import *


class Datebase():
    def __init__(self):
        text1_1 = '0.1%氢氧化钠或1%的Na4-EDTA（乙二胺四乙酸四钠）,清洗条件：pH12/30℃（最高）,pH13/25℃（最高）'
        text1_2 = '0.1%氢氧化钠或0.025%的十二烷基硫酸钠,清洗条件：pH12/30℃（最高）'
        text1_3 = '0.2%盐酸,清洗条件：pH1/45℃（最高）'
        text1_4 = '2.0%柠檬酸，清洗条件：pH1/45℃（最高）'
        text1_5 = '1.0%连二亚硫酸钠'
        text1_6 = '1.0%亚硫酸氢胺'
        text1_7 = '1.0%连二亚硫酸钠'
        self.text_med = [text1_1, text1_2, text1_3, text1_4, text1_5, text1_6, text1_7]
        text2_1 = '\n直接原因：氧化损坏，存在余氯、臭氧、高锰酸钾等氧化剂，\n处理意见： 更换膜元件，查找并去除氧化源，'
        text2_2 = '\n直接原因：严重背压，产水管正压较大或浓水管存在较大负压，\n处理意见： 更换受损膜元件，去除背压原因，'
        text2_3 = '\n直接原因：严重机械损伤，连接件断裂，\n处理意见： 查找受损处，更换受损连接件，'
        text2_4 = '\n直接原因：o型圈泄漏，安装不正确，\n处理意见： 查找受损处，更换o型圈，'
        text2_5 = '\n直接原因： 膜结垢污染，预处理不当，\n处理意见： 根据结垢污染物选择清洗方法，并改善预处理工艺，'
        text2_6 = '\n直接原因： 压密，水锤或运行压力过高，膜选型不当，\n处理意见： 降低运行压力，更换耐压膜元件，'
        text2_7 = '\n直接原因： 生物、机械杂质或活性炭污染，\n处理意见： 生物污染采用碱性药剂清洗，提高预处理工艺，机械杂质及活性炭污染，采用膜元件单独冲洗或可部分恢复'
        text2_8 = '\n直接原因： 油或有机物聚阳离子污染，\n处理意见： 采用碱性药剂清洗，提高除油，改进预处理工艺'
        self.text_bec = [text2_1, text2_2, text2_3, text2_4, text2_5, text2_6, text2_7, text2_8]

    def choose(self, s):
        if s == '1':  # 脱盐率低，产水量大
            self.text_out = self.text_bec[0] + self.text_bec[1] + self.text_bec[2]  # 氧化和背压
        elif s == '2':  # 脱盐率低，产水量不变，压差不变
            self.text_out = self.text_bec[3]  # o圈损伤
        elif s == '3':  # 脱盐率不变，产水量低，压差后端大
            self.text_out = self.text_bec[4]  # 膜结垢污染
        elif s == '4':  # 脱盐率不变，产水量低，压差前端大
            self.text_out = self.text_bec[6]  # 生物污染或机械杂质
        elif s == '5':  # 脱盐率不变，产水量低，压差不变
            self.text_out = self.text_bec[7]  # 油或有机污染
        elif s == '6':  # 脱盐率低，产水量低，压差不变
            self.text_out = self.text_bec[5]  # 压密
        else:
            self.text_out = '无当前现象，请重新选择'

    def choose_1(self, s1):
        if s1 == '1':
            self.text_out_1 = '优选药剂：\n   ' + self.text_med[1] + '\n 备选药剂：\n   ' + self.text_med[0]
        elif s1 == '2':
            self.text_out_1 = '优选药剂：\n   先用' + self.text_med[1] + '再用' + self.text_med[2] + '\n 备选药剂：\n   先用' + \
                              self.text_med[0] + '再用' + self.text_med[2]
        elif s1 == '3':
            self.text_out_1 = '优选药剂：\n   ' + self.text_med[2] + '\n 备选药剂：\n   ' + self.text_med[3]
        elif s1 == '4':
            self.text_out_1 = '优选药剂：\n   ' + self.text_med[0] + '\n 备选药剂：\n   ' + self.text_med[1]
        elif s1 == '5':
            self.text_out_1 = '优选药剂：\n   ' + self.text_med[1]
        elif s1 == '6':
            self.text_out_1 = '优选药剂：\n   ' + self.text_med[1] + '\n 备选药剂：\n   ' + self.text_med[0]
        elif s1 == '7':
            self.text_out_1 = '优选药剂：\n   ' + self.text_med[4] + '\n 备选药剂：\n   ' + self.text_med[3] + self.text_med[5]


if __name__ == '__main__':
    a = Datebase()
    a.choose('100')
