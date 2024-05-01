import pandas as pd
import numpy as np

 # question 2...

df_gods = pd.read_csv("C:\githubrepo\TrainingWork\PYTHON\pandaspractice\gods.csv")
print(df_gods)
print('_'*100)
df_goddesses = pd.read_csv("C:\githubrepo\TrainingWork\PYTHON\pandaspractice\goddess.csv")
print(df_goddesses)
print('_'*100)

#print(dfgod.merge(dfgoddess, how='left', on='domain'))

# 1. Merge the data from greek_gods.csv and greek_goddesses.csv based on a common field and create a new table that includes information about both gods and goddesses.

# df_gods.rename(columns={'god': 'deity'}, inplace=True)
# df_goddesses.rename(columns={'goddess': 'deity'}, inplace=True)

# Now concatenate them

df = pd.concat([df_gods, df_goddesses], ignore_index=True)
print(df)
print('_'*100)
# 2. Filter the merged table to only include gods and goddesses who are older than 8000 years, then sort them based on their ages in descending order.

df2 =df[df['Age'] > 8000].sort_values(by='Age', ascending=False)
print(df2)
print('_'*100) 

# 3.Join the two tables based on the "Domain" field and calculate the average age of gods and goddesses in each domain.
domain = set(df_gods['Domain']).intersection(set(df_goddesses['Domain']))
print("Common Domains:", domain)
print('_'*100) 
# Merge the two dataframes based on the 'Domain' column
df3 = pd.merge(df_gods, df_goddesses, on='Domain', suffixes=('_god', '_goddess'))

# Calculate the average age for each domain
# average_age_by_domain = df3.groupby('Domain')[['Age_god', 'Age_goddess']].mean()
# print(average_age_by_domain)
# print('_'*100) 
# df3
# avg_age_per_domain = df3.groupby('Domain')['Age'].mean()
# print(avg_age_per_domain)
# print('_'*100) 

# 4.Determine which god/goddess has the highest age, and then find out if they are a god or a goddess.
df4 = pd.concat([df_gods, df_goddesses], ignore_index=True)
# Find the entry with the highest age
max_age_entry = df4.loc[df4['Age'].idxmax()]
# Determine if the entry is a god or a goddess
highest_age_name = max_age_entry['God'] if 'God' in max_age_entry else max_age_entry['Goddess']
highest_age_gender = max_age_entry['Gender']
print(f"The {highest_age_gender.lower()} with the highest age is {highest_age_name}, aged {max_age_entry['Age']}.")
print('_'*100) 

# 5.Create a new column in each table called "Age Group" and categorize
# the gods/goddesses into groups such as "Young" (age < 5000), "Middle-aged" (age between 5000 and 8000), and "Old" (age > 8000)

def categorize_age(age):
    if age < 5000:
        return 'Young'
    elif 5000 <= age < 8000:
        return 'Middle-aged'
    elif age >= 8000:
        return 'Old'
    else:
        return 'Unknown'

# Apply the function to create the "Age Group" column
df_gods['Age Group'] = df_gods['Age'].apply(categorize_age)
df_goddesses['Age Group'] = df_goddesses['Age'].apply(categorize_age)

# Display the updated tables
print("Table for Gods:")
print(df_gods)
print("\nTable for Goddesses:")
print(df_goddesses)

