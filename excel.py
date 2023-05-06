import os
import pandas as pd # For working with data frames

def write_excel(data, max_zones, output_file):

    # Creating output directory if it doesn't exist
    output_folder = os.path.dirname(output_file)
    if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    # Define the list of columns in the final table, including columns from the 'zones' list
    columns = ['file_name', 'version', 'campaign', 'team_name', 'type', 'score_cap', 'spawn_cost']
    for i in range(1, max_zones + 1):
        columns += [f'zone_number_{i}', f'cap_time_{i}', f'cap_reward_{i}']

    # Create a list of dictionaries containing the data for each row in the final table
    rows = []
    for d in data:
        row = {}
        row['file_name'] = d['file_name']
        row['version'] = d['version']
        row['campaign'] = d['campaign']
        row['team_name'] = d['team_name']
        row['type'] = d['type']
        row['score_cap'] = float(d['score_cap'])
        if 'spawn_cost' in d:
            row['spawn_cost'] = float(d.get('spawn_cost'))
        else:
            row['spawn_cost'] = ''

        zones = d.get('zones', [])
        for i, p in enumerate(zones):
            row[f'zone_number_{i+1}'] = p.get('zone_number', '')
            if 'cap_time' in p:
                row[f'cap_time_{i+1}'] = float(p.get('cap_time'))
            else:
                row[f'cap_time_{i+1}'] = ''
            if 'cap_reward' in p:
                row[f'cap_reward_{i+1}'] = float(p.get('cap_reward'))
            else:
                row[f'cap_reward_{i+1}'] = ''
            
        rows.append(row)
        
    # Create a pandas DataFrame from the list of dictionaries and specify the column order
    df = pd.DataFrame(rows, columns=columns)

    # Create a new Excel file and write the DataFrame to the first sheet
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    df.to_excel(writer, index=False)

    # Get the workbook and worksheet objects to modify formatting
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add a filter to the first row of the worksheet
    worksheet.autofilter(0, 0, 0, len(df.columns) - 1)

    # Set the width of each column based on the length of its header or the length of its longest value
    for i, col in enumerate(df.columns):
        column_len = df[col].astype(str).str.len().max()
        column_len = max(column_len, len(col))
        worksheet.set_column(i, i, column_len)

    # Close the workbook and save the Excel file
    workbook.close()
