from typing import List

import pandas as pd
import numpy as np
import folium
import streamlit_folium
import streamlit as st
import kaggle
import os
from folium import plugins
import plotly.express as px


@st.cache_resource(show_spinner="Downloading data")
def download_dataset() -> None:
    """Download dataset from kaggle """
    # Kinda weird function, refactor later to look better
    dataset_folder = "../lakes_streamlit/data/bathing_water_quality_eu/eea_t_bathing-water-status_p_1990-2022_v01_r00"

    if os.path.exists(dataset_folder):
        return

    kaggle.api.dataset_download_files(
        dataset="krzysztofkulasik/status-of-bathing-water-europe-union-2008-2022",
        path="../lakes_streamlit/data/bathing_water_quality_eu",
        unzip=True
    )
    return


@st.cache_data(show_spinner="Loading data")
def load_data() -> pd.DataFrame:
    """
    Check if parquet file with concatenated .xlsx files exists, then return it.
    If parquet file doesn't exist, concatenate files, save parquet file to directory and return DataFrame

    Returns:
        data (pd.DataFrame) : DataFrame that contains concatenated files from dataset
    """

    parquet_filename = "../lakes_streamlit/data/bathing_water_quality_eu/data_concat.parquet.gzip"
    if os.path.exists(parquet_filename):
        data = pd.read_parquet(parquet_filename)
    else:
        files = []
        for dirname, _, filenames in os.walk("../lakes_streamlit/data/bathing_water_quality_eu"):
            for file in filenames:
                if file.endswith(".xlsx"):
                    files.append(os.path.join(dirname, file))

        datasets = [
            pd.read_excel(file, sheet_name=1) for file in files
        ]

        data = process_data(datasets)
        data.to_parquet(parquet_filename, compression='gzip')

    return data


@st.cache_data(show_spinner="Processing data")
def process_data(datasets: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatenate list of DataFrames and process (drop unnecessary columns, replace values in columns, change type of
    columns, etc. ) them to single DataFrame

    Parameters:
        datasets (List[pd.DataFrame]) : List of DataFrames to concatenate and process

    Returns:
        data (pd.DataFrame) : Concatenated and processed DataFrame

    """
    # TODO: Reduce columns, replace values in columns,
    data = pd.concat(datasets, axis=0).reset_index().drop("index", axis=1)
    countries_to_replace = {'BE': 'Belgium', 'EE': 'Estonia', 'NL': 'Netherlands',
                            'IE': 'Ireland', 'AT': 'Austria', 'LT': 'Lithuania', 'LU': 'Luxembourg',
                            'MT': 'Malta', 'DK': 'Denmark', 'EL': 'Greece', 'PL': 'Poland',
                            'IT': 'Italy', 'SE': 'Sweden', 'CZ': 'Czechia', 'FI': 'Finland',
                            'RO': 'Romania', 'ES': 'Spain', 'HR': 'Croatia', 'SI': 'Slovenia',
                            'HU': 'Hungary', 'CY': 'Cyprus', 'LV': 'Latvia',
                            'AL': 'Albania', 'BG': 'Bulgaria', 'CH': 'Switzerland',
                            'FR': 'France', 'PT': 'Portugal', 'DE': 'Germany', 'SK': 'Slovakia'}

    data = data.replace({"countryCode": countries_to_replace})
    data = data.astype({"lon": "float32", "lat": "float32"})
    return data


@st.cache_data(show_spinner=False)
def find_unique_country(data: pd.DataFrame) -> List[str]:
    """
    Find unique country names for given DataFrame

    Parameters:
        data (pd.DataFrame) : Given DataFrame
    Returns:
        countries (List[str] : List of unique country names
    """
    countries = data["countryCode"].unique()
    return countries


@st.cache_data(show_spinner=False)
def find_unique_zone_types(data: pd.DataFrame, countries: List[str]) -> List[str]:
    """
    Find unique zone types for given countries in given DataFrame

    Parameters:
        data (pd.DataFrame) : Given DataFrame to be filtered by countries names
        countries (List[str]) : List of country names
    Returns:
        zone_types (List[str] : List of unique zone types for given country names
    """
    zone_types = data.loc[(df["countryCode"].isin(countries)), "specialisedZoneType"].unique()
    return zone_types


@st.cache_data(show_spinner=False)
def find_available_bathing_water(data: pd.DataFrame, countries: List[str], zone_types: List[str]) -> List[str]:
    """
    Find available bathing waters for given countries and zone types in given DataFrame

    Parameters:
        data (pd.DataFrame) : Given DataFrame to be filtered by countries names
        countries (List[str]) : List of country names
        zone_types (List[str] : List of unique zone types for given country names
    Returns:
        available_bathing_waters (List[str]) : List of unique names of bathing waters for given countries names and zone types
    """
    available_bathing_waters = data.loc[
        ((data["countryCode"].isin(countries)) & (data["specialisedZoneType"].isin(zone_types))), "nameText"].unique()
    return available_bathing_waters



download_dataset()
with st.container():
    df = load_data()
    selected_country = st.multiselect(
        label="Name of country",
        placeholder="Choose or write name of country",
        options=find_unique_country(df)

    )

    selected_zone_type = st.multiselect(
        label="Zone type",
        placeholder="Choose zone type of bathing water",
        options=find_unique_zone_types(df, selected_country)
    )

    selected_bathing_water = st.multiselect(
        label="Name of bathing water",
        placeholder="Choose bathing water",
        options=find_available_bathing_water(df, selected_country, selected_zone_type)
    )

    st.dataframe(df[df["nameText"].isin(selected_bathing_water)])

# TODO: Add map TODO: Add geolocation TODO: Add subgroups in map by zoneType TODO: TODO: Add metrics to display short
#  info about bathing water location (e.q. Water quality for each year or water quality for recent year and period of
#  monitoring it)
