import os # For accessing the file system
import re # For working with regular expressions
import json # For working with JSON files
import map_parser # Custom module for parsing game maps
import excel # Custom module for writing to Excel files
import average # Custom module for calculating averages
import chart # Custom module for creating charts
import pair_maps # Custom module for creating pair maps stats

# Path to the directory where the files need to be found
folder_path = "enlisted-game.vromfs.bin/gamedata/scenes/"

# Regular expression pattern to match file names
file_pattern = r"^(?!_).*inv.*\.blkx$"

# Incomplete or inactive maps
file_exclude = ['volokolamsk_forest_inv.blkx','volokolamsk_monastery_inv2.blkx','stalingrad_station_inv.blkx','berlin_goering_inv_empty.blkx','pacific_colonist_inv.blkx','normandy_factory_inv_without_area.blkx','volokolamsk_village_inv.blkx']

# List of files that meet the criteria
file_list = [file for file in os.listdir(folder_path) if re.match(file_pattern, file)
              and "solo" not in file and "modern" not in file and "comp" not in file and "trailer" not in file and "_mech_" not in file
              and file not in file_exclude]

# Parsing game maps and returning data and max_zones
data, max_zones = map_parser.parse(file_list, folder_path)
print('parse complete')

# Creating output directory if it doesn't exist
if not os.path.exists('output'):
      os.makedirs('output')

# Writing data to a JSON file
with open('output/data.json', 'w') as f:
        json.dump(data, f, indent=4)
print('data.json created')

# Writing data to an Excel file
excel.write_excel(data, max_zones, 'output/data.xlsx')
print('data.xlsx created')

# Writing average values to a text file
parameters = [("moscow", "ussr"), ("moscow", "germany"), ("berlin", "ussr"), ("berlin", "germany"), ("stalingrad", "ussr"), ("stalingrad", "germany"), ("normandy", "usa"), ("normandy", "germany"), ("tunisia", "usa"), ("tunisia", "germany"), ("pacific", "usa"), ("pacific", "japan")]
average.write_average(data, 'output/average.txt', parameters)
print('average.txt created')

# Creating charts for average values
averages = average.get_all_average(data, parameters)
parameters = [("moscow", "ussr", "germany"), ("berlin", "ussr", "germany"), ("stalingrad", "ussr", "germany"), ("normandy", "usa", "germany"), ("tunisia", "usa", "germany"), ("pacific", "usa", "japan")]
chart.write_chart(averages, 'output/charts/', parameters)
print('all average charts created')

# Creating charts for pair maps
pair_maps.pair_maps_stats(file_list, data)
print('all pair maps stats created')