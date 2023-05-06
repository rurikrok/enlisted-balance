import os
import tools

def get_average(data, campaign, team_name, parameter):
    sum = 0
    i = 0
    for item in data:
        if item["campaign"] == campaign and item["team_name"] == team_name and item["type"] == "attack":
            sum += float(item[parameter])
            i += 1
    if i == 0:
        return None
    else:
        return sum/i
    
def get_average_zones_parameter(data, campaign, team_name, zones_parameter):
    sum = 0
    i = 0
    for item in data:
        if item["campaign"] == campaign and item["team_name"] == team_name and item["type"] == "attack":
            for zone in item["zones"]:
                if (zones_parameter in zone):
                    sum += float(zone[zones_parameter])
                    i += 1
    if i == 0:
        return None
    else:
        return sum/i
    
def get_average_zone_parameter(data, campaign, team_name, zone_parameter, zone_num):
    sum = 0
    i = 0
    reverse_maps_list = ['berlin_moat_inv_counter.blkx','berlin_station_inv_counter.blkx','berlin_station_inv_counter_axis.blkx','pacific_gavutu_inv_counter_axis.blkx','tunisia_city_inv_counter.blkx','tunisia_city_inv_counter_axis.blkx','tunisia_farm_inv_counter.blkx','tunisia_farm_inv_counter_axis.blkx']
    for item in data:
        if item["campaign"] == campaign and item["team_name"] == team_name and item["type"] == "attack":
            if item["file_name"] not in reverse_maps_list:
                for zone in item["zones"]:
                    if zone_parameter in zone and str(zone_num) in zone["zone_number"]:
                        sum += float(zone[zone_parameter])
                        i += 1
            else:
                for zone in item["zones"]:
                    if zone_parameter in zone and str(6-int(zone_num)) in zone["zone_number"]:
                        sum += float(zone[zone_parameter])
                        i += 1
    if i > 0:
        return sum/i
    else:
        return None
    
def get_all_average(data, parameters):
    averages = {}
    for parameter in parameters:

        averages[(parameter[0], parameter[1], 'score_cap')] = [get_average(data, parameter[0], parameter[1], "score_cap")]
        averages[(parameter[0], parameter[1], 'cap_time')] = [get_average_zones_parameter(data, parameter[0], parameter[1], "cap_time")]
        averages[(parameter[0], parameter[1], 'cap_reward')] = [get_average_zones_parameter(data, parameter[0], parameter[1], "cap_reward")]

        for i in range(1, 6):
            averages[(parameter[0], parameter[1], 'cap_time_zone', i)] = [get_average_zone_parameter(data, parameter[0], parameter[1], "cap_time", i)]

        for i in range(1, 5):
            averages[(parameter[0], parameter[1], 'cap_reward_zone', i)] = [get_average_zone_parameter(data, parameter[0], parameter[1], "cap_reward", i)]

    return averages
    
def write_average(data, output_file, parameters):

    # Creating output directory if it doesn't exist
    output_folder = os.path.dirname(output_file)
    if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    with open(output_file, 'w') as f:
        for parameter in parameters:
            campaign = parameter[0]
            team_name = tools.get_team_name(parameter[1])
            f.write(f"{campaign.capitalize()} {team_name} average score_cap: " + '{:.2f}'.format(get_average(data, parameter[0], parameter[1], "score_cap")) + "\n----------------------------------------\n")
        for parameter in parameters:
            campaign = parameter[0]
            team_name = tools.get_team_name(parameter[1])
            f.write(f"{campaign.capitalize()} {team_name} average cap_time: " + '{:.2f}'.format(get_average_zones_parameter(data, parameter[0], parameter[1], "cap_time")) + "\n----------------------------------------\n")
        for parameter in parameters:
            campaign = parameter[0]
            team_name = tools.get_team_name(parameter[1])
            f.write(f"{campaign.capitalize()} {team_name} average cap_reward: " + '{:.2f}'.format(get_average_zones_parameter(data, parameter[0], parameter[1], "cap_reward")) + "\n----------------------------------------\n")
        for parameter in parameters:
            campaign = parameter[0]
            team_name = tools.get_team_name(parameter[1])
            for i in range(1, 6):
                f.write(f"{parameter[0].capitalize()} {parameter[1].capitalize()} average cap_time for zone {i}: " + '{:.2f}'.format(get_average_zone_parameter(data, parameter[0], parameter[1], "cap_time", i)) + "\n----------------------------------------\n")
        for parameter in parameters:
            campaign = parameter[0]
            team_name = tools.get_team_name(parameter[1])
            for i in range(1, 5):
                f.write(f"{parameter[0].capitalize()} {parameter[1].capitalize()} average cap_reward for zone {i}: " + '{:.2f}'.format(get_average_zone_parameter(data, parameter[0], parameter[1], "cap_reward", i)) + "\n----------------------------------------\n")