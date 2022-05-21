import streamlit as st
from model import trmf_model
import pandas as pd
import matplotlib.pyplot as plt


def app():
    #data = pd.read_csv("data/customer_segmentation.csv", encoding="cp1252")
    #sales, clv, train_preds, nd = trmf_model.apply_trmf_model(data)
    sales = pd.read_csv('model/sales.csv')
    train_preds = pd.read_csv('model/train_preds.csv')
    train_preds.dropna(inplace=True)
    train_preds_df = pd.DataFrame(train_preds)
    clv = pd.read_csv('model/clv.csv')
    clv.dropna(inplace = True)
    clv_df = pd.DataFrame(clv)
    st.subheader("Sales v/s Total Hours Graph from TRMF:")
    st.line_chart(sales)

    st.subheader("Performance of TRMF Predictions:")
    fig = plt.figure()
    #st.write(clv_df.to_numpy()[0][:100])
    plt.plot(clv_df.to_numpy()[0][:200], label='train data', color='blue')
    plt.plot(train_preds.to_numpy()[0][:200], label='prediction', color='red')
    plt.title('Performance in train data')
    plt.xlabel('timepoint')
    plt.ylabel('value')
    plt.legend(loc=4)
    st.pyplot(fig)
