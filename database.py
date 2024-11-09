import os
import sqlite3
from settings import (IS_TEST_MODE, APP_ROOT_FOLDER_TEST_MODE, APP_ROOT_FOLDER)


# Define the path for the Echo Library application directory and the database file
root_directory = os.path.expanduser("~")  # e.g. '/Users/nicholaspackham'

# Using two different directories for testing and prod
if IS_TEST_MODE:
    db_directory = os.path.join(root_directory, APP_ROOT_FOLDER_TEST_MODE)
else:
    db_directory = os.path.join(root_directory, APP_ROOT_FOLDER)

# Append 'SQLite DB' on to APP_ROOT_FOLDER*
db_directory = os.path.join(db_directory, "SQLite DB")

# Create the directory - if it does not exist
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# Generate the file name - which will provide the full database_path
database_path = os.path.join(db_directory, "echo_library.db")


def setup_database():
    # Ensure the directory exists
    os.makedirs(db_directory, exist_ok=True)

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Used to clear the songs table when testing - uncomment this line and comment out the 'CREATE TABLE' section below
    # cursor.execute("DROP TABLE IF EXISTS songs")

    # Using "time" (with speech marks) as a column name instead of time, as 'time' is a keyword
    cursor.execute('''CREATE TABLE IF NOT EXISTS songs
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        song TEXT NOT NULL,
                        album TEXT NOT NULL,
                        artist TEXT NOT NULL,
                        approx_release_date DATE NOT NULL,
                        "time" TEXT NOT NULL,
                        file_size TEXT NOT NULL,
                        created_date DATETIME NOT NULL
                    )''')

    conn.commit()
    conn.close()


def insert_into_database(is_duplicate, metadata):
    if is_duplicate:
        return  # duplicate found

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO songs 
                            (
                                 song
                                ,album
                                ,artist
                                ,approx_release_date
                                ,"time"
                                ,file_size
                                ,created_date
                            ) 
                            VALUES 
                            (
                                 ?
                                ,?
                                ,?
                                ,?
                                ,?
                                ,?
                                ,?
                            )''',
                   (metadata['song'], metadata['album'], metadata['artist'],
                    metadata['approx_release_date'], metadata['time'], metadata['file_size'],
                    metadata['created_date']))

    conn.commit()
    conn.close()


def get_all_songs():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT 
                         song
                        ,album
                        ,artist
                        ,approx_release_date
                        ,"time"
                        ,file_size
                        ,created_date
                    FROM songs
                    ORDER BY created_date DESC'''
                   )
    songs = cursor.fetchall()

    conn.close()

    return songs


def get_songs_by_name(song_name):
    # Fetch songs from the database that match the provided song name.
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT 
                                song
                                ,album
                                ,artist
                                ,approx_release_date
                                ,"time"
                                ,file_size
                                ,created_date 
                            FROM songs 
                            WHERE song LIKE ?
                            ORDER BY created_date DESC''',
                   ('%' + song_name + '%',))

    results = cursor.fetchall()
    conn.close()

    return results


def delete_song(song, album, artist):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM songs WHERE song=? AND album=? AND artist=?",
                   (song, album, artist))

    conn.commit()
    conn.close()


def check_song_exists(song, album, artist):
    # Check if a song already exists in the database.
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM songs WHERE song=? AND album=? AND artist=?",
                   (song, album, artist))

    result = cursor.fetchone()
    conn.close()

    return bool(result)  # returns True if a record is found, otherwise False
