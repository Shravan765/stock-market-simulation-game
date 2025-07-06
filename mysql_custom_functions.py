import pymysql
import streamlit as st
import cryptography

def get_connection():
    return pymysql.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
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
    conn.commit()
    cursor.close()
    conn.close()

def insert_entry(player_name:str, PnL:float, tick_type:int):
    conn = get_connection()
    cursor = conn.cursor()
    values = (player_name, PnL)
    if tick_type == 100:
        query = "INSERT INTO leaderboard_100_ticks (player_name, PnL) VALUES (%s, %s)"
    else:
        query = "INSERT INTO leaderboard_300_ticks (player_name, PnL) VALUES (%s, %s)"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

def show_position_at_end(PnL:float, tick_type:int):
    st.write("Showing position")
    conn = get_connection()
    cursor = conn.cursor()
    values = (PnL,)
    if tick_type == 100:
        query = "SELECT count(*) FROM leaderboard_100_ticks WHERE PnL > %s"
    else:
        query = "SELECT count(*) FROM leaderboard_300_ticks WHERE PnL > %s"
    st.write("Showing position 2")
    cursor.execute(query, values)
    st.write("Showing position 3")
    output = cursor.fetchone()
    cursor.close()
    conn.close()
    return output[0] + 1

def show_leaderboard_of_tick_100():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, datetime, pnl FROM leaderboard_100_ticks ORDER BY PnL DESC")
    output = cursor.fetchall()
    cursor.close()
    conn.close()
    return output

def show_leaderboard_of_tick_300():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, datetime, pnl FROM leaderboard_300_ticks ORDER BY PnL DESC")
    output = cursor.fetchall()
    cursor.close()
    conn.close()
    return output

def delete_oldest_entry_if_1000_entries_are_reached(tick_type:int):
    conn = get_connection()
    cursor = conn.cursor()
    if tick_type == 100:
        query = "DELETE FROM leaderboard_100_ticks ORDER BY datetime ASC LIMIT 1;"
    else:
        query = "DELETE FROM leaderboard_300_ticks ORDER BY datetime ASC LIMIT 1;"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    
