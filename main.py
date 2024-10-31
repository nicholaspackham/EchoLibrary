from gui import setup_gui
from database import setup_database

if __name__ == "__main__":
    setup_database()  # Ensure the database is ready
    root = setup_gui()  # Set up GUI and table
    root.mainloop()  # Start the GUI event loop
