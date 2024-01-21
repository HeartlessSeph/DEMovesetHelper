def add_column(battle_skill, new_player):
    battle_skill["columnValidity"][new_player] = "1"
    battle_skill["columnTypes"][new_player] = 1
    battle_skill["COLUMN_COUNT"] += 1
    battle_skill["COLUMN_INDICES"].append(len(battle_skill["COLUMN_INDICES"]))
    for entry in [e for e in battle_skill if e.isdigit()]:
        f_name = list(battle_skill[entry].keys())[0]
        my_dict = battle_skill[entry][f_name]
        my_dict = list(my_dict.items())
        my_dict.insert(-2, (new_player, 0))
        my_dict = dict(my_dict)
        battle_skill[entry][f_name] = my_dict
    return battle_skill
