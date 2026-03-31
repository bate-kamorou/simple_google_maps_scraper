from multiprocessing import Pool
from scraper import Business_scraper
from tracker import load_progress


# queries to use
industries = [
    "solar installer",
    "roofing contractor",
    # "construction company"
]

cities = [
    # "Amsterdam",
    "Rotterdam",
    # "Utrecht",
    "Antwerp",
    # "Ghent"
]

# construct the query
queries = [f"{industry} {city}" for industry in industries for city in cities]


# run
if __name__ == "__main__":
    

    with Pool(2) as pool:
        pool.map(Business_scraper, queries)

        # load the completes queries
        completed = load_progress()

        # only run unfinished queries
        remaining = [query for query in  queries if query not in completed]

        for remains in remaining :
            print(f"Query: {remains} is remaining 🔏🔏🔏")


        if remaining:
            pool.map(Business_scraper, remaining)

    
