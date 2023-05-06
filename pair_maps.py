import average
import chart

def pair_maps_stats(file_list, data):

    maps_pairs = []
    for filename in file_list:
        if filename.endswith('.blkx'):
            base_name = filename.replace('.blkx', '')
            if base_name + '_axis.blkx' in file_list:
                maps_pairs.append((filename, base_name + '_axis.blkx'))
            elif base_name + '_allies.blkx' in file_list:
                maps_pairs.append((filename, base_name + '_allies.blkx'))
            elif base_name + '_ussr.blkx' in file_list:
                maps_pairs.append((filename, base_name + '_ussr.blkx'))

    for pair in maps_pairs:
        pairs_data = []
        for item in data:
            if item["file_name"] in pair and item["type"] == "attack":
                pairs_data.append(item)
                if item["campaign"] == "moscow":
                    parameters_for_average = [("moscow", "ussr"), ("moscow", "germany")]
                    parameters_for_chart = [("moscow", "ussr", "germany")]
                elif item["campaign"] == "berlin":
                    parameters_for_average = [("berlin", "ussr"), ("berlin", "germany")]
                    parameters_for_chart = [("berlin", "ussr", "germany")]
                elif item["campaign"] == "stalingrad":
                    parameters_for_average = [("stalingrad", "ussr"), ("stalingrad", "germany")]
                    parameters_for_chart = [("stalingrad", "ussr", "germany")]
                elif item["campaign"] == "normandy":
                    parameters_for_average = [("normandy", "usa"), ("normandy", "germany")]
                    parameters_for_chart = [("normandy", "usa", "germany")]
                elif item["campaign"] == "tunisia":
                    parameters_for_average = [("tunisia", "usa"), ("tunisia", "germany")]
                    parameters_for_chart = [("tunisia", "usa", "germany")]
                elif item["campaign"] == "pacific":
                    parameters_for_average = [("pacific", "usa"), ("pacific", "japan")]
                    parameters_for_chart = [("pacific", "usa", "japan")]
        
        map_name = pair[0].replace('.blkx', '')
        average.write_average(pairs_data, 'output/pair_maps/' + map_name + '.txt', parameters_for_average)
        print(map_name + '.txt created')
        averages = average.get_all_average(pairs_data, parameters_for_average)
        print(map_name + ' charts creating...')
        chart.write_chart(averages, 'output/pair_maps/charts/' + map_name + '/', parameters_for_chart, map_name)