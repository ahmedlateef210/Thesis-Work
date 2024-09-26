# -*- coding: utf-8 -*-
"""Dataset_Basins.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nWwUKby3bkNwReeQ0mRIltv_OTwLEtk5
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("dataset_v1.csv")
data.drop(columns=["Unnamed: 0", "Wind_spd", "Present_weather", "Past_weather", "River"], inplace = True)
data

def threshold_level(station_name):
  if station_name == "Bandarban":
    return 15.25
  if station_name == "Bogura":
    return 16.32
  if station_name == "Chattogram":
    return 4.60
  if station_name == "Chuadanga":
    return 12.05
  if station_name == "Coxs Bazar":
    return 6.25
  if station_name == "Dhaka":
    return 6.00
  if station_name == "Dinajpur":
    return 33.50
  if station_name == "Habiganj":
    return 9.50
  if station_name == "Jamalpur":
    return 17.00
  if station_name == "Mymensingh":
    return 12.50
  if station_name == "Netrokona":
    return 29.20
  if station_name == "Nilphamari":
    return 52.60
  if station_name == "Rajshahi":
    return 18.50
  if station_name == "Rangamati":
    return 17.85
  if station_name == "Rangpur":
    return 33.15
  if station_name == "Sirajganj":
    return 13.35
  if station_name == "Srimongal":
    return 11.75
  if station_name == "Sylhet":
    return 11.25
  if station_name == "Teknaf":
    return 12.25

data['Area_threshold'] = data['station'].map(threshold_level)
data

def basin(station_name):
  if station_name == "Bandarban":
    return "South East Hill"
  if station_name == "Bogura":
    return "Brahmaputra"
  if station_name == "Chattogram":
    return "South East Hill"
  if station_name == "Chuadanga":
    return "Ganges"
  if station_name == "Coxs Bazar":
    return "South East Hill"
  if station_name == "Dhaka":
    return "Brahmaputra"
  if station_name == "Dinajpur":
    return "Ganges"
  if station_name == "Habiganj":
    return "Meghna"
  if station_name == "Jamalpur":
    return "Brahmaputra"
  if station_name == "Mymensingh":
    return "Brahmaputra"
  if station_name == "Netrokona":
    return "Brahmaputra"
  if station_name == "Nilphamari":
    return "Brahmaputra"
  if station_name == "Rajshahi":
    return "Ganges"
  if station_name == "Rangamati":
    return "South East Hill"
  if station_name == "Rangpur":
    return "Brahmaputra"
  if station_name == "Sirajganj":
    return "Brahmaputra"
  if station_name == "Srimongal":
    return "Meghna"
  if station_name == "Sylhet":
    return "Meghna"
  if station_name == "Teknaf":
    return "South East Hill"

data['Basin'] = data['station'].map(basin)
data

label_encoder = LabelEncoder()
data['Wind_dir_encoded'] = label_encoder.fit_transform(data['Wind_dir'])
data[['Wind_dir', 'Wind_dir_encoded']].head()

"""Grouping Data by Basin"""

data_grouped = data.groupby("Basin")
data_BrBasin = data_grouped.get_group("Brahmaputra").reset_index()
data_GaBasin = data_grouped.get_group("Ganges").reset_index()
data_MeBasin = data_grouped.get_group("Meghna").reset_index()
data_SEHBasin = data_grouped.get_group("South East Hill").reset_index()

data_BrBasin.drop(columns=["index"], inplace = True)
data_GaBasin.drop(columns=["index"], inplace = True)
data_MeBasin.drop(columns=["index"], inplace = True)
data_SEHBasin.drop(columns=["index"], inplace = True)

"""Working on Brahmaputra Basin Dataset"""

imputer = SimpleImputer(missing_values=pd.NA, strategy="mean")

imputer.fit(data_BrBasin[["Rainfall"]])
data_BrBasin["Rainfall"] = imputer.transform(data_BrBasin[["Rainfall"]])

imputer.fit(data_BrBasin[["Humidity"]])
data_BrBasin["Humidity"] = imputer.transform(data_BrBasin[["Humidity"]])

imputer.fit(data_BrBasin[["Tmax"]])
data_BrBasin["Tmax"] = imputer.transform(data_BrBasin[["Tmax"]])

imputer.fit(data_BrBasin[["Tmin"]])
data_BrBasin["Tmin"] = imputer.transform(data_BrBasin[["Tmin"]])

imputer.fit(data_BrBasin[["Cloud_amt"]])
data_BrBasin["Cloud_amt"] = imputer.transform(data_BrBasin[["Cloud_amt"]])

imputer.fit(data_BrBasin[["max_wl"]])
data_BrBasin["max_wl"] = imputer.transform(data_BrBasin[["max_wl"]])

imputer.fit(data_BrBasin[["min_wl"]])
data_BrBasin["min_wl"] = imputer.transform(data_BrBasin[["min_wl"]])

imputer.fit(data_BrBasin[["avg_wl"]])
data_BrBasin["avg_wl"] = imputer.transform(data_BrBasin[["avg_wl"]])
data_BrBasin

imputer = SimpleImputer(missing_values=pd.NA, strategy="most_frequent")

imputer.fit(data_BrBasin[["Wind_dir"]])
data_BrBasin["Wind_dir"] = imputer.transform(data_BrBasin[["Wind_dir"]])

data_BrBasin['Tavg'] = (data_BrBasin["Tmax"] + data_BrBasin["Tmin"])/2

data_BrBasin['avg_wl'] = data_BrBasin['avg_wl'].astype(float)
def flood_marker(water_level):
  if water_level > 0:
    return 1
  else:
    return 0

data_BrBasin['Flood'] = (data_BrBasin['avg_wl'] - (data_BrBasin['Area_threshold'])).map(flood_marker)

flood_True = len(data_BrBasin.loc[data_BrBasin['Flood'] == 1])
flood_False = len(data_BrBasin.loc[data_BrBasin['Flood'] == 0])
print('1s :', flood_True,'  0s :',flood_False)

"""Working on Ganges Basin Dataset"""

imputer = SimpleImputer(missing_values=pd.NA, strategy="mean")

imputer.fit(data_GaBasin[["Rainfall"]])
data_GaBasin["Rainfall"] = imputer.transform(data_GaBasin[["Rainfall"]])

imputer.fit(data_GaBasin[["Humidity"]])
data_GaBasin["Humidity"] = imputer.transform(data_GaBasin[["Humidity"]])

imputer.fit(data_GaBasin[["Tmax"]])
data_GaBasin["Tmax"] = imputer.transform(data_GaBasin[["Tmax"]])

imputer.fit(data_GaBasin[["Tmin"]])
data_GaBasin["Tmin"] = imputer.transform(data_GaBasin[["Tmin"]])

imputer.fit(data_GaBasin[["Cloud_amt"]])
data_GaBasin["Cloud_amt"] = imputer.transform(data_GaBasin[["Cloud_amt"]])

imputer.fit(data_GaBasin[["max_wl"]])
data_GaBasin["max_wl"] = imputer.transform(data_GaBasin[["max_wl"]])

imputer.fit(data_GaBasin[["min_wl"]])
data_GaBasin["min_wl"] = imputer.transform(data_GaBasin[["min_wl"]])

imputer.fit(data_GaBasin[["avg_wl"]])
data_GaBasin["avg_wl"] = imputer.transform(data_GaBasin[["avg_wl"]])

imputer = SimpleImputer(missing_values=pd.NA, strategy="most_frequent")

imputer.fit(data_GaBasin[["Wind_dir"]])
data_GaBasin["Wind_dir"] = imputer.transform(data_GaBasin[["Wind_dir"]])

data_GaBasin['Tavg'] = (data_GaBasin["Tmax"] + data_GaBasin["Tmin"])/2

data_GaBasin['avg_wl'] = data_GaBasin['avg_wl'].astype(float)
def flood_marker(water_level):
  if water_level > 0:
    return 1
  else:
    return 0

data_GaBasin['Flood'] = (data_GaBasin['avg_wl'] - (data_GaBasin['Area_threshold'])).map(flood_marker)

flood_True = len(data_GaBasin.loc[data_GaBasin['Flood'] == 1])
flood_False = len(data_GaBasin.loc[data_GaBasin['Flood'] == 0])
print('1s :', flood_True,'  0s :',flood_False)

"""Working on Meghna Basin Dataset"""

imputer = SimpleImputer(missing_values=pd.NA, strategy="mean")

imputer.fit(data_MeBasin[["Rainfall"]])
data_MeBasin["Rainfall"] = imputer.transform(data_MeBasin[["Rainfall"]])

imputer.fit(data_MeBasin[["Humidity"]])
data_MeBasin["Humidity"] = imputer.transform(data_MeBasin[["Humidity"]])

imputer.fit(data_MeBasin[["Tmax"]])
data_MeBasin["Tmax"] = imputer.transform(data_MeBasin[["Tmax"]])

imputer.fit(data_MeBasin[["Tmin"]])
data_MeBasin["Tmin"] = imputer.transform(data_MeBasin[["Tmin"]])

imputer.fit(data_MeBasin[["Cloud_amt"]])
data_MeBasin["Cloud_amt"] = imputer.transform(data_MeBasin[["Cloud_amt"]])

imputer.fit(data_MeBasin[["max_wl"]])
data_MeBasin["max_wl"] = imputer.transform(data_MeBasin[["max_wl"]])

imputer.fit(data_MeBasin[["min_wl"]])
data_MeBasin["min_wl"] = imputer.transform(data_MeBasin[["min_wl"]])

imputer.fit(data_MeBasin[["avg_wl"]])
data_MeBasin["avg_wl"] = imputer.transform(data_MeBasin[["avg_wl"]])

imputer = SimpleImputer(missing_values=pd.NA, strategy="most_frequent")

imputer.fit(data_MeBasin[["Wind_dir"]])
data_MeBasin["Wind_dir"] = imputer.transform(data_MeBasin[["Wind_dir"]])

data_MeBasin['Tavg'] = (data_MeBasin["Tmax"] + data_MeBasin["Tmin"])/2

data_MeBasin['avg_wl'] = data_MeBasin['avg_wl'].astype(float)
def flood_marker(water_level):
  if water_level > 0:
    return 1
  else:
    return 0

data_MeBasin['Flood'] = (data_MeBasin['avg_wl'] - (data_MeBasin['Area_threshold'])).map(flood_marker)

flood_True = len(data_MeBasin.loc[data_MeBasin['Flood'] == 1])
flood_False = len(data_MeBasin.loc[data_MeBasin['Flood'] == 0])
print('1s :', flood_True,'  0s :',flood_False)

"""Working on South East Hill Basin Dataset"""

imputer = SimpleImputer(missing_values=pd.NA, strategy="mean")

imputer.fit(data_SEHBasin[["Rainfall"]])
data_SEHBasin["Rainfall"] = imputer.transform(data_SEHBasin[["Rainfall"]])

imputer.fit(data_SEHBasin[["Humidity"]])
data_SEHBasin["Humidity"] = imputer.transform(data_SEHBasin[["Humidity"]])

imputer.fit(data_SEHBasin[["Tmax"]])
data_SEHBasin["Tmax"] = imputer.transform(data_SEHBasin[["Tmax"]])

imputer.fit(data_SEHBasin[["Tmin"]])
data_SEHBasin["Tmin"] = imputer.transform(data_SEHBasin[["Tmin"]])

imputer.fit(data_SEHBasin[["Cloud_amt"]])
data_SEHBasin["Cloud_amt"] = imputer.transform(data_SEHBasin[["Cloud_amt"]])

imputer.fit(data_SEHBasin[["max_wl"]])
data_SEHBasin["max_wl"] = imputer.transform(data_SEHBasin[["max_wl"]])

imputer.fit(data_SEHBasin[["min_wl"]])
data_SEHBasin["min_wl"] = imputer.transform(data_SEHBasin[["min_wl"]])

imputer.fit(data_SEHBasin[["avg_wl"]])
data_SEHBasin["avg_wl"] = imputer.transform(data_SEHBasin[["avg_wl"]])

imputer = SimpleImputer(missing_values=pd.NA, strategy="most_frequent")

imputer.fit(data_SEHBasin[["Wind_dir"]])
data_SEHBasin["Wind_dir"] = imputer.transform(data_SEHBasin[["Wind_dir"]])

data_SEHBasin['Tavg'] = (data_SEHBasin["Tmax"] + data_SEHBasin["Tmin"])/2

data_SEHBasin['avg_wl'] = data_SEHBasin['avg_wl'].astype(float)
def flood_marker(water_level):
  if water_level > 0:
    return 1
  else:
    return 0

data_SEHBasin['Flood'] = (data_SEHBasin['avg_wl'] - (data_SEHBasin['Area_threshold'])).map(flood_marker)

flood_True = len(data_SEHBasin.loc[data_SEHBasin['Flood'] == 1])
flood_False = len(data_SEHBasin.loc[data_SEHBasin['Flood'] == 0])
print('1s :', flood_True,'  0s :',flood_False)

"""Dataset Download"""

data_BrBasin.to_csv('dataset_Br.csv')
data_GaBasin.to_csv('dataset_Ga.csv')
data_MeBasin.to_csv('dataset_Me.csv')
data_SEHBasin.to_csv('dataset_SEH.csv')