import streamlit as st
import pandas as pd

def app():
    st.title('ABOUT US')

    st.subheader('Team Members:')
    names = pd.DataFrame(['Dania Juvale','Nandinee Kaushik', 'Reeha Parkar'], [60001180014, 60001180033, 60001180046], columns=['Names'])
    st.dataframe(names)

    st.write("We are a group of three students from DJ Sanghvi college of engineering, pursuing a credited course offered by IBM in the specialisation of Artificial Intelligence and Machine Learning. We have a created a web app that is used for storing, and efficiently visualising real-time data, to understand insights from metrics data and make predictions.")

    st.subheader("For more info:")

    st.write("Dania's [GitHub](https://github.com/Daniajuvale)")
    st.write("Nandinee's [GitHub](https://github.com/Nandinee14)")
    st.write("Reeha's [GitHub](https://github.com/reeha-parkar)")
    

