import pandas as pd
import numpy as np
import os.path

def performAnalytics():
  listOfPopulationDataFiles = ["Datasets\\Input\\Tree_Data\\p1.csv",
                 "Datasets\\Input\\Tree_Data\\p2.csv",
                 "Datasets\\Input\\Tree_Data\\p3.csv",
                 "Datasets\\Input\\Tree_Data\\p4.csv",
                 "Datasets\\Input\\Tree_Data\\p5.csv"]
  # read data for tree from 5 files
  tree_datasetTemp = pd.DataFrame()

  for f in listOfPopulationDataFiles:
    data = pd.read_csv(f, low_memory = False)
    tree_datasetTemp = tree_datasetTemp.append(data)
  
  # read population data
  population_dataset = pd.read_excel('Datasets\\Input\\Population_Data\\population ward wise.xlsx')

  # read vehicle data
  vehicle_dataset = pd.read_excel('Datasets\\Input\\Vehicle_Data\\trafficdataxl.xlsx')

  # read growthfactor data
  growth_dataset = pd.read_excel('Datasets\\Input\\Tree_Data\\growthfactor.xlsx')

  tree_dataset= tree_datasetTemp[['id', 'geom', 'girth_cm', 'height_m', 'condition', 'common_name', 'economic_i', 'phenology', 'ward']].copy()

  tree_dataset['Growth Factor'] = tree_dataset['common_name'].map(growth_dataset.set_index('Common Name')['Growth Factor'])

  tree_dataset['Diameter']= (tree_dataset['girth_cm'].values/3.14)*0.393701

  tree_dataset['Age']= tree_dataset['Diameter'].values *  tree_dataset['Growth Factor'].values

  def calc(s):
      if((s['Diameter']) <11):
          return 0.25*(s['Diameter']*s['Diameter'])*(3.28084*s['height_m'])
      else:
          return 0.15*(s['Diameter']*s['Diameter'])*(3.28084*s['height_m'])

  tree_dataset['Weight']= tree_dataset.apply(calc, axis=1)

  tree_dataset['Dry_Weight']= tree_dataset['Weight'].values * 0.725 

  tree_dataset['Carbon_Weight']= tree_dataset['Dry_Weight'].values * 0.5 

  tree_dataset['CO2_seq']= tree_dataset['Carbon_Weight'].values * 3.6663

  tree_dataset['CO2_seq_peryear']= tree_dataset['CO2_seq'].values/tree_dataset['Age'].values

  # In tonnes
  tree_dataset['CO2_seq_peryear']= tree_dataset['CO2_seq_peryear'].values * 0.453592*0.00110231

  #-------------------------------------------------------------------------------------------------

  population_dataset['CO2_emmited']= population_dataset['Population(2017)'].values * 365 * 0.00098421 * 0.7

  vehicle_dataset['CO2_two_wh']= vehicle_dataset['Two_Wheeler Traffic(per day)'].values * 0.0002817073 
  vehicle_dataset['CO2_three_wh']= vehicle_dataset['Three Wheeler Traffic (per day)'].values * 0.0002817073
  vehicle_dataset['CO2_four_wh']= vehicle_dataset['Four_Wheeler Traffic(Personal Transport per day)'].values * 0.0003042683
  vehicle_dataset['CO2_Public_trans']= vehicle_dataset['Public Transport vehicles Traffic'].values * 0.0003242683

  vehicle_dataset['Total_CO2']= vehicle_dataset['CO2_two_wh'].values+vehicle_dataset['CO2_Public_trans'].values+vehicle_dataset['CO2_three_wh'].values+vehicle_dataset['CO2_four_wh'].values

  #--------------------------
  temp_grp = tree_dataset.groupby('ward')[['id']].count()

  temp_grp['CO2_consumed']=tree_dataset.groupby('ward')[['CO2_seq_peryear']].sum()

  temp_grp = temp_grp.merge(population_dataset, left_index=True, right_on='Ward_Name')

  temp_grp['co2_vehicles_emitted'] = temp_grp['Ward_Name'].map(vehicle_dataset.set_index('ward_name')['Total_CO2'])

  temp_grp['CO2_emmited_total']= temp_grp['CO2_emmited'].values + temp_grp['co2_vehicles_emitted'].values

  temp_grp['excess_co2']= temp_grp['CO2_emmited_total'].values - temp_grp['CO2_consumed'].values

  temp_grp['tree_required']= temp_grp['excess_co2'].values/(temp_grp['CO2_consumed'].values / temp_grp['id'].values)

  alldetails= temp_grp[['Ward_Name','id','Population(2017)','CO2_consumed','CO2_emmited','co2_vehicles_emitted','CO2_emmited_total','excess_co2','tree_required']].copy()

  alldetails.columns= ['ward_no','no_trees','population','co2_absorbtion','co2_emitted_population','co2_emitted_vehicles','co2_emitted_total','excess_co2','tree_required']

  alldetails['tree_required'] = alldetails['tree_required'].apply(np.int64)

  alldetails.to_csv('Datasets\\Output\\AllDetails.csv')

  return 1
