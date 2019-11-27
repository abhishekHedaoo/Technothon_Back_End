import pandas as pd
from flask import json
import src.models.DetailsModel as DM
import src.DAModule.DataAnalyticModule as DAM

def getAllDetails():
  df = pd.read_csv('Datasets/Output/AllDetails.csv')
  allDetailsList = []
  for index, row in df.iterrows():
    allDetailsList.append(DM.DetailsModel(row['ward_no'],row['no_trees'],row['population'],row['co2_absorbtion'],row['co2_emitted_population'],row['co2_emitted_vehicles'],row['co2_emitted_total'],row['excess_co2'],row['tree_required']))
  
  jsonStr = json.dumps([t.toJSON() for t in allDetailsList])
  return jsonStr


def runDataAnalyticsModule():
  DAM.performAnalytics()
