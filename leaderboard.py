import streamlit as st
import mysql_custom_functions
import pandas as pd
import pymysql

st.write("### ⭐ STOCK STAMPEDE! ⭐")
st.write("Leaderboard below!")
def show_entries(entries):
    df = pd.DataFrame(entries, columns=["player_name", "datetime", "PnL"])
    styled_df = df.style.background_gradient(
    cmap="RdYlGn", subset=["PnL"])
    st.dataframe(styled_df)

st.write("NOTE: Shows only the latest 1000 entries")

#st.write("DB Host:", st.secrets["mysql"]["host"])

if(st.checkbox(label ="### See 100 ticks leaderboard 🏆")): 
    try:
        entries = mysql_custom_functions.show_leaderboard_of_tick_100()
        show_entries(entries)
    except pymysql.err.InterfaceError:
        st.error("Database temporarily unavailable. Please try again.")

if(st.checkbox(label ="### See 300 ticks leaderboard 🏆")):
    try:
        entries = mysql_custom_functions.show_leaderboard_of_tick_300()
        show_entries(entries)
    except pymysql.err.InterfaceError:
        st.error("Database temporarily unavailable. Please try again.")
