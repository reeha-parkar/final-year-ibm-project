import streamlit as st
from views import customer_data, graphs, home, signup, about, clv_output, trmf_output
import utils as utl

st.set_page_config(layout="wide", page_title='TRMF & CLV')
st.set_option('deprecation.showPyplotGlobalUse', False)
utl.inject_custom_css()
utl.navbar_component()
route = utl.get_current_route()

if route == "home":
    home.app()
elif route == "customer_data":
    customer_data.app()
elif route == "graphs":
    graphs.app()
elif route == "clv":
    clv_output.app()
elif route == 'trmf_output':
    trmf_output.app()
elif route == "signup":
    signup.app()
elif route =="about":
    about.app()
elif route == None:
    home.app()