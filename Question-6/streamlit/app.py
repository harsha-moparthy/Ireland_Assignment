import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px 
import time
from kafka import KafkaConsumer

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    st.sidebar.title("Filter Data")
    modify = st.sidebar.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.sidebar.container()

    with modification_container:
        to_filter_columns = st.sidebar.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.sidebar.columns((1, 20))
            # Treat columns with string unique values as categorical
            if isinstance(df[column][0],str):
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique()
                )
                df = df[df[column].isin(user_cat_input)]
            elif column.lower() == "timezone":
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique()
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df
# Flask API base URL
API_URL = "http://127.0.0.1:5000/api"

# Dashboard Section
st.title("Global Weather Data")

# Section 1: Data Dashboard
st.header("Data Dashboard")

# # Add filter sidebar
response = requests.get(f"{API_URL}/weather")
data = pd.DataFrame(response.json())
filtered_data = filter_dataframe(data)
filtered_data = filtered_data.drop(columns=["Unnamed: 0"])
filtered_data.reset_index(drop=True, inplace=True)
st.write(filtered_data)



# Section 2: Live Data Updates
st.header("Live Weather Updates")
st.write("Real-time weather updates stream")


# Define the fixed columns based on the known JSON structure
columns = data.columns

# Initialize the DataFrame with fixed columns
df = pd.DataFrame(columns=columns)
df = st.session_state.df if "df" in st.session_state else df
# df = pd.concat([df, data], ignore_index=True)

country = st.sidebar.selectbox("Select Country", options=data["country"].unique())
st.sidebar.title("Plotly Plot")
plot_x = st.sidebar.selectbox("Select X-axis attribute", options=df.columns)
plot_y = st.sidebar.selectbox("Select Y-axis attribute", options=df.columns)
var = st.sidebar.button("Generate Plot")

def consume_stream():
    new_url = f"{API_URL}/stream"
    dataframe_placeholder = st.empty()  # Placeholder for a single, updated DataFrame display
    plot_placeholder = st.empty()  # Placeholder for a single, updated Plotly chart display

    try:
        consumer = KafkaConsumer(
        'global_weather', 
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        i = 0
        for message in consumer:
            i+=1
            line = message.value
            row_data = json.loads(line)
            # Convert to a single-row DataFrame
            row_df = pd.DataFrame([row_data], columns=columns)
            # Append to the main DataFrame
            global df
            df = pd.concat([df, row_df], ignore_index=True)
            # Update the Streamlit placeholder with the latest DataFrame
            st.session_state.df = df
            dataframe_placeholder.dataframe(st.session_state.df)
            df_c = df[df["country"] == country]
            # Generate Plotly plot
            fig = px.line(df_c, x = plot_x, y=plot_y, title=f"{plot_x} vs {plot_y}")
            plot_placeholder.plotly_chart(fig,key=f"plotly{i}")
                
            # Optional: small delay to reduce flickering
            time.sleep(0.1)

        st.session_state.df = df
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        st.write("Attempting to reconnect...")



# Stream data and update chart
if st.button("Start Streaming"):
    consume_stream()
