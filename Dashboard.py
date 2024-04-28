import pymongo
import streamlit as st
from datetime import datetime
import time
from prediction import predict


client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["MachineDB"] 
collection = db["result"] 

def get_latest_readings():
    latest_reading = collection.find_one(sort=[('datetime', -1)])
    return latest_reading

def display_latest_readings():
    st.title("Telemetry")
    st.divider()
    latest_record = get_latest_readings()
    if latest_record:
        current_datetime = datetime.now()
        st.write("Latest Readings:")
        st.write("Current Date and Time:", current_datetime)
        st.write("Vibration:", latest_record["vibration"])
        st.write("Voltage:", latest_record["volt"])
        st.write("RPM:", latest_record["rotate"])
        st.write("Pressure:", latest_record["pressure"])
        machine_status = "OK" if latest_record["failure"] == "none" else "possible failure"
        st.write("Machine status:", machine_status)

def main():
    predict()
    display_latest_readings()
    time.sleep(2)
    st.rerun()
    
main()
