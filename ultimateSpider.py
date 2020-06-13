import requests
import re
import pandas as pd
from threading import Thread
import time


class ultimate():
    def __init__(self):
        self.home = 'https://www.ultimaterollercoaster.com'
        self.index = '/coasters/browse/a-to-z'
        self.thread_count = 200
        self.info_list = []

    def requestGET(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            return None

    def parser_index(self, url):
        result = []
        try:
            text = self.requestGET(url)
            if text:
                ul_list = re.findall('<ul class="tpList">(.*?)</ul>', text, re.S | re.I)
                for ul in ul_list:
                    li_list = re.findall('<li><a href="(.*?)">', ul)
                    for li in li_list:
                        result.append(li)
        except Exception as e:
            pass
        finally:
            return result

    def parser_info(self, url):
        try:
            textInfo = self.requestGET(url)
            if textInfo:
                title_re = re.search('<h1 class="new">(.*?)</h1>', textInfo, re.I)
                title = title_re[1].strip() if title_re else ''
                park_re = re.search('<h2 class="topgrn"><a.*?>(.*?)</a></h2>', textInfo, re.I)
                park = park_re[1].strip() if park_re else ''
                year_re = re.search(
                    '<table class="rc_detail">\s*?<tr>.*?</tr>\s*?<tr>\s*?<td>(.*?)</td>\s*?<td>(.*?)</td>\s*?<td>(.*?)</td>',
                    textInfo,
                    re.I | re.S)
                year = year_re[1].strip() if year_re else '0'
                Track = year_re[2].strip()
                Type = year_re[3].strip()
                height_re = re.search('<li>Height:(.*?)feet</li>', textInfo, re.I | re.S)
                height = height_re[1].strip() if height_re else '0'
                length_re = re.search('<li>Length:(.*?)feet.*?</li>', textInfo, re.I | re.S)
                length = length_re[1].strip().replace(',', '').replace('Alpha', '') if length_re else '0'
                speed_re = re.search('<li>Top Speed:(.*?)mph</li>', textInfo, re.I | re.S)
                speed = speed_re[1].strip() if speed_re else '0'
                Inversions_re = re.search('<li>Inversions:(.*?)</li>', textInfo, re.I | re.S)
                Inversions = Inversions_re[1].strip() if Inversions_re else '0'
                Drop_re = re.search('<li>Drop:(.*?)feet</li>', textInfo, re.I | re.S)
                Drop = Drop_re[1].strip() if Drop_re else '0'
                Drop = re.search('\d+', Drop)
                info = [title, park, year, Track, Type, height, length, speed, Inversions, Drop[0]]
                print(info)
                self.info_list.append(info)
        except Exception as e:
            pass

    def thread_pool(self, li_list):
        try:
            for i in range(0, len(li_list), self.thread_count):
                self.result = []
                self.task_list = [Thread(target=self.parser_info, args=(self.home + li,)) for
                                  li in li_list[i:i + self.thread_count]]
                [task.start() for task in self.task_list]
                [task.join() for task in self.task_list]
                time.sleep(1)
        except Exception as e:
            print(e)

    def spiderMain(self):
        li_list = self.parser_index(self.home + self.index)
        self.thread_pool(li_list)
        df = pd.DataFrame(self.info_list,
                          columns=['name', 'park', 'year', 'Track', 'Type', 'height', 'length', 'speed', 'Inversions',
                                   'Drop'])
        df.to_excel('./data/rollerCoasters.xlsx')


if __name__ == '__main__':
    ultimate_obj = ultimate()
    ultimate_obj.spiderMain()
