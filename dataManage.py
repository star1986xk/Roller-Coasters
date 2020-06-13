import pandas as pd
import numpy as np
import re


class dataManage():
    def Top10(self,key,asc):
        self.df = pd.read_excel('./data/rollerCoasters_result.xlsx')
        df = self.df[~self.df[key].isin([0])]
        df = df.sort_values([key], ascending=asc).head(10)
        df = df.reset_index(drop=True)
        pd.set_option('display.max_columns', None)

        df = df.sort_values(['height'],ascending=asc)
        df = df.reset_index(drop=True)
        df.loc[:,'height'] = df.index+1

        df = df.sort_values(['length'],ascending=asc)
        df = df.reset_index(drop=True)
        df.loc[:,'length'] = df.index+1

        df = df.sort_values(['speed'],ascending=asc)
        df = df.reset_index(drop=True)
        df.loc[:,'speed'] = df.index+1

        df = df.sort_values(['Inversions'],ascending=asc)
        df = df.reset_index(drop=True)
        df.loc[:,'Inversions'] = df.index+1

        df = df.sort_values(['Drop'],ascending=asc)
        df = df.reset_index(drop=True)
        df.loc[:,'Drop'] = df.index+1

        df = df.sort_values([key],ascending=asc).head(10)
        df = df.reset_index(drop=True)

        return df

    def Top_rank(self,key,asc):
        self.df = pd.read_excel('./data/rollerCoasters_result.xlsx')
        df = self.df.sort_values([key],ascending=asc).head(10)

        df = df.reset_index(drop=True)
        df.loc[:,key] = df.index+1

        df = df.sort_values(['height'])
        df = df.reset_index(drop=True)
        df.loc[:,'height'] = df.index+1

        df = df.sort_values(['length'])
        df = df.reset_index(drop=True)
        df.loc[:,'length'] = df.index+1

        df = df.sort_values(['speed'])
        df = df.reset_index(drop=True)
        df.loc[:,'speed'] = df.index+1

        df = df.sort_values(['Inversions'])
        df = df.reset_index(drop=True)
        df.loc[:,'Inversions'] = df.index+1

        df = df.sort_values(['Drop'])
        df = df.reset_index(drop=True)
        df.loc[:,'Drop'] = df.index+1

        df = df.sort_values([key],ascending=asc)
        df = df.reset_index(drop=True)
        return df


    def merge(self):
        self.df = pd.read_excel('./data/rollerCoasters.xlsx')
        df_rank1 = pd.read_excel('./data/rank1.xlsx')
        df_rank2 = pd.read_excel('./data/rank2.xlsx')
        df_rcdb = pd.read_excel('./data/rcdb.xlsx')

        self.df.loc[self.df['Track'] == '2014', 'Track'] = 'Steel'
        self.df.loc[self.df['Track'] == 'Stee', 'Track'] = 'Steel'
        self.df.loc[self.df['Track'] == 'Steels', 'Track'] = 'Steel'
        self.df.loc[self.df['Track'] == 'Wood Junior', 'Track'] = 'Wood'


        for i, row in df_rank1.iterrows():
            self.df.loc[(self.df['name'] == row['Name']) & (self.df['park'] == row['Park']),'rank1'] = row['rank']
        for i, row in df_rank2.iterrows():
            self.df.loc[(self.df['name'] == row['Name']) & (self.df['park'] == row['Park']),'rank2'] = row['rank']
        for i, row in df_rcdb.iterrows():
            self.df.loc[self.df['name'] == row['name'] ,'speed'] = row['speed']

        self.df['height'] = self.df['height'].apply(lambda x: x if re.search("^\d+\.?\d*?$", str(x)) else np.nan)
        self.df['length'] = self.df['length'].apply(lambda x: x if re.search("^\d+.?\d*?$", str(x)) else np.nan)
        self.df['speed'] = self.df['speed'].apply(lambda x: x if re.search("^\d+.?\d*?$", str(x)) else np.nan)
        self.df.to_excel('./data/rollerCoasters_result.xlsx',columns=['name', 'park', 'year','Track','Type', 'height', 'length', 'speed', 'Inversions','Drop','rank1','rank2'])


if __name__ == '__main__':
    data_obj = dataManage()
    data_obj.merge()
