import pandas as pd
from pandas_datareader import data as web

'''
with open("../cfg/forex.cfg") as f:
   s_list = f.read().splitlines()
'''

dfs = web.DataReader("TUD", data_source="oecd")
print(dfs["Brazil"].head())


'''
for s in s_list:
   s = s.rstrip()

   try:
      dfs = web.DataReader(s, data_source="yahoo", start="01-01-2016")

      print("*INFO - Captured %s." %(s))

      s2save = s.split("=")[0]
      dfs.to_csv("/home/jduarte/series/YAHOO_"+ s2save +".csv")

   except:
      print("*WARN - Could not capture %s." %(s))
'''
