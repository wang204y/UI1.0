#coding= utf-8
import win32com
from win32com.client import Dispatch, constants,gencache
import os,sys


class Word():  #word类
    def __init__(self,filename = None):      #输入参数列表
        self.wdApp = Dispatch('Word.Application')#建立链接启动word
        self.wdApp.Visible = 0             #后台运行，不显示
        self.wdApp.DisplayAlerts = 0       #不警告
        self.filename = os.path.dirname(__file__) + '/res/' +filename   #当前路径转为绝对路径
        print(self.filename)
        if os.path.exists(self.filename):
            self.ddoc = self.wdApp.Documents.Open(self.filename)
            print(11111)
        else:
            self.ddoc = self.wdApp.Documents.Add()
            print(33333)
            # self.doc.SaveAs(self.filename)
    def replace_doc(self,string,new_string):
        self.wdApp.Selection.Find.ClearFormatting()
        self.wdApp.Selection.Find.Replacement.ClearFormatting()
        self.wdApp.Selection.Find.Execute(string, False, False, False, False, False, True, 1, True, new_string, 2)
        # string 搜索文本，True 区分大小写，完全匹配单词，使用通配符，同音，查找单词的各种形式，向文档尾部搜索，排格式的文字，
        # new_string 替换文本，2 全部替换
    def save(self):
        # self.ddoc.Save()
        pass
    def save_as(self):
        self.path  = 'D:/RO.docx'
        print(self.path)
        try:
            for i in range(200):
                if os.path.exists(self.path):
                    n = str(i)
                    self.path = 'D:\\'  + n + 'RO.docx'
                    self.ddoc.SaveAs(self.path)
                    break
                else:
                    self.ddoc.SaveAs(self.path)
                    break
        except Exception as e :
            print(e)
    def close(self):
        self.ddoc.Close()
        self.wdApp.Quit()
    def form(self,a,b,c,d):
        t1 = d
        self.ddoc.Tables[a].Rows[b].Cells[c].Range.Text = t1
        pass

    def wd2pdf(self):
        n = '0'
        self.path1 =  'D:/' + n + 'RO膜计算书.pdf'
        for i in range(200):
            if os.path.exists(self.path1):
                n = str(i+1)
                self.path1 = 'D:/' + n + 'RO膜计算书.pdf'
            else:
                self.ddoc.SaveAs(self.path1,FileFormat=17)  #17为PDF,16为DOCX，4为txt,10为HTML
                break

if __name__ =='__main__':
    # path = 'E:/xxx.docx'
    # doc = Word(path)
    # doc.replace_doc('aaa','bbb')

    path = 'jisuanshu.docx'
    doc1 = Word(path)
    doc1.form(1,2,2,'你很好')
    doc1.save_as()
    doc1.wd2pdf()
    doc1.close()