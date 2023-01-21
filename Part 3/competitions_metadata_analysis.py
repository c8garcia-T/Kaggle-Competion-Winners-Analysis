#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 21:49:45 2023

@author: carlosgarcia
"""
# Tools
import pandas as pd
import plotly.express as px
from plotly.offline import plot

#%% Loading Data
competitions_meta = pd.read_csv(
    "Part 2/Kaggle_monetary_competitions_cleaned.csv", parse_dates=["deadline_estimate"]
)
#%% Validating structure of the dataset
print("Shape of dataset:", competitions_meta.shape)
print(competitions_meta.info())
print(competitions_meta.iloc[0, :])
assert competitions_meta.isna().sum().sum() == 0
#%% Getting a sense of the distribution of the data
# Numerical Variable's Descriptive statistics
print(competitions_meta.describe(datetime_is_numeric=True))
"""
Observations:
    deadline_estimate:
        50% of the competitions that had a reward took place before before 2018
        earliest record of monetary reward competition took place in year 2010
        it appears that monetary reward competitions have slowed down *thought*
    teams_participated:
        min=0 is explained by competitions which did not have a leaderboard tab
        there where <= 651 teams in 50% of the competitions
        the maximum amount of teams thus far in a competition was 8751
        the standard deviation is quite large at 1281
    reward:
        the standard deviation is quite large at 1.28e5
        the min reward was $100 while the highest reward thus far is 1.5e6
        however the iqr is between 10_000 USD and 50_000 USD
"""
# category column Descriptive statistic
print(competitions_meta.category.unique())
print(competitions_meta.category.describe())

"""
Observations:
    category:
        out of 11 distinct categories 'Featured' was the top one with a freq of 175
        that makes 'Featured' making up ~46% of the compeitions
        'Featured' although the most frequent the label is not insightful ...
        ... as the other categories label
"""
#%% Visualizations of distribution
fig = px.ecdf(
    competitions_meta, x="reward", height=500, width=500, marginal="histogram"
)
plot(fig, filename="temp1.html")
fig = px.histogram(
    competitions_meta, x="teams_participated", height=500, width=500, marginal="box"
)
plot(fig, filename="temp2.html")
fig = px.histogram(
    competitions_meta, x="deadline_estimate", height=500, width=500, marginal="box"
)
plot(fig, filename="temp3.html")
fig = px.histogram(competitions_meta, x="category", height=500, width=500)
plot(fig, filename="temp4.html")

"""
Observations:
    ECDF reward plot:
        Shape:
            vertical slope nearly form 0-0.8 y-axis
            skewed left
            
        Histogram margin:
            unimodal
            confirms that most records are in bin ~0-50k
            can easily see presence of outliers
    Teams Participated Histogram and boxplot margin plot:
        Shape:
            Skewed left
            unimodal
    Deadline Estimate histogram:
        Bimodal (2013, 2022)
    Category Bar Plot:
        Notable bars: Featured > Research > Featured Code Compeition      
"""
#%% Correlation Analysis
fig = px.scatter_matrix(
    competitions_meta[["reward", "teams_participated", "deadline_estimate"]]
)
plot(fig)
"""
Observations:
    Looking at deadline_estimate x_axis and seeing it against teams_participated and ...
    ... reward variable is the most insightful.
    deadline_estimate vs reward:
    The trend that competitions typically hold reward values <100k is evident across...
    ... time. The plot makes it easy to see the competition with reward outliers and...
    ... when they took place. 
    deadline_estimate vs teams_participated
    2014->2015 after 2015 it appears that the variation in teams participated increased
    teams_participated vs reward:
        no linear correlation present at a glance
"""
#%%
# For fun visualization
fig = px.scatter(
    competitions_meta,
    x="reward",
    y="teams_participated",
    color="category",
    hover_name="category",
    log_x=True,
)
plot(fig)
