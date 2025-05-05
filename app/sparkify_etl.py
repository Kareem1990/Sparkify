# Required package:
# pip install cassandra-driver
# Import Python packages 

import time
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
import csv
import pandas as pd
from cassandra.cluster import Cluster

# -----------------------------------
# STEP 1: Connect to Cassandra
# -----------------------------------
# انتظر شوية عشان Cassandra تكون اشتغلت
print("⏳ Waiting for Cassandra to be ready...")
time.sleep(20)

# إعداد الاتصال
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "cassandra")

try:
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect()
    print("✅ Connected to Cassandra cluster.")
except Exception as e:
    print(f"❌ Connection to Cassandra at {CASSANDRA_HOST} failed:", e)
    exit(1)
# -----------------------------------
# STEP 2: Create and set keyspace
# -----------------------------------
try:
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS sparkify
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
    """)
    session.set_keyspace('sparkify')
    print("✅ Keyspace 'sparkify' created and set.")
except Exception as e:
    print("❌ Keyspace error:", e)

# -----------------------------------
# STEP 3: Helper and CSV file setup
# -----------------------------------
csv_file = 'event_datafile_new.csv'

def is_valid_line(line):
    return len(line) >= 11 and line[0] != ''

# -----------------------------------
# STEP 4: Table 1 - song_session_library
# Query: artist, song, length WHERE sessionId=338 AND itemInSession=4
# -----------------------------------
query = """
CREATE TABLE IF NOT EXISTS song_session_library (
    sessionId int,
    itemInSession int,
    artist text,
    song text,
    length float,
    PRIMARY KEY (sessionId, itemInSession)
)
"""
session.execute(query)

with open(csv_file, encoding='utf8') as f:
    reader = csv.reader(f)
    next(reader)
    for line in reader:
        if not is_valid_line(line): continue
        session.execute("""
            INSERT INTO song_session_library (sessionId, itemInSession, artist, song, length)
            VALUES (%s, %s, %s, %s, %s)
        """, (int(line[8]), int(line[3]), line[0], line[9], float(line[5])))

# -----------------------------------
# STEP 5: Table 2 - user_session_library
# Query: artist, song, firstName, lastName WHERE userId=10 AND sessionId=182 ORDER BY itemInSession
# -----------------------------------
query = """
CREATE TABLE IF NOT EXISTS user_session_library (
    userId int,
    sessionId int,
    itemInSession int,
    artist text,
    song text,
    firstName text,
    lastName text,
    PRIMARY KEY ((userId, sessionId), itemInSession)
)
"""
session.execute(query)

with open(csv_file, encoding='utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader)
    for line in csvreader:
        if not is_valid_line(line):
            continue
        query = """
        INSERT INTO user_session_library 
        (userId, sessionId, itemInSession, artist, song, firstName, lastName)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        session.execute(query, (
            int(line[10]),   # userId
            int(line[8]),    # sessionId
            int(line[3]),    # itemInSession
            line[0],         # artist
            line[9],         # song
            line[1],         # firstName
            line[4]          # lastName
        ))

# -----------------------------------
# STEP 6: Table 3 - song_user_library
# Query: firstName, lastName WHERE song='All Hands Against His Own'
# -----------------------------------
query = """
CREATE TABLE IF NOT EXISTS song_user_library (
    song text,
    userId int,
    firstName text,
    lastName text,
    PRIMARY KEY (song, userId)
)
"""
session.execute(query)

with open(csv_file, encoding='utf8') as f:
    reader = csv.reader(f)
    next(reader)
    for line in reader:
        if not is_valid_line(line): continue
        session.execute("""
            INSERT INTO song_user_library (song, userId, firstName, lastName)
            VALUES (%s, %s, %s, %s)
        """, (line[9], int(line[10]), line[1], line[4]))

# -----------------------------------
# STEP 7: Sample SELECT Queries
# -----------------------------------
print("\n🎵 Sample Queries Output:\n")

# Query 1
rows = session.execute("""
    SELECT artist, song, length 
    FROM song_session_library 
    WHERE sessionId = 338 AND itemInSession = 4
""")
# for row in rows:
#     print("[Q1]", row.artist, row.song, row.length)

# Query 2
rows = session.execute("""
    SELECT artist, song, firstName, lastName 
    FROM user_session_library 
    WHERE userId = 10 AND sessionId = 182
    ORDER BY itemInSession
""")
for row in rows:
    print("[Q2]", row.artist, row.song, row.firstname, row.lastname)

# Query 3
rows = session.execute("""
    SELECT firstName, lastName 
    FROM song_user_library 
    WHERE song = 'All Hands Against His Own'
""")
for row in rows:
    print("[Q3]", row.firstname, row.lastname)

# -----------------------------------
# STEP 8: Clean up tables
# -----------------------------------
for tbl in ["song_session_library", "user_session_library", "song_user_library"]:
    session.execute(f"DROP TABLE IF EXISTS {tbl}")
    print(f"🧹 Dropped table: {tbl}")

# -----------------------------------
# STEP 9: Shutdown session
# -----------------------------------
session.shutdown()
cluster.shutdown()
print("👋 Cassandra session closed.")
