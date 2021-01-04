import pandas as pd

#Reading in Pandas Dataframe and Cleaning Data
excel_catalogue = pd.read_excel('SAO.xlsx')
tidy_catalogue = excel_catalogue.rename(columns = {'Unnamed: 0': 'Star ID', 'Unnamed: 1': 'RA', 'Unnamed: 2': 'DE', 'Unnamed: 3': "Magnitude"}, inplace=False)

#Filtering Magnitude
less_and_equal_6 = tidy_catalogue['Magnitude']<=6.0
filtered_catalogue = tidy_catalogue[less_and_equal_6]

#Saving to CSV File
filtered_catalogue.to_csv("Below_6.0_SAO.csv")