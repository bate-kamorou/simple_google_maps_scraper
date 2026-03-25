import pandas as pd
import sys

# read the data set 
def save_to_retry(data:str):
    if data.endswith(".csv"):
        df = pd.read_csv(data)
    if data.endswith(".json"):
        df= pd.read_json(data)

    # find rows with missing phone
    missing = df[df["phone"]].isna()

    print("Missing phones:", len(missing))

    #save for reprocessing
    missing.to_csv("missing_phone.csv", index=False)

if __name__ == "__main__":
    # get the data to retry on 
    file = sys.argv[1]

    save_to_retry(file)