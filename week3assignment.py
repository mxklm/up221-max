#!/usr/bin/env python
# coding: utf-8

# # Identifying LA County Census Tracts with the Highest Percentage of Transit Use in 2010 and 2020 
# ## Maxwell Kilman
# We have chosen to identify a census tract with the highest percentage of public transit users to conduct our broader analysis on shade/tree cover, heat equity, and transportation use. In this assignment, I will only focus on identifying the tract with the greatest proportion of public transit users in comparison with other modes of transportation. I will conduct this form of data exploration using American Community Survey (ACS) data from both 2010 and 2022. I have chosen these two sets of census data, as our broader analysis will aim to identify changes over time in urban tree cover after the LADWP launched their “Trees for a Green LA” program in 2001. 

# #### Importing and Cleaning Datasets 

# I will begin by importing both `pandas` and `geopandas`

# In[2]:


# import necessary modules
import pandas as pd
import geopandas as gpd


# As always, the first step in this process is to load the relevant census variables into Jupyter Hub. Next, I will import each dataset into my notebook.

# In[3]:


# importing two ACS datasets
ACS_22 = pd.read_csv('Census_Data/ACS_22.csv')
ACS_10 = pd.read_csv('Census_Data/ACS_10.csv')


# To aid in the process of cleaning my datasets, I have assigned the census data from 2022 to the dataframe `ACS_22` and 2010 data to the dataframe `ACS_10` 

# To identify potential issues with my dataframe, I will first use the `.shape` and `.head` commands.

# In[4]:


# shape of dataframe
ACS_22.shape


# In[5]:


# shape of dataframe
ACS_10.shape


# As noted above, I have 2499 samples/rows and 45 columns from the 2022 ACS dataset and 2347 samples and 45 columns in the 2010 dataset. 

# Another critical step before I proceed is to examine the column `GEO_ID` to identify that Python has dropped the leading zero in the FIPS state code.

# In[6]:


# .head to check leading zeros in 2022 data
ACS_22.GEO_ID.head()


# In[7]:


# .head to check leading zeros in 2010 data
ACS_10.GEO_ID.head()


# As expected, python dropped the leading zeros in both datasets, so I will use the `dtype` command to convert `GEO_ID` to a `str` or `object`

# In[8]:


# converting GEO_ID to a string for 22
ACS_22 = pd.read_csv(
    'Census_Data/ACS_22.csv',
    dtype=
    {
        'GEO_ID':str
    }
)


# In[9]:


# converting GEO_ID to a string 10  
ACS_10 = pd.read_csv(
    'Census_Data/ACS_22.csv',
    dtype=
    {
        'GEO_ID':str
    }
)


# Now, if we use the same `.head` command as above, we should hopefully see our `GEO_ID` with the necessary leading zero.

# In[10]:


# .head to check leading zeros in 2022 data again
ACS_22.GEO_ID.head()


# In[11]:


# .head to check leading zeros in 2010 data again
ACS_10.GEO_ID.head()


# Next, we will want to make sure our datasets do not have null or missing values and have each values in the correct types (`object` and `int64`)

# In[12]:


# verifying non-null values/missing values/type 22
ACS_22.info(verbose=True, show_counts=True)


# In[13]:


# verifying non-null values/missing values/type 22
ACS_10.info(verbose=True, show_counts=True)


# In both datasets, our type and non-null values seem appropriate. We do not appear to need to drop any null values or use `.dtype` further. 

# Next, we will want to create a subset of our data to use in our analysis. We are only interested in the `GEO_ID` column as well as the column for the total counts of public transportation use excluding taxicab (column `B08301_010E`). That said, it is also necessary to include the overall total of commuters for each census tract (`B08301_001E`). The total number of commuters will allow us to appropriately scale the count of public transportation users by census tract. We will want to add a column to our reduced dataframe that lists the transportation users as a percentage of the total commuters. 

# In[14]:


# reducing the dataframe for 2022
columns_to_keep = ['GEO_ID',
                   'B08301_010E',
                   'B08301_001E'
                  ]
ACS_22B = ACS_22[columns_to_keep]


# In[15]:


# reducing the dataframe for 2010
columns_to_keep2 = ['GEO_ID',
                   'B08301_010E',
                   'B08301_001E'
                  ]
ACS_10B = ACS_10[columns_to_keep2]


# We can review these changes using the `.head()` command

# In[16]:


# Reviewing reduced dataframe
ACS_22B.head()


# In[17]:


# Reviewing reduced dataframes
ACS_10B.head()


# Now that we are satisfied with our reduced two dataframes, we can add a column for the percentages of transportation users out of the total commuters in each tract. 

# In[18]:


# adding percentage transit for 2022
ACS_22B['transit_pct'] = (ACS_22B['B08301_010E'] / ACS_22B['B08301_001E']) * 100


# In[19]:


# adding percentage transit for 2010
ACS_10B['transit_pct'] = (ACS_10B['B08301_010E'] / ACS_10B['B08301_001E']) * 100


# Let's check the results of that addition using the `.sample()` command

# In[20]:


# Verifying results of column change
ACS_22B.sample(5)


# In[21]:


# Verifying results of column change
ACS_10B.sample(5)


# The results seem reasonable. We can now proceed by editing the column names. 

# In[22]:


# changing column names 22
ACS_22B.columns = ['FIPS',
'Total Transit Users (excluding taxicabs)',                 
'Total Commuters', 
'Percent Transit Users'
                  ]


# In[23]:


# changing column names 10
ACS_10B.columns = ['FIPS',
'Total Transit Users (excluding taxicabs)',                 
'Total Commuters', 
'Percent Transit Users'
                  ]


# In[24]:


# Review column label changes 
ACS_22B.head()


# In[25]:


# Review column label changes 
ACS_10B.head()


# Now that we have successfully prepared our dataframes, we can proceed with some basic descriptive statistics. First and foremost, we will want to identify the tracts with the highest percentage of transit users. 

# #### Basic Descriptive Statistics 

# To sort the dataframes by `Percent Transit Users` in descending order, we will need to create an index based on the magnitude of the percentage values. Then, we will be able to sort the index column from greatest to lowest and more easily identify the census tracts with the highest proportion of total transit users. 

# In[26]:


# indexing based on percent transit users and sorting by rank 
ACS_22B['Rank'] = ACS_22B['Percent Transit Users'].rank(ascending = 0) 
ACS_22B = ACS_22B.set_index('Rank') 
ACS_22B = ACS_22B.sort_index() 
ACS_22B.head()


# In[27]:


# indexing based on percent transit users and sorting by rank 
ACS_10B['Rank'] = ACS_10B['Percent Transit Users'].rank(ascending = 0) 
ACS_10B = ACS_10B.set_index('Rank') 
ACS_10B = ACS_10B.sort_index() 
ACS_10B.head()


# Now that we prepared our rank-ordered dataframes, we can create some simple plots to visualize the differences in `Percent Transit Users` between tracts. 

# While it will become apparent once we map our dataframe, a preliminary search for information on these top five tracts reveals that three fall in the Westlake-MacArthur Park area and two are transects of Skid Row. Before creating any visuals, however, I will look at some statistics related to the `percent transit users` column. First, I'll examine the mean using the `.mean()` command

# In[28]:


# finding the mean
ACS_22B['Percent Transit Users'].mean()


# In[29]:


# finding the mean
ACS_10B['Percent Transit Users'].mean()


# We notice a fairly consistent mean of 4.91% of commuters using public transit. That said, our mean is likely skewed by the presence of outliers, namely the several LAC census tracts with a population of 0. We can identify this by running a simple command like `.tail()` 

# In[30]:


# reviewing the tail of our df
ACS_22B.tail()


# Recognizing the influence of these outliers, a more informative descriptive statistic might be acquired by using the `.median()` command. By doing so, we will be able to identify the `percent transit users` at the 50th percentile.

# In[31]:


# comparing the median to the mean
ACS_22B['Percent Transit Users'].median()


# In[32]:


# finding the median for comparison with the mean 
ACS_10B['Percent Transit Users'].median()


# But wait, we have to realize the "outliers" have 0 commuters overall and a value of "NaN" for `Percent Transit Users`. Thus, they are not factored into the calculation of the mean. In addition, we might note with caution that the median remains lower than the mean. This could suggest the tracts with a high percentage of transit users are fairly limited. At this point, it might help to use the `.describe()` command.

# In[33]:


# running a basic .describe function to look at SD and percentiles
ACS_22B['Percent Transit Users'].describe()


# In[34]:


# running a basic .describe function to look at SD and percentiles
ACS_10B['Percent Transit Users'].describe()


# As expected, this prediction regarding the typical value in our distribution seems accurate. Most values (75%) in the `Percent Transit Users` column remain below around 6.4%, a stark difference from the 57% in the Westlake Census Tract. 

# We can visualize these outliers using a simple boxplot: 

# In[35]:


# making a boxplot to visualize the distribution
ACS_22B.boxplot(column=['Percent Transit Users'])


# Interestingly, quite a few census tracts lie outside the "whiskers" of our boxplot. This might indicate some form of error with my approach. I'll need to review this. For now, I will proceed with the visualization process by matching geojson data with my ACS data.

# In[36]:


# importing corresponding geojson data using gpd
tracts=gpd.read_file('Census_Data/Census_Tracts_2020-Copy1.geojson')
tracts2=gpd.read_file('Census_Data/Census_Tracts_2020-Copy1.geojson')
tracts.head()


# At this point, it's easiest to subset the geojson data, keeping only the necessary columns: FIPS and geometry. 

# In[37]:


# subsetting data and editing to create a FIPS column
tracts = tracts[['CT20','geometry']]
tracts['FIPS'] ='06' + '037' + tracts['CT20']
tracts2 = tracts2[['CT20','geometry']]
tracts2['FIPS'] ='06' + '037' + tracts['CT20']
tracts.head()


# Our geojson dataframe looks like it's in good shape, so we can proceed with the process of merging it with our ACS data. We will have to complete this step for both dataframes

# In[38]:


# merging on FIPS for ACS 22
tracts_transit22=tracts.merge(ACS_22B,on="FIPS")
tracts_transit22.head()


# In[39]:


# merging on FIPS for ACS 10
tracts_transit10=tracts2.merge(ACS_10B,on="FIPS")
tracts_transit10.head()


# In[40]:


import folium 


# In[41]:


# mapping
m = folium.Map(location=[34.2,-118.2], 
               zoom_start = 9,
               tiles='CartoDB positron', 
               attribution='CartoDB')

# plot chorpleth 
folium.Choropleth(
                  geo_data=tracts_transit22, 
                  data=tracts_transit22,        
                  key_on='feature.properties.FIPS', 
                  columns=['FIPS', 'Percent Transit Users'], 
                  fill_color='BuPu',
                  line_weight=0.1, 
                  fill_opacity=0.8,
                  line_opacity=0.2, 
                  legend_name='Percent Transit Users (2022)').add_to(m)    
m


# In[42]:


# mapping
m = folium.Map(location=[34.2,-118.2], 
               zoom_start = 9,
               tiles='CartoDB positron', 
               attribution='CartoDB')

# plot chorpleth 
folium.Choropleth(
                  geo_data=tracts_transit10, 
                  data=tracts_transit10,          
                  key_on='feature.properties.FIPS', 
                  columns=['FIPS', 'Percent Transit Users'], 
                  fill_color='BuPu',
                  line_weight=0.1, 
                  fill_opacity=0.8,
                  line_opacity=0.2, # line opacity (of the border)
                  legend_name='Percent Transit Users (2010)').add_to(m)   
m


# After creating a `Choropleth` map using `folium`, we can easily identify the geography of transit use in LA County, most notably in the Westlake-MacArthur Park area and sections of Skid Row. To tidy up thes maps, it may help to drop our `NaN` values. 

# In[43]:


# filtering for only values that are not NaN
tracts_transit22b = tracts_transit22[tracts_transit22['Percent Transit Users'].notnull()]
tracts_transit10b = tracts_transit10[tracts_transit10['Percent Transit Users'].notnull()]


# In[44]:


# mapping revised
m = folium.Map(location=[34.2,-118.2], 
               zoom_start = 9,
               tiles='CartoDB positron', 
               attribution='CartoDB')

# plot chorpleth 
folium.Choropleth(
                  geo_data=tracts_transit22b, 
                  data=tracts_transit22b,         
                  key_on='feature.properties.FIPS', 
                  columns=['FIPS', 'Percent Transit Users'], 
                  fill_color='BuPu',
                  line_weight=0.1, 
                  fill_opacity=0.8,
                  line_opacity=0.2, 
                  legend_name='Percent Transit Users (2022)').add_to(m)    
m


# In[45]:


# mapping revised
m = folium.Map(location=[34.2,-118.2], 
               zoom_start = 9,
               tiles='CartoDB positron', 
               attribution='CartoDB')

# plot chorpleth over the base map
folium.Choropleth(
                  geo_data=tracts_transit10b, 
                  data=tracts_transit10b,         
                  key_on='feature.properties.FIPS', 
                  columns=['FIPS', 'Percent Transit Users'], 
                  fill_color='BuPu',
                  line_weight=0.1, 
                  fill_opacity=0.8,
                  line_opacity=0.2, 
                  legend_name='Percent Transit Users (2010)').add_to(m)    
m


# ### Closing Remarks 
# Ultimately, this census data exploration revealed minimal changes in transit use between 2010 and 2020 regarding the top five census tracts with the highest percentage of transit users. Nevertheless, this sorted data will aid in our broader analysis, as we can more accurately focus on areas with the highest transit use and make comparisons with those areas with minimal transit use. It will be useful to assess how shade cover differs between these two groups of census tracts.  

# In[ ]:




