import os, json

PROGESS_FILE = "progress.json"

def save_progress(completed_queries):
    """
    Save completed queries to file
    """
    with open(PROGESS_FILE, "w") as file:
        json.dump(completed_queries, file, indent=4)

def load_progress():
    """
    Load completed queries from file
    """
    if os.path.exists(PROGESS_FILE):
        with open(PROGESS_FILE, "r") as file:
            content = file.read().strip()
            if content:
                return json.loads(content)
    return []


def mark_done(query):
    """
    Mark a query completed
    """

    progress = load_progress()
    if query not in progress:
        progress.append(query)
        save_progress(completed_queries=progress)
        print(f"{query} marked as completed 💡💡💡")
