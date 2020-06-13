import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pylab as mpl
import copy

class infoWin(tk.Tk):
    '''
    文件夹选择程序
    界面与逻辑分离
    '''

    def __init__(self):
        '''初始化'''
        super().__init__()  # 有点相当于tk.Tk()
        self.wm_title("过山车数据查询")
        self.geometry("1550x900")  # #窗口位置500后面是字母x
        self.resizable(0, 0)
        # self.state("zoomed")
        self.df = pd.DataFrame()

        self.createWidgets()

    def createWidgets(self):
        Label = tk.Label(self, text='名字')
        Label.place(x=10, y=10)
        self.entryName = tk.Entry(self)
        self.entryName.place(x=50, y=10, width=100)

        Label = tk.Label(self, text='公园')
        Label.place(x=10, y=40)
        self.entryPark = tk.Entry(self)
        self.entryPark.place(x=50, y=40, width=100)

        Label = tk.Label(self, text='结构')
        Label.place(x=10, y=70)
        self.ddl = ttk.Combobox(self)
        self.ddl['value'] = ('Steel', 'Wildcat', 'Wood')
        self.ddl.place(x=50, y=70, width=100)

        Label = tk.Label(self, text='长度')
        Label.place(x=10, y=100)
        self.entryLength = tk.Entry(self)
        self.entryLength.place(x=50, y=100, width=100)


        Label = tk.Label(self, text='高度')
        Label.place(x=10, y=130)
        self.entryHeight = tk.Entry(self)
        self.entryHeight.place(x=50, y=130, width=100)

        Label = tk.Label(self, text='速度')
        Label.place(x=10, y=160)
        self.entrySpeed = tk.Entry(self)
        self.entrySpeed.place(x=50, y=160, width=100)

        Label = tk.Label(self, text='倒置')
        Label.place(x=10, y=190)
        self.entryInversions = tk.Entry(self)
        self.entryInversions.place(x=50, y=190, width=100)

        Label = tk.Label(self, text='落差')
        Label.place(x=10, y=220)
        self.entryDrop = tk.Entry(self)
        self.entryDrop.place(x=50, y=220, width=100)

        Label = tk.Label(self, text='年份')
        Label.place(x=10, y=250)
        self.entryYear = tk.Entry(self)
        self.entryYear.place(x=50, y=250, width=100)

        tk.Button(master=self, text='搜索', command=self.search).place(x=50, y=280, width=100)
        tk.Button(master=self, text='画大饼', command=self.btn_fig).place(x=50, y=310, width=100)
        '''
        表格
        '''
        self.tree = ttk.Treeview(self, show='headings')  # #创建表格对象
        self.tree["columns"] = ('序号', "名称", "公园", "年份", "结构", "类型", "高度", "长度", "速度", "倒置", '落差')  # #定义列
        self.tree.column("序号", width=50)  # #设置列
        self.tree.column("名称", width=100)  # #设置列
        self.tree.column("公园", width=100)
        self.tree.column("年份", width=50)
        self.tree.column("结构", width=50)
        self.tree.column("类型", width=50)
        self.tree.column("高度", width=50)
        self.tree.column("长度", width=50)
        self.tree.column("速度", width=50)
        self.tree.column("倒置", width=50)
        self.tree.column("落差", width=50)
        self.tree.heading("序号", text="序号")
        self.tree.heading("名称", text="名称")  # #设置显示的表头名
        self.tree.heading("公园", text="公园")
        self.tree.heading("年份", text="年份")
        self.tree.heading("结构", text="结构")
        self.tree.heading("类型", text="类型")
        self.tree.heading("高度", text="高度")
        self.tree.heading("长度", text="长度")
        self.tree.heading("速度", text="速度")
        self.tree.heading("倒置", text="倒置")
        self.tree.heading("落差", text="落差")

        VScroll1 = tk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        VScroll1.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
        # 给treeview添加配置
        self.tree.configure(yscrollcommand=VScroll1.set)
        self.tree.place(x=200, y=10, width=1300, height=330)

        fig = Figure(figsize=(10, 3), dpi=100)
        fig.subplots_adjust(wspace =0.5)
        self.ax1 = fig.add_subplot(241)
        self.ax2 = fig.add_subplot(242)
        self.ax3 = fig.add_subplot(243)
        self.ax5 = fig.add_subplot(245)
        self.ax6 = fig.add_subplot(246)
        self.ax7 = fig.add_subplot(247)
        self.ax8 = fig.add_subplot(248)
        # 指定字体,显示中文
        mpl.rcParams['font.sans-serif'] = ['FangSong']
        mpl.rcParams['axes.unicode_minus'] = False
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().place(x=0, y=340, width=1500, height=550)
        self.canvas._tkcanvas.place(x=0, y=340, width=1500, height=550)

    def search(self):
        entryName = self.entryName.get().strip()
        entryPark = self.entryPark.get().strip()
        ddl = self.ddl.get().strip()
        entryLength = self.entryLength.get().strip()
        entryHeight = self.entryHeight.get().strip()
        entrySpeed = self.entrySpeed.get().strip()
        entryInversions = self.entryInversions.get().strip()
        entryDrop = self.entryDrop.get().strip()
        entryYear = self.entryYear.get().strip()
        if entryName or entryPark or ddl or entryLength or entryHeight or entrySpeed or entryInversions or entryDrop or entryYear:
            items = self.tree.get_children()
            [self.tree.delete(item) for item in items]
            self.df = pd.read_excel('./data/rollerCoasters_result.xlsx')
            self.df['year'] = self.df['year'].fillna(0)
            self.df['year'] = self.df['year'].astype('int')
            if entryName:
                self.df = self.df.loc[self.df['name'].str.contains(entryName)]
            if entryPark:
                self.df = self.df.loc[self.df['park'].str.contains(entryPark)]
            if ddl:
                self.df = self.df.loc[self.df['Track'] == ddl]
            if entryLength:
                self.df = self.df.loc[self.df['length'] == float(entryLength)]
            if entryHeight:
                self.df = self.df.loc[self.df['height'] == float(entryHeight)]
            if entrySpeed:
                self.df = self.df.loc[self.df['speed'] == float(entrySpeed)]
            if entryInversions:
                self.df = self.df.loc[self.df['Inversions']== float(entryInversions)]
            if entryDrop:
                self.df = self.df.loc[self.df['Drop']== float(entryDrop)]
            if entryYear:
                self.df = self.df.loc[self.df['year']== int(entryYear)]

            for i, row in self.df.iterrows():
                self.tree.insert('', i, values=(
                i + 1, row['name'], row['park'], row['year'], row['Track'], row['Type'], row['height'], row['length'],
                row['speed'], row['Inversions'], row['Drop']))

    def btn_fig(self):
        if not self.df.empty:
            df = self.df['Track'].value_counts()
            self.ax1.clear()  # 清除原来的Axes区域
            self.ax1.pie(df,labels=df.index,autopct='%1.1f%%') # 重新画
            self.ax1.set_title('结构比例')

            self.df['year'] = np.floor(self.df['year'].astype('float')/10)*10
            self.df['year'] = self.df['year'].astype('int')
            df = self.df['year'].value_counts()
            self.ax2.clear()  # 清除原来的Axes区域
            self.ax2.pie(df,labels=df.index,autopct='%1.1f%%', textprops={'size': 'smaller'}) # 重新画
            self.ax2.set_title('年代比例')

            self.df.loc[self.df['Inversions'] >0, 'Inversions'] = '是'
            self.df.loc[self.df['Inversions'] ==0, 'Inversions'] = '否'
            df = self.df['Inversions'].value_counts()
            self.ax3.clear()  # 清除原来的Axes区域
            self.ax3.pie(df,labels=df.index,autopct='%1.1f%%') # 重新画
            self.ax3.set_title('是否倒置')

            df_all = pd.read_excel('./data/rollerCoasters_result.xlsx')
            df1 = df_all.sort_values(['speed'], ascending='asc').head(10)
            df2 = df_all.sort_values(['length'], ascending='asc').head(10)
            df3 = df_all.sort_values(['height'], ascending='asc').head(10)
            df4 = df_all.sort_values(['Drop'], ascending='asc').head(10)
            result_df1 = copy.deepcopy(self.df)
            result_df2 = copy.deepcopy(self.df)
            result_df3 = copy.deepcopy(self.df)
            result_df4 = copy.deepcopy(self.df)

            for i, row in df1.iterrows():
                result_df1.loc[result_df1['name'] == row['name'], 'top'] = 'speed'
            result_df1['top'] = result_df1['top'].fillna('否')
            df = result_df1['top'].value_counts()
            self.ax5.clear()  # 清除原来的Axes区域
            self.ax5.pie(df,labels=df.index,autopct='%1.1f%%') # 重新画
            self.ax5.set_title('是否speed')

            for i, row in df2.iterrows():
                result_df2.loc[result_df2['name'] == row['name'], 'top'] = 'length'
            result_df2['top']= result_df2['top'].fillna('否')
            df = result_df2['top'].value_counts()
            self.ax6.clear()  # 清除原来的Axes区域
            self.ax6.pie(df, labels=df.index, autopct='%1.1f%%')  # 重新画
            self.ax6.set_title('是否length')

            for i, row in df3.iterrows():
                result_df3.loc[result_df3['name'] == row['name'], 'top'] = 'height'
            result_df3['top'] = result_df3['top'].fillna('否')
            df = result_df3['top'].value_counts()
            self.ax7.clear()  # 清除原来的Axes区域
            self.ax7.pie(df, labels=df.index, autopct='%1.1f%%')  # 重新画
            self.ax7.set_title('是否height')

            for i, row in df4.iterrows():
                result_df4.loc[result_df4['name'] == row['name'], 'top'] = 'Drop'
            result_df4['top'] = result_df4['top'].fillna('否')
            df = result_df4['top'].value_counts()
            self.ax8.clear()  # 清除原来的Axes区域
            self.ax8.pie(df, labels=df.index, autopct='%1.1f%%')  # 重新画
            self.ax8.set_title('是否Drop')
            self.canvas.draw()