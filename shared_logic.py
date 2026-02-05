# We'll use pandas to handle CSV files and tabulate for nice table display
import pandas as pd  # pandas helps with reading + joining CSV tables

def load_data(subject_file, location_file):
    """Loads the two CSV files safely (subjects + locations)."""
    try:                                        #try-except ensures the program does not crash if CSVs fail to load.
        subjects_df = pd.read_csv(subject_file) # load subjects CSV into a Dataframe
        locations_df = pd.read_csv(location_file) # load locations CSV into a Dataframe
        print(" CSV files loaded successfully!")
        return subjects_df, locations_df
    except FileNotFoundError:
        print(" CSV files are missing.")
        return None, None
    except Exception as e:                                   # if anything goes wrong (file missing, wrong format, etc.)
        print(" Some error occurred while loading files:", e)
        return None, None


def merge_data(subjects_df, locations_df):         # This  will gives us one combined table with subject, classmark, and location.

    """Merges both datasets on 'classmark' column."""
    try:
        merged_df = pd.merge(
            subjects_df,      # left table: all subjects
            locations_df,     # right table: locations
            on="classmark",   # merge on classmark
            how="outer"       # Keeps all subjects, even if classmark is missing in locations.( how= how=left),
                              #Keeps all locations, even if classmark is missing in subjects.( how=right)
        )
        print(" Data merged successfully!")
        return merged_df
    except Exception as e:
        print(" Error merging data:", e)
        return pd.DataFrame()


def search_by_subject(df, keyword):
    """Finds rows where subject contains the search word (case-insensitive)."""
    if df is None or df.empty:
        return pd.DataFrame()
    keyword = keyword.lower()  # convert search keyword to lowercase
    return df[df["subject"].str.lower().str.contains(keyword, na=False)] # filter rows where subject column contains the keyword


def search_by_classmark(df, code):
    """Finds rows where classmark contains the entered code."""
    if df is None or df.empty:
        return pd.DataFrame()
    code = code.lower()       # convert search code to lowercase
    return df[df["classmark"].str.lower().str.contains(code, na=False)] # filter rows where 'classmark' column contains the code


def search_by_location(df, location):
    """Finds all records for a specific location (exact match)."""
    if df is None or df.empty:
        return pd.DataFrame()
    return df[df["location"].str.lower() == location.lower()] # filter rows where 'location' column exactly matches the input
