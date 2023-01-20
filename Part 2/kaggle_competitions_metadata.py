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
import numpy as np

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
# Price str -> float
usd_euro_equivalent = 1.08
competition_data["Price"] = competition_data["Price"].apply(
    lambda price: float(price.strip("$").replace(",", "_"))
    if "$" in price
    else usd_euro_equivalent * float(price.strip("€").replace(",", "_"))
)
#%%
"""
metadata deconstruction:
    maxium elements is 4.
    main pattern: type of competition, teams count, time elapsed
    alternative pattern: type of competition(2 descriptior strings), teams count,
    time elapsed
"""

# metadata separation
metadata_cols = competition_data["metadata"].str.split("·", expand=False)
metadata_cols = metadata_cols.apply(
    lambda metadata: metadata
    if len(metadata) == 3
    else [metadata[0] + metadata[1]] + metadata[2:]
)
assert sum([len(arr) == 3 for arr in metadata_cols.values]) == len(metadata_cols.values)
metadata_cols = metadata_cols.str.join("·").str.split("·", expand=True)
metadata_cols.rename(
    columns={
        0: "competition_category",
        1: "teams_participated",
        2: "competition_closed_reference",
    },
    inplace=True,
)
assert metadata_cols.shape[1] == 3
competition_data_merged = competition_data.merge(
    metadata_cols, how="inner", left_index=True, right_index=True, copy=False
)
# teams participated value extraction
competition_data_merged["teams_participated"] = (
    competition_data_merged["teams_participated"].str.extract("(\d+)").iloc[:, 0]
)
"""
Observations:
    teams participated value == 0 does not imply no teams participated
    it could mean that that competition did not have a leaderboard tab available
"""
#%% Extracting date
