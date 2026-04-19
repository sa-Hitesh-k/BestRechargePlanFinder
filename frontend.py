# importing all the libraries and uniqueottlist for selection
import streamlit as st
import requests 
from CreatingTable import uniqueottlist

selected=[]
st.title("Filter JIO plans")
st.header("Select the below OTTs and find the plans which provide them!")

# A container with all the otts
with st.container(border=True):
    selected=st.pills('OTTs',uniqueottlist,selection_mode='multi')
st.write(f'You selected {selected}')

url = "http://127.0.0.1:8000/allJioplans/"

response_all_otts = requests.get(url)
allpacks=response_all_otts.json()

# An expanding container with all the plans available
with st.expander("📦 View All Plans"):

    for index, pack in enumerate(allpacks, start=1):

        lines = []

        lines.append(f"ID: {pack['id']}")
        lines.append(f"Price: ₹{pack['price']}")
        lines.append(f"Category: {pack['category']}")

        for item in pack["benefits"]:
            for key, value in item.items():
                if key not in ["id", "price", "category"]:
                    lines.append(f"{key}: {value}")

        formatted_text = "<br>".join(lines)

        st.markdown(
            f"""
            <div style="
                background-color:#f0f2f6;
                padding:20px;
                border-radius:12px;
                border:1px solid #ddd;
                margin-bottom:15px;
            ">
                <h4>Pack {index}</h4>
                <p>{formatted_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
# If a user selects OTT(s) then this code is executed and a container with packs is displayed
if selected:
    packcard={}
    with st.container(border=True):
        urlsubs="http://127.0.0.1:8000/filter-plans-by-OTTs"
        query_params={
            "q":selected
        }
        response_otts=requests.get(urlsubs,query_params)
        ans=response_otts.json()

        for i in ans:
            number=0
            for j in ans[i]:
                number+=1
                for k in j:
                    lines = []

                    for item in j[k]:   # each item is dict
                        for key, value in item.items():
                                lines.append(f"{key}: {value}")

                    formatted_text = "<br>".join(lines)

                    st.markdown(
                            f"""
                            <div style="
                                background-color:#f0f2f6;
                                padding:20px;
                                border-radius:10px;
                                border:1px solid #ddd;
                                margin-bottom:15px;
                            ">
                                <h4>{i} Pack {number}</h4>
                                <p>{formatted_text}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )