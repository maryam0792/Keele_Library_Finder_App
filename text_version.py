
from tabulate import tabulate
from shared_logic import load_data, merge_data, search_by_subject, search_by_classmark, search_by_location

def main():
    print("Welcome to Keele Library Finder (Text Version)")
    print("**********************************************")

    subject_file = "subject_classmark_expanded.csv" # CSV containing subjects and classmarks
    location_file = "classmark_location.csv"        # CSV containing classmarks and locations

    subjects_df, locations_df = load_data(subject_file, location_file)
    merged_df = merge_data(subjects_df, locations_df)

    if merged_df is None or merged_df.empty:
        print("Sorry, could not prepare the data.")
        return

    while True:                           # infinite loop until user chooses to exit
        print("Please select an option:")
        print("1. Search by Subject")
        print("2. Search by Classmark")
        print("3. Search by Location")
        print("4. Exit")

        choice = input("Enter your choice (1–4): ").strip()

        if choice == "1":
            keyword = input("\nEnter subject name or part of it: ")
            results = search_by_subject(merged_df, keyword)

        elif choice == "2":
            code = input("\nEnter classmark or part of it: ")
            results = search_by_classmark(merged_df, code)

        elif choice == "3":
            print("\nAvailable locations:")
            available_locations = sorted(merged_df["location"].dropna().unique()) # Drop NaN values, convert to string, then sort
            for loc in available_locations:
                print("-", loc)      # show all unique non-null locations
            location = input("\nEnter a location (exactly as shown): ")
            results = search_by_location(merged_df, location)

        elif choice == "4":
            print("\n Goodbye! Thanks for using Keele Library Finder.")
            break  # exit the loop

        else:
            print("\n Invalid choice. Try again.")
            continue    # go back to start of loop if input is invalid

        if results.empty:
            print("\nNo matches found.\n")  # handle case where search returns nothing
        else:
            print("\nHere are your results:\n")
            print(tabulate(results[["classmark", "location", "subject"]], headers="keys", tablefmt="grid")) # print results nicely in a table using tabulate

        again = input("\nDo you want to search again? (y/n): ").lower()
        if again != "y": # exit if user does not want to search again
            print("\n Goodbye!\n")
            break

if __name__ == "__main__":
    main()
