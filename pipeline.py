import datetime as dt
import datetime
from datetime import datetime
import pandas as pd
import pymongo





client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["MachineDB"] 
collection = db["demonstration"] 

def get_latest_telemetry_record():
    collection = db["demonstration"]
    import datetime
    from datetime import datetime
    now = datetime.now()
    now = now.replace(microsecond=0)
    datetime = now
    query = {"datetime": datetime}
    telemetry_record = collection.find_one(query)
    voltage = telemetry_record["volt"]
    rpm = telemetry_record["rotate"]
    pressure = telemetry_record["pressure"]
    vibration = telemetry_record["vibration"]
    machine_id = telemetry_record["machineID"]
    datetime = telemetry_record["datetime"]
    return voltage, rpm, pressure, vibration, machine_id, datetime


def get_model_and_age(machine_id, collection_name="model"):
    collection = db[collection_name]
    query = {"machineID": machine_id}
    model_and_age = collection.find_one(query)  

    if model_and_age["model"] == "model1":
        model = 1
    elif model_and_age["model"] == "model2":
        model = 2
    elif model_and_age["model"] == "model3":
        model = 3
    else:
        model = 4
    
    age = model_and_age["age"]
    return model,age

def error(machine_id, datetime, collection_name="error"):
    collection = db[collection_name]
    query = {
        "machineID": machine_id,
        "datetime": datetime
    }
    errors = list(collection.find(query))  
    return errors



def sum_up_errors():
    telemetry = get_latest_telemetry_record()
    hourly_errors = error(telemetry[4], telemetry[5])
    error_counts = {'error1': 0, 'error2': 0, 'error3': 0, 'error4': 0, 'error5': 0}
    
    for err in hourly_errors:
        if 'errorID' in err:
            error_counts[err['errorID']] += 1
    
    error_counts_tuple = tuple(error_counts.values())
    return error_counts_tuple  



def days_since_last_repair(machine_id, provided_datetime):
    collection = db['maintenance']
    query = {
        "machineID": machine_id,
        "datetime": {"$lt": provided_datetime}
    }
    comp_values = ["comp1", "comp2", "comp3", "comp4"]
    result = []
    
    for comp in comp_values:        
        query["comp"] = comp        
        record = collection.find_one(query, sort=[('datetime', -1)])
        result.append(record)
       
    days_since_last_repair = []

    for entry in result:
        record_datetime = entry['datetime']      
        difference = (provided_datetime - record_datetime).total_seconds() / 3600  # Convert to hours
        days_since_last_repair.append(difference)
    return tuple(days_since_last_repair)



def final():
    telemetry = get_latest_telemetry_record()
    model_and_age = get_model_and_age(telemetry[4])
    total_errors = sum_up_errors()
    last_repair = days_since_last_repair(telemetry[4], telemetry[5])
    columns = ['volt', 'rotate', 'pressure', 'vibration', 'error1', 'error2', 'error3', 'error4', 'error5',
           'comp1', 'comp2', 'comp3', 'comp4', 'model', 'age']
    combined_tuple = telemetry[:4] + total_errors + last_repair + model_and_age
    df = pd.DataFrame([combined_tuple], columns=columns)
    df['model'] = df['model'].astype('category')    
    df['machineID'] = telemetry[4]
    df['datetime'] = telemetry[5]
    print("dataframe ready for prediction")
    return df

