#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Libraries needed
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# In[2]:


#Reading CSV Files
df = pd.read_csv("Desktop/DisneyMoviesDataset.csv")
print(df)


# In[3]:


print(f'summary of the data: \n{df.info()}')


# In[4]:


print(f'checking null values: \n{df.isnull().sum()}')


# In[5]:


#Cleaning data
df = df.drop(['Unnamed: 0', 'Running time', 'Release date', 'Budget', 'Box office', 'Music by', 'Distributed by', 'Story by', 'Narrated by', 'Cinematography', 'Edited by', 'Produced by', 'Screenplay by', 'Production companies', 'Adaptation by', 'Traditional', 'Simplified'],axis=1)
df


# In[6]:


# creating a new revenue column
df['Revenue'] = df['Box office (float)'] - df['Budget (float)']
df.head()


# In[7]:


top10 = df["Revenue"].sort_values(ascending=False).head(10).reset_index()["Revenue"]
top10


# In[8]:


fig = px.bar(df[df["Revenue"].isin(top10)], 
              x="title", 
              y="Revenue", 
              title = "Top 10 profitable Disney Movies")
fig.show()


# In[9]:


import json
import re
import math

# Add convert function to convert multiple directors into list of directors
def convert_list(list_as_str):
    # If the data looks like a list, do the conversion
    if not list_as_str:
        return []
    elif isinstance(list_as_str, str) and list_as_str.startswith('['):
        # Change to JSON style quotes
        list_as_str = list_as_str.replace("'", '"')
        # Remove bracket in name
        list_as_str = re.sub("\(.*\)", "", list_as_str)
        # Remove white space
        list_as_str = list_as_str.strip()
         # Use JSON loads to convert string of list to list
        try:
          return json.loads(list_as_str)
        # Return empty if not JSON
        except json.JSONDecodeError as e:
            return []
    elif isinstance(list_as_str, str):
        return [list_as_str]
    # Return empty if NaN
    elif math.isnan(list_as_str):
        return []
    else:
        return [list_as_str]
  
directed_df = df['Directed by'].transform(convert_list)

# Use explode to create rows for each director
exploded_df = directed_df.explode('Directed by')
# Create new DF
new_df = pd.DataFrame(exploded_df)

# Count number of times each director is in df
keys_director = new_df['Directed by'].value_counts().keys().to_list()
values_director = new_df['Directed by'].value_counts().to_list()

fig_director = px.bar(x = keys_director[:10], y = values_director[:10], data_frame = new_df, 
             title="Top 10 Directors", 
             labels={'x': 'Directors', 'y': 'Number of Movies'})
fig_director.show()


# In[10]:


starring_df = df['Starring'].transform(convert_list)

# Use explode to create rows for each cast
exploded_df = starring_df.explode('Starring')
# Create new DF
new_df = pd.DataFrame(exploded_df)

keys_cast = new_df['Starring'].value_counts().keys().to_list()
values_cast = new_df['Starring'].value_counts().to_list()

fig = px.bar(x = keys_cast[:10], y = values_cast[:10], data_frame=new_df, 
             title="Top 10 Casts", 
             labels={'x': 'Casts', 'y': 'Number of Movies'})
fig.show()


# In[11]:


top20imdb = df["imdb"].sort_values(ascending=False).head(20).reset_index()["imdb"]
top20imdb


# In[12]:


fig = px.bar(df[df["imdb"].isin(top20imdb)], 
              x="title", 
              y="imdb", 
              title = "IMDB Top 20 Disney Movies")
fig.show()


# In[13]:


fig = px.scatter(df, x="Running time (int)", y="imdb", title="How Movie Running Time Related to IMDB Rating Score")
fig.show()


# In[14]:


fig = px.scatter(df, x="Release date (datetime)", y="imdb", title="How Release Year related to IMDB Rating Scores")
fig.show()


# In[ ]:




