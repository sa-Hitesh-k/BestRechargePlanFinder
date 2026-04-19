import streamlit as st
import requests 
from CreatingTable import uniqueottlist
selected=[]
st.title("Filter JIO plans")
st.header("Select the below Subscriptions and find the plans which provide them!")
with st.container(border=True):
    selected=st.pills('Subscriptions',uniqueottlist,selection_mode='multi')
st.write(f'You selected {selected}')


url = "http://127.0.0.1:8000/allJioplans/"

responseall = requests.get(url)
allpacks=responseall.json()
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
    

if selected:
    packcard={}
    with st.container(border=True):
        urlsubs="http://127.0.0.1:8000/filter-plans-by-subscriptions"
        query_params={
            "q":selected
        }
        responsesubs=requests.get(urlsubs,query_params)
        # st.write(responsesubs.json())
        ans=responsesubs.json()

#         #ans: dictionary(subs. : values[])->list(packs)->dictionary(details : list(details))->(beneftiname : benefitvalue)
        # for i in ans:
        #     # st.write('ans=',ans[i],type(ans[i]))#list
        #     for j in ans[i]:
        #         for k in j:
        #             pack=[]
        #             # st.write('j[k]=',j[k])
        #             for l in j[k]:
        #                 # st.write(l)
        #                 pack.append(l)
        #                 pack.append("\n")
        #         st.markdown(
        #                 f"""
        #                 <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        #                     <h4>Pack {i}</h4>
        #                     <p>{pack}</p>
        #                 </div>
        #                 """,
        #                 unsafe_allow_html=True
        #             )
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
        #             packcard[j[k]]=st.components.v2.component(
        #                 name="packs",
        #                 html=f"""
        #                     <div>
        #                     <p>
        #                     {j[k]}
        #                     </p>
        #                     </div>
        #                     """
        #             )
        # result=packcard.items()(key="themed_example")
                # st.write(j)
                # for k in ans
                # st.write(j)
                # for k in i[j]:
                #     st.write(k)
            # st.write(ans[i][0]['details'][0])
        # spec='*.*.details.*'
        # detlist=glom(ans,spec)
        # st.write(detlist)
