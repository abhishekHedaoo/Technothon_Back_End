import pandas as pd
from flask import Flask, json
import src.models.TreeNeededModel as TNM

def getTreeNeeded():
  fin = pd.read_csv('Datasets/TreeNeeded.csv')
  dataList = []
  for index, row in fin.iterrows():
    dataList.append(TNM.TreeNeededModel(row['ward_no'], row['no_trees'], row['no_trees_needed']))

  jsonStr = json.dumps([t.toJSON() for t in dataList])
  return jsonStr
