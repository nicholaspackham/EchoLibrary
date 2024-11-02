import tkinter as tk
from tkinter import (ttk, Toplevel)
from tkinterdnd2 import (TkinterDnD, DND_FILES)
from gui_components import (create_custom_style, create_button, set_search_bar_placeholder, on_focus_in, on_focus_out,
                            setup_treeview, on_drop, load_all_songs, refresh_db_data, search_song,
                            delete_selected_songs, export_to_excel)
from constants import HELP_AND_INFORMATION_TEXT


# ---- Windows (Main Frame & Database Frame) ----
def setup_gui(icon_path):
    # Main window setup
    root = TkinterDnD.Tk()

    # Set the initial window size
    root.geometry("1220x325")
    root.title("Echo Library")
    root.configure(bg="#333333")

    # Set the window icon
    icon = tk.PhotoImage(file=icon_path)
    root.iconphoto(True, icon)

    # Apply custom style for buttons
    create_custom_style(root)

    # Setup main drag-and-drop area and table for the main window
    main_frame = ttk.Frame(root)
    mf_tree = setup_mf_table(main_frame)

    # Setup button frame
    setup_button_frame_mf(root, mf_tree)

    # Complete main_frame
    main_frame.pack(fill='both', expand=True, pady=(0, 0))

    return root


def open_database_window():
    # Create a new Toplevel window
    db_window = Toplevel()
    db_window.title("Echo Library - Database Viewer")

    # Set the window size (width x height) and position (optional)
    db_window.geometry("1220x700")  # Adjust width and height as needed

    # Apply custom style for buttons
    create_custom_style(db_window)

    # Configure grid layout for db_window
    db_window.grid_rowconfigure(1, weight=1)  # Allow row 1 (Treeview row) to expand
    db_window.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand

    # Column names and properties
    column_properties = {
        "Song": {"width": 200, "anchor": "w"},
        "Album": {"width": 250, "anchor": "w"},
        "Artist": {"width": 250, "anchor": "w"},
        "Approx. Release Date": {"width": 100, "anchor": "center"},
        "Time": {"width": 40, "anchor": "center"},
        "File Size": {"width": 50, "anchor": "center"},
        "Created Date": {"width": 125, "anchor": "center"}
    }
    columns = list(column_properties.keys())

    # Create a frame for the Treeview and initialize db_tree
    tree_frame = tk.Frame(db_window)
    tree_frame.grid(row=1, column=0, sticky="nsew")
    db_tree = setup_dbw_table(tree_frame, column_properties)

    # Set up the button frame above the Treeview, passing db_tree to it
    button_frame = tk.Frame(db_window)
    button_frame.grid(row=0, column=0, sticky="ew", pady=5)
    setup_button_frame_dbw(button_frame, db_tree, columns)

    # Load all songs into the db_tree after setup
    load_all_songs(db_tree)


def open_help_and_info_window():
    # Create a new Toplevel window
    help_and_info_window = tk.Toplevel()
    help_and_info_window.title("Echo Library - Help & Information")
    help_and_info_window.geometry("400x300")  # Set window size as needed

    # Add a Text widget to display information about the app
    help_and_info_text = HELP_AND_INFORMATION_TEXT

    # Display the information in a Text widget
    text_widget = tk.Text(help_and_info_window, wrap="word", font=("Arial", 10))
    text_widget.insert("1.0", help_and_info_text)
    text_widget.configure(state="disabled")  # Make text read-only
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Optionally add a close button
    close_button = tk.Button(help_and_info_window, text="Close", command=help_and_info_window.destroy)
    close_button.pack(pady=10)


# ---- Main Frame (Contents) ----
def setup_button_frame_mf(main_frame, tree):
    # Set up the frame holding all buttons and their commands.
    button_frame = tk.Frame(main_frame, bg="#333333")
    button_frame.pack(anchor="w", pady=(10, 0), padx=5)

    # Create each button and add to the button frame
    db_button = create_button(button_frame, "Open Database Viewer", open_database_window)
    db_button.pack(side="left", padx=5)

    remove_button = create_button(button_frame,
                                  "Remove Selected Song(s)",
                                  lambda: delete_selected_songs(False, tree)
                                  )
    remove_button.pack(side="left", padx=5)

    export_button = create_button(button_frame,
                                  "Export to Excel",
                                  lambda: export_to_excel("new-songs",
                                                          ["Song", "Album", "Artist",
                                                           "Approx. Release Date", "Status"], tree))
    export_button.pack(side="left", padx=5)

    help_button = create_button(button_frame, "Help", open_help_and_info_window)
    help_button.pack(side="top", padx=5)


def setup_mf_table(frame):
    columns_properties = {
        "Song": {"width": 200, "anchor": "w"},
        "Album": {"width": 250, "anchor": "w"},
        "Artist": {"width": 250, "anchor": "w"},
        "Approx. Release Date": {"width": 100, "anchor": "center"},
        "Status": {"width": 50, "anchor": "center"}
    }
    tree = setup_treeview(frame, columns_properties)

    frame.drop_target_register(DND_FILES)
    frame.dnd_bind('<<Drop>>', lambda event: on_drop(event, tree))

    return tree


# ---- Database Window (Contents) ----
def setup_button_frame_dbw(db_window, db_tree, columns):
    # Set up the frame holding all buttons and their commands.
    button_frame = tk.Frame(db_window, bg="#333333")
    button_frame.pack(anchor="w", pady=(10, 0), padx=5)

    # Defining a data grid (positioning of the buttons)
    button_frame.grid_columnconfigure(0, weight=1)  # Left side (search_frame)
    button_frame.grid_columnconfigure(1, weight=1)  # Right side (action_frame)

    # ---- Search bar ----
    search_frame = tk.Frame(button_frame)
    search_frame.grid(row=0, column=0, sticky="w", pady=(0, 0), padx=0)

    search_bar_font = ("Arial", 11)
    search_bar = tk.Entry(search_frame, width=60, font=search_bar_font)
    search_bar.pack(side="left", padx=5)

    # Set the placeholder (Select song...)
    set_search_bar_placeholder(search_bar)

    # Bind focus in and out events for placeholder behavior
    # Bind 'Enter' key - run search_song func when the 'enter' key is pressed
    search_bar.bind("<FocusIn>", lambda event: on_focus_in(event))
    search_bar.bind("<FocusOut>", lambda event: on_focus_out(event))
    search_bar.bind("<Return>", lambda event: search_song(db_tree, search_bar.get(), search_bar))

    # ---- Action buttons ----
    action_frame = tk.Frame(button_frame, bg="#333333")
    action_frame.grid(row=0, column=1, sticky="e", pady=(0, 0), padx=5)

    refresh_button = create_button(action_frame,
                                   "Refresh",
                                   command=lambda: refresh_db_data(search_bar, db_tree)
                                   )
    refresh_button.pack(side="left", padx=5)

    delete_button = create_button(action_frame,
                                  "Delete Selected Song(s)",
                                  command=lambda: delete_selected_songs(True, db_tree)
                                  )
    delete_button.pack(side="left", padx=5)

    doc_prefix = "database-songs"
    col_headers = columns
    export_button = create_button(action_frame,
                                  "Export to Excel",
                                  command=lambda: export_to_excel(doc_prefix, col_headers, db_tree)
                                  )
    export_button.pack(side="left", padx=5)

    help_button = create_button(action_frame, "Help", open_help_and_info_window)
    help_button.pack(side="left", padx=5)


def setup_dbw_table(db_window, column_properties):
    return setup_treeview(db_window, column_properties)
