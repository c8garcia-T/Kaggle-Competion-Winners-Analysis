#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cleaning data for analysis
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
from IPython.display import display
from dateutil.relativedelta import relativedelta
import os

#%% Loading Data
competition_data = pd.read_csv("Part 2/Kaggle_monetary_competitions.csv")
# Getting to know data
print(competition_data.info())
"""
Cleaning objectives:
    Price needs to be in float type.
    separate contents in metadata
    extract total team count from metadata column
    extract date of competition completion from metadata column
"""
print(competition_data.isna().sum())
assert competition_data.isna().sum().sum() == 0
# Sample record
display(competition_data.iloc[0, :])
# Cleaning Process
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
# Extracting date
competition_data_merged["competition_closed_reference"] = competition_data_merged[
    "competition_closed_reference"
].apply(lambda text: text.split()[:2])

elements_in_date_metadata = competition_data_merged[
    "competition_closed_reference"
].apply(lambda text: len(text))
assert elements_in_date_metadata.std() == 0
"""
pattern of date str:
    3 elements
    [integer(str), days/months/years(str), 'ago'(str)]
    therefore we can adjust above code by slicing list to remove 'ago'
"""

confound_date_element_identifier = (
    competition_data_merged["competition_closed_reference"]
    .apply(lambda text: text[0])
    .tolist()
)

confound_date_element_identifier = [
    element for element in confound_date_element_identifier if element.isalpha()
]
# Observation: since all cofounds have value 'a'. 'a' == 1 integer

competition_data_merged["competition_closed_reference"] = competition_data_merged[
    "competition_closed_reference"
].apply(lambda text: [1 if text[0] == "a" else text[0]] + [text[1]])

units_of_date = (
    competition_data_merged["competition_closed_reference"]
    .apply(lambda text: text[1])
    .unique()
)
print("Date units present in data:", units_of_date)


def list_to_datetime(date_series):
    """

    Parameters
    ----------
    date_series : pandas.series
        contains elements required to form datetime object.

    Returns
    -------
    date_series : list
        an approximation of the date the competition was closed.

    """
    time_data_collected = pd.to_datetime("Jan 19 20:13:51 2023")
    date_series = date_series.tolist()
    for indx, row in enumerate(date_series):
        if "month" in row[1]:
            date_series[indx] = time_data_collected - relativedelta(
                months=float(row[0])
            )
        elif "year" in row[1]:
            date_series[indx] = time_data_collected - relativedelta(years=float(row[0]))
        else:
            date_series[indx] = time_data_collected - relativedelta(days=float(row[0]))
    return date_series


competition_data_merged["competition_closed_reference"] = list_to_datetime(
    date_series=competition_data_merged["competition_closed_reference"]
)
print(
    competition_data_merged["competition_closed_reference"].describe(
        datetime_is_numeric=True
    )
)

destination_path = "Part 2/Kaggle_monetary_competitions_cleaned.csv"
"""
Deleting repetetive columns:
    metadata
    
"""
competition_data_merged.drop(columns="metadata", inplace=True)
competition_data_merged.rename(
    columns={
        "Price": "reward",
        "competition_category": "category",
        "competition_closed_reference": "deadline_estimate",
    },
    inplace=True,
)
competition_data_merged.columns = [
    col.lower() for col in competition_data_merged.columns
]
# cleaning up string
competition_data_merged["category"] = competition_data_merged["category"].str.strip()
# Sample record
display(competition_data_merged.iloc[0, :])
if os.path.exists(destination_path):
    print("File exists")
else:
    print("File created")
    competition_data_merged.to_csv(destination_path, index=False)
