import os
import yaml
import pandas as pd
from collections import Counter

# Directory containing all YAML files
YAML_DIR = "C:/Users/Admin/Desktop/End-to-End IPL Analysis Dashboard and Live Insights/historical_data/yaml_files"

# Output Excel file
OUTPUT_FILE = 'ipl_ball_by_ball_2008_2025.xlsx'

# Initialize list to hold all rows
all_data = []

# Get sorted list of YAML files
yaml_files = sorted([f for f in os.listdir(YAML_DIR) if f.endswith('.yaml')])



print(f"Found {len(yaml_files)} YAML files.")
print("Sample files:", yaml_files[:5])

# Loop through all YAML files
for file in yaml_files:
    file_path = os.path.join(YAML_DIR, file)
    with open(file_path, 'r') as stream:
        try:
            print(f"\nParsing file: {file}")
            data = yaml.safe_load(stream)
            innings_data = data.get('innings', [])
        except Exception as e:
            print(f"Failed to parse {file}: {e}")
            continue

        match_id = int(file.replace('.yaml', '')) if file.replace('.yaml', '').isdigit() else file.replace('.yaml', '')

        # Initialize counters for the current file
        player_out_counter = Counter()
        dismissal_kind_counter = Counter()
        fielders_counter = Counter()

        for inning_index, inning in enumerate(innings_data, start=1):
            inning_name = list(inning.keys())[0]
            inning_data = inning[inning_name]
            batting_team = inning_data.get('team', 'NA')

            if 'deliveries' not in inning_data:
                continue

            for delivery in inning_data['deliveries']:
                if not isinstance(delivery, dict):
                    continue
                for ball_id, details in delivery.items():
                    if not isinstance(details, dict):
                        continue

                    over = int(str(ball_id).split('.')[0])
                    ball_number = int(str(ball_id).split('.')[1])
                    batter = details.get('batsman', 'NA')
                    bowler = details.get('bowler', 'NA')
                    non_striker = details.get('non_striker', 'NA')
                    extras = details.get('extras', {})
                    extra_type = list(extras.keys())[0] if extras else 'NA'
                    runs = details.get('runs', {'batsman': 0, 'extras': 0, 'total': 0})
                    batsman_run = runs.get('batsman', 0)
                    extras_run = runs.get('extras', 0)
                    total_run = runs.get('total', 0)
                    non_boundary = 1 if batsman_run not in [4, 6] else 0

                    # Handle both 'wickets' and 'wicket'
                    wickets_list = []
                    if 'wickets' in details:
                        wickets_list = details['wickets'] if isinstance(details['wickets'], list) else [details['wickets']]
                    elif 'wicket' in details:
                        wickets_list = [details['wicket']]

                    iswicket_delivery = 1 if wickets_list else 0

                    player_out = 'NA'
                    dismissal_kind = 'NA'
                    fielders_involved = 'NA'

                    for wicket in wickets_list:
                        player_out = wicket.get('player_out', 'NA')
                        dismissal_kind = wicket.get('kind', 'NA')
                        fielders = wicket.get('fielders', [])
                        fielders_involved_list = [f['name'] if isinstance(f, dict) else f for f in fielders] if fielders else ['NA']
                        fielders_involved = ', '.join(fielders_involved_list)

                        # Update counters
                        player_out_counter[player_out] += 1
                        dismissal_kind_counter[dismissal_kind] += 1
                        for fielder in fielders_involved_list:
                            fielders_counter[fielder] += 1

                    all_data.append([
                        match_id,
                        inning_index,
                        over,
                        ball_number,
                        batter,
                        bowler,
                        non_striker,
                        extra_type,
                        batsman_run,
                        extras_run,
                        total_run,
                        non_boundary,
                        iswicket_delivery,
                        player_out,
                        dismissal_kind,
                        fielders_involved,
                        batting_team
                    ])
                    

        # Print summary for the file
        print(f"\nSummary for file: {file}")
        print("Player Out Count:", dict(player_out_counter))
        print("Dismissal Kind Count:", dict(dismissal_kind_counter))
        print("Fielders Involved Count:", dict(fielders_counter))

# Define DataFrame columns
columns = [
    'id', 'innings', 'overs', 'ball_number', 'batter', 'bowler', 'non_striker',
    'extra_type', 'batsman_run', 'extras_run', 'total_run', 'non_boundary',
    'iswicket_delivery', 'player_out', 'dismissal_kind', 'fielders_involved',
    'batting_team'
]

# Convert to DataFrame and save to Excel
df = pd.DataFrame(all_data, columns=columns)
df.to_excel(OUTPUT_FILE, index=False)

print(f"\n Data saved to {OUTPUT_FILE}")
print(f" Total deliveries processed: {len(df)}")