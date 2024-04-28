import streamlit as st
import pandas as pd
import pymongo
import time



client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["MachineDB"] 
collection = db["result"]

def fetch_latest_records_with_failure():
    query = {'failure': {'$ne': 'none'}}
    records = collection.find(query).sort("_id", -1).limit(15)
    df = pd.DataFrame(records)
    return df

def latest_logs():
    st.title("Recent Possible Failure Reports")
    df = fetch_latest_records_with_failure()
    report_columns = ['datetime', 'machineID', 'model', 'failure']
    df = df[report_columns]


    csv_data = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="latest_records.csv",
        mime="text/csv"
    )

    st.write(df)


def window():
    latest_logs()
    time.sleep(1)
    st.rerun()

window()