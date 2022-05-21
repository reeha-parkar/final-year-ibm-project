from turtle import width
import streamlit as st
import pandas as pd

def app():

    col1, col2 = st.columns([2,3])
    with col1:
        st.image("media/image.jpg")
    with col2:
        st.title("CUSTOMER LIFETIME VALUE MODELLING")
        st.write("Know which customers are adding value to your store's lifetime!.")

        st.subheader('Team Members:')
        names = pd.DataFrame(['Dania Juvale','Nandinee Kaushik', 'Reeha Parkar'], [60001180014, 60001180033, 60001180046], columns=['Names'])
        st.dataframe(names)

   