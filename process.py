"""
This file is used to answer the following questions:
1. How many notifications are anything other than “no”?
2. How many orders changes at all? (regardless of any communication)
"""

# server game file
game_file_name = "beta_de_2"

import json, re, logging

# for finding unit
pattern = r"(\w+)\Wadded: (\w{1} \w{3})(.+)"


# outputs the filtered messages and order changes to json files
def filter_messages_order_changes(order_logs, filtered_messages):
    with open("./order_changes/" + game_file_name + "_order_changes.json", "w") as f:
        json.dump(order_logs, f, indent=4)
    f.close()

    with open("./deceptive_messages/" + game_file_name + "_messages.json", "w") as f:
        json.dump(filtered_messages, f, indent=4)
    f.close()


with open("./games/" + game_file_name + ".json") as f:
    game_data = json.load(f)
    season_count = 0
    messages = []
    order_logs = {}
    order_count = 0
    duplicate_order_count = 0

    # put current messages and message history together into messages
    for message_season in game_data["message_history"]:
        season_count += 1
        current_season = game_data["message_history"][message_season]

        for message in current_season:
            messages.append(message)

    for message in game_data["messages"]:
        messages.append(message)
    # count number of seasons

    # get timestamps for all annotated messages
    annotated_messages = {int(k): v for k, v in game_data["annotated_messages"].items()}

    # incoming messages marked as deceptive
    filtered_messages = [
        dict(v | {"recipient_annotation": annotated_messages[v["time_sent"]]})
        for v in messages
        if v["time_sent"]
        in annotated_messages and annotated_messages[v["time_sent"]] == 'True'  # TODO filter out messages with deceptive annotation
    ]

    # get repeated orders for units, for persuasion analysis
    for order_season in game_data["order_log_history"]:
        current_season = game_data["order_log_history"][order_season]
        moves = {}
        power_unit_dict = {}

        for timestamp in current_season:
            order_with_text = current_season[timestamp]
            order = re.search(pattern, order_with_text)

            if order:
                # print(timestamp, order.group(1), order.group(2), order.group(3))
                order_count += 1
                power = order.group(1)
                unit = order.group(2)
                order_string = order.group(3)
                power_unit_dict[unit] = power
                complete_order = unit + order_string

                # calculate repeated orders
                if unit in moves:
                    existing_moves = moves[unit]
                    moves[unit][int(timestamp)] = complete_order

                    """ # ignore duplicate orders
                    if complete_order not in existing_moves:
                        existing_moves.append(complete_order)
                        moves[unit] = existing_moves """
                else:
                    moves[unit] = {int(timestamp): complete_order}

        # filter out units with only one order
        filtered_moves = {k: v for k, v in moves.items() if len(v) > 1}
        duplicate_order_count += len(filtered_moves)

        power_order_dict = {}

        for unit, move in filtered_moves.items():
            power = power_unit_dict[unit]
            if power in power_order_dict:
                existing_orders = power_order_dict[power]
                existing_orders.append(move)
                power_order_dict[power] = existing_orders
            else:
                power_order_dict[power] = [move]

        if len(power_order_dict) > 0:
            order_logs[order_season] = power_order_dict
f.close()

print("Game: ", game_file_name)
print("Total seasons: ", season_count)

print("Total deceptive: ", len(filtered_messages))
print("perceived deceptive messages / incoming messages:", len(filtered_messages) / len(annotated_messages) * 100, "%")
print("Percentage moves are changed: ", duplicate_order_count / order_count * 100, "%")

# using timestamp as key for messages
message_dict = {}

for message in messages:
    time_sent = message["time_sent"]
    message_dict[time_sent] = message

# auxiliary function for adding messages to order logs
def filter_message_by_power_phase(power, phase):
    return {
        k: v
        for k, v in message_dict.items()
        if phase == v["phase"] and (v["sender"] == power or v["recipient"] == power)
    }

# insert messages to order logs
def add_messages_to_order_logs(order_logs, incoming_messages_only=True):
    output = {}

    for season in order_logs:
        powers = order_logs[season]
        all_power_messages = {}

        for power in powers:
            units: list = powers[power]
            possibly_relevant_messages = filter_message_by_power_phase(power, season)
            all_unit_messages = []

            for unit_dict in units:
                keys = list(unit_dict.keys())
                keys.sort()
                order_message_dict = {}

                for i in range(len(keys) - 1):
                    preceding_order = keys[i]
                    following_order = keys[i + 1]
                    relevant_messages = {
                        k: v
                        for k, v in possibly_relevant_messages.items()
                        if preceding_order <= k <= following_order and v['recipient'] == power
                    } if incoming_messages_only else {
                        k: v
                        for k, v in possibly_relevant_messages.items()
                        if preceding_order < k <= following_order
                    }
                    order_message_dict[preceding_order] = unit_dict[preceding_order]
                    order_message_dict.update(relevant_messages)

                order_message_dict[following_order] = unit_dict[following_order]
                all_unit_messages.append(order_message_dict)
            
            all_power_messages[power] = all_unit_messages

        output[season] = all_power_messages

    return output

""" with open("./order_with_msgs/" + game_file_name + ".json", "w") as f:
    json.dump(add_messages_to_order_logs(order_logs), f, indent=4)
f.close()
 """
