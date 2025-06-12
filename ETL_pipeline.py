import requests

from sqlalchemy import create_engine

# Replace these with your actual MySQL credentials
user = "root"
password = "root"
host = "localhost"
port = "3306"
database = "ipl_live_data"

# SQLAlchemy engine (using pymysql as driver)
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

def upload_table(df, table_name):
    try:
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"✅ '{table_name}' uploaded successfully with {len(df)} rows.")
    except Exception as e:
        print(f"❌ Failed to upload '{table_name}': {e}")


#### Base API Call from cricbuzz-cricket.p.rapidapi.com ####

import requests

# Base API Match list

# Define the API URL and headers
api_url = "https://cricbuzz-cricket.p.rapidapi.com/series/v1/9237"
headers = {
    "X-RapidAPI-Key": "61d311baf4msh4fd1dcdeb3d4427p121b42jsnd5a9e5a48a9c",  # Replace with your key
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

# Make the GET request
Base_API_Matches_List = requests.get(api_url, headers=headers)

# Check for successful Base_API_Matches_List
if Base_API_Matches_List.status_code == 200:
    # Parse and print the JSON Base_API_Matches_List
    Base_API_Matches_List = Base_API_Matches_List.json()
    # print(Base_API_Matches_List)
    print("Base_API_Matches_List DF created from  API")
else:
    print(f"Error: {Base_API_Matches_List.status_code} - {Base_API_Matches_List.text}")


#### Extracting match list from Base_API_Matches_List and saving it in Match_List df ####
import pandas as pd

# Step 1: Parse JSON from existing response
data = Base_API_Matches_List

# Step 2: Extract and flatten matchDetails
match_details = data.get("matchDetails", [])

records = []
for item in match_details:
    match_detail_map = item.get("matchDetailsMap", {})
    date_key = match_detail_map.get("key")
    matches = match_detail_map.get("match", [])
    
    for match in matches:
        match_info = match.get("matchInfo", {})
        match_score = match.get("matchScore", {})
        team1 = match_info.get("team1", {})
        team2 = match_info.get("team2", {})

        # Skip if date is null (mimicking Power Query filter)
        if date_key is None:
            continue

        # Build flattened record
        record = {
            "Date": date_key,
            "MatchID": match_info.get("matchId"),
            "SeriesId": match_info.get("seriesId"),
            "Match_Number": match_info.get("matchDesc"),
            "State": match_info.get("state"),
            "Status": match_info.get("status"),
            "TeamId_1": team1.get("teamId"),
            "TeamName_1": team1.get("teamName"),
            "TeamSName_1": team1.get("teamSName"),
            "TeamId_2": team2.get("teamId"),
            "TeamName": team2.get("teamName"),
            "TeamSName_2": team2.get("teamSName")
        }
        records.append(record)

# Step 3: Create DataFrame
Match_List = pd.DataFrame(records)

# Step 4: Convert 'Date' to datetime
Match_List["Date"] = pd.to_datetime(Match_List["Date"], errors='coerce')

# Step 5: Create 'Match_Number (Filter)' by extracting digits
Match_List["Match_Number (Filter)"] = Match_List["Match_Number"].str.extract(r"(\d+)")

# Final cleaned DataFrame: Match_List
print("Match_List DF Created from API")


#### Calling another api for Points Table ####
import requests
import pandas as pd

api_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/series/9237/points-table"
headers = {
    "X-RapidAPI-Key": "61d311baf4msh4fd1dcdeb3d4427p121b42jsnd5a9e5a48a9c",  # Replace this with your actual API key
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

table_api_data = requests.get(api_url, headers=headers)
table_api_data = table_api_data.json()

# print(table_api_data)


#### Loading team logo data from Excel ####
logo_path = r"C:\Users\Admin\Desktop\End-to-End IPL Analysis Dashboard and Live Insights\Team_Logo.xlsx"
Team_logo = pd.read_excel(logo_path)

#### Loading cleaned preproced team info data from CSV ####
info_path = r"C:\Users\Admin\Desktop\End-to-End IPL Analysis Dashboard and Live Insights\Cleaned_IPL_Player_Summary_With_Img.csv"
Team_Info = pd.read_csv(info_path)


#### Creating Points Table ####
points_table = table_api_data["pointsTable"]
records = []
for entry in points_table:
    team_info = entry.get("pointsTableInfo", [])
    records.extend(team_info)

df_api = pd.DataFrame(records)

df_api = df_api.rename(columns={
    "teamId": "TeamId",
    "teamName": "TeamName",
    "matchesPlayed": "matchesPlayed",
    "matchesWon": "matchesWon",
    "points": "points",
    "nrr": "Net Run Rate",
    "teamFullName": "TeamFullName"
})



# Remove extra spaces in 'Team' column just in case
Team_logo["Team"] = Team_logo["Team"].str.strip()
# print("Team logo from excel")
# print(Team_logo)

# Step 5: Merge both DataFrames
df_merged = df_api.merge(Team_logo, how="left", left_on="TeamFullName", right_on="Team")

# Step 6: Convert data types
df_merged[["matchesPlayed", "matchesWon", "points"]] = df_merged[["matchesPlayed", "matchesWon", "points"]].astype(int)

Table_Points = df_merged

# Step 7: Optional – Preview or save to Excel
# print(df_merged.head())
print("Table_Points DF Created From API")


#### Making API call for Live Score card ####


# Step 1: Select MatchID where State is "Live", else fallback to "Preview"

# def get_live_or_preview_match_id(match_list_df):
#     live_matches = match_list_df[match_list_df["Status"] == "In Progress"]
#     if not live_matches.empty:
#         return str(live_matches.iloc[0]["match_id"])
    
#     preview_matches = match_list_df[match_list_df["Status"] == "Preview"]
#     if not preview_matches.empty:
#         return str(preview_matches.iloc[0]["match_id"])
    
#     return None

def fetch_match_data(match_id, data_type):
    import requests

    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/{data_type}"
    headers = {
        "x-rapidapi-key": "61d311baf4msh4fd1dcdeb3d4427p121b42jsnd5a9e5a48a9c",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    return response.json()

# if match_id:
    # Base_API_Iive_Score = fetch_match_data(match_id, endpoint)
    # print(f"Fetched match data for Match ID: {match_id}")

# Example usage:
Base_API_Iive_Score = fetch_match_data("118928", "hscard")
print(f"Fetched match data for Match ID: {118928}")
# print(Base_API_Iive_Score)


#### Extracting Live_Team_Score from Base_API_Iive_Score ####
import pandas as pd

# Extract innings list from nested 'scoreCard'
innings_list = Base_API_Iive_Score.get("scoreCard", [])

# Build DataFrame
rows = []
for inn in innings_list:
    bat = inn.get("batTeamDetails", {})
    row = {
        "MatchId": Base_API_Iive_Score.get("matchId", None),
        "inningsId": inn.get("inningsId"),
        "batTeamName": bat.get("batTeamName"),
        "batTeamSName": bat.get("batTeamSName"),
        "runs": int(bat.get("score", 0)),
        "wickets": int(bat.get("wickets", 0)),
        "overs": float(bat.get("overs", 0)),
        "runRate": float(bat.get("runRate", 0)),
        "ballNbr": int(bat.get("ballNbr", 0)),
        "runsPerBall": round(float(bat.get("rpb", 0)) * 6) if bat.get("rpb") is not None else None
    }
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Load team logos
team_logo_df = pd.read_excel(r"C:\Users\Admin\Desktop\End-to-End IPL Analysis Dashboard and Live Insights\Team_Logo.xlsx")
# print(f" Load team logos \n {team_logo_df}")

# Merge logos
df = df.merge(team_logo_df[['Team', 'Logo', 'Captain Images']], how='left',
              left_on='batTeamName', right_on='Team').rename(columns={
    'Logo': 'Bat_Team_Logo',
    'Captain Images': 'Bat_Team_Captain'
}).drop(columns=['Team'])

# Set Batting Team label based on innings
df['Batting Team'] = df.apply(lambda x: x['batTeamName'] if x['inningsId'] == 1 else "Opponent Team", axis=1)

# Add formatted score
df['Current-Score'] = df.apply(lambda x: f"{x['runs']}/{x['wickets']} ({x['overs']})", axis=1)

# Final DataFrame
Live_Team_Score = df

print("Live_Team_Score DF Created From API")



#### Extracting Live_Batsman_Score from Base_API_Iive_Score ####
import pandas as pd

# Step 1: Extract innings
scoreCard = Base_API_Iive_Score.get("scoreCard", [])

# Step 2: Process batsmen
expanded_rows = []
for inn in scoreCard:
    bat_team = inn.get('batTeamDetails', {})
    bat_team_id = bat_team.get('batTeamId')
    bat_team_name = bat_team.get('batTeamName')
    bat_team_short_name = bat_team.get('batTeamShortName')
    match_id = inn.get('matchId')
    innings_id = inn.get('inningsId')
    batsmen_data = bat_team.get('batsmenData', {})
    
    for key, batsman in batsmen_data.items():
        batsman = batsman.copy()
        batsman['Order'] = key.replace('bat_', 'batsman_')
        batsman['MatchID'] = match_id
        batsman['inningsId'] = innings_id
        batsman['batTeamId'] = bat_team_id
        batsman['batTeamName'] = bat_team_name
        batsman['batTeamShortName'] = bat_team_short_name
        expanded_rows.append(batsman)

# Step 3: Convert to DataFrame
batsmen_df = pd.DataFrame(expanded_rows)

# Step 4: Standardize and clean
batsmen_df.rename(columns={
    'batId': 'batId',
    'batName': 'batName',
    'batShortName': 'batShortName',
    'isCaptain': 'isCaptain',
    'runs': 'runs',
    'balls': 'balls',
    'dots': 'dots',
    'fours': 'fours',
    'sixes': 'sixes',
    'mins': 'mins',
    'strikeRate': 'strikeRate',
    'outDesc': 'Status',
    'bowlerId': 'bowlerId',
    'ones': 'ones',
    'twos': 'twos',
    'threes': 'threes',
    'fives': 'fives',
    'boundaries': 'boundaries',
    'sixers': 'sixers'
}, inplace=True)

# Step 5: Fill missing columns
expected_cols = ['sixers', 'boundaries', 'fives', 'threes', 'twos', 'ones', 'mins', 'sixes', 'fours', 'dots', 'balls', 'runs']
for col in expected_cols:
    if col not in batsmen_df.columns:
        batsmen_df[col] = 0

# Step 6: Type conversions
batsmen_df[expected_cols] = batsmen_df[expected_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
batsmen_df['strikeRate'] = pd.to_numeric(batsmen_df['strikeRate'], errors='coerce').fillna(0).astype(float)
batsmen_df['inningsId'] = batsmen_df['inningsId'].astype(int)

# Step 7: Merge external data
players_info_df = pd.read_csv(r"C:\Users\Admin\Desktop\End-to-End IPL Analysis Dashboard and Live Insights\Cleaned_IPL_Player_Summary_With_Img.csv")
team_logo_df = pd.read_excel(r"C:\Users\Admin\Desktop\End-to-End IPL Analysis Dashboard and Live Insights\Team_Logo.xlsx")

batsmen_df = batsmen_df.merge(players_info_df[['player', 'Image']], how='left', left_on='batName', right_on='player').drop(columns='player')
default_img = "https://i.postimg.cc/vmWdWzRy/soccer-player.png"
batsmen_df['Image'] = batsmen_df['Image'].replace("https://wassets.hscicdn.com/static/images/player-jersey.svg", default_img)
batsmen_df['Image'] = batsmen_df['Image'].fillna(default_img)

batsmen_df = batsmen_df.merge(team_logo_df[['Team', 'Logo']], how='left', left_on='batTeamName', right_on='Team').rename(columns={'Logo': 'Bat_Logo'}).drop(columns='Team')

# Final Output
Live_Batsman_Score = batsmen_df

print("Live_Batsman_Score DF Created from API")

#### Extracting Live_Bowler_Score from Base_API_Iive_Score ####
import pandas as pd

# Step 1: Get the raw innings list from the API
scoreCard = Base_API_Iive_Score.get("scoreCard", [])

# Step 2: Manually parse each innings
expanded_rows = []

for inn in scoreCard:
    bowl_team = inn.get('bowlTeamDetails', {})
    bowl_team_id = bowl_team.get('bowlTeamId')
    bowl_team_name = bowl_team.get('bowlTeamName')
    bowl_team_short_name = bowl_team.get('bowlTeamShortName')
    match_id = inn.get('matchId')
    innings_id = inn.get('inningsId')
    bowlers_data = bowl_team.get('bowlersData', {})

    for key, bowler in bowlers_data.items():
        row = bowler.copy()
        row["Order"] = key.replace("bowl_", "bowler_")
        row["MatchId"] = match_id
        row["inningsId"] = innings_id
        row["bowlTeamId"] = bowl_team_id
        row["bowlTeamName"] = bowl_team_name
        row["bowlTeamShortName"] = bowl_team_short_name
        expanded_rows.append(row)

# Step 3: Create DataFrame from list
bowlers_df = pd.DataFrame(expanded_rows)

# Step 4: Clean and rename columns
bowlers_df.rename(columns={
    'bowlerId': 'bowlerId',
    'bowlName': 'bowlName',
    'bowlShortName': 'bowlShortName',
    'isCaptain': 'isCaptain',
    'overs': 'overs',
    'maidens': 'maidens',
    'runs': 'runs',
    'wickets': 'wickets',
    'economy': 'economy',
    'no_balls': 'no_balls',
    'wides': 'wides',
    'dots': 'dots',
    'balls': 'balls',
    'runsPerBall': 'runsPerBall'
}, inplace=True)

# Step 5: Ensure all expected numeric columns exist
expected_cols = ['overs', 'maidens', 'runs', 'wickets', 'economy', 'no_balls', 'wides', 'dots', 'balls', 'runsPerBall']
for col in expected_cols:
    if col not in bowlers_df.columns:
        bowlers_df[col] = 0

# Step 6: Type conversion
bowlers_df[expected_cols] = bowlers_df[expected_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
bowlers_df['inningsId'] = bowlers_df['inningsId'].astype(int)

# Step 7: Merge player and team images
players_info_df = pd.read_csv(r"C:\Users\Admin\Desktop\End-to-End IPL Analysis Dashboard and Live Insights\Cleaned_IPL_Player_Summary_With_Img.csv")
team_logo_df = pd.read_excel(r"C:\Users\Admin\Desktop\End-to-End IPL Analysis Dashboard and Live Insights\Team_Logo.xlsx")

# Merge player images
bowlers_df = bowlers_df.merge(players_info_df[['player', 'Image']], how='left', left_on='bowlName', right_on='player').drop(columns='player')

# Default image handling
default_img = "https://i.postimg.cc/vmWdWzRy/soccer-player.png"
bowlers_df['Image'] = bowlers_df['Image'].replace("https://wassets.hscicdn.com/static/images/player-jersey.svg", default_img)
bowlers_df['Image'] = bowlers_df['Image'].fillna(default_img)

# Merge team logos
bowlers_df = bowlers_df.merge(team_logo_df[['Team', 'Logo']], how='left', left_on='bowlTeamName', right_on='Team').rename(columns={'Logo': 'Bowl_Team'}).drop(columns='Team')

Live_Bowler_Score = bowlers_df

print("Live_Bowler_Score DF Created from API")

#### Extracting Live_Toss_info from Base_API_Iive_Score ####
import pandas as pd

# Step 1: Access the base object
Source = Base_API_Iive_Score

# Step 2: Navigate to matchHeader
matchHeader = Source.get("matchHeader", {})

# Step 3: Extract tossResults
tossResults = matchHeader.get("tossResults", {})

# Step 4: Convert tossResults dictionary to a DataFrame
Live_Toss_Info = pd.DataFrame(list(tossResults.items()), columns=["Field", "Value"])

print("Live_Toss_Info DF Created from API")


def upload_table(df, table_name):
    try:
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"✅ '{table_name}' uploaded successfully with {len(df)} rows.")
    except Exception as e:
        print(f"❌ Failed to upload '{table_name}': {e}")

# Upload all tables with status
upload_table(Match_List, "match_list")
upload_table(Team_logo, "team_logo")
upload_table(Team_Info, "team_info")
for col in Table_Points.columns:
    Table_Points[col] = Table_Points[col].apply(lambda x: str(x) if isinstance(x, (list, dict)) else x)
upload_table(Table_Points, "table_points")
upload_table(Live_Team_Score, "live_team_score")
upload_table(Live_Batsman_Score, "live_batsman_score")
upload_table(Live_Bowler_Score, "live_bowler_score")
upload_table(Live_Toss_Info, "live_toss_info")

Match_List = pd.DataFrame(Match_List)
Match_List.to_excel('C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/Live Data Excel/Match_List.xlsx', index=False)
# print(Team_logo)
Team_logo = pd.DataFrame(Team_logo)
Team_logo.to_excel('C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/Live Data Excel/Team_logo.xlsx', index=False)
Team_Info = pd.DataFrame(Team_Info)
Team_Info.to_excel('C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/Live Data Excel/Player_Info.xlsx', index=False)
Table_Points = pd.DataFrame(df_merged)
Table_Points.to_excel('C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/Live Data Excel/Table_Points.xlsx', index=False)
Live_Team_Score = pd.DataFrame(Live_Team_Score)
Live_Team_Score.to_excel('C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/Live Data Excel/Live_Team_Score.xlsx', index=False)
Live_Batsman_Score = pd.DataFrame(Live_Batsman_Score)
Live_Batsman_Score.to_excel('C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/Live Data Excel/Live_Batsman_Score.xlsx', index=False)
Live_Bowler_Score = pd.DataFrame(Live_Bowler_Score)
Live_Bowler_Score.to_excel('C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/Live Data Excel/Live_Bowler_Score.xlsx', index=False)
Live_Toss_Info = pd.DataFrame(Live_Toss_Info)
Live_Toss_Info.to_excel('C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/Live Data Excel/Live_Toss_Info.xlsx', index=False)


