import pandas as pd
import glob
import sys

def merge_result(file_extension:str=".csv"):
    """
    Merge output results into a final dataset

    Agrs:
        file_extension: files type to merge together (.csv or .json)
    """
    try:
        # get the files with extension
        files = glob.glob(pathname=f"output/*{file_extension.lower()}")

        if file_extension.lower() == ".csv":
            # read the csv files and combine them together
            df = pd.concat([pd.read_csv(file) for file in files])
            
            # remove duplicates
            df = df.drop_duplicates(subset="company_name")

            # save file to csv
            df.to_csv("output/Final_dataset.csv", index=False)

            print("Final CSV file saved 🗃️🗃️🗃️")
        
        elif file_extension.lower() == ".json":
            # read the json files and combine them together
            df  = pd.concat([pd.read_json(file) for file in files])

            # remove duplicates
            df = df.drop_duplicates(subset="company_name")

            # save file to json 
            df.to_json("output/Final_dataset.json", indent=4)

            print(f"Final JSON file saved 🗃️🗃️🗃️")
        else:
            print("❌❌❌  File extension not covered use .csv or .json")

    except Exception as e:
        print(f"ERROR❌❌❌: Merge didn't succedd \nERROR Description {e}")


if __name__ == "__main__":

    # get the input from terminal 
    input = sys.argv[1]

    # Run the function  to merge csv files in the output directory
    merge_result(file_extension=input)

