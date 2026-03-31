import pandas as pd
import sys

# read the query set 
def save_missing_and_retry(filename:str) -> pd.DataFrame:
    if filename.endswith(".csv"):
        df = pd.read_csv(filename)
    elif filename.endswith(".json"):
        df = pd.read_json(filename)
    else:
        print("❌ can't prefrom retry as file format not of json or csv")

    # find rows with missing phone
    missing = df[df["phone"].isna()]

    print("🪧🪧🪧  Missing phones:", len(missing))

    # construct filename 
    filname_const = f"missing_phone_{filename}.csv"

    # save for reprocessing
    missing.to_csv(filname_const, index=False)

    return missing

if __name__ == "__main__":
    # get the query to retry on 
    file = sys.argv[1]

    save_missing_and_retry(file)