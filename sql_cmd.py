from os.path import isfile
import sqlite3
from sqlite3 import Connection

def setup(custom_message=None):
    if isfile("animu.db") and not custom_message:
        message = "Database connection established"
    elif not custom_message:
        message = "(setup) Database setup successfully"
    else:
        message = custom_message
    conn = sqlite3.connect("animu.db")
    print(message)
    return conn

def create_data_table(conn : Connection):
    # SECTION 1: SHARED DATA
    # SECTION 2: MANGA  DATA
    # SECTION 3: ANIME  DATA
    # SECTION 4: UNIQUE DATA
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
               GENRE       TEXT             NOT NULL,
               SEARCH_TYPE TEXT             NOT NULL,
               JSON        TEXT             NOT NULL,
               IMAGE       BLOB             NOT NULL,

               PUBLISHING  TEXT                     ,
               CHAPTERS    TEXT                     ,
               VOLUMES     TEXT                     ,

               EPISODES    TEXT                     ,
               RATED       TEXT                     ,
               AIRING      TEXT                     ,

               LIBRARY     TEXT);''')
    print("(setup) Created DATA table successfully")

def insert_data(conn : Connection, values ):
    cur = conn.cursor()
    if values.search_type == "Anime":
        vals = (values.mal_id,
                values.animu,
                values.url,
                values.image_url,
                values.title,
                values.synopsis,
                values.type,
                values.score,
                values.start_date,
                values.end_date,
                values.members,
                values.genre,
                values.search_type,
                values.json,
                values.image,
                values.episodes,
                values.rated,
                values.airing,
                values.library)
        cmd = '''INSERT INTO DATA 
                (MAL_ID,
                 NAME,
                 URL,
                 IMAGE_URL,
                 TITLE,
                 SYNOPSIS,
                 TYPE,
                 SCORE,
                 START_DATE,
                 END_DATE,
                 MEMBERS,
                 GENRE,
                 SEARCH_TYPE,
                 JSON,
                 IMAGE,
                 EPISODES,
                 RATED,
                 AIRING,
                 LIBRARY) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(cmd, vals)
        conn.commit()
    
    if values.search_type == "Manga":
        vals = (values.mal_id,
                values.animu,
                values.url,
                values.image_url,
                values.title,
                values.synopsis,
                values.type,
                values.score,
                values.start_date,
                values.end_date,
                values.members,
                values.genre,
                values.search_type,
                values.json,
                values.image,
                values.publishing,
                values.chapters,
                values.volumes,
                values.library)

        cmd = '''INSERT INTO DATA 
                (MAL_ID,
                 NAME,
                 URL,
                 IMAGE_URL,
                 TITLE,
                 SYNOPSIS,
                 TYPE,
                 SCORE,
                 START_DATE,
                 END_DATE,
                 MEMBERS,
                 GENRE,
                 SEARCH_TYPE,
                 JSON,
                 IMAGE,
                 PUBLISHING,
                 CHAPTERS,
                 VOLUMES,
                 LIBRARY) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(cmd, vals)
        conn.commit()

def format(rows : list):
    library = []

    for row in rows:
        library.append({
            "mal_id":row[0],
            "animu":row[1],
            "url":row[2],
            "image_url":row[3],
            "title":row[4],
            "synopsis":row[5],
            "type":row[6],
            "score":row[7],
            "start_date":row[8],
            "end_date":row[9],
            "members":row[10],
            "genre":row[11],
            "search_type":row[12],
            "json":row[13],
            "image":row[14],
            "publishing":row[15],
            "chapters":row[16],
            "volumes":row[17],
            "episodes":row[18],
            "rated":row[19],
            "airing":row[20],
            "library":row[21]
            })
            
    return library

def load(conn : Connection, library_type : str, sort : int):
    cur = conn.cursor()
    if sort == 0:
        cmd = '''SELECT * FROM DATA WHERE LIBRARY=?'''
    if sort == 1:
        cmd = '''SELECT * FROM DATA WHERE LIBRARY=? ORDER BY NAME ASC'''
    if sort == 2:
        cmd = '''SELECT * FROM DATA WHERE LIBRARY=? ORDER BY TYPE ASC'''
    if sort == 3:
        cmd = '''SELECT * FROM DATA WHERE LIBRARY=? ORDER BY TYPE ASC, NAME ASC'''
    
    response = cur.execute(cmd, [library_type])
    library = response.fetchall()
    
    if library:
        library = format(library)
    
    return library

def check_exists(conn : Connection, mal_id : int):
    cur = conn.cursor()
    cmd = '''SELECT EXISTS(SELECT 1 FROM DATA WHERE MAL_ID=? LIMIT 1)'''
    response = cur.execute(cmd, [mal_id])
    exists = response.fetchone()

    return exists[0]

def delete(conn : Connection, mal_id : int):
    cur = conn.cursor()
    cmd = '''DELETE FROM DATA WHERE MAL_ID=?'''
    cur.execute(cmd, [mal_id])
    conn.commit()

def create_config_table(conn : Connection):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS CONFIG
              (LIBRARY    TEXT PRIMARY KEY NOT NULL,
               SORT       INT              NOT NULL,
               ACTIVE     INT);''')
    conn.commit()
    print("(setup) Created CONFIG table successfully")

def default_config(conn : Connection):
    print("(setup) Creating default config values")
    cur = conn.cursor()
    cmd = '''INSERT INTO CONFIG (LIBRARY, SORT, ACTIVE) VALUES(?, ?, ?);'''
    cur.execute(cmd, ("finished", 0, 1))
    cur.execute(cmd, ("unfinished", 0, 0))
    cur.execute(cmd, ("wishlist", 0, 0))
    conn.commit()
    print("(setup) Default config values created")

def active_config(conn : Connection):
    cur = conn.cursor()
    cur.execute("SELECT * FROM CONFIG WHERE ACTIVE=1")
    active = cur.fetchall()
    if active:
        active = list(active[0])
    return active

def set_config(conn : Connection, update : tuple, sort : bool):
    cur = conn.cursor()
    if sort:
        values = (next(update[1]), update[0])
        cur.execute('''UPDATE CONFIG SET SORT=? WHERE LIBRARY=?''', values)
    else:
        cur.execute('''UPDATE CONFIG SET ACTIVE = 0''')
        cur.execute('''UPDATE CONFIG SET ACTIVE = ? WHERE LIBRARY = ?''', (update[2], update[0]))
    conn.commit()

def get_configs(conn : Connection):
    cur = conn.cursor()
    cur.execute("SELECT * FROM CONFIG")
    rows = cur.fetchall()
    #rows = list(map(lambda row: list(row), rows))
    configs = {}
    for config in rows:
        config = list(config)
        sort_gen = sort_generator(initial=config[1])
        next(sort_gen) # Initialize generator
        config[1] = sort_gen # Set library sorting generator
        configs[config[0]] = config
    return configs

def sort_generator(initial=0):
        """Return current sort value, unless changing to next sort type, then increment sort value"""
        sort = initial
        change = False
        while True:
            if change:
                sort += 1
                if sort == 4:
                    sort = 0
            change = False
            change = yield sort
