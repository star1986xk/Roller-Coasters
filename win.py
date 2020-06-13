import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from dataManage import dataManage
import pylab as mpl
from infoWin import infoWin

class Application(tk.Tk):
    '''
    文件夹选择程序
    界面与逻辑分离
    '''

    def __init__(self):
        '''初始化'''
        super().__init__()  # 有点相当于tk.Tk()
        self.state("zoomed")
        self.wm_title("过山车数据分析")
        self.createWidgets()

    def createWidgets(self):
        '''界面'''
        fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = fig.add_subplot(111)
        # 指定字体,显示中文
        mpl.rcParams['font.sans-serif'] = ['FangSong']
        mpl.rcParams['axes.unicode_minus'] = False
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        footframe = tk.Frame(master=self).pack(side=tk.BOTTOM)

        # 创建一个顶级菜单
        menubar = tk.Menu(self)
        menubar.add_command(label="过山车信息",command=self.open_infowin)
        # 显示菜单
        self.config(menu=menubar)

        tk.Button(master=footframe, text='matadornetwork网站排名前十', command=lambda: self.draw('rank1')).pack(side=tk.LEFT)
        tk.Button(master=footframe, text='coasterbuzz网站排名前十', command=lambda: self.draw('rank2')).pack(side=tk.LEFT)
        tk.Button(master=footframe, text='matadornetwork网站排名前十详细分析', command=lambda: self.draw1('rank1')).pack(
            side=tk.LEFT)
        tk.Button(master=footframe, text='coasterbuzz网站排名前十网站排名前十详细分析', command=lambda: self.draw1('rank2')).pack(
            side=tk.LEFT)
        self.text = tk.Entry(master=footframe)
        self.text.pack(side=tk.LEFT)
        tk.Button(master=footframe, text='前十搜索', command=lambda: self.search(False)).pack(side=tk.LEFT)
        tk.Button(master=footframe, text='前十指标', command=lambda: self.search1(False)).pack(side=tk.LEFT)
        tk.Button(master=footframe, text='后十搜索', command=lambda: self.search(True)).pack(side=tk.LEFT)
        tk.Button(master=footframe, text='后十指标', command=lambda: self.search1(True)).pack(side=tk.LEFT)
    def open_infowin(self):
        self.infoOBJ = infoWin()
        self.infoOBJ.mainloop()

    def draw(self, key):
        '''绘图逻辑'''
        data_obj = dataManage()
        df = data_obj.Top10(key, True)
        x = [n+' '+str(i)  for n,i in zip(df['name'],df.index)]
        y = df[key]
        y = list(y)
        y.reverse()

        self.ax.clear()  # 清除原来的Axes区域
        self.ax.bar(x, y)  # 重新画
        self.ax.set_xticklabels(x, rotation=-15)
        self.ax.set_xlabel('过山车')
        self.ax.set_ylabel('排名')
        self.canvas.draw()

    def draw1(self, key):
        '''绘图逻辑'''
        data_obj = dataManage()
        df = data_obj.Top_rank(key, True)
        x = [n+' '+str(i)  for n,i in zip(df['name'],df.index)]
        y = df[key]
        y = list(y)
        y.reverse()

        y1 = df['height']
        y2 = df['length']
        y3 = df['speed']
        y4 = df['Inversions']
        y5 = df['Drop']

        self.ax.clear()  # 清除原来的Axes区域
        self.ax.plot(x, y, label='排名')  # 重新画
        self.ax.plot(x, y1, label='高度')  # 重新画
        self.ax.plot(x, y2, label='长度')  # 重新画
        self.ax.plot(x, y3, label='速度')  # 重新画
        self.ax.plot(x, y4, label='倒置')  # 重新画
        self.ax.plot(x, y5, label='落差')  # 重新画
        self.ax.legend(loc='upper right')
        self.ax.set_xticklabels(x, rotation=-15)
        self.ax.set_xlabel('过山车')
        self.ax.set_ylabel('排名')
        self.canvas.draw()

    def draw2(self, key,asc):
        '''绘图逻辑'''
        data_obj = dataManage()
        df = data_obj.Top10(key, asc)
        x = [n+' '+str(i)  for n,i in zip(df['name'],df.index)]
        y = df[key]
        self.ax.clear()  # 清除原来的Axes区域
        self.ax.bar(x, y)  # 重新画
        self.ax.set_xticklabels(x, rotation=-15)
        self.ax.set_xlabel('过山车')
        self.ax.set_ylabel('排名')
        self.canvas.draw()

    def draw3(self, key,asc):
        '''绘图逻辑'''
        data_obj = dataManage()
        df = data_obj.Top10(key, asc)
        x = [n+' '+str(i)  for n,i in zip(df['name'],df.index)]
        y1 = df['height']
        y2 = df['length']
        y3 = df['speed']
        y4 = df['Inversions']
        y5 = df['Drop']
        self.ax.clear()  # 清除原来的Axes区域
        self.ax.plot(x, y1, label='高度')  # 重新画
        self.ax.plot(x, y2, label='长度')  # 重新画
        self.ax.plot(x, y3, label='速度')  # 重新画
        self.ax.plot(x, y4, label='倒置')  # 重新画
        self.ax.plot(x, y5, label='落差')  # 重新画
        self.ax.legend(loc='upper right')
        self.ax.set_xticklabels(x, rotation=-15)
        self.ax.set_xlabel('过山车')
        self.ax.set_ylabel('指标')
        self.canvas.draw()

    def draw4(self, key):
        '''绘图逻辑'''
        data_obj = dataManage()
        df = data_obj.Top10(key, True)
        x = [n+' '+str(i)  for n,i in zip(df['name'],df.index)]
        y = df[key]
        self.ax.clear()  # 清除原来的Axes区域
        self.ax.bar(x, y)  # 重新画
        self.ax.set_xticklabels(x, rotation=-15)
        self.ax.set_xlabel('过山车')
        self.ax.set_ylabel('排名')
        self.canvas.draw()

    def draw5(self, key):
        '''绘图逻辑'''
        data_obj = dataManage()
        df = data_obj.Top10(key, True)
        x =  [n+' '+str(i)  for n,i in zip(df['name'],df.index)]
        y1 = df['height']
        y2 = df['length']
        y3 = df['speed']
        y4 = df['Inversions']
        y5 = df['Drop']

        self.ax.clear()  # 清除原来的Axes区域
        self.ax.plot(x, y1, label='高度')  # 重新画
        self.ax.plot(x, y2, label='长度')  # 重新画
        self.ax.plot(x, y3, label='速度')  # 重新画
        self.ax.plot(x, y4, label='倒置')  # 重新画
        self.ax.plot(x, y5, label='落差')  # 重新画
        self.ax.legend(loc='upper right')
        self.ax.set_xticklabels(x,rotation=-15)
        self.ax.set_xlabel('过山车')
        self.ax.set_ylabel('指标')
        self.canvas.draw()

    def search(self,asc):
        text = self.text.get().strip()
        if text in '速度':
            self.draw2('speed',asc)
        elif text in '长度':
            self.draw2('length',asc)
        elif text in '高度':
            self.draw2('height',asc)
        elif text in '倒置':
            self.draw2('Inversions',asc)
        elif text in '落差':
            self.draw2('Drop',asc)

    def search1(self,asc):
        text = self.text.get().strip()
        if text in '速度':
            self.draw3('speed',asc)
        elif text in '长度':
            self.draw3('length',asc)
        elif text in '高度':
            self.draw3('height',asc)
        elif text in '倒置':
            self.draw3('Inversions',asc)
        elif text in '落差':
            self.draw3('Drop',asc)


if __name__ == '__main__':
    # 实例化Application
    app = Application()
    # 主消息循环:
    app.mainloop()
