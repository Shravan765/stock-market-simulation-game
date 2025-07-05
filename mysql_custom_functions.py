import pymysql
import streamlit as st
import cryptography

conn = pymysql.connect(
    host=st.secrets["mysql"]["host"],
    port=st.secrets["mysql"]["port"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)

cursor = conn.cursor()

#DEFAULT CURRENT_TIMESTAMP helps in entering the time when the pnl was recorded
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaderboard_100_ticks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(100),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    PnL NUMERIC(10,2)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS leaderboard_300_ticks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(100),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    PnL NUMERIC(10,2)
)
""")

def insert_entry(player_name:str, PnL:float, tick_type:int):
    values = (player_name, PnL)
    if tick_type == 100:
        query = "INSERT INTO leaderboard_100_ticks (player_name, PnL) VALUES (%s, %s)"
        cursor.execute(query, values)
        conn.commit()
    elif tick_type == 300:
        query = "INSERT INTO leaderboard_300_ticks (player_name, PnL) VALUES (%s, %s)"
        cursor.execute(query, values)
        conn.commit()

def show_position_at_end(PnL:float , tick_type:int):
    values = (PnL,)
    if tick_type == 100:
        query = "SELECT count(*) FROM leaderboard_100_ticks WHERE PnL > %s"
        cursor.execute(query, values)
        output = cursor.fetchall()
        return output[0][0]+1
        
    elif tick_type == 300:
        query = "SELECT count(*) FROM leaderboard_300_ticks WHERE PnL > %s"
        cursor.execute(query, values)
        output = cursor.fetchall()
        return output[0][0]+1

def show_leaderboard_of_tick_100():
    cursor.execute("SELECT player_name, datetime, pnl FROM leaderboard_100_ticks ORDER BY PnL DESC")
    return cursor.fetchall()

def show_leaderboard_of_tick_300():
    cursor.execute("SELECT player_name, datetime, pnl FROM leaderboard_300_ticks ORDER BY PnL DESC")
    return cursor.fetchall()

def delete_oldest_entry_if_1000_entries_are_reached(tick_type:int):
    if(tick_type == 100):
        cursor.execute("DELETE FROM leaderboard_100_ticks ORDER BY datetime ASC LIMIT 1;")
        conn.commit()
    elif(tick_type == 300):
        cursor.execute("DELETE FROM leaderboard_300_ticks ORDER BY datetime ASC LIMIT 1;")
        conn.commit()

    