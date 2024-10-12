import pandas as pd 
import csv
import numpy as np 
import seaborn as sns
print("seaborn")
import matplotlib.pyplot as plt
print("matplotlib")
from sklearn.model_selection import train_test_split
print("sklearn")
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, StandardScaler
print("sklearn2")
from imblearn.over_sampling import RandomOverSampler
print("imblearn")
from sklearn.impute import SimpleImputer
print("sklearn3")
import tensorflow as tf
print("tensorflow")

# Load the Data

df = pd.read_csv("data/BostonCrashDetails.csv")

cols = ["Crash_Number", "City_Town_Name", "Crash_Date", "Crash_Time", "Crash_Severity", "Maximum_Injury_Severity_Reported", 
        "Number_of_Vehicles", "Total_Nonfatal_Injuries", "Total_Fatal_Injuries", "Manner_of_Collision", "Vehicle_Action_Prior_to_Crash", 
        "Vehicle_Travel_Directions", "Most_Harmful_Events", "Vehicle_Configuration", "Road_Surface_Condition", "Ambient_Light", "Weather_Condition", 
        "At_Roadway_Intersection", "Distance_From_Nearest_Roadway_Intersection", "Distance_From_Nearest_Milemarker", "Distance_From_Nearest_Exit", 
        "Distance_From_Nearest_Landmark", "Non_Motorist_Type", "X_Cooordinate", "Y_Cooordinate"]

df.columns = cols 

#reorder + take data we need
cols_keep = ["Road_Surface_Condition", "Weather_Condition", "Maximum_Injury_Severity_Reported" ,"Total_Nonfatal_Injuries", "Total_Fatal_Injuries"]
df = df[cols_keep]

print(df.head())



# #sort our data
# df_filtered = df[df['weather_condition'] != 'Not Reported']


# #road_surface_condition:
# encoder_road = OrdinalEncoder(categories=[['dry', 'wet', 'ice']])
# encoded_data_road = encoder_road.fit_transform(df[['Road_Surface_Condition']])

# # Weather_Condition:


# unique_entries = sorted(list(set(df['Road_Surface_Condition'])))
# print(unique_entries)

categories = {
    'Good_Weather': [],
    'Okay_Weather': [],
    'Precipitation': [],
    'Severe': []
}





# def csvFilter():
#     with open('data/BostonCrashDetails.csv', newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=' ')
#         out = []

#         for row in reader:
#                 print(row[0])


# csvFilter()






