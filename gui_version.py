
import tkinter as tk
from tkinter import ttk, messagebox
from shared_logic import load_data, merge_data, search_by_subject, search_by_classmark, search_by_location

def main():
    subject_file = "subject_classmark_expanded.csv"
    location_file = "classmark_location.csv"

    subjects_df, locations_df = load_data(subject_file, location_file)
    merged_df = merge_data(subjects_df, locations_df)

    if merged_df is None or merged_df.empty:
        messagebox.showerror("Error", "Data could not be loaded. Please check your CSV files.")
        return

    root = tk.Tk()    # Create the main window 
    root.title("Keele Library Finder (GUI Version)")
    root.geometry("850x600") #size

    tk.Label(root, text="Search by:", font=("Arial", 11)).pack(pady=5)
    search_type = ttk.Combobox(root, values=["Subject", "Classmark", "Location"])  #Search Type Menu (Subject / Classmark / Location) 
    search_type.pack(pady=5)

    tk.Label(root, text="Enter value or select location:", font=("Arial", 11)).pack(pady=5)
    user_input = ttk.Entry(root, width=40)
    user_input.pack(pady=5)

    available_locations = sorted(merged_df["location"].dropna().unique())
    location_dropdown = ttk.Combobox(root, values=available_locations, width=40)
    location_dropdown.pack_forget()

    def update_input_field(event=None):
        if search_type.get() == "Location":
            user_input.pack_forget()
            location_dropdown.pack(pady=5)
        else:
            location_dropdown.pack_forget()
            user_input.pack(pady=5)

    search_type.bind("<<ComboboxSelected>>", update_input_field)

    columns = ("Classmark", "Location", "Subject")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=250)
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def run_search(): #  Perform Search Function
        stype = search_type.get()
        if not stype:
            messagebox.showwarning("Warning", "Please select what you want to search by.")
            return

        if stype == "Location":
            value = location_dropdown.get()
        else:
            value = user_input.get()

        if not value.strip():
            messagebox.showwarning("Warning", "Please enter or select a value.")
            return

        try:
            if stype == "Subject":
                results = search_by_subject(merged_df, value)
            elif stype == "Classmark":
                results = search_by_classmark(merged_df, value)
            elif stype == "Location":
                results = search_by_location(merged_df, value)
            else:
                messagebox.showerror("Error", "Unknown search type.")
                return

            for row in tree.get_children():
                tree.delete(row)

            if results.empty:
                messagebox.showinfo("No Results", "No records found for that search.")
            else:
                for _, row in results.iterrows():
                    tree.insert("", "end", values=(row["classmark"], row["location"], row["subject"]))

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

    tk.Button(root, text="Search", command=run_search, bg="#5cb85c", fg="white", width=10).pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy, bg="#d9534f", fg="white", width=10).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":  # Run only if this file is executed directly 
    main()
