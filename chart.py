import os
import matplotlib.pyplot as plt # For plotting graphs
import tools

def write_chart(averages, output_folder, parameters, map_name=None):
    for parameter in parameters:
        campaign = parameter[0]
        team_name_1 = tools.get_team_name(parameter[1])
        team_name_2 = tools.get_team_name(parameter[2])

        # Creating output directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Create a dictionary where the keys are the names of the graphs and the values are the data for plotting
        data = {'score_cap': {team_name_1: averages[(campaign, parameter[1], 'score_cap')][0], team_name_2: averages[(campaign, parameter[2], 'score_cap')][0]}, 
                'cap_time': {team_name_1: averages[(campaign, parameter[1], 'cap_time')][0], team_name_2: averages[(campaign, parameter[2], 'cap_time')][0]},
                'cap_reward': {team_name_1: averages[(campaign, parameter[1], 'cap_reward')][0], team_name_2: averages[(campaign, parameter[2], 'cap_reward')][0]}}

        # Create a list of colors for the graphs
        if campaign in ['moscow', 'berlin', 'stalingrad']:
            colors = ['r', 'k']
        elif campaign in ['normandy', 'tunisia', 'pacific']:
            colors = ['b', 'k']
        else:
            colors = ['r', 'b']

        # Create a list of labels for the graphs
        labels = [team_name_1, team_name_2]

        # Create a list of names for the axes
        x_labels = ['score_cap', 'cap_time', 'cap_reward']
        y_labels = ['Average Score Cap', 'Average Cap Time', 'Average Cap Reward']

        # Create a figure for the graphs
        fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))

        # Draw the corresponding graph for each axis
        for i, ax in enumerate(axs.flat):
            values = [data[x_labels[i]][label] for label in labels]
            bars = ax.bar(labels, values, color=colors)
            ax.set_title(y_labels[i], fontsize=12, fontweight='bold')
            ax.set_ylim([0, max(values) * 1.1])
            for bar, value in zip(bars, values):
                x = bar.get_x() + bar.get_width() / 2
                y = value / 2
                ax.annotate(f'{value:.2f}', xy=(x, y), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=10, fontweight='bold', color='white')
            
        # Add a general title for all graphs
        if (map_name):
            fig.suptitle(map_name)
        else:
            fig.suptitle(campaign.capitalize())

        # Save the figure as a PNG file
        fig.savefig(output_folder + campaign.capitalize() + '.png', dpi=300, bbox_inches='tight')

        # Close the figure
        plt.close(fig)

        print(campaign + ' chart created')

        # Create a dictionary for the cap_time_zones data
        data = {}
        for i in range(1, 6):
            zone_data = {team_name_1: averages[(campaign, parameter[1], 'cap_time_zone', i)][0],
                        team_name_2: averages[(campaign, parameter[2], 'cap_time_zone', i)][0]}
            data[f'cap_time_zone_{i}'] = zone_data

        # Create a list of names for the cap_time_zones axes
        x_labels = [f'cap_time_zone_{i}' for i in range(1, 6)]
        y_labels = [f'Average Cap Time Zone {i}' for i in range(1, 6)]

        # Create a figure for the cap_time_zones graphs
        fig, axs = plt.subplots(nrows=5, ncols=1, figsize=(10, 10))

        # Draw the corresponding graph for each axis
        for i, ax in enumerate(axs.flat):
            values = [data[x_labels[i]][label] for label in labels]
            bars = ax.bar(labels, values, color=colors)
            ax.set_title(y_labels[i], fontsize=12, fontweight='bold')
            ax.set_ylim([0, max(values) * 1.1])
            for bar, value in zip(bars, values):
                x = bar.get_x() + bar.get_width() / 2
                y = value / 2
                ax.annotate(f'{value:.2f}', xy=(x, y), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=10, fontweight='bold', color='white')

        # Add a general title for all graphs
        if (map_name):
            fig.suptitle(map_name)
        else:
            fig.suptitle(campaign.capitalize())

        # Save the figure as a PNG file
        fig.savefig(output_folder + campaign.capitalize() + ' Zones Cap Time' + '.png', dpi=300, bbox_inches='tight')

        # Close the figure
        plt.close(fig)

        print(campaign + ' zones cap time chart created')

        # Create a dictionary for the cap_reward_zones data
        data = {}
        for i in range(1, 5):
            zone_data = {team_name_1: averages[(campaign, parameter[1], 'cap_reward_zone', i)][0],
                        team_name_2: averages[(campaign, parameter[2], 'cap_reward_zone', i)][0]}
            data[f'cap_reward_zone_{i}'] = zone_data

        # Create a list of names for the cap_reward_zones axes
        x_labels = [f'cap_reward_zone_{i}' for i in range(1, 5)]
        y_labels = [f'Average Cap Reward Zone {i}' for i in range(1, 5)]

        # Create a figure for the cap_reward_zones graphs
        fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(10, 10))

        # Draw the corresponding graph for each axis
        for i, ax in enumerate(axs.flat):
            values = [data[x_labels[i]][label] for label in labels]
            bars = ax.bar(labels, values, color=colors)
            ax.set_title(y_labels[i], fontsize=12, fontweight='bold')
            ax.set_ylim([0, max(values) * 1.1])
            for bar, value in zip(bars, values):
                x = bar.get_x() + bar.get_width() / 2
                y = value / 2
                ax.annotate(f'{value:.2f}', xy=(x, y), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=10, fontweight='bold', color='white')

        # Add a general title for all graphs
        if (map_name):
            fig.suptitle(map_name)
        else:
            fig.suptitle(campaign.capitalize())

        # Save the figure as a PNG file
        fig.savefig(output_folder + campaign.capitalize() + ' Zones Cap Reward' + '.png', dpi=300, bbox_inches='tight')

        # Close the figure
        plt.close(fig)

        print(campaign + ' zones cap reward chart created')