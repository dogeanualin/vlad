
import mysql.connector
import tkinter as tk
from tkinter import ttk


# Establish a connection to the OLAP database
olap_cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
olap_cursor = olap_cnx.cursor()

# Establish a connection to the OLTP database
oltp_cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
oltp_cursor = oltp_cnx.cursor()

# Create the main GUI window
window = tk.Tk()
window.title("Database Viewer")

# Create a frame to display the tables
tables_frame = tk.Frame(window)
tables_frame.pack()

# Create a function to show the table structure
def show_table_structure(database, table_name):
    # Clear the tables frame
    clear_frame(tables_frame)

    # Select the appropriate database based on the button click
    if database == "OLAP Database":
        cnx = olap_cnx
        cursor = olap_cursor
    elif database == "OLTP Database":
        cnx = oltp_cnx
        cursor = oltp_cursor
    else:
        return

    # Fetch the table structure from the selected table
    cursor.execute(f"DESCRIBE {table_name}")
    table_structure = cursor.fetchall()

    # Create a table to display the structure
    table = ttk.Treeview(tables_frame)
    table["columns"] = ("Field", "Type", "Null", "Key", "Default", "Extra")
    table.column("#0", width=0, stretch=tk.NO)
    table.column("Field", anchor=tk.W, width=100)
    table.column("Type", anchor=tk.W, width=100)
    table.column("Null", anchor=tk.W, width=100)
    table.column("Key", anchor=tk.W, width=100)
    table.column("Default", anchor=tk.W, width=100)
    table.column("Extra", anchor=tk.W, width=100)

    table.heading("#0", text="")
    table.heading("Field", text="Field")
    table.heading("Type", text="Type")
    table.heading("Null", text="Null")
    table.heading("Key", text="Key")
    table.heading("Default", text="Default")
    table.heading("Extra", text="Extra")

    for field, field_type, null, key, default, extra in table_structure:
        table.insert("", tk.END, values=(field, field_type, null, key, default, extra))

    table.pack()

# Function to clear a frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Create a function to fetch table names from the database
def fetch_table_names(database):
    # Select the appropriate database
    if database == "OLAP Database":
        cnx = olap_cnx
        cursor = olap_cursor
    elif database == "OLTP Database":
        cnx = oltp_cnx
        cursor = oltp_cursor
    else:
        return []

    # Fetch the table names from the selected database
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor]
    return tables


# Close the database connections
olap_cursor.close()
olap_cnx.close()
oltp_cursor.close()
oltp_cnx.close()
