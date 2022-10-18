# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 16:56:03 2022

@author: ΔΗΜΗΤΡΗΣ
"""

# https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
# https://www.analyticsvidhya.com/blog/2021/06/build-web-app-instantly-for-machine-learning-using-streamlit/
# https://docs.streamlit.io/library/api-reference
# https://towardsdatascience.com/data-visualization-using-streamlit-151f4c85c79a
# https://carpentries-incubator.github.io/python-interactive-data-visualizations/07-add-widgets/index.html
# https://docs.streamlit.io/library/api-reference/layout/st.expander
# https://towardsdatascience.com/deploying-a-web-app-with-streamlit-sharing-c320c79ae350
# https://share.streamlit.io/dimpolitik/trawlers/main/myapp.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import altair as alt

st.set_page_config(layout="wide")

# streamlit run visulaise_maturity_data.py --server.port 8080

# Functions
    
@st.cache
def load_data():
    xls = pd.ExcelFile('maturity_data_clean.xlsx') 
    df = pd.read_excel(xls)
    df['DATUM'] = df['DATUM'].astype(str)
    df['SPECIES'] = df['SPECIES'].replace({'Merluccius merluccius': 'M. merluccius', 
                                           'Mullus barbatus': 'M. barbatus', 
                                           'Parapenaeus longirostris': 'P. longirostris'})
    df = df.dropna(subset=['MATURITY'])
    df['MATURITY'] = df['MATURITY'].astype(int)
    df['DATUM'] = [c.replace("AU", "") for c in df['DATUM']]
    df['DATUM'] = [c.replace("WI", "") for c in df['DATUM']]
    df['DATUM'] = [c.replace("SP", "") for c in df['DATUM']]
    df['DATUM'] = [c.replace("SU", "") for c in df['DATUM']]
    df['DATUM'] = [c.replace("-", "0") for c in df['DATUM']]      
    df['YEAR'] = [x[0:4] for x in df['DATUM']]
    df['MONTH'] = [x[4:6] for x in df['DATUM']]             
    return df

df = load_data()

st.title('Visualisation of maturity data in the Ionian Sea')

st.markdown("Explore maturity data in the Ionian Sea for M. merluccius, M. barbatus and P. longirostris")

# user choices
with st.sidebar:
    st.subheader("Select")
    species = st.sidebar.selectbox('Species', [None, "M. merluccius", "M. barbatus", "P. longirostris"])
    #gender = st.sidebar.selectbox('Mesh size', [None, 'Both','M','F'])
    
    year = st.multiselect('Year', sorted(list(set(df['YEAR']))))
    
    dfc = df.copy()
    all_options = st.checkbox("Select all years")

    if all_options:
        selected_options = sorted(list(set(df['YEAR'])))
        dfc = dfc[(dfc['SPECIES'] == species) & (dfc['YEAR'].isin(selected_options))]
    else:
        dfc = dfc[(dfc['SPECIES'] == species) & (dfc['YEAR'].isin(year))]
    
    st.image('urk-fishing-trawlers.jpg')


if  ((species is not None) & (len(year) >0 or all_options is not None) ):
  
    col1, col2  = st.columns(2)
   
    with col1:
        if not dfc.empty:
            fig, ax = plt.subplots()
            dfc.groupby('YEAR')['MATURITY'].value_counts().unstack().plot(kind='bar', stacked=True, ax = ax)
            ax.set_xlabel('Year')
            ax.set_ylabel('Frequency')
            ax.set_title('Maturity per year')
            st.pyplot(fig)
    
    with col2:   
        if not dfc.empty:
            fig, ax = plt.subplots()
            dfc.groupby('MONTH')['MATURITY'].value_counts().unstack().plot(kind='bar', stacked=True, ax = ax)
            ax.set_xlabel('Month')
            ax.set_ylabel('Frequency')
            ax.set_title('Maturity per month')
            st.pyplot(fig)
            
    
