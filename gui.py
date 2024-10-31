import os
import subprocess
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import (ttk, messagebox, Toplevel, filedialog)
from tkinterdnd2 import (TkinterDnD, DND_FILES)
from openpyxl import Workbook
from database import (check_song_exists, insert_into_database, get_all_songs, get_songs_by_name, delete_song)
from metadata_extractor import (extract_metadata, is_valid_folder)


# ---------------------------------------------------------------------------------
# TODO (GUI Improvements):
# Set the Song Name, Album Name and Artist to LEFT aligned
# Have the window the full width and top half of the screen (both home and Database Viewer)
# Organise the screens better - fix the buttons, etc
# Add loading icons
# ---------------------------------------------------------------------------------


def setup_gui():
    # Main window setup
    root = TkinterDnD.Tk()

    # Title and Icon
    root.title("Echo Library")
    icon = tk.PhotoImage(file='images/echo-library-icon.png')  # load the icon image as a PhotoImage object
    root.iconphoto(True, icon)  # set the icon

    # Add a button to open the database window
    db_button = tk.Button(root, text="Open Database Viewer", command=open_database_window)
    db_button.pack(pady=10)

    # Setup main drag-and-drop area and table for the main window
    main_frame = ttk.Frame(root)
    home_tree = setup_dnd_table(main_frame)

    # Add a Remove button
    remove_button = tk.Button(root, text="Remove Selected Song",
                              command=lambda: delete_selected_songs(False, home_tree))
    remove_button.pack(pady=5)

    # Export To Excel button
    doc_prefix = "new-songs"
    col_headers = ["Song", "Album", "Artist", "Approx. Release Date", "Status"]
    export_button = tk.Button(root,
                              text="Export to Excel",
                              command=lambda: export_to_excel(doc_prefix, col_headers, home_tree)
                              )
    export_button.pack(pady=5)

    # Finish creation of main window
    main_frame.pack(fill='both', expand=True)

    return root


def setup_dnd_table(frame):
    columns = ("Song", "Album", "Artist", "Approx. Release Date", "Status")
    tree = setup_treeview(frame, columns)

    frame.drop_target_register(DND_FILES)
    frame.dnd_bind('<<Drop>>', lambda event: on_drop(event, tree))

    return tree


def on_drop(event, tree):
    file_paths = event.widget.tk.splitlist(event.data)
    for file_path in file_paths:
        if not is_valid_folder(file_path):
            messagebox.showerror("Invalid Folder", "Please drag folders from the allowed path.")
            continue
        if os.path.isdir(file_path):
            process_folder(file_path, tree)


def process_folder(folder_path, tree):
    m4p_files = [os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files if file.endswith('.m4p')]
    for m4p_file in m4p_files:
        song_metadata = extract_metadata(m4p_file)
        is_duplicate = check_song_exists(song_metadata['song'], song_metadata['album'],
                                         song_metadata['artist'])
        insert_into_database(is_duplicate, song_metadata)
        display_metadata(tree, song_metadata, is_duplicate)


def display_metadata(tree, metadata, is_duplicate):
    status = "Duplicate" if is_duplicate else "New"

    tree.insert("", "end", values=(
        metadata.get('song', 'N/A'), metadata.get('album', 'N/A'), metadata.get('artist', 'N/A'),
        metadata.get('approx_release_date', 'N/A'), status
    ))


def open_database_window():
    # Create a new Toplevel window
    db_window = Toplevel()
    db_window.title("Database Viewer")

    # Search bar and button
    search_frame = tk.Frame(db_window)
    search_frame.pack(pady=5)

    search_label = tk.Label(search_frame, text="Search Song:")
    search_label.pack(side="left")

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", padx=5)

    search_button = tk.Button(search_frame, text="Search", command=lambda: search_song(db_tree, search_entry.get()))
    search_button.pack(side="left")

    # Table
    columns = ("Song", "Album", "Artist", "Approx. Release Date", "Time", "File Size", "Created Date")
    db_tree = setup_treeview(db_window, columns)

    # Refresh button
    refresh_button = tk.Button(db_window, text="Refresh", command=lambda: refresh_db_data(search_entry, db_tree))
    refresh_button.pack(pady=5)

    # Delete button
    delete_button = tk.Button(db_window, text="Delete Selected",
                              command=lambda: delete_selected_songs(True, db_tree))
    delete_button.pack(pady=5)

    # Export to Excel button
    doc_prefix = "database-songs"
    col_headers = ["Song", "Album", "Artist", "Approx. Release Date", "Time", "File Size", "Created Date"]
    export_button = tk.Button(db_window,
                              text="Export to Excel",
                              command=lambda: export_to_excel(doc_prefix, col_headers, db_tree)
                              )
    export_button.pack(pady=5)

    # Initial load of all songs
    load_all_songs(db_tree)


def load_all_songs(tree):
    # Clear existing entries in the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Fetch all songs from the database
    songs = get_all_songs()

    # Insert each song into the Treeview
    for (song, album, artist, approx_release_date, time, file_size, created_date) in songs:
        tree.insert("",
                    "end",
                    values=(song, album, artist, approx_release_date, time, file_size, created_date)
                    )


def refresh_db_data(search_entry, tree):
    search_entry.delete(0, tk.END)  # clear search box
    load_all_songs(tree)  # reload all songs
    tree.focus_set()  # change focus to tree - so cursor not flashing in search box


def search_song(tree, song_name):
    # Clear current Treeview contents
    for row in tree.get_children():
        tree.delete(row)

    # Fetch songs that match the search query
    results = get_songs_by_name(song_name)

    # Insert matching songs into the Treeview
    for song in results:
        tree.insert("", "end", values=song)

    # Show message if no results found
    if not results:
        messagebox.showinfo("No Results", "No songs found with that name.")


# Functions for both Main and Database Viewer
#   -setup_treeview, delete_selected_songs, export_to_excel

def setup_treeview(parent, columns):
    tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)
    tree.pack(padx=10, pady=10, fill='both', expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    return tree


def delete_selected_songs(full_delete, tree):
    selected_items = tree.selection()

    if not selected_items:
        messagebox.showwarning("No Selection", "Please select one or more songs to delete.")
        return

    # Confirm deletion for all selected items
    if full_delete and not messagebox.askyesno("Confirm Delete",
                                               "Are you sure you want to delete the selected song(s)?"):
        return

    # Loop through selected items and delete each from database and Treeview
    for selected_item in selected_items:
        item = tree.item(selected_item)  # retrieve song info for each selected item
        song_data = item['values']

        if full_delete:
            song, album, artist, *_ = song_data  # unpack relevant fields - '_' ignores unneeded fields
            delete_song(song, album, artist)     # delete from database

        # Remove from Treeview
        tree.delete(selected_item)

    # Show confirmation message
    if full_delete:
        messagebox.showinfo("Deleted", "Selected song(s) have been deleted.")


def export_to_excel(doc_prefix, col_headers, tree):
    # Check if the Treeview is empty
    if not tree.get_children():
        messagebox.showwarning("Export Failed", "No data to export.")
        return

    # Set file path to Desktop with the name 'songs_YYYY-MM-DD.xlsx'
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(desktop_path, f"{doc_prefix}_{current_date}.xlsx")

    # Create a new Excel workbook and sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Songs"

    # Add headers
    sheet.append(col_headers)

    # Add Treeview data to the Excel sheet
    for row_id in tree.get_children():
        row = tree.item(row_id)['values']
        sheet.append(row)

    # Save the workbook
    workbook.save(file_path)
    messagebox.showinfo("Export Successful", f"Success! Data has been exported to {file_path}")

    # Automatically open the file
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.Popen(['open', file_path] if os.uname().sysname == 'Darwin' else ['xdg-open', file_path])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file: {e}")
