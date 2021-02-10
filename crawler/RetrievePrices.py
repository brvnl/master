import pandas as pd
from pandas_datareader import data as web

path2save=""

with open("../cfg/securities.cfg") as f:
   s_list = f.read().splitlines()


for s in s_list:
   s = s.rstrip()

   try:
      df_previous = pd.read_csv("/home/jduarte/series/YAHOO_"+ s +".csv")
   except:
      print("*WARN - No previous history was found for %s. Saving serie from zero." %(s))
      df_previous = pd.DataFrame()


   try:
      dfs = web.DataReader(s, data_source="yahoo", start="01-01-2016")

      n_previous = len(df_previous)
      n_actual   = len(dfs)

      if (n_actual > n_previous):
         print("*INFO - Captured %s. %d points added to previous serie." %(s, (n_actual - n_previous)))
         dfs.to_csv("/home/jduarte/series/YAHOO_"+ s +".csv")
      else:
         print("*WARN - New serie for %s has less data points: Previous=%d/ Now=%d. File won't be updated, check data source for more info." %(s, n_previous, n_actual))

   except:
      print("*WARN - Could not capture %s." %(s))
