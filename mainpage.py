import streamlit as st

game = st.Page(page="stock_market_sim.py", title="Start Stock Sampede??", icon="📊")
leaderboard = st.Page(page="leaderboard.py", title="Leaderboard", icon="🏆")

pg = st.navigation([game, leaderboard])
pg.run()
