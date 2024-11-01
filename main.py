from gui import setup_gui
from database import setup_database

if __name__ == "__main__":
    setup_database()  # ensure the database is ready
    root = setup_gui()  # set up GUI and table
    root.mainloop()  # start the GUI event loop
