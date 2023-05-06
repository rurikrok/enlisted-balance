def get_team_name(team):
    if team == 'ussr' or team == 'usa':
        return team.upper()
    else:
        return team.capitalize()