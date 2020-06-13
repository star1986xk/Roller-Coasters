import requests
import re
import pandas as pd
from threading import Thread
import time

class rcdb():
    def __init__(self):
        self.home = 'https://rcdb.com/rhr.htm'
        self.info_list = []

    def requestGET(self, url):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
            }
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            return None

    def spiderMain(self):
        text = self.requestGET(self.home)
        res = re.findall('<span class=float>(.*?)</span> mph<td><a href=.*?>(.*?)</a>',text)
        data = [[r[1],r[0]] for r in res]
        df = pd.DataFrame(data, columns=['name', 'speed'])
        df.to_excel('./data/rcdb.xlsx')


if __name__ == '__main__':
    rcdb_obj = rcdb()
    rcdb_obj.spiderMain()

