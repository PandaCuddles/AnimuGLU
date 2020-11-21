import sqlite3
from sqlite3 import Connection


def setup():
    conn = sqlite3.connect("data.db")
    print("Database connection setup successfully")
    return conn

def create_config(conn : Connection):
    conn.execute('''CREATE TABLE IF NOT EXISTS CONFIG
              (LIBRARY    TEXT PRIMARY KEY NOT NULL,
               TYPE       TEXT             NOT NULL,
               CONFIG     INT              NOT NULL,
               ACTIVE     INT);''')
    conn.commit()
    print("Created CONFIG table successfully")

def create_data(conn : Connection):
    # SECTION 1: SHARED DATA
    # SECTION 2: MANGA  DATA
    # SECTION 3: ANIME  DATA
    conn.execute('''CREATE TABLE IF NOT EXISTS DATA
              (MAL_ID      INT  PRIMARY KEY NOT NULL,
               NAME        TEXT             NOT NULL,
               URL         TEXT             NOT NULL,
               IMAGE_URL   TEXT             NOT NULL,
               TITLE       TEXT             NOT NULL,
               SYNOPSIS    TEXT             NOT NULL,
               TYPE        TEXT             NOT NULL,
               SCORE       TEXT             NOT NULL,
               START_DATE  TEXT             NOT NULL,
               END_DATE    TEXT             NOT NULL,
               MEMBERS     TEXT             NOT NULL,
               IMAGE       BLOB             NOT NULL,
               SEARCH_TYPE TEXT             NOT NULL,
               JSON        TEXT             NOT NULL,

               PUBLISHING  TEXT                     ,
               CHAPTERS    TEXT                     ,
               VOLUMES     TEXT                     ,

               EPISODES    TEXT);''')
    print("Created DATA table successfully")

# TODO: Add library type to database, as well as a library_type variable to anime/manga objects
def insert_data(conn : Connection, values ):

    if values.search_type == "Anime":
        vals = (values.mal_id,
                values.anime,
                values.url,
                values.image_url,
                values.title,
                values.synopsis,
                values.type,
                values.score,
                values.start_date,
                values.end_date,
                values.members,
                values.image,
                values.search_type,
                values.json,
                values.episodes)
        cmd = '''INSERT INTO DATA 
                (MAL_ID, NAME, URL, IMAGE_URL, TITLE, SYNOPSIS, TYPE, SCORE, START_DATE, END_DATE, MEMBERS, IMAGE, SEARCH_TYPE, JSON, EPISODES) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        conn.execute(cmd, vals)
        conn.commit()
    
    if values.search_type == "Manga":
        vals = (values.mal_id,
                values.manga,
                values.url,
                values.image_url,
                values.title,
                values.synopsis,
                values.type,
                values.score,
                values.start_date,
                values.end_date,
                values.members,
                values.image,
                values.search_type,
                values.json,
                values.publishing,
                values.chapters,
                values.volumes)

        cmd = '''INSERT INTO DATA 
                (MAL_ID, NAME, URL, IMAGE_URL, TITLE, SYNOPSIS, TYPE, SCORE, START_DATE, END_DATE, MEMBERS, IMAGE, SEARCH_TYPE, JSON, PUBLISHING, CHAPTERS, VOLUMES) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        conn.execute(cmd, vals)
        conn.commit()

def insert_config(conn : Connection, values : tuple):
    conn.execute('''INSERT INTO CONFIG (LIBRARY, TYPE, CONFIG, ACTIVE) VALUES(?, ?, ?, ?);''', values)
    conn.commit()
    print(f"Inserted values into CONFIG table: {values}")

def test_data(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS TEST
              (ID INT PRIMARY KEY NOT NULL,
               IMAGE BLOB NOT NULL);''')
    print("Created TEST table successfully")

def insert_test(conn : Connection, values : tuple):
    conn.execute('''INSERT INTO TEST (ID, IMAGE) VALUES(?, ?);''', values)
    conn.commit()
    print(f"Inserted values into CONFIG table: ({values[0]},BLOB)")
