import os
import pandas as pd
from sqlalchemy import create_engine, text

# MySQL connection config
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'ipl_historical_data'

# Excel files
BASE_DIR = "C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/historical_data"
MATCHES_XLSX = os.path.join(BASE_DIR, "./Dataset/ipl_ball_by_ball_2008_2025.xlsx")
BALLS_XLSX = os.path.join(BASE_DIR, "./Dataset/ipl_matches_2008_2025.xlsx")

# Load Excel files
df_matches = pd.read_excel(MATCHES_XLSX)
df_balls = pd.read_excel(BALLS_XLSX)

# Rename column for typo consistency
df_balls.rename(columns={'non_boundary': 'non_boundry'}, inplace=True)

# Connect to MySQL
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

with engine.connect() as conn:
    # Create matches table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ipl_matches_2008_2025 (
            id BIGINT PRIMARY KEY,
            city VARCHAR(50),
            match_date DATE,
            season VARCHAR(50),
            match_number VARCHAR(50),
            team1 VARCHAR(50),
            team2 VARCHAR(50),
            venue VARCHAR(100),
            toss_winner VARCHAR(50),
            toss_decision VARCHAR(50),
            superover VARCHAR(50),
            winning_team VARCHAR(50),
            won_by VARCHAR(50),
            margin VARCHAR(50),
            method VARCHAR(50),
            player_of_match VARCHAR(50),
            umpire1 VARCHAR(50),
            umpire2 VARCHAR(50)
        );
    """))

    # Create ball-by-ball table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ipl_ball_by_ball_2008_2025 (
            id BIGINT NOT NULL,
            innings BIGINT,
            overs BIGINT,
            ball_number BIGINT,
            batter VARCHAR(50),
            bowler VARCHAR(50),
            non_striker VARCHAR(50),
            extra_type VARCHAR(50),
            batsman_run BIGINT,
            extras_run BIGINT,
            total_run BIGINT,
            non_boundry BIGINT,
            iswicket_delivery BIGINT,
            player_out VARCHAR(50),
            dismisal_kind VARCHAR(50),
            fielders_involved VARCHAR(50),
            batting_team VARCHAR(50)
        );
    """))

# Insert data into tables
df_matches.to_sql(name='ipl_matches_2008_2025', con=engine, if_exists='replace', index=False)
df_balls.to_sql(name='ipl_ball_by_ball_2008_2025', con=engine, if_exists='replace', index=False)

print("Data inserted into MySQL database successfully.")
