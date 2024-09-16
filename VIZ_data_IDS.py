import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import datetime

# Simulate some log data
data = {
    'timestamp': [datetime.datetime.now() - datetime.timedelta(minutes=i) for i in range(100)],
    'requests': [50 + i*5 for i in range(100)]
}

df = pd.DataFrame(data)

# Create a line plot
st.title("Basic IDS Dashboard")
st.line_chart(df.set_index('timestamp'))

# Display data as a table
st.dataframe(df)
