import os # For accessing the file system
import re # For working with regular expressions
import subprocess # For executing git commands

def parse(file_list, folder_path):

    # List to store the data
    data = []

    # Regular expression pattern to search for necessary data in lines
    team_name_pattern = r'_template:t="team_([^+]+)(?:\+)'
    score_cap_pattern = r'team__scoreCap:r=(\d+\.\d+)'
    spawn_cost_pattern = r'team__squadSpawnCost:i=(\d+)'
    zone_number_pattern = r'groupName:t="([^"]+)"'
    cap_time_pattern = r'capzone__capTime:r=(\d+\.\d+)'
    cap_reward_pattern = r'capzone__capReward:r=(\d+\.\d+)'

    # Dictionary for data transformation
    team_map = {
        "ussr_berlin": "ussr",
        "germany_berlin": "germany",
        "usa": "usa",
        "germany": "germany",
        "pacific_allies": "usa",
        "pacific_axis": "japan",
        "stalingrad_allies": "ussr",
        "stalingrad_axis": "germany",
        "tunisia_allies": "usa",
        "tunisia_axis": "germany",
        "germany_winter": "germany"
    }

    max_zones = 0
    zones = 0

    # Loop through the list of file names
    for file_name in file_list:
        # Open file and read lines
        with open(os.path.join(folder_path, file_name), "r") as f:
            lines = f.readlines()
        # Initialize variables to store data for each team
        found_teams = 0 # number of teams found in the current file
        zone_entity = False  # whether the current line is inside a zone entity
        attack_team = 0  # index of the attacking team for the current file
        if zones > max_zones:
            max_zones = zones
        zones = 0

        # Loop through each line in the file
        for line in lines:
            # Use regular expressions to search for relevant data in the line
            match_team_name = re.search(team_name_pattern, line.strip())
            match_score_cap = re.search(score_cap_pattern, line.strip())
            match_spawn_cost = re.search(spawn_cost_pattern, line.strip())
            match_zone_number = re.search(zone_number_pattern, line.strip())
            match_cap_time = re.search(cap_time_pattern, line.strip())
            match_cap_reward = re.search(cap_reward_pattern, line.strip())

            # Check if the line contains a zone entity definition
            if "_template:t=\"defend_zone_chained_" in line:
                zone_entity = True
            # Check if the line marks the end of the zone entity definition
            if "}" in line:
                zone_entity = False

            # Process the line if it contains team data
            if match_team_name:
                # Get team name
                team_name = match_team_name.group(1)

                # Convert the team name if it is in the team_map
                if team_name in team_map:
                    team_name = team_map[team_name]

                # Get the campaign name from the file name
                campaign = file_name.split("_")[0]
                if campaign == "volokolamsk":
                    campaign = "moscow"

                # Get the version number of the file from Git
                version = commit_message = subprocess.check_output(f'git log -1 --pretty=format:"%s" {os.path.join(folder_path, file_name)}', shell=True).decode().strip()

                # Add the team data to the list of data dictionaries
                data.append({"file_name": file_name, "version": version, "campaign": campaign, "team_name": team_name})
                found_teams += 1

            # Process the line if it contains score cap data
            elif match_score_cap:
                # Get scoreCap value
                score_cap = match_score_cap.group(1)

                # Add the score cap data to the last team in the list
                data[-1]["score_cap"] = score_cap

            # Process the line if it contains spawn cost data
            elif match_spawn_cost:
                # Get squadSpawnCost value
                spawn_cost = match_spawn_cost.group(1)

                # Add the spawn cost data to the last team in the list and initialize the list of zones for that team
                data[-1]["spawn_cost"] = spawn_cost 
                data[-1].update({"zones": []})

                # Store the index of the attacking team for the current file
                attack_team = found_teams

            # If the current line is inside a zone entity:
            if zone_entity:
                # If the line matches the zone number pattern:
                if match_zone_number:
                    # Get the number of the zone
                    zone_number = match_zone_number.group(1)

                    # Create a new dictionary for the zone
                    zone_data = {"zone_number": zone_number}

                    # Add the zone data to the list of zones for the attacking team
                    if attack_team == 1:
                        data[-2]["zones"].append(zone_data)
                    elif attack_team == 2:
                        data[-1]["zones"].append(zone_data)

                    zones += 1

                # If the line matches the cap time pattern:
                elif match_cap_time:
                    # Get the cap_time value
                    cap_time = match_cap_time.group(1)

                # Add the cap time data to the last zone for the attacking team
                    if attack_team == 1:
                        data[-2]["zones"][-1]["cap_time"] = cap_time
                    elif attack_team == 2:
                        data[-1]["zones"][-1]["cap_time"] = cap_time

                # If the line matches the cap reward pattern:
                elif match_cap_reward:
                    # Get the capReward value
                    cap_reward = match_cap_reward.group(1)
                    if ('5' in zone_number or '1' in zone_number) and zones >= 5:
                        continue
                    else:
                        # Add the cap reward data to the last zone for the attacking team
                        if attack_team == 1:
                            data[-2]["zones"][-1]["cap_reward"] = cap_reward
                        elif attack_team == 2:
                            data[-1]["zones"][-1]["cap_reward"] = cap_reward

        print(f"Processed {file_name}")

    # Add a 'type' key to each item in the data list based on the presence of 'spawn_cost' key
    for item in data:
        if "spawn_cost" in item:
            item["type"] = "attack"
        else:
            item["type"] = "defense"

    return data, max_zones