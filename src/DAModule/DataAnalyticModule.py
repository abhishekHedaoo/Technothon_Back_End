import pandas as pd
import numpy as np

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

  ################################################################

  temp_grp = tree_dataset.groupby('ward')[['id']].count()

  temp_grp['CO2_consumed']=tree_dataset.groupby('ward')[['CO2_seq_peryear']].sum().apply(np.int64)

  temp_grp_41 = pd.DataFrame(
      {
          "ward_no":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41]
      }
  )

  temp_grp_41['No_trees']=0
  temp_grp_41['CO2_consumed']=0


  temp_grp_41.loc[temp_grp_41['ward_no'] == 1, 'No_trees'] = (temp_grp.at[5,'id']*1)+(temp_grp.at[1,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 1, 'CO2_consumed'] = (temp_grp.at[5,'CO2_consumed']*1)+(temp_grp.at[1,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 2, 'No_trees'] = (temp_grp.at[4,'id']*1)+(temp_grp.at[16,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 2, 'CO2_consumed'] = (temp_grp.at[4,'CO2_consumed']*1)+(temp_grp.at[16,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 3,'No_trees'] = (temp_grp.at[17,'id']*0.5)+(temp_grp.at[1,'id']*0.5)+(temp_grp.at[3,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 3,'CO2_consumed'] = (temp_grp.at[17,'CO2_consumed']*0.5)+(temp_grp.at[1,'CO2_consumed']*0.5)+(temp_grp.at[3,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 4, 'No_trees'] = (temp_grp.at[2,'id']*1)+(temp_grp.at[19,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 4, 'CO2_consumed'] = (temp_grp.at[2,'CO2_consumed']*1)+(temp_grp.at[19,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 5, 'No_trees'] = (temp_grp.at[17,'id']*0.5)+(temp_grp.at[18,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 5, 'CO2_consumed'] = (temp_grp.at[17,'CO2_consumed']*0.5)+(temp_grp.at[18,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 6, 'No_trees'] = (temp_grp.at[14,'id']*1)+(temp_grp.at[15,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 6, 'CO2_consumed'] = (temp_grp.at[14,'CO2_consumed']*1)+(temp_grp.at[15,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 7, 'No_trees'] = (temp_grp.at[13,'id']*1)+(temp_grp.at[7,'id']*1)+(temp_grp.at[11,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 7, 'CO2_consumed'] = (temp_grp.at[13,'CO2_consumed']*1)+(temp_grp.at[7,'CO2_consumed']*1)+(temp_grp.at[11,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 8, 'No_trees'] = (temp_grp.at[6,'id']*1)+(temp_grp.at[8,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 8, 'CO2_consumed'] = (temp_grp.at[6,'CO2_consumed']*1)+(temp_grp.at[8,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 9, 'No_trees'] = (temp_grp.at[9,'id']*1)+(temp_grp.at[10,'id']*1)+(temp_grp.at[8,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 9, 'CO2_consumed'] = (temp_grp.at[9,'CO2_consumed']*1)+(temp_grp.at[10,'CO2_consumed']*1)+(temp_grp.at[8,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 10, 'No_trees'] = (temp_grp.at[29,'id']*1)+(temp_grp.at[28,'id']*0.3)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 10, 'CO2_consumed'] = (temp_grp.at[29,'CO2_consumed']*1)+(temp_grp.at[28,'CO2_consumed']*0.3)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 11, 'No_trees'] = (temp_grp.at[26,'id']*1)+(temp_grp.at[27,'id']*1)+(temp_grp.at[28,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 11, 'CO2_consumed'] = (temp_grp.at[26,'CO2_consumed']*1)+(temp_grp.at[27,'CO2_consumed']*1)+(temp_grp.at[28,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 12, 'No_trees'] = (temp_grp.at[28,'id']*0.2)+(temp_grp.at[33,'id']*1)+(temp_grp.at[34,'id']*0.6)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 12, 'CO2_consumed'] = (temp_grp.at[28,'CO2_consumed']*0.2)+(temp_grp.at[33,'CO2_consumed']*1)+(temp_grp.at[34,'CO2_consumed']*0.6)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 13, 'No_trees'] = (temp_grp.at[35,'id']*0.8)+(temp_grp.at[34,'id']*0.4)+(temp_grp.at[32,'id']*0.4)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 13, 'CO2_consumed'] = (temp_grp.at[35,'CO2_consumed']*0.8)+(temp_grp.at[34,'CO2_consumed']*0.4)+(temp_grp.at[32,'CO2_consumed']*0.4)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 14, 'No_trees'] = (temp_grp.at[12,'id']*1)+(temp_grp.at[25,'id']*1)+(temp_grp.at[24,'id']*1)+(temp_grp.at[36,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 14, 'CO2_consumed'] = (temp_grp.at[12,'CO2_consumed']*1)+(temp_grp.at[25,'CO2_consumed']*1)+(temp_grp.at[24,'CO2_consumed']*1)+(temp_grp.at[36,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 15, 'No_trees'] = (temp_grp.at[37,'id']*1)+(temp_grp.at[50,'id']*1)+(temp_grp.at[51,'id']*0.1)+(temp_grp.at[58,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 15, 'CO2_consumed'] = (temp_grp.at[37,'CO2_consumed']*1)+(temp_grp.at[50,'CO2_consumed']*1)+(temp_grp.at[51,'CO2_consumed']*0.1)+(temp_grp.at[58,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 16, 'No_trees'] = (temp_grp.at[23,'id']*1)+(temp_grp.at[38,'id']*0.5)+(temp_grp.at[39,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 16, 'CO2_consumed'] = (temp_grp.at[23,'CO2_consumed']*1)+(temp_grp.at[38,'CO2_consumed']*0.5)+(temp_grp.at[39,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 17, 'No_trees'] = (temp_grp.at[48,'id']*1)+(temp_grp.at[38,'id']*0.5)+(temp_grp.at[39,'id']*0.5)+(temp_grp.at[49,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 17, 'CO2_consumed'] = (temp_grp.at[48,'CO2_consumed']*1)+(temp_grp.at[38,'CO2_consumed']*0.5)+(temp_grp.at[39,'CO2_consumed']*0.5)+(temp_grp.at[49,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 18, 'No_trees'] = (temp_grp.at[59,'id']*1)+(temp_grp.at[49,'id']*0.5)+(temp_grp.at[58,'id']*0.5)+(temp_grp.at[65,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 18, 'CO2_consumed'] =  (temp_grp.at[59,'CO2_consumed']*1)+(temp_grp.at[49,'CO2_consumed']*0.5)+(temp_grp.at[58,'CO2_consumed']*0.5)+(temp_grp.at[65,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 19, 'No_trees'] = (temp_grp.at[60,'id']*1)+(temp_grp.at[65,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 19, 'CO2_consumed'] = (temp_grp.at[60,'CO2_consumed']*1)+(temp_grp.at[65,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 20, 'No_trees'] = (temp_grp.at[40,'id']*1)+(temp_grp.at[22,'id']*1)+(temp_grp.at[47,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 20, 'CO2_consumed'] = (temp_grp.at[40,'CO2_consumed']*1)+(temp_grp.at[22,'CO2_consumed']*1)+(temp_grp.at[47,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 21, 'No_trees'] = (temp_grp.at[21,'id']*1)+(temp_grp.at[41,'id']*0.5)+(temp_grp.at[20,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 21, 'CO2_consumed'] = (temp_grp.at[21,'CO2_consumed']*1)+(temp_grp.at[41,'CO2_consumed']*0.5)+(temp_grp.at[20,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 22, 'No_trees'] = (temp_grp.at[20,'id']*0.5)+(temp_grp.at[43,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 22, 'CO2_consumed'] = (temp_grp.at[20,'CO2_consumed']*0.5)+(temp_grp.at[43,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 23,'No_trees'] = (temp_grp.at[44,'id']*1)+(temp_grp.at[42,'id']*0.5)+(temp_grp.at[45,'id']*0.05)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 23,'CO2_consumed'] = (temp_grp.at[44,'CO2_consumed']*1)+(temp_grp.at[42,'CO2_consumed']*0.5)+(temp_grp.at[45,'CO2_consumed']*0.05)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 24, 'No_trees'] = (temp_grp.at[42,'id']*0.5)+(temp_grp.at[45,'id']*0.25)+(temp_grp.at[46,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 24, 'CO2_consumed'] = (temp_grp.at[42,'CO2_consumed']*0.5)+(temp_grp.at[45,'CO2_consumed']*0.25)+(temp_grp.at[46,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 25, 'No_trees'] = (temp_grp.at[46,'id']*0.5)+(temp_grp.at[61,'id']*0.9)+(temp_grp.at[41,'id']*0.5)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 25, 'CO2_consumed'] = (temp_grp.at[46,'CO2_consumed']*0.5)+(temp_grp.at[61,'CO2_consumed']*0.9)+(temp_grp.at[41,'CO2_consumed']*0.5)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 26, 'No_trees'] = (temp_grp.at[45,'id']*0.7)+(temp_grp.at[61,'id']*0.1)+(temp_grp.at[62,'id']*0.25)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 26, 'CO2_consumed'] = (temp_grp.at[45,'CO2_consumed']*0.7)+(temp_grp.at[61,'CO2_consumed']*0.1)+(temp_grp.at[62,'CO2_consumed']*0.25)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 27, 'No_trees'] = (temp_grp.at[63,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 27, 'CO2_consumed'] = (temp_grp.at[63,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 28, 'No_trees'] = (temp_grp.at[64,'id']*1)+(temp_grp.at[66,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 28, 'CO2_consumed'] =  (temp_grp.at[64,'CO2_consumed']*1)+(temp_grp.at[66,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 29, 'No_trees'] = (temp_grp.at[57,'id']*1)+(temp_grp.at[52,'id']*0.9)+(temp_grp.at[51,'id']*0.9)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 29, 'CO2_consumed'] = (temp_grp.at[57,'CO2_consumed']*1)+(temp_grp.at[52,'CO2_consumed']*0.9)+(temp_grp.at[51,'CO2_consumed']*0.9)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 30, 'No_trees'] = (temp_grp.at[52,'id']*0.1)+(temp_grp.at[56,'id']*1)+(temp_grp.at[35,'id']*0.2)+(temp_grp.at[53,'id']*0.1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 30, 'CO2_consumed'] = (temp_grp.at[52,'CO2_consumed']*0.1)+(temp_grp.at[56,'CO2_consumed']*1)+(temp_grp.at[35,'CO2_consumed']*0.2)+(temp_grp.at[53,'CO2_consumed']*0.1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 31, 'No_trees'] = (temp_grp.at[32,'id']*0.6)+(temp_grp.at[31,'id']*0.5)+(temp_grp.at[30,'id']*0.1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 31, 'CO2_consumed'] = (temp_grp.at[32,'CO2_consumed']*0.6)+(temp_grp.at[31,'CO2_consumed']*0.5)+(temp_grp.at[30,'CO2_consumed']*0.1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 32, 'No_trees'] = (temp_grp.at[31,'id']*0.5)+(temp_grp.at[30,'id']*0.9)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 32, 'CO2_consumed'] = (temp_grp.at[31,'CO2_consumed']*0.5)+(temp_grp.at[30,'CO2_consumed']*0.9)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 33, 'No_trees'] = (temp_grp.at[55,'id']*1)+(temp_grp.at[54,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 33, 'CO2_consumed'] = (temp_grp.at[55,'CO2_consumed']*1)+(temp_grp.at[54,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 34, 'No_trees'] = (temp_grp.at[53,'id']*0.9)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 34, 'CO2_consumed'] = (temp_grp.at[53,'CO2_consumed']*0.9)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 35, 'No_trees'] = (temp_grp.at[70,'id']*0.1)+(temp_grp.at[69,'id']*0.5)+(temp_grp.at[67,'id']*1)+(temp_grp.at[68,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 35, 'CO2_consumed'] = (temp_grp.at[70,'CO2_consumed']*0.1)+(temp_grp.at[69,'CO2_consumed']*0.5)+(temp_grp.at[67,'CO2_consumed']*1)+(temp_grp.at[68,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 36, 'No_trees'] = (temp_grp.at[71,'id']*1)+(temp_grp.at[70,'id']*0.9)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 36, 'CO2_consumed'] = (temp_grp.at[71,'CO2_consumed']*1)+(temp_grp.at[70,'CO2_consumed']*0.9)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 37, 'No_trees'] = (temp_grp.at[72,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 37, 'CO2_consumed'] = (temp_grp.at[72,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 38, 'No_trees'] = (temp_grp.at[76,'id']*0.7)+(temp_grp.at[73,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 38, 'CO2_consumed'] = (temp_grp.at[76,'CO2_consumed']*0.7)+(temp_grp.at[73,'CO2_consumed']*1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 39, 'No_trees'] = (temp_grp.at[69,'id']*0.5)+(temp_grp.at[74,'id']*0.9)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 39, 'CO2_consumed'] = (temp_grp.at[69,'CO2_consumed']*0.5)+(temp_grp.at[74,'CO2_consumed']*0.9)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 40, 'No_trees'] = (temp_grp.at[75,'id']*1)+(temp_grp.at[74,'id']*0.1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 40, 'CO2_consumed'] = (temp_grp.at[75,'CO2_consumed']*1)+(temp_grp.at[74,'CO2_consumed']*0.1)
  #
  temp_grp_41.loc[temp_grp_41['ward_no'] == 41, 'No_trees'] = (temp_grp.at[62,'id']*1)+(temp_grp.at[76,'id']*0.3)+(temp_grp.at[77,'id']*1)
  temp_grp_41.loc[temp_grp_41['ward_no'] == 41, 'CO2_consumed'] = (temp_grp.at[62,'CO2_consumed']*1)+(temp_grp.at[76,'CO2_consumed']*0.3)+(temp_grp.at[77,'id']*1)

  vehicle_dataset['CO2_two_wh']= vehicle_dataset['Two_Wheeler Traffic(per day)'].values * 0.0002817073*5000
  vehicle_dataset['CO2_three_wh']= vehicle_dataset['Three Wheeler Traffic (per day)'].values * 0.0002817073*10000
  vehicle_dataset['CO2_four_wh']= vehicle_dataset['Four_Wheeler Traffic(Personal Transport per day)'].values * 0.0003042683*10000
  vehicle_dataset['CO2_Public_trans']= vehicle_dataset['Public Transport vehicles Traffic'].values * 0.0003242683*20000

  vehicle_dataset['Total_CO2']= vehicle_dataset['CO2_two_wh'].values+vehicle_dataset['CO2_Public_trans'].values+vehicle_dataset['CO2_three_wh'].values+vehicle_dataset['CO2_four_wh'].values

  #############################################################################

  population_dataset['CO2_emmited']= population_dataset['Population(2017)'].values * 365 * 0.00098421 * 0.7

  ##############################################################################

  temp_grp_41['Population'] = temp_grp_41['ward_no'].map(population_dataset.set_index('Ward_Name')['Population(2017)'])

  temp_grp_41['CO2_emmited'] = temp_grp_41['ward_no'].map(population_dataset.set_index('Ward_Name')['CO2_emmited'])

  temp_grp_41['co2_vehicles_emitted'] = temp_grp_41['ward_no'].map(vehicle_dataset.set_index('Ward No')['Total_CO2'])

  temp_grp_41['CO2_emmited_total']= temp_grp_41['CO2_emmited'].values + temp_grp_41['co2_vehicles_emitted'].values

  temp_grp_41['excess_co2']= temp_grp_41['CO2_emmited_total'].values - temp_grp_41['CO2_consumed'].values

  temp_grp_41['excess_co2']= temp_grp_41['excess_co2'].values*0.4

  temp_grp_41['tree_required']= temp_grp_41['excess_co2'].values/(temp_grp_41['CO2_consumed'].values / temp_grp_41['No_trees'].values)

  alldetails= temp_grp_41[['ward_no','No_trees','Population','CO2_consumed','CO2_emmited','co2_vehicles_emitted','CO2_emmited_total','excess_co2','tree_required']].copy()

  alldetails.columns= ['ward_no','no_trees','population','co2_absorbtion','co2_emitted_population','co2_emitted_vehicles','co2_emitted_total','excess_co2','tree_required']

  alldetails['tree_required'] = alldetails['tree_required'].apply(np.int64)
  alldetails['co2_emitted_population'] = alldetails['co2_emitted_population'].apply(np.int64)
  alldetails['co2_emitted_vehicles'] = alldetails['co2_emitted_vehicles'].apply(np.int64)
  alldetails['co2_emitted_total'] = alldetails['co2_emitted_total'].apply(np.int64)
  alldetails['excess_co2'] = alldetails['excess_co2'].apply(np.int64)
  alldetails['no_trees'] = alldetails['no_trees'].apply(np.int64)

  alldetails.to_csv('Datasets\\Output\\AllDetails.csv')
  return