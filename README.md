# Sparkify Music App: Apache Cassandra Data Modeling Project

This project demonstrates how to model a NoSQL database using **Apache Cassandra** to support specific analytical queries for a fictional music streaming app called **Sparkify**. The focus is on applying Cassandra's query-driven data modeling principles, designing denormalized tables, and running queries using real-world event data.

---

## 📁 Project Structure

```
Sparkify/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── sparkify_etl.py
├── event_datafile_new.csv
└── app/
    └── sparkify_etl.py (same as above)
```

---

## 🚀 How to Run the Project Using Docker

> ⚠️ Make sure you have Docker Desktop installed and running on your machine.

### 1. Navigate to the project root directory:

```bash
cd path/to/Sparkify
```

### 2. Run the following command to build and launch the containers:

```bash
docker compose up --build
```

This command:

* Spins up a **Cassandra** database container.
* Runs the `sparkify_etl.py` script inside a Python container.
* Automatically populates the Cassandra database and executes 3 analytical queries.

Once complete, the container logs will show the output for:

* ✅ Data ingestion
* ✅ Query results
* ✅ Table cleanup

---

## 🧠 What the ETL Script Does (`sparkify_etl.py`)

1. **Connects to Cassandra** (container hostname: `cassandra`).

2. **Creates a keyspace** named `sparkify`.

3. **Defines and populates 3 tables** for 3 analytical queries:

   ### Query 1: Song Session Lookup

   * **Question:** Give me the artist, song title, and song's length during `sessionId = 338` and `itemInSession = 4`
   * **Primary Key:** `(sessionId, itemInSession)`

   ### Query 2: User Session Playlist

   * **Question:** Give me artist, song, and user name (first & last) for `userId = 10` and `sessionId = 182` sorted by `itemInSession`
   * **Primary Key:** `((userId, sessionId), itemInSession)`

   ### Query 3: Song Listeners

   * **Question:** Give me every user's name (first & last) who listened to the song `'All Hands Against His Own'`
   * **Primary Key:** `(song, userId)`

4. **Performs SELECT queries** and prints results.

5. **Drops all tables** and shuts down the Cassandra session.

---

## 📦 Dependencies

The Docker container installs the following Python packages:

```txt
cassandra-driver
pandas
```

All dependencies are listed in `requirements.txt`.

---

## ✅ Success Criteria

* Efficient use of **Cassandra primary keys**.
* Queries return exact expected output.
* Full automation inside Docker.
* Tables are cleaned up after run.

---

## 💡 Why This Project Matters

This project simulates a real-world scenario where:

* Data is queried in a specific way (query-first design).
* Denormalization is not optional—it's necessary.
* You optimize for **read efficiency** and **partition design**.

It’s a great demonstration of applied NoSQL design thinking and distributed data engineering in action.

---

## 🧰 Useful Docker Commands

```bash
# View running containers
docker ps

# Stop containers
docker compose down

# Rebuild and rerun
docker compose up --build

# Clean up dangling resources
docker system prune -a
```

---

## 🙌 Credits

Built as part of Udacity's Data Engineering Nanodegree.

Created by Kareem Rizk
AWS Certified | Cloud & Data Engineer | DevOps Enthusiast
