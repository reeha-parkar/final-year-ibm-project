from turtle import color
from matplotlib import markers

from matplotlib.pyplot import scatter
import streamlit as st
import sys
from model import clv
import pandas as pd
import plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go

def app():
    st.title('CLV MODEL OUTPUT')
    data = pd.read_csv('data/customer_segmentation.csv', encoding='cp1252')
    data_user = clv.get_all_clusters(data)
    st.subheader("Frequency, Revenue and Recency Cluster Distribution of UK Data")
    st.write(data_user)
    st.write(" ")


    data_graph, data_cluster, stats_data = clv.get_clv(data, data_user)
    #st.write(data_graph)
    st.subheader("6 Months Customer Lifetime Vale Prediction")
    st.write(data_cluster)
    plot_data = [
        go.Scatter(
            x = data_graph.query("Segment == 'Low-Value'")['OverallScore'],
            y = data_graph.query("Segment == 'Low-Value'")['m6_Revenue'],
            mode = 'markers',
            name = 'Low',
            marker = dict(size= 7,
                line = dict(width=1),
                color = 'blue',
                opacity = 0.8
            )
        ),
            go.Scatter(
            x = data_graph.query("Segment == 'Mid-Value'")['OverallScore'],
            y = data_graph.query("Segment == 'Mid-Value'")['m6_Revenue'],
            mode = 'markers',
            name = 'Mid',
            marker = dict(size= 9,
                line = dict(width=1),
                color = 'green',
                opacity = 0.5
            )
        ),
            go.Scatter(
            x = data_graph.query("Segment == 'High-Value'")['OverallScore'],
            y = data_graph.query("Segment == 'High-Value'")['m6_Revenue'],
            mode='markers',
            name='High',
            marker = dict(size= 11,
                line = dict(width=1),
                color= 'red',
                opacity= 0.9
            )
        ),
    ]

    plot_layout = go.Layout(
            yaxis = {'title': "6m LTV"},
            xaxis = {'title': "RFM Score"},
            title ='Customer Lifetime Values:'
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    st.plotly_chart(fig)
    st.subheader("Conclusion:")
    st.write("Above is a correlation between overall RFM score and revenue. Positive correlation is quite visible here. High RFM score means high LTV.")
    st.write(" ")
    st.subheader("Statistical data of LTV Clusters")
    st.write(stats_data)
    st.write("Cluster 2 is the best with average 8.2k LTV whereas 0 is the worst with 396. Hence, customers from this cluster are crucial in improving the Revenue of the store")


