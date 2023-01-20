#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 20:13:51 2023

@author: carlosgarcia
"""

"""
About data:
    data was scraped using octoparse.
    data is from competitions that have ended as of January 19, 2023
    data is from competitions that had monetary rewards
"""

#%%Tools
import pandas as pd
import plotly.express as px

#%% Loading Data
competition_data = pd.read_csv("Part 2/Kaggle_monetary_competitions.csv")
#%% Getting to know data
print(competition_data.info())
"""
Cleaning objectives:
    Price needs to be in float type.
    separate contents in metadata
    extract total team count from metadata column
    extract date of competition completion from metadata column
"""
# Sample record
display([competition_data[col][0] for col in competition_data.columns])
#%% Cleaning Process
"""
Note: 
    At time of analysis 1.08 usd == 1 euro
    The currency of the rewards in kaggle in this dataset where either usd $ or euro €
"""
usd_euro_equivalent = 1.08
competition_data["Price"] = competition_data["Price"].apply(
    lambda price: float(price.strip("$").replace(",", "_"))
    if "$" in price
    else usd_euro_equivalent * float(price.strip("€").replace(",", "_"))
)
#%%
