# ----------------------------------------------------------------------------------------------------------------
# NOTES: Using "time" (with speech marks) as a column name instead of time, as 'time' is a keyword
# ----------------------------------------------------------------------------------------------------------------

import sqlite3


def setup_database():
    conn = sqlite3.connect('music_metadata.db')
    cursor = conn.cursor()

    # cursor.execute("DROP TABLE IF EXISTS songs")

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

    conn = sqlite3.connect('music_metadata.db')
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
    conn = sqlite3.connect('music_metadata.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT 
                         song
                        ,album
                        ,artist
                        ,approx_release_date
                        ,"time"
                        ,file_size
                        ,created_date
                    FROM songs''')
    songs = cursor.fetchall()

    conn.close()

    return songs


def get_songs_by_name(song_name):
    # Fetch songs from the database that match the provided song name.
    conn = sqlite3.connect('music_metadata.db')
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
                            WHERE song LIKE ?''',
                   ('%' + song_name + '%',))

    results = cursor.fetchall()
    conn.close()

    return results


def delete_song(song, album, artist):
    conn = sqlite3.connect('music_metadata.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM songs WHERE song=? AND album=? AND artist=?",
                   (song, album, artist))

    conn.commit()
    conn.close()


def check_song_exists(song, album, artist):
    # Check if a song already exists in the database.
    conn = sqlite3.connect('music_metadata.db')
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM songs WHERE song=? AND album=? AND artist=?",
                   (song, album, artist))

    result = cursor.fetchone()
    conn.close()

    return bool(result)  # returns True if a record is found, otherwise False
