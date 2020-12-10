#!/usr/bin/env python
# coding: utf-8

# In[139]:


import pandas as pd
import numpy as np


# In[140]:


df = pd.read_csv('Attribution_and_Allocation_subid_tier_match.csv')
#df_true=df[(df.convert_TF=='True')]
df_true


# In[123]:


tech_people = {} 
#{comp: 0 for comp in ['attribution_technical'].unique()}
for comp in df_true['attribution_technical'].unique():
    tech_people[comp] = [[] for i in range(df_true['Tier'].nunique())]

survey_people = {comp: [[] for i in range(df_true['Tier'].nunique())] for comp in df['attribution_technical'].unique()}
survey_people.pop('display')
survey_people.pop('bing')

tier = df_true['Tier'].unique()
tier.sort()
for i in tier:
    temp = df_true.loc[df['Tier']==i,:]
    for j in range(len(temp['attribution_technical'].value_counts())):
        tech_people[temp['attribution_technical'].unique()[j]][i-1] = temp['attribution_technical'].value_counts()[j]
        
for i in tier:
    temp = df_true.loc[(df['Tier']==i)&(df_true['attribution_survey'].isin(survey_people.keys())),:]
    for j in range(len(temp['attribution_survey'].value_counts())):
        survey_people[temp['attribution_survey'].unique()[j]][i-1] = temp['attribution_survey'].value_counts()[j]


# In[124]:


tech_people


# In[125]:


survey_people


# In[126]:


df_tech_people=pd.DataFrame(columns=tech_people.keys(),index=tier)
for k in tech_people:
    df_tech_people[k]=tech_people[k]
df_tech_people


# In[127]:


df_survey_people=pd.DataFrame(columns=survey_people.keys(),index=tier)
for j in survey_people:
    df_survey_people[j]=survey_people[j]
df_survey_people


# In[128]:


channel_spend=pd.read_csv("channel_spend_undergraduate.csv")


# In[129]:


channel_spend


# In[130]:


#df_s=pd.DataFrame(columns=tech.keys(),index=tier)
#for c in df_s.columns:
    #spend = []
    #df_tech[k]=tech[k]
#df_tech


# In[131]:


import json


# In[132]:


chan_spend_dict={}
#tier_list=['tier1','tier2','tier3','tier4','tier5','tier6','tier7','tier8']
for i in range(8):
  chan_spend_dict[i+1]= json.loads(channel_spend['spend'][i].replace("'",'"'))
  print(chan_spend_dict[i+1])
#assign the value of chan_spand_dict to channel_spend
channel_spend=chan_spend_dict
channel_spend


# In[133]:


df_spend=pd.DataFrame(columns=tech_people.keys(),index=tier)
for c in df_spend.columns:
    l = []
    for i in tier:
        l.append(channel_spend[i][c])
    print(l)
        
    df_spend[c] = l


# In[134]:


df_spend


# In[135]:


df_avg_CAC_tech=pd.DataFrame(columns=tech_people.keys(),index=tier)

for v in df_spend.columns:
    for i in tier:
        df_avg_CAC_tech[v][i] = df_spend[v][i] / df_tech_people[v][i]
        
df_avg_CAC_tech


# In[136]:


df_avg_CAC_survey=pd.DataFrame(columns=survey_people.keys(),index=tier)

for k in [k for k in df_spend.columns if k in survey_people.keys()]:
    for i in tier:
        df_avg_CAC_survey[k][i] = df_spend[k][i] / df_survey_people[k][i]

df_avg_CAC_survey


# In[137]:


df_Marg_CAC_tech=pd.DataFrame(columns=tech_people.keys(),index=tier)

for z in df_spend.columns:
    for i in tier:
        if i == 1:
            df_Marg_CAC_tech[z][i] = df_spend[z][i] / df_tech_people[z][i]
        else:
            df_Marg_CAC_tech[z][i] = (df_spend[z][i] - df_spend[z][i-1]) / df_tech_people[z][i]
    
        
df_Marg_CAC_tech


# In[138]:


df_Marg_CAC_survey=pd.DataFrame(columns=survey_people.keys(),index=tier)

for z in [z for z in df_spend.columns if z in survey_people.keys()]:
    for i in tier:
        if i == 1:
            df_Marg_CAC_survey[z][i] = df_spend[z][i] / df_survey_people[z][i]
        else:
            df_Marg_CAC_survey[z][i] = (df_spend[z][i] - df_spend[z][i-1]) / df_survey_people[z][i]

df_Marg_CAC_survey


# In[ ]:




