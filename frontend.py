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
st.title("🚀 Recharge Plan Finder v0")
st.header("WELCOME TO RPF")
st.markdown("This website helps you find \nThe Recharge Plans provided by Jio based on the subscriptions selected by YOU")

# Fetch the OTT list (This is now instant after the first load)
unique_otts = fetch_ott_list()

with st.container(border=True):
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
                                    color: blue;
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

# 5. THE "EXPANDER" (Lazy Loading)
# We fetch all plans only when the user opens this.
with st.expander("📦 View All Available Plans"):
    if st.button("Load All Plans"): # Prevents loading 100+ plans until clicked
        all_packs = fetch_all_plans()
        for index, pack in enumerate(all_packs, start=1):

            lines = []

            lines.append(f"Price: ₹{pack['price']}")

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
                    <h4 style="
                                    color: blue;
                                    ">Pack {index}</h4>
                    <p style="
                    color: blue;
                    ">{formatted_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

with st.container(border=True):
    st.markdown("FUTURE SCOPE:")
    st.markdown("We are looking to include other Telecom providers and filters like price, validity... in future")
    st.markdown("AND Thats Why Its Version V0")