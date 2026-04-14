import streamlit as st
import requests 
from CreatingTable import uniqueottlist
selected=[]
with st.container(border=True):
    selected=st.pills('Subscriptions',uniqueottlist,selection_mode='multi')
# st.write(f'You selected {selected}')


url = "http://127.0.0.1:8000/allJioplans/"

responseall = requests.get(url)
with st.container(border=True):
    st.write(responseall.json())
    
if selected:
    with st.container(border=True):
        urlsubs="http://127.0.0.1:8000/filter-plans-by-subscriptions"
        query_params={
            "q":selected
        }
        responsesubs=requests.get(urlsubs,query_params)
        st.write(responsesubs.json())
        