import streamlit as st
import pandas as pd
import pymongo


st.set_page_config(page_title="Recon Dashboard", page_icon=":mag:", layout="wide")

st.markdown(
    """
    <style>
        footer {display: none}
        [data-testid="stHeader"] {display: none}
    </style>
    """, unsafe_allow_html = True
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Connect to MongoDB
def get_mongo_collection(collection_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["recon"]
    collection = db[collection_name]
    return collection


def fetch_data(collection_name):
    collection = get_mongo_collection(collection_name)
    data = list(collection.find())
    df_data = pd.DataFrame(data)
    return df_data


def main():
    st.markdown('<h1 class="title">Recon Dashboard</h1>', unsafe_allow_html=True)

    domains, subdomains = st.columns(2)

    with domains:
        domains_count = fetch_data("verified_subdomains")["domain"].nunique()
        st.markdown(
            '<div class="box"><p class="domains">Top Level Domains</p><p class="count">{}</p></div>'.format(domains_count),
            unsafe_allow_html=True
        )

    with subdomains:
        subdomains_count = fetch_data("verified_subdomains")["subdomain"].nunique()
        st.markdown(
            '<div class="box"><p class="subdomains">Sub Domains</p><p class="count">{}</p></div>'.format(subdomains_count),
            unsafe_allow_html=True
        )



    # st.markdown('<h4 class="subtitle">Final Subdomains List</h4>', unsafe_allow_html=True)
    # subdomains = fetch_data("verified_subdomains")
    # st.dataframe(subdomains.drop(["_id", "age"], axis=1))

    # # Display data as a chart
    # st.subheader("Subdomains Status Code Distribution")
    # status_code_counts = subdomains['status_code'].value_counts()
    # st.bar_chart(status_code_counts)
    #
    # # Display data as a pie chart
    # st.subheader("Technology Distribution")
    # tech_counts = subdomains['tech'].value_counts()
    # st.write(tech_counts.plot.pie(autopct='%1.1f%%'))
    # st.pyplot()



if __name__ == "__main__":
    main()
