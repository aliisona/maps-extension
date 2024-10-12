import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.impute import SimpleImputer
import tensorflow as tf

#Load the Data

df = pd.read_csv("C:/Users/chens/AI and Coding/Hackathons/maps-extension/ML/data/crashdata_boston.csv")

cols = ["Crash_Number", "City_Town_Name", "Crash_Date", "Crash_Time", "Crash_Severity", "Maximum_Injury_Severity_Reported", 
        "Number_of_Vehicles", "Total_Nonfatal_Injuries", "Total_Fatal_Injuries", "Manner_of_Collision", "Vehicle_Action_Prior_to_Crash", 
        "Vehicle_Travel_Directions", "Most_Harmful_Events", "Vehicle_Configuration", "Road_Surface_Condition", "Ambient_Light", "Weather_Condition", 
        "At_Roadway_Intersection", "Distance_From_Nearest_Roadway_Intersection", "Distance_From_Nearest_Milemarker", "Distance_From_Nearest_Exit", 
        "Distance_From_Nearest_Landmark", "Non_Motorist_Type", "X_Cooordinate", "Y_Cooordinate"]

df.columns = cols 
print(df.head())

#reorder + take data we need
cols_keep = ["Road_Surface_Condition", "Ambient_Light", "Weather_Condition", "Maximum_Injury_Severity_Reported" ,"Total_Nonfatal_Injuries", "Total_Fatal_Injuries"]
df = df[cols_keep]

print(df.head())

#sort our data

#road_surface_condition:
encoder_road = OrdinalEncoder(categories=[['dry', 'wet', 'ice']])
encoded_data_road = encoder_road.fit_transform(df[['Road_Surface_Condition']])

#Weather_Condition:
possible_weather_conditions = ['Sleet, hail (freezing rain or drizzle)', 
']









