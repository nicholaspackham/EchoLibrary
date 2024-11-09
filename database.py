import os
import sqlite3
from datetime import datetime
from enums import (ErrorType)

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

    cursor.execute('''CREATE TABLE IF NOT EXISTS error_log
                    (
                        error_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        error_type TEXT NOT NULL,
                        error_message TEXT NOT NULL,
                        created_date DATETIME NOT NULL
                    )''')

    conn.commit()
    conn.close()


def insert_into_songs(is_duplicate, metadata):
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


def insert_into_error_log(error_type, error_message):
    if not isinstance(error_type, ErrorType):
        raise ValueError("Error: The 'error_type' passed in must be an instance of ErrorType")

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''INSERT INTO error_log 
                      (error_type, error_message, created_date) 
                      VALUES (?, ?, ?)''',
                   (error_type.value, error_message, created_date))  # Use ErrorType.value for the TEXT

    error_id = cursor.lastrowid  # retrieve the ID of the newly inserted row
    conn.commit()
    conn.close()

    return error_id


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


def get_all_error_logs():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT 
                         error_id
                        ,error_type
                        ,error_message
                        ,created_date 
                    FROM error_log 
                    ORDER BY created_date DESC'''
                   )
    song_error_logs = cursor.fetchall()

    conn.close()

    return song_error_logs


def get_processing_error_logs():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT 
                         error_id
                        ,error_type
                        ,error_message
                        ,created_date 
                      FROM error_log 
                      WHERE error_type=? 
                      ORDER BY created_date DESC''',
                   (ErrorType.PROCESSING_ERROR.value,)
                   )
    processing_error_logs = cursor.fetchall()

    conn.close()

    return processing_error_logs


def delete_song(song, album, artist):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM songs WHERE song=? AND album=? AND artist=?",
                   (song, album, artist))

    conn.commit()
    conn.close()


def delete_error_log(error_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Even if single param, SQLite expects a tuple '(item,)'
    cursor.execute("DELETE FROM error_log WHERE error_id=?", (error_id,))

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
