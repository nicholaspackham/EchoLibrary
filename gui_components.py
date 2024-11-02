import os
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import (ttk, messagebox)
from openpyxl import Workbook
from database import (check_song_exists, insert_into_database, get_all_songs, get_songs_by_name, delete_song)
from metadata_extractor import (extract_metadata, is_valid_folder)
from constants import (SONG_SEARCH_BAR_PLACEHOLDER)


# ---- Treeview Setup ----
def setup_treeview(parent, column_properties):
    columns = list(column_properties.keys())  # extract column names from the keys of column_properties

    tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)
    tree.pack(padx=10, pady=10, fill='both', expand=True)

    for col, properties in column_properties.items():
        # Set the heading and apply width and alignment
        #   -The 'get' function looks for the specific key, if it cannot find it, it uses the default
        #   -E.G. properties.get("width", 120) - looks for "width", if not found uses 120.
        tree.heading(col, text=col)
        tree.column(col, width=properties.get("width", 120), anchor=properties.get("anchor", "center"))

    return tree


# ---- Custom Button Styles ----
def create_custom_style(root):
    # Create and apply a custom style for ttk buttons.
    style = ttk.Style(root)
    button_font = ("Arial", 9, "bold")

    # Default background color and font
    style.configure("Custom.TButton", font=button_font, background="#555555", foreground="#FFFFFF")

    # Different shades for different button states
    style.map("Custom.TButton",
              background=[("active", "#FFFFFF"),  # hover effect
                          ("pressed", "#FFFFFF"),  # clicked effect
                          ("!active", "#555555")],  # default state
              foreground=[("disabled", "#AAAAAA")])  # gray out text if button is disabled


def create_button(parent, text, command):
    # Helper function to create a styled button with predefined style.
    return ttk.Button(parent, text=text, style="Custom.TButton", command=command)


# ---- Search Bar (Database Window) ----
def set_search_bar_placeholder(search_bar):
    # Set the search bar placeholder text if the search_bar is empty.
    if search_bar.get() == "":
        search_bar.insert(0, SONG_SEARCH_BAR_PLACEHOLDER)
        search_bar.configure(fg="gray")


def on_focus_in(event):
    # Remove the placeholder text when search_bar is focused.
    search_bar = event.widget
    if search_bar.get() == SONG_SEARCH_BAR_PLACEHOLDER:
        search_bar.delete(0, tk.END)
        search_bar.configure(fg="white")


def on_focus_out(event):
    # Set the placeholder text if search_bar is empty on focus out.
    search_bar = event.widget
    set_search_bar_placeholder(search_bar)


# ---- Data Processing ----
def on_drop(event, tree):
    file_paths = event.widget.tk.splitlist(event.data)
    for file_path in file_paths:
        if not is_valid_folder(file_path):
            messagebox.showerror("Invalid Folder", ("Please drag folders from the allowed path.\n\n" +
                                                         " Allowed path: "
                                                         "/Users/*user_name*/Music/Music/Media.localized/Apple Music")
                                 )
            continue

        if os.path.isdir(file_path):
            process_folder(file_path, tree)


def process_folder(folder_path, tree):
    m4p_files = [os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files if
                 file.endswith('.m4p')]
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
        metadata.get('approx_release_date', 'N/A'), status)
    )


# ---- Data Manipulation ----
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


def refresh_db_data(search_bar, tree):
    search_bar.delete(0, tk.END)  # clear search box
    load_all_songs(tree)  # reload all songs
    tree.focus_set()  # change focus to tree - so cursor not flashing in search box
    set_search_bar_placeholder(search_bar)  # reset the search bar placeholder


def search_song(tree, song_name, search_bar):
    # Clear current Treeview contents
    for row in tree.get_children():
        tree.delete(row)

    # Fetch songs that match the search query
    results = get_songs_by_name(song_name)

    # Insert matching songs into the Treeview
    for song in results:
        tree.insert("", "end", values=song)


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
            delete_song(song, album, artist)  # delete from database

        # Remove from Treeview
        tree.delete(selected_item)


# ---- Exporting ----
def export_to_excel(doc_prefix, col_headers, tree):
    # Check if the Treeview is empty
    if not tree.get_children():
        messagebox.showwarning("Export Failed", "No data to export.")
        return

    # Confirmation to export to Excel
    if not messagebox.askyesno("Confirm Excel Export", "Are you sure you to export this data to Excel?"):
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
