import os
import yaml
import pandas as pd

# Path where all YAML files are stored
YAML_DIR = "C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/historical_data/yaml_files"

# Output Excel file
OUTPUT_FILE = "ipl_matches_2008_2025.xlsx"

# List to hold parsed match data
match_meta = []

# Get sorted list of YAML files
yaml_files = sorted([f for f in os.listdir(YAML_DIR) if f.endswith('.yaml')])
print(f"Found {len(yaml_files)} YAML files.")

# Parse each file
for file in yaml_files:
    file_path = os.path.join(YAML_DIR, file)
    with open(file_path, 'r') as stream:
        try:
            print(f"Parsing file: {file}")
            data = yaml.safe_load(stream)
            info = data.get("info", {})
        except Exception as e:
            print(f"Failed to parse {file}: {e}")
            continue

        match_id = int(file.replace('.yaml', '')) if file.replace('.yaml', '').isdigit() else file.replace('.yaml', '')
        city = info.get("city", "NA")
        match_date = info.get("dates", ["NA"])[0]
        match_date = pd.to_datetime(match_date) if match_date != "NA" else pd.NaT
        season = match_date.year if not pd.isna(match_date) else "NA"

        teams = info.get("teams", ["NA", "NA"])
        team1 = teams[0] if len(teams) > 0 else "NA"
        team2 = teams[1] if len(teams) > 1 else "NA"

        venue = info.get("venue", "NA")
        toss = info.get("toss", {})
        toss_winner = toss.get("winner", "NA")
        toss_decision = toss.get("decision", "NA")
        superover = info.get("super_over", "NA")

        outcome = info.get("outcome", {})
        winning_team = outcome.get("winner", "NA")

        # Margin and method
        by = outcome.get("by", {})
        if "runs" in by:
            won_by = "runs"
            margin = by["runs"]
        elif "wickets" in by:
            won_by = "wickets"
            margin = by["wickets"]
        else:
            won_by = "NA"
            margin = "NA"

        method = outcome.get("method", "NA")

        # Player of match
        player_of_match = info.get("player_of_match", ["NA"])[0]

        # Umpires
        umpires = info.get("umpires", [])
        umpire1 = umpires[0] if len(umpires) > 0 else "NA"
        umpire2 = umpires[1] if len(umpires) > 1 else "NA"

        match_meta.append({
            "id": match_id,
            "city": city,
            "match_date": match_date,
            "season": season,
            "team1": team1,
            "team2": team2,
            "venue": venue,
            "toss_winner": toss_winner,
            "toss_decision": toss_decision,
            "superover": superover,
            "winning_team": winning_team,
            "won_by": won_by,
            "margin": margin,
            "method": method,
            "player_of_match": player_of_match,
            "umpire1": umpire1,
            "umpire2": umpire2
        })

# Create DataFrame
df = pd.DataFrame(match_meta)

# Sort by season and date to assign match numbers
df = df.sort_values(by=["season", "match_date"]).reset_index(drop=True)
df["match_number"] = df.groupby("season").cumcount() + 1
df["match_number"] = df["match_number"].apply(lambda x: f"Match {x}")

# Reorder columns
df = df[[
    "id", "city", "match_date", "season", "match_number", "team1", "team2",
    "venue", "toss_winner", "toss_decision", "superover", "winning_team",
    "won_by", "margin", "method", "player_of_match", "umpire1", "umpire2"
]]

# Replace NaN with 'NA'
df = df.fillna("NA")

# Save to Excel
df.to_excel(OUTPUT_FILE, index=False)
print(f"\n✅ Match metadata with match_number saved to {OUTPUT_FILE}")
