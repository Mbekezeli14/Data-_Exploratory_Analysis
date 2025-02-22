# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 02:14:00 2025

@author: Mbekezeli Tshabalala
"""

'''
Import libraries
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

'''
 Data loading and Inspection
'''
data = pd.read_csv("C:/Users/Mbekezeli Tshabalala/OneDrive/Documents/My projects/Hex Softwares/Week 1/Project_1/Airbnb_Open_Data.csv")


# Inspect the dataset using the info() function: The info() function from the pandas library provides us with a list of column names, the number of non null values in each column and the data type of each column.
# It also provides us with the total number of entries and columns

data.info()

# From the results of this function, we can see that our dataframe contain 102 599 records and a total of 26 columns
# We also see that there are missing values in most of our columns
# Column names are not consistent. Name column is in uppercases while other column names are in lowercases
# We see that other column names contain spaces between them while others are separated by an underscore character


# Show the first 10 entries of the data frame
data.head(10)

"""
 Data cleaning process
"""
#1. Ensure consistent column name: The output of the info() showed us that there is inconsistency in column names.
#The id column name was in lower cases while the name column name was in upper cases.
#Other column names had spaces between words and others had underscores between them.
#To fix these inconsistencies we are going to use the strpip(), lower() and replace() from str 

data.columns = data.columns.str.strip().str.lower().str.replace(' ','_')


# 2. Remove irrelevent columns
data = data.drop(columns=['id','host_id','host_identity_verified','lat','long','country','country_code','calculated_host_listings_count','house_rules','license','last_review'], axis=1)
print(data.shape) # Inspect the number of rows and columns 

#3. Convert column data types: From the dataset we can see that the price and service_fee columns are of string type since the values have a dollar sign before the numbers. 
# We will convert them to float type by removing the dollar sign from each value and placing it next to each column name.
# Rename the column names of price and service_fee
data.rename(columns={'price':'price($)','service_fee':'service_fee($)'}, inplace= True)

#Remove the dollar sign and the comma from the price values 
data['price($)'] = data['price($)'].str.strip('$')
data['price($)'] = data['price($)'].str.replace(',','')

#Remove the dollar sign from the service_fee values
data['service_fee($)'] = data['service_fee($)'].str.strip('$')

#Convert the data type of price from string to float
data['price($)'] = data['price($)'].astype(float)
data['service_fee($)'] = data['service_fee($)'].astype(float)

# 4. Handling missing values

#Check for missing values
print(data.isnull().sum())

# Impute the name column with the 'no name provided' value
data['name'] =data['name'].fillna("No Name Provided")

# Impute the name column with the 'unknown' value
data['host_name'] = data['host_name'].fillna('Unknown')
data['neighbourhood_group'] = data['neighbourhood_group'].fillna('unknown')
data['neighbourhood'] = data['neighbourhood'].fillna('unknown')

# Impute with the most common value
data['instant_bookable'] = data['instant_bookable'].fillna(data['instant_bookable'].mode()[0])
data['cancellation_policy'] = data['cancellation_policy'].fillna(data['cancellation_policy'].mode()[0])




#Imputing the price column
#1. Check the distribution of the variable to determine whether to impute with the mean or the median
plt.title('Box-plot of listing prices')
sns.boxplot(x='price($)',data=data) #Since the box-plot shows that the data is normally distributed and no outliers, I'm going to use the mean
data['price($)'] = data['price($)'].fillna(data['price($)'].mean())
data.info()
#Check the distribution of the service_fee($) variable

sns.boxplot(x='service_fee($)', data=data) #Since the data is normally distributed and no outliers, we are going to impute using the mean
data['service_fee($)'] = data['service_fee($)'].fillna(data['service_fee($)'].mean())

#
sns.boxplot(data=data, x = 'construction_year')
data['construction_year'] = data['construction_year'].fillna(data['construction_year'].mean())

#
sns.boxplot(data['minimum_nights']) #Since the data has outliers, I am going to impute using a median
data['minimum_nights'] = data['minimum_nights'].fillna(data['minimum_nights'].median())

#
sns.boxplot(data=data, x='number_of_reviews') #Since the data has outliers, I am going to impute using a median
data['number_of_reviews'] = data['number_of_reviews'].fillna(data['number_of_reviews'].median())

#
sns.boxplot(data=data, x='reviews_per_month') #Since the data has outliers, I am going to impute using a median
data['reviews_per_month'] = data['reviews_per_month'].fillna(data['reviews_per_month'].median())

#
sns.boxplot(data=data, x='review_rate_number') #Since the data has no outliers, I am going to impute using a mean
data['review_rate_number'] = data['review_rate_number'].fillna(data['review_rate_number'].mean())

#
sns.boxplot(data=data, x='availability_365') #Since the data has no outliers, I am going to impute using a mean
data['availability_365'] = data['availability_365'].fillna(data['availability_365'].median())
#
for x in data.index:
    if data.loc[x,'availability_365'] > 365.0:
        data.loc[x,'availability_365']= data['availability_365'].median()
    else:
        continue
#
print(data.isnull().sum())

# 5. Remove duplicate or irrelevant observations:

# Show the number of duplicates in the dataframe
print(data.duplicated().sum())  # Our dataset contain 6545 duplicates

#Remove duplicates
data = data.drop_duplicates()

# Separate categorical values from numerical values
cols = ['price($)','service_fee($)','number_of_reviews','review_rate_number','availability_365','reviews_per_month','minimum_nights','construction_year']
cat = ['neighbourhood_group','neighbourhood','room_type','instant_bookable']
"""
Data distributions
"""
#Multiple scatter-plots and distributions To explore relationships between variables
cor = data[cols].corr()
sns.pairplot(data[cols], diag_kind="kde", corner=True)
plt.show()
#Based on these scatter plots and correlation values:
# We see that the is a strong posivite relationship between price and service fee (0.99769)
# The is a weak positive relationship between reviews_per_month and number of reviews (0.590444)
# And no relationship between the rest of the variabels
# Distributions of the variables:
# price, service fee and construction year are symmetrically distributed but have a large variance
# number of reviews, reviews per month and availability have a distribution that is skewed to the right
# review_rate_number distribution is multimodal



g = sns.FacetGrid(data, col="room_type", height=4)
g.map_dataframe(sns.scatterplot, x="price($)", y="number_of_reviews", alpha=0.5)
plt.show()

#Room Type vs Price- Boxplot
plt.title('Prices by room_types')
sns.boxplot(x='room_type', y='price($)', data=data)
sns.barplot(x='room_type', y='price($)', hue='room_type', data=data)
# Based on the bar plot, we see that Hotel room prices are slightly greater than the other listing types


#
plt.title("Room Type count")
sns.countplot(x="room_type", data=data, palette="Set2")
# Based on this plot we can see that the apartment listing are greater than the other listing types,
# followed by private room and the Hotels are the least listings

#
plt.figure(figsize=(8, 5))
sns.countplot(x="neighbourhood_group", hue="room_type", data=data, palette="Set2")
plt.title("neighbourhood_group vs Room Type")
plt.xlabel("neighbourhood_group")
plt.ylabel("Count")
#Based on the plot, we see that Manhattan has more apartment listings, followed by Brooklyn then Queens.
#Brooklyn has more private room listings followed by Manhattan then Queens