import pandas as pd
from pandas_datareader import data as web


with open("../cfg/commodity.cfg") as f:
   s_list = f.read().splitlines()


for s in s_list:
   s = s.rstrip()

   try:
      dfs = web.DataReader(s, data_source="yahoo", start="01-01-2016")

      print("*INFO - Captured %s." %(s))

      s2save = s.split("^")[1]
      dfs.to_csv("/home/jduarte/series/YAHOO_"+ s2save +".csv")

   except:
      print("*WARN - Could not capture %s." %(s))
