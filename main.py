import os
import sys
from gui import setup_gui, backup_database
from database import setup_database


def resource_path(relative_path):
    # Get the absolute path to the resource, works for both dev and PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def on_close():
    backup_database()
    root.destroy()  # close the tkinter application


if __name__ == "__main__":
    setup_database()  # ensure the database is ready
    icon_path = resource_path("images/echo-library-icon.png")  # Get absolute path for icon
    root = setup_gui(icon_path)  # Pass icon_path to setup_gui
    root.protocol("WM_DELETE_WINDOW", on_close)  # set up the close protocol
    root.mainloop()  # start the GUI event loop
