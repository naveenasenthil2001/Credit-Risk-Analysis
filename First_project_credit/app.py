import os
import pandas as pd
import streamlit as st
import plotly.express as px

file_path = os.path.join(
    os.path.dirname(__file__),
    "loan_data_cleaned.csv"
)

df = pd.read_csv(file_path)

st.title("Credit Risk Analysis")
st.dataframe(df.head())
st.write("Dataset Shape:", df.shape)

st.subheader("Key Performance Indicators")

total_applications = len(df)

approved = len(df[df['NAME_CONTRACT_STATUS']=="Approved"])

refused = len(df[df['NAME_CONTRACT_STATUS']=="Refused"])

total_credit = df['AMT_CREDIT'].sum()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Applications", total_applications)
col2.metric("Approved", approved)
col3.metric("Refused", refused)
col4.metric("Total Credit", round(total_credit))

st.subheader("Contract Status Distribution")

status = df['NAME_CONTRACT_STATUS'].value_counts().reset_index()

status.columns = ['Status','Count']

fig = px.bar(
    status,
    x='Status',
    y='Count',
    color='Status'
)

st.plotly_chart(fig)


import numpy as np

df['RISK_FLAG'] = np.where(
    df['NAME_CONTRACT_STATUS']=='Refused',
    'High Risk',
    'Low Risk'
)

st.subheader("Risk Distribution")

risk = df['RISK_FLAG'].value_counts().reset_index()

risk.columns=['Risk','Count']

fig = px.pie(
    risk,
    names='Risk',
    values='Count'
)

st.plotly_chart(fig)
st.subheader("Client Type Analysis")

client = df['NAME_CLIENT_TYPE'].value_counts().reset_index()

client.columns=['Client Type','Count']

fig = px.bar(
    client,
    x='Client Type',
    y='Count',
    color='Count'
)

st.plotly_chart(fig)

st.subheader("Top Seller Industries")

industry = (
    df.groupby('NAME_SELLER_INDUSTRY')['AMT_CREDIT']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    industry,
    x='NAME_SELLER_INDUSTRY',
    y='AMT_CREDIT',
    color='AMT_CREDIT'
)

st.plotly_chart(fig)

st.subheader("SQL Query Results")

query_option = st.selectbox(
    "Select Analysis",
    [
        "Contract Status",
        "Client Type",
        "Product Combination"
    ]
)

if query_option == "Contract Status":
    st.dataframe(
        df['NAME_CONTRACT_STATUS']
        .value_counts()
        .reset_index()
    )

elif query_option == "Client Type":
    st.dataframe(
        df['NAME_CLIENT_TYPE']
        .value_counts()
        .reset_index()
    )

elif query_option == "Product Combination":
    st.dataframe(
        df['PRODUCT_COMBINATION']
        .value_counts()
        .head(10)
        .reset_index()
    )
