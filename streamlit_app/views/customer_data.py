from msilib.schema import CustomAction
import streamlit as st
import hashlib
import SessionState
import pandas as pd

COLUMNS = ['Select All', 'InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
COUNTRIES = [None, 'Australia', 'Austria', 'Bahrain', 'Belgium', 'Brazil', 'Canada', 'Channel Islands', \
    'Cyprus', 'Czech Republic', 'Denmark', 'EIRE', 'European Community', 'Finland', 'France', 'Germany', \
        'Greece', 'Hong Kong', 'Iceland', 'Israel', 'Italy', 'Japan', 'Lebanon', 'Lithuania', 'Malta', \
            'Netherlands', 'Norway', 'Poland', 'Portugal', 'RSA', 'Saudi Arabia', 'Singapore', \
                'Spain', 'Sweden', 'Switzerland', 'United Arab Emirates', 'United Kingdom', \
                    'Unspecified', 'USA']
session_state = SessionState.get(checkboxed=False)
def make_hashes(password):
	    return hashlib.sha256(str.encode(password)).hexdigest()
        
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# DB  Functions
def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def app():
    st.title("Get your customer data")
    st.sidebar.subheader("Login to view Dashboard")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    hashed_pswd = make_hashes(password)
    login = st.sidebar.button("Login")
    check = False
    try:
        check = session_state.checkboxed
    except:
        pass
    if login or check:
        result = login_user(username, check_hashes(password,hashed_pswd))
    
        if result:
            session_state.checkboxed = True
            st.sidebar.success("Logged in as {}".format(username))
            st.title("Customer Data of your Store:")
            col1, col2 = st.columns(2)
            with col1:
                row_option = st.number_input(label="Select Rows for Display", min_value=0, max_value=500000)
            with col2:
                column_options = st.multiselect('Select Columns for Display', tuple(COLUMNS))
            country_option = st.selectbox("Select Country", tuple(COUNTRIES))
            col1, col2 = st.columns(2)
            with col1:
                customer_id = float(st.number_input("Enter Customer ID"))
            with col2:
                stock_code_option = st.text_input("Enter Stock Code")

            if(st.button("Fetch Data")):
                df = pd.read_csv("data/customer_segmentation.csv", encoding="cp1252")
                st.success("Selected {} rows".format(row_option))
                data = df[:450000]
                if column_options[0] != "Select All":
                    columns = column_options
                    if "Select All" in columns:
                        columns.remove("Select All")
                    data = data[columns]
                if country_option:
                    data = data[df["Country"]==country_option]
                if customer_id:
                    data = data[df["CustomerID"]==customer_id]
                if stock_code_option:
                    data = data[df["StockCode"]==stock_code_option]
                if row_option > 0:
                    data = data[:row_option]
                st.dataframe(data)
        else:
            st.warning("Incorrect Username/Password")