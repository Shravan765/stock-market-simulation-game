import streamlit as st
from stock_player_class_library import Stock, Player
import mysql_custom_functions
import pandas as pd
import numpy as np
import streamlit_autorefresh
import pymysql

if("game_started" not in st.session_state):
    st.session_state.game_started = False

#0 => game ongoing
#-1 => game ended by user
#1 => game ended as per ticks 
if("game_ended" not in st.session_state):
        st.session_state.game_ended = 0 

if("end_at_tick" not in st.session_state):
    st.session_state.end_at_tick = 0
if("inserted" not in st.session_state):
    st.session_state.inserted  = False

if("player_name" not in st.session_state):
    st.session_state.player_name = ""
    
if(st.session_state.game_started == False):
    st.write("### ⭐ STOCK STAMPEDE! ⭐")
    player_name = st.text_input(label="How would you like to be called as ?", key="initialise_player_name")
    ticks_to_play = st.selectbox(label="Choose the duration of the game in TICKS (default selected is 100) : ", options=[100,300])
    st.write("##### Tips FYI")
    st.write("1. Ticks -> 100 ticks would correspond to around a minute")
    st.write("2. Placing orders -> Keep an eye on the position to ensure your buy got registered")
    st.write("3. Events -> Every 10 ticks, you'll get some flash news. React (or not react) to it smartly!")
    st.write("P.S : Even if you clicked buy/sell and it didn't register," \
            "Click again! And hence PLEASE keep an eye on the position")
    button_disabled = player_name.strip() == ""
    if(button_disabled):
        st.write("\n\n\n\n")
        st.write("Please enter a non empty name!")
    
    if(st.button("Start the game", disabled=button_disabled)):
        st.session_state.game_started = True
        st.session_state.player_name = player_name
        st.session_state.end_at_tick = ticks_to_play
        st.rerun() #prevents double clicking submit to start the game
        #st.rerun() re runs the scripts, but with the session state values unchanged

elif(st.session_state.game_ended == -1):
    st.write(f"#### Your final PnL `{st.session_state.player.show_PnL(st.session_state.stock.price)}`")
    st.write(f"Since you ended the game abruptly, your score will not be considered in the leaderboard\n")
    #add rank
    if(st.button(label="Replay", help="Start the game fresh again!", key="replay_game")):
        del st.session_state.game_started
        del st.session_state.player_name
        del st.session_state.stock
        del st.session_state.player
        del st.session_state.prices_list
        del st.session_state.ticks_list
        del st.session_state.tick
        del st.session_state.news_feed
        del st.session_state.news_action
        del st.session_state.news
        del st.session_state.game_ended
        del st.session_state.end_at_tick
        if "initialise_player_name" in st.session_state:
            del st.session_state.initialise_player_name
        st.rerun()

#ticks ended
elif(st.session_state.game_ended == 1):
    st.write("### You never gave up and completed the game!")
    st.balloons()
    st.write(f"##### Duration selected : `{st.session_state.end_at_tick} ticks` ")
    st.write(f"#### Your final PnL `{st.session_state.player.show_PnL(st.session_state.stock.price)}`")
    try:
        #checking before inserting the size
        if(st.session_state.end_at_tick == 100):
            st.write("loading...")
            entries = mysql_custom_functions.show_leaderboard_of_tick_100()
            st.write("loading...")
            if(len(entries) > 1000):
                mysql_custom_functions.delete_oldest_entry_if_1000_entries_are_reached(100)
        elif(st.session_state.end_at_tick == 300):
            entries = mysql_custom_functions.show_leaderboard_of_tick_300()
            if(len(entries) > 1000):
                mysql_custom_functions.delete_oldest_entry_if_1000_entries_are_reached(300)
        if st.session_state.inserted == False:
            mysql_custom_functions.insert_entry(st.session_state.player_name,
                                                st.session_state.player.show_PnL(st.session_state.stock.price),
                                                st.session_state.end_at_tick)
            st.session_state.inserted = True
        position = mysql_custom_functions.show_position_at_end(st.session_state.player.show_PnL(st.session_state.stock.price),
                                            st.session_state.end_at_tick)
        st.write(f"#### Your final Position `{position}`")
        st.write(f"Caveat : this position indicates {position-1} players did better than you right now")
    except pymysql.err.InterfaceError:
        st.error("Database temporarily unavailable. Please try again.")

    if(st.button(label="Replay", help="Start the game fresh again!", key="replay_game")):
        del st.session_state.game_started
        del st.session_state.player_name
        del st.session_state.stock
        del st.session_state.player
        del st.session_state.prices_list
        del st.session_state.ticks_list
        del st.session_state.tick
        del st.session_state.news_feed
        del st.session_state.news_action
        del st.session_state.news
        del st.session_state.game_ended
        del st.session_state.end_at_tick
        if "initialise_player_name" in st.session_state:
            del st.session_state.initialise_player_name
        st.rerun()

else:
    if("stock" not in st.session_state):
        st.session_state.stock = Stock()
    if("player" not in st.session_state):
        st.session_state.player = Player()
    if("prices_list" not in st.session_state):    
        st.session_state.prices_list = [st.session_state.stock.price]
    if("tick" not in st.session_state):
        st.session_state.tick = 0
    if("ticks_list" not in st.session_state):
        st.session_state.ticks_list = [0,]
    if("news_feed" not in st.session_state):
        temp_df = pd.read_csv("newsfeed.csv", encoding="utf-8")
        st.session_state.news_feed = temp_df[["news", "change"]].values.tolist()
    if("news_action" not in st.session_state):
        st.session_state.news_action = 0
        #basically will tell percentage change, unless its greater than 100, 
        # in which case we have to increase volatility by news_action-100
    if("news" not in st.session_state):
        st.session_state.news = "None"

    if(st.session_state.end_at_tick <= st.session_state.tick):
        st.session_state.game_ended = 1
        st.rerun()
    
    col1, col2, col3 = st.columns([1,6,1])
    st.write(f"🔔 Ticks remaining : `{st.session_state.end_at_tick - st.session_state.tick}`")
    with col2:
        if(st.session_state.tick%2 == 0):
            if(st.session_state.news_action == 0):
                st.session_state.stock.fluctuate_from_current_normal(1)
            elif(st.session_state.news_action > 100):
                st.session_state.stock.fluctuate_from_current_random(st.session_state.news_action-100)
                #not percentage change, but signal to raise volatility
            else:
                price_aimed = st.session_state.stock.price*(1 + st.session_state.news_action/100)
                st.session_state.stock.fluctuate_with_direction(price_aimed, 1)
            st.session_state.prices_list.append(st.session_state.stock.price)
            st.session_state.ticks_list.append(st.session_state.tick)

        col21, col22, col23 = st.columns([1,1,1])
        with col22:
            st.write(f"##### Maximise your profit `{st.session_state.player_name}`!")
            st.write(f"##### PnL `{st.session_state.player.show_PnL(st.session_state.stock.price)}`")
            st.write(f"##### Net Position `{round(st.session_state.player.net_position , 2)}`")
            st.write(f"\n\n Current Price : `{round(st.session_state.stock.price, 2)}`")
    
    st.write("\n\n")
    
    if(st.session_state.tick%10 == 0):
        news_chosen = st.session_state.news_feed[np.random.randint(low=0, high= len(st.session_state.news_feed))]
        st.session_state.news = news_chosen[0]
        st.session_state.news_action = news_chosen[1]
    st.write("##### Current News : ", st.session_state.news)
    st.write("\n\n\n\n")
    
    df = pd.DataFrame({"Price" : st.session_state.prices_list} , index=st.session_state.ticks_list)
    st.line_chart(df)
    col_new_1 , col_new_2, col_new_3 = st.columns([1,1,1])
    with col_new_1:
        if(st.button("🟩 Buy", help="Buy 1 unit of stock at market price",type="primary") == True):
            st.session_state.player.buy(st.session_state.stock.price)         
            
    with col_new_3:
        if(st.button("🟥 Sell", help="Sell 1 unit of stock at market price", type="primary") == True):
            st.session_state.player.sell(st.session_state.stock.price)
            
    st.write("\n\n\n\n\n\n\n\n")
    col21, col22, col23 = st.columns([1,1,1])
    with col22:
        if(st.button(label = "End Game", help="Ends the game prematurely (your score won't be counted in the leaderboard)", key="end_game")):
            st.session_state.game_ended = -1
            st.rerun()
    
    st.session_state.tick+=1
    streamlit_autorefresh.st_autorefresh(interval=700, key="auto_refresh")
    



