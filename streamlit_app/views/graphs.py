import streamlit as st
import SessionState
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

def app():
	st.title("Graphical Overview of Your Store")

	df = pd.read_csv("data/customer_segmentation.csv", encoding="cp1252")
	
	countries = df.Country.unique()
	#st.write(countries)
	map_data = pd.DataFrame()
	map_data["Country"] = countries
	map_data["latitude"] = 0.0
	map_data["longitude"] = 0.0
	for i, country in enumerate(countries):
		st.write()
		map_data["latitude"][i] = df[df['Country']==country]["latitude"].unique()[0]
		map_data["longitude"][i] = df[df['Country']==country]["longitude"].unique()[0]
		continue
	#st.write(map_data)
	st.subheader("All your Customers' Locations:")
	st.map(map_data)

	st.subheader("Country Contribution")
	
	country_data = pd.DataFrame(df["Country"].value_counts())
	st.write("Values for each country:")
	st.dataframe(country_data)
	st.write("Graphical Comparison:")
	st.bar_chart(data=country_data, width=0.8, use_container_width=True)
	
	
	st.subheader("Customer Purchases")
	customer_id = float(st.number_input("Enter Customer ID"))
	customer = pd.DataFrame({'Date': df[df["CustomerID"] == customer_id]["InvoiceDate"], 'Price': df[df["CustomerID"] == customer_id]["UnitPrice"]})
	
	c = alt.Chart(customer).mark_circle().encode(x='Date', y='Price', tooltip=['Date', 'Price'])
	col1, col2 = st.columns([3,2])
	with col1:
		st.write("Customer's Price v/s Time of Purchase")
		st.altair_chart(c)
	with col2:
		st.write("Data of Customer's Purchases")
		st.write(customer)
	



