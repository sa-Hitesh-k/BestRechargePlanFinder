import streamlit as st
import requests

# 1. SETUP & CONFIG
BASE_URL = "https://mobilerechargeplanfinder.onrender.com"
# 2. CACHED DATA FETCHING (The "Speed" Secret)
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def fetch_ott_list():
    # Calling the API endpoint, NOT the local script!
    response = requests.get(f"{BASE_URL}/unique-subscriptions")
    return response.json() if response.status_code == 200 else []

@st.cache_data(ttl=600)
def fetch_all_plans():
    response = requests.get(f"{BASE_URL}/allJioplans/")
    return response.json() if response.status_code == 200 else []

# 3. UI RENDERING
st.title("🚀 Recharge Plan Finder")
st.header("WELCOME TO RPF")
st.html(
    "<p>This website helps you find The Recharge Plans provided by Jio based on the <i>Subscriptions</i> and <i>Other filters</i> selected by "
    "<strong>YOU</strong>"
    "</p>"
)
# Fetch the OTT list 
unique_otts = fetch_ott_list()

with st.container(border=True):
    st.subheader('Filter By OTTs')
    selected_otts = st.pills('Filter by OTT Subscriptions', unique_otts, selection_mode='multi')

# 4. FILTERED VIEW (Only runs if user selects something)
if selected_otts:
    st.subheader(f"Plans including: {', '.join(selected_otts)}")
    # We call the filter endpoint
    res = requests.get(
        f"{BASE_URL}/filter-plans-by-OTTs",
          params={"q": selected_otts}
          )
    
    if res.status_code == 200:
        packcard={}
        with st.container(border=True):
            urlsubs=f"{BASE_URL}/filter-plans-by-OTTs"
            query_params={
                "q":selected_otts
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
                                    if key=="Subscriptions":                            
                                        lines.append(f"{key}: <strong>{value}</strong>")
                                    else:
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
                                    <h4 style="
                                    color: orange;
                                    ">{i} Pack {number}</h4>
                                    <p style="
                                    color: blue;
                                    ">{formatted_text}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
    else:
        st.error("Backend server is sleeping. Please wait 30s.")

with st.expander("Filter By Price Range ?"):
    with st.container(border=True):
        st.subheader('Filter By Price Range')
        price1= st.number_input("Enter minimum price: ", step=1)
        price2= st.number_input("Enter maximum price: ", step=1)

    if (st.button("Apply")):
        st.subheader(f"Plans in Range: {price1} and {price2}")

        res = requests.get(
                f"{BASE_URL}/filter-plans-by-prices",
                params={"q1":price1,"q2":price2}
                )
        
        if res.status_code == 200:
            packcard={}
            with st.container(border=True):
                urlsubs=f"{BASE_URL}/filter-plans-by-prices"
                query_params={
                    "q1":price1,"q2":price2
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
                                        if key=="price":                            
                                            lines.append(f"{key}: <strong>{value}</strong>")
                                        else:
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
                                        <h4 style="
                                        color: orange;
                                        ">{i} Pack {number}</h4>
                                        <p style="
                                        color: blue;
                                        ">{formatted_text}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
        else:
            st.error("Backend server is sleeping. Please wait 30s.")

with st.expander("Filter By Validity Range ?"):
    with st.container(border=True):
        st.subheader('Filter By Validity Range')
        min_validity = st.number_input("Enter minimum validity (days): ", step=1, key="min_val")
        max_validity = st.number_input("Enter maximum validity (days): ", step=1, key="max_val")

    if (st.button("Fetch")):
        st.subheader(f"Plans with Validity Range: {min_validity} to {max_validity} days")
        
        res = requests.get(
            f"{BASE_URL}/filter-plans-by-validity",
            params={"min_days": int(min_validity), "max_days": int(max_validity)}
        )
        
        if res.status_code == 200:
            with st.container(border=True):
                ans = res.json()
                
                for i in ans:
                    number = 0
                    for j in ans[i]:
                        number += 1
                        for k in j:
                            lines = []
                            
                            for item in j[k]:
                                for key, value in item.items():
                                    if key=="Pack validity":                            
                                        lines.append(f"{key}: <strong>{value}</strong>")
                                    else:
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
                                    <h4 style="color: orange;">{i} Pack {number}</h4>
                                    <p style="color: blue;">{formatted_text}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
        else:
            st.error("Backend server is sleeping. Please wait 30s.")

with st.expander("Filter By Data ?"):
    with st.container(border=True):
        st.subheader('Filter By Data Range')
        min_data = st.number_input("Enter minimum data (GB): ", step=1.0, key="min_data")
        max_data = st.number_input("Enter maximum data (GB): ", step=1.0, key="max_data")

    if (st.button("Find")):
        st.subheader(f"Plans with Data Range: {min_data} to {max_data} GB")
        
        res = requests.get(
            f"{BASE_URL}/filter-plans-by-data",
            params={"min_gb": min_data, "max_gb": max_data}
        )
        
        if res.status_code == 200:
            with st.container(border=True):
                ans = res.json()
                
                for i in ans:
                    number = 0
                    for j in ans[i]:
                        number += 1
                        for k in j:
                            lines = []
                            
                            for item in j[k]:
                                for key, value in item.items():
                                    if key=="Total data":                            
                                        lines.append(f"{key}: <strong>{value}</strong>")
                                    else:
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
                                    <h4 style="color: orange;">{i} Pack {number}</h4>
                                    <p style="color: blue;">{formatted_text}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
        else:
            st.error("Backend server is sleeping. Please wait 30s.")
        
# 5. THE "EXPANDER" (Lazy Loading)
# We fetch all plans only when the user opens this.
with st.expander("📦 View All Available Plans"):
    if st.button("Load All Plans"): # Prevents loading 100+ plans until clicked
        all_packs = fetch_all_plans()
        i=0
        for index, pack in enumerate(all_packs, start=1):
            
            lines = []
            
            for benefit_dict in pack[f"benefits pack {i}"]:
                for key, value in benefit_dict.items():
                    if key=="Subscriptions":                            
                        lines.append(f"{key}: <strong>{value}</strong>")
                    else:
                        lines.append(f"{key}: {value}")
            i+=1
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
                    <h4 style="
                                    color: orange;
                                    ">Pack {index}</h4>
                    <p style="
                    color: blue;
                    ">{formatted_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )