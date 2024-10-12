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

exclude_weather_conditions = ['Not Reported', 'Snow/Other', 'Clear/Other', 'Unknown', 'Cloudy/Other', 
                      'Snow/Unknown', 'Cloudy/Unknown', 'Clear/Unknown', 'Rain/Unknown', 'Other', 
                      'Unknown/Unknown', 'Unknown/Cloudy', 'Rain/Other', 'Other/Snow', 'Other/Clear', 
                      'Other/Other', 'Sleet, hail (freezing rain or drizzle)/Unknown', 'Unknown/Clear', 
                      'Other/Unknown', 'Severe crosswinds/Other', 'Other/Rain']

df = df[~df['Weather_Condition'].isin(exclude_weather_conditions)]

exclude_road_conditions = ['Not reported', 'Unknown', 'Other']

df = df[~df['Road_Surface_Condition'].isin(exclude_road_conditions)]
#sort the data

road_categories =  {
    'Good Road': ['Dry'],
    'Mediocre Road': ['Wet'],
    'Bad Road': ['Snow', 'Slush', 'Sand, mud, dirt, oil, gravel', 'Water (standing, moving)'],
    'Extreme Road': ['Ice'] }

weather_categories = {
    'Good Weather': ['Clear', 'Clear/Clear'],
    
    'Mediocre Weather': ['Cloudy', 'Cloudy/Cloudy', 'Clear/Cloudy', 'Cloudy/Clear'],
    
    'Bad Weather': ['Rain', 'Snow', 'Snow/Snow', 'Cloudy/Snow', 'Snow/Rain', 'Clear/Snow', 'Snow/Clear', 'Cloudy/Rain', 'Rain/Cloudy', 'Rain/Rain', 'Rain/Snow', 'Rain/Clear', 'Snow/Cloudy', 'Fog, smog, smoke', 'Rain/Fog, smog, smoke', 'Cloudy/Fog, smog, smoke', 'Fog, smog, smoke/Rain', 'Fog, smog, smoke/Fog, smog, smoke', 'Fog, smog, smoke/Cloudy', 'Snow/Fog, smog, smoke']
,
    
    'Extreme Weather': ['Sleet, hail (freezing rain or drizzle)', 'Snow/Sleet, hail (freezing rain or drizzle)', 'Snow/Blowing sand, snow', 'Clear/Blowing sand, snow', 'Sleet, hail (freezing rain or drizzle)/Sleet, hail (freezing rain or drizzle)', 'Rain/Sleet, hail (freezing rain or drizzle)', 'Rain/Severe crosswinds', 'Clear/Sleet, hail (freezing rain or drizzle)', 'Clear/Severe crosswinds', 'Snow/Severe crosswinds', 'Cloudy/Blowing sand, snow', 'Blowing sand, snow/Blowing sand, snow', 'Sleet, hail (freezing rain or drizzle)/Rain', 'Cloudy/Sleet, hail (freezing rain or drizzle)', 'Sleet, hail (freezing rain or drizzle)/Cloudy', 'Rain/Blowing sand, snow', 'Severe crosswinds', 'Blowing sand, snow', 'Sleet, hail (freezing rain or drizzle)/Blowing sand, snow', 'Clear/Fog, smog, smoke', 'Sleet, hail (freezing rain or drizzle)/Clear', 'Sleet, hail (freezing rain or drizzle)/Snow', 'Sleet, hail (freezing rain or drizzle)/Severe crosswinds', 'Severe crosswinds/Blowing sand, snow', 'Cloudy/Severe crosswinds', 'Severe crosswinds/Severe crosswinds', 'Blowing sand, snow/Sleet, hail (freezing rain or drizzle)', 'Severe crosswinds/Rain', 'Severe crosswinds/Clear']
}

#apply sorting

def categorize_condition(condition, categories):
    for category, conditions in categories.items():
        if condition in conditions:
            return category

df['Road_Category'] = df['Road_Surface_Condition'].apply(lambda x: categorize_condition(x, road_categories))
df['Weather_Category'] = df['Weather_Condition'].apply(lambda x: categorize_condition(x, weather_categories))

print(df.head())
print(df.shape())

#One hot encoding
columns_one_hot= ["Road_Category", "Weather_Category"]
df = pd.get_dummies(df, columns = columns_one_hot, prefix = columns_one_hot, drop_first = True )


