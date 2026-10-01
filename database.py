import sqlite3
import json



def connect():

    return sqlite3.connect(
        "forensic.db"
    )



def create_table():

    db = connect()

    cursor = db.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS result(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        data TEXT

    )
    """)


    db.commit()

    db.close()



def save_result(filename,data):

    db = connect()

    cursor = db.cursor()


    cursor.execute(
        """
        INSERT INTO result
        (filename,data)

        VALUES (?,?)
        """,

        (
            filename,
            json.dumps(data)
        )
    )


    db.commit()

    db.close()



create_table()