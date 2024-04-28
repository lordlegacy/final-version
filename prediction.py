import pickle
import pymongo
import time
from pipeline import final



client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["MachineDB"]  
collection = db["result"]  

with open("rf_classifier_version_2.pkl", "rb") as f:
    classifier = pickle.load(f)

def predict():
    df = final()
    finalFrame = df.drop(['machineID','datetime'], axis=1)
    prediction = classifier.predict(finalFrame)
    df["failure"] = prediction
    collection.insert_many(df.to_dict("records"))


predict()

