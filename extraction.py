import os, json, re, copy

from openai import OpenAI
from sklearn.metrics import f1_score, precision_score, recall_score
import numpy as np
import matplotlib.pyplot as plt

client = OpenAI(api_key="")

game_dir = "./human_games/"
POWERS = ["AUSTRIA", "ENGLAND", "FRANCE", "GERMANY", "ITALY", "RUSSIA", "TURKEY"]
order_log_regex = r"([A-Z]+)\W(.*)"

power_mapping = {
    "russia": "rus",
    "austria": "aus",
    "england": "eng",
    "france": "fra",
    "germany": "ger",
    "italy": "ita",
    "turkey": "tur",
}

performance_mapping = {
    "jashper": 4,
    "JHenrichs": 3,
    "NewEnglandFireSquad": 5,
    "pbansal674@gmail.com": 0,
    "abhishekh.singhal@gmail.com": 4,
    "parip": 3,
    "aguoman": 0,
    "CMRawles": 4,
    "Conq": 5,
    "Mikalis Kamaritis": 5,
    "harvey_birdman": 4,
    "Sheringford": 4,
    "slothDC": 5,
    "sloth.dc@gmail.com": 5,
    "pyxxy": 5,
    "ShotAway": 4,
    "eddie": 3,
    "totonchyms": 4,
    'cicero': 0,
    'sloth': 5,
    'Klaus Mikaelson ': 5,
    'gauty7': 2,
    'Sploack': 5,
    'Dan Wang': 3,
    'david.s.graff@icloud.com': 5,
    'Connorknight94': 0,
    'wardiecj': 5,
}

performance_mapping_reverse = {
    0: ['aguoman', 'pbansal674@gmail.com'],
    3: ['JHenrichs', 'parip', 'eddie'],
    4: ['jashper', 'abhishekh.singhal@gmail.com', 'CMRawles', 'harvey_birdman', 'Sheringford', 'ShotAway', 'totonchyms'],
    5: ['NewEnglandFireSquad', 'Conq', 'Mikalis Kamaritis', 'slothDC', 'sloth.dc@gmail.com', 'pyxxy']
}


def human_players(data):
    """
    get all human players in the game

    :param data: dictionary of game data after json.load
    :return: a list of powers that does not have cicero prefix usernames
    """
    bots = bot_players(data)
    humans = []

    for power in POWERS:
        if power not in bots:
            humans.append(power)

    return humans


def bot_players(data):
    """
    get all cicero players in the game

    :param data: dictionary of game data after json.load
    :return: a list of powers that has cicero prefix usernames
    """
    bots = []
    all_powers = data["powers"]

    for power in all_powers:
        power_controllers = all_powers[power]["controller"]

        for controller in power_controllers.values():
            if controller not in bots and controller.startswith("cicero"):
                bots.append(power)

    return bots


def get_player_name(data, power):
    all_powers = data["powers"]
    power_controllers = all_powers[power]["controller"]

    for controller in power_controllers.values():
        if controller == "dummy":
            continue
        elif controller.startswith("cicero"):
            return "cicero"
        else:
            return controller

    return "dummy"


def num_phases(data):
    """
    get number of phases played in the game

    :param data: dictionary of game data after json.load
    :return: integer of number of phases played
    """
    return len(data["state_history"])


def get_state_history(data):
    """
    get state history of the game

    :param data: dictionary of game data after json.load
    :return: a dictionary of state history, with phase as key and state as value
    """
    return data["state_history"]


def num_phases_with_msg(data):
    """
    get number of phases with messages in the game

    :param data: dictionary of game data after json.load
    :return: integer of number of phases with messages, which should be the same or less than num_phases
    """

    cnt = 0
    message_history = data["message_history"]

    for _, msgs in message_history.items():
        if len(msgs) > 0:
            cnt += 1

    return cnt


def all_logs(data):
    """
    get cicero's log history in the game

    :param data: dictionary of game data after json.load

    :return: a dictionary of logs, with phase as key and list of logs as value
    """
    return data["log_history"]


def all_orders(data):
    """
    get the final orders for each power for each phase in the game

    :param data: dictionary of game data after json.load

    :return: a dictionary of logs, with phase as key and {power: [orders]} as value
    """
    return data["order_history"]


def all_stances(data):
    """
    get the player stances for each power for each phase in the game
    stance ranges from 1 to 5, with 1 being very hostile and 5 being very friendly
    :param data: dictionary of game data after json.load

    :return: a dictionary of stances, with phase as key and {power: {stance_power: stance}} as value
    """

    return data["stance_history"]


def perceived_bots(data):
    """
    get the player perceptions of the bots
    :param data: dictionary of game data after json.load

    :return: a dictionary with phase as key and {power: {stance_power: bool}} as value
    """

    return data["is_bot_history"]


def all_order_logs(data):
    """
    get the logs of orders for each player for each phase in the game
    :param data: dictionary of game data after json.load

    :return: a dictionary with phase as key and {str(time_sent): log} as value
    """

    return data["order_log_history"]


def all_msgs(data):
    """
    get all messages in the game

    :param data: dictionary of game data after json.load
    :return: a dictionary of messages, with phase as key and list of messages as value
    """

    return data["message_history"]


def all_annotations(data):
    """
    get all annotations in the game

    :param data: dictionary of game data after json.load
    :return: a dictionary of annotations, with phase as key and list of annotations as value
    """

    return data["annotated_messages"]


def filter_msgs(data, filter_func):
    msgs = {}
    msgs_by_phase = all_msgs(data)

    for phase in msgs_by_phase:
        curr_msgs = msgs_by_phase[phase]
        curr_phase_msgs = list(filter(filter_func, curr_msgs))

        if len(curr_phase_msgs) > 0:
            msgs[phase] = curr_phase_msgs

    return msgs


def msgs_from_humans(data, humans):
    """
    get all messages sent by humans in the game

    :param data: dictionary in which key is phase and value is list of messages
    :param humans: list of human powers in the game
    :return: a dictionary of messages, with phase as key and list of messages as value
    """
    msgs = {}
    # msgs_by_phase = all_msgs(data)
    # humans = human_players(data)

    for phase in data:
        curr_phase_msgs = []

        for msg in data[phase]:
            if msg["sender"] in humans:
                curr_phase_msgs.append(msg)

        if len(curr_phase_msgs) > 0:
            msgs[phase] = curr_phase_msgs

    return msgs


def msgs_to_humans(data, humans):
    """
    get all messages sent to humans in the game

    :param data: dictionary in which key is phase and value is list of messages
    :param humans: list of human powers in the game
    :return: a dictionary of messages, with phase as key and list of messages as value
    """

    msgs = {}
    # msgs_by_phase = all_msgs(data)
    # humans = human_players(data)

    for phase in data:
        curr_phase_msgs = []

        for msg in data[phase]:
            if msg["recipient"] in humans:
                curr_phase_msgs.append(msg)

        if len(curr_phase_msgs) > 0:
            msgs[phase] = curr_phase_msgs

    return msgs


def msgs_from_to_humans(data, humans):
    """
    get all messages sent by humans to humans in the game

    :param data: dictionary in which key is phase and value is list of messages
    :param humans: list of human powers in the game
    :return: a dictionary of messages, with phase as key and list of messages as value
    """

    msgs = {}
    msgs_from_humans_by_phase = msgs_from_humans(data, humans)
    # humans = human_players(data)

    for phase in msgs_from_humans_by_phase:
        curr_phase_msgs = []

        for msg in msgs_from_humans_by_phase[phase]:
            if msg["recipient"] in humans:
                curr_phase_msgs.append(msg)

        if len(curr_phase_msgs) > 0:
            msgs[phase] = curr_phase_msgs

    return msgs


def human_lies(data, humans):
    """
    get all lies sent by humans in the game

    :param data: dictionary in which key is phase and value is list of messages
    :param humans: list of human powers in the game
    :return: a dictionary of messages, with phase as key and list of messages as value
    """
    lies = {}
    msgs_from_humans_by_phase = msgs_from_humans(data, humans)

    for phase in msgs_from_humans_by_phase:
        curr_phase_lies = []

        for msg in msgs_from_humans_by_phase[phase]:
            if msg["truth"] is not None and msg["truth"] == "Lie":
                curr_phase_lies.append(msg)

        if len(curr_phase_lies) > 0:
            lies[phase] = curr_phase_lies

    return lies


def annotated_msgs(data, annotations, humans):
    """
    get all messages annotated by humans in the game

    :param data: dictionary in which key is phase and value is list of messages
    :param annotations: dictionary in which key is str(time_sent) and value is annotation
    :param humans: list of human powers in the game
    :return: a dictionary of messages, with phase as key and list of messages as value
    """
    msgs = {}
    msgs_to_humans_by_phase = msgs_to_humans(data, humans)
    time_sents = list(map(lambda x: int(x), annotations.keys()))

    for phase in msgs_to_humans_by_phase:
        curr_phase_msgs = []

        for msg in msgs_to_humans_by_phase[phase]:
            if msg["time_sent"] in time_sents:
                msg["annotation"] = annotations[str(msg["time_sent"])]
                curr_phase_msgs.append(msg)

        if len(curr_phase_msgs) > 0:
            msgs[phase] = curr_phase_msgs

    return msgs


def perceived_lies(data, annotations, humans):
    """
    get all lies perceived by humans in the game

    :param data: dictionary in which key is phase and value is list of messages
    :param annotations: dictionary in which key is str(time_sent) and value is annotation
    :param humans: list of human powers in the game
    :return: a dictionary of messages, with phase as key and list of messages as value
    """
    lies = {}
    annotated_msgs_by_phase = annotated_msgs(data, annotations, humans)

    for phase in annotated_msgs_by_phase:
        curr_phase_lies = []

        for msg in annotated_msgs_by_phase[phase]:
            if msg["annotation"] == "yes":
                curr_phase_lies.append(msg)

        if len(curr_phase_lies) > 0:
            lies[phase] = curr_phase_lies

    return lies


def order_logs_by_country(data):
    """
    reorder time_sent logs by country

    :param data: dictionary of game data after json.load
    :return: a dictionary of order logs, with phase as key and {power: {time_sent: log}} as value
    """

    logs = {}
    logs_by_phase = all_order_logs(data)

    for phase in logs_by_phase:
        curr_phase_logs = {}

        for time_sent, log in logs_by_phase[phase].items():
            time_sent = int(time_sent)
            m = re.match(order_log_regex, log)
            power = m.group(1)
            order = m.group(2)

            if power not in curr_phase_logs:
                curr_phase_logs[power] = {}

            curr_phase_logs[power][time_sent] = order

        if len(curr_phase_logs) > 0:
            logs[phase] = curr_phase_logs

    return logs


def msgs_by_time_sent(data):
    """
    sort messages by time_sent

    :param data: dictionary in which key is phase and value is list of messages
    :return: a list of messages sorted by time_sent
    """

    msgs = {}

    for phase in data:
        curr_phase_msgs = data[phase]
        sorted_msgs = {}

        for msg in curr_phase_msgs:
            time_sent = msg["time_sent"]
            sender = msg["sender"]
            recipient = msg["recipient"]
            message = msg["message"]
            truth = msg["truth"]
            msg_phase = msg["phase"]
            annotation = msg["annotation"] if "annotation" in msg else None

            sorted_msgs[time_sent] = {
                "sender": sender,
                "recipient": recipient,
                "message": message,
                "truth": truth,
                "annotation": annotation,
                "phase": msg_phase,
            }

        msgs[phase] = sorted_msgs

    return msgs


def message_channels(data, humans):
    """
    get conversations between players

    :param data: a dictionary of messages, with phase as key and list of messages as value
    :return: a dictionary of messages, with {POWER1}-{POWER2} as key and {phase: {time_sent: msg_obj}} as value
    """
    convos = {}

    for power1 in POWERS:
        for power2 in POWERS:
            if power1 != power2 and (power1 in humans or power2 in humans):
                sorted_powers = sorted([power1, power2])
                convo_key = sorted_powers[0] + "-" + sorted_powers[1]

                if convo_key not in convos:
                    convos[convo_key] = {}

    for phase in data:
        for time_sent, msg in data[phase].items():
            sender = msg["sender"]
            recipient = msg["recipient"]

            if (
                sender not in POWERS
                or recipient not in POWERS
                or (sender not in humans and recipient not in humans)
            ):
                continue

            sorted_powers = sorted([sender, recipient])
            convo_key = sorted_powers[0] + "-" + sorted_powers[1]

            if phase not in convos[convo_key]:
                convos[convo_key][phase] = {}

            convos[convo_key][phase][time_sent] = msg

    return convos


def combine_msgs_orders(convos, orders, humans):
    """
    combine messages and orders by time_sent

    :param convos: message_channels() output
    :param orders: all_order_logs() output
    :return: a dictionary of order logs, with phase as key and {power: {time_sent: log}} as value
    """
    convos_with_orders = convos

    for phase in orders:
        for time_sent, log in orders[phase].items():
            time_sent = int(time_sent)
            m = re.match(order_log_regex, log)
            if not m:
                continue
            power = m.group(1)
            order = m.group(2)

            for convo in convos_with_orders:
                if power in convo and phase in convos_with_orders[convo].keys():
                    convos_with_orders[convo][phase][time_sent] = log

    for convo in convos_with_orders:
        power1, power2 = convo.split("-")

        for phase in convos_with_orders[convo]:
            if phase[-1] != "M":
                continue

            power_msg_logs = {power1: {}, power2: {}}
            initial_orders = {power1: [], power2: []}

            for time_sent, msg in convos_with_orders[convo][phase].items():
                if isinstance(msg, str):
                    m = re.match(order_log_regex, msg)
                    power = m.group(1)

                    if power == power1:
                        power_msg_logs[power1][time_sent] = msg
                    if power == power2:
                        power_msg_logs[power2][time_sent] = msg
                    if power != power1 and power != power2:
                        raise Exception("power not in convo", power, convo)
                else:
                    sender = msg["sender"]

                    if sender == power1:
                        power_msg_logs[power1][time_sent] = msg
                    if sender == power2:
                        power_msg_logs[power2][time_sent] = msg
                    if sender != power1 and sender != power2:
                        raise Exception("sender not in convo", sender, convo)

            for power in [power1, power2]:
                if power not in humans:
                    continue

                cache = {}

                if phase == "S1904M" and convo == "AUSTRIA-ITALY":
                    pass
                    #print(sorted(power_msg_logs[power].items()))

                for time_sent, msg_order in sorted(power_msg_logs[power].items()):
                    if isinstance(msg_order, str):
                        cache[time_sent] = power_msg_logs[power].pop(time_sent)
                    else:
                        reduced_orders = reduce_duplicate_orders(cache)[power]
                        initial_orders[power] = sorted(reduced_orders)
                        cache = {}
                        break

                if len(cache) > 0:
                    reduced_orders = reduce_duplicate_orders(cache)[power]
                    initial_orders[power] = sorted(reduced_orders)

            updated_dict = {}

            for power in [power1, power2]:
                updated_dict.update(power_msg_logs[power])

            updated = {}
            cache = {}

            for time_sent, log in sorted(updated_dict.items()):
                if isinstance(log, str):
                    cache[time_sent] = log
                else:
                    if len(cache) == 0:
                        updated[time_sent] = log
                        continue
                    else:
                        reduced_orders = reduce_duplicate_orders(cache)
                        updated[time_sent - 1] = reduced_orders
                        cache = {}
                        updated[time_sent] = log

            if len(cache) > 0:
                reduced_orders = reduce_duplicate_orders(cache)
                updated[time_sent] = reduced_orders

            updated[0] = initial_orders

            # sort updated by key
            updated = dict(sorted(updated.items()))
            convos_with_orders[convo][phase] = updated

    return convos_with_orders


def reduce_duplicate_orders(orders):
    """
    simplify orders

    :param orders: a dict of orders
    :return: a dictionary of {power: [orders]}
    """
    remove_all_regex = r"([A-Z]+) removed its orders\:"
    add_order_regex = r"([A-Z]+) added\:\W([A-Z]\W[A-Z]{3})(.*)"
    remove_order_regex = r"([A-Z]+) removed\:\W([A-Z]\W[A-Z]{3})(.*)"
    cleaned_orders = {}

    for time_sent, order_log in orders.items():
        if "updated" in order_log:
            continue

        m = re.match(remove_all_regex, order_log)
        if m:
            power = m.group(1)
            cleaned_orders[power] = {}
            continue

        m = re.match(add_order_regex, order_log)
        if m:
            power = m.group(1)
            unit = m.group(2)
            move = m.group(3)

            if power not in cleaned_orders:
                cleaned_orders[power] = {}

            cleaned_orders[power][unit] = move
            continue

        m = re.match(remove_order_regex, order_log)
        if m:
            power = m.group(1)
            unit = m.group(2)
            move = m.group(3)

            if power in cleaned_orders and unit in cleaned_orders[power]:
                del cleaned_orders[power][unit]

            continue

    results = {}
    for power in cleaned_orders:
        results[power] = []
        moves = cleaned_orders[power]

        for unit, move in moves.items():
            results[power].append(unit + move)

        results[power].sort()
    return results


def start_phase_logs(data):
    """
    get cicero's start of phase logs in the game

    :param data: dictionary of game data after json.load
    :return: a dictionary of logs
    """

    start_phase_log_regex = r"At the start of this phase\, I intend to do: \((.*)\)"
    start_phase_logs = {}

    all_cicero_logs = all_logs(data)

    for phase, logs in all_cicero_logs.items():
        current_phase_logs = {}

        for log in logs:
            log_sender = log["sender"]
            m = re.match(start_phase_log_regex, log["message"])
            if m:
                orders = m.group(1).split(",")

                stripped_orders = map(lambda x: x.replace("'", "").strip(), orders)
                filtered_orders = filter(lambda x: x != "", stripped_orders)
                current_phase_logs[log_sender] = list(filtered_orders)

        if len(current_phase_logs) > 0:
            start_phase_logs[phase] = current_phase_logs

    return start_phase_logs


def add_start_phase_logs_to_msg_orders(msg_orders, start_phase_logs, bots):
    """
    add cicero's start of phase logs to message orders

    :param msg_orders: existing message orders
    :param start_phase_logs: cicero logs
    :param bots: a list of powers that has cicero prefix usernames
    :return: message orders with cicero's start of phase logs
    """

    for convo, phases in msg_orders.items():
        power1, power2 = convo.split("-")

        for phase, msg_logs in phases.items():
            if 0 not in msg_logs:
                start_of_phase_orders = {}
            else:
                start_of_phase_orders = msg_logs[0]

            if phase in start_phase_logs:
                cicero_logs = start_phase_logs[phase]

                if power1 in bots and power1 in cicero_logs:
                    start_of_phase_orders[power1] = sorted(cicero_logs[power1])

                if power2 in bots and power2 in cicero_logs:
                    start_of_phase_orders[power2] = sorted(cicero_logs[power2])

                msg_logs[0] = start_of_phase_orders
                phases[phase] = msg_logs

        msg_orders[convo] = phases

    return msg_orders


def add_end_phase_orders_to_msg_orders(msg_orders, end_phase_orders):
    """
    add order results to message orders

    :param msg_orders: existing message orders
    :param end_phase_orders: order results for each power for each phase
    :return: message orders with end of phase orders
    """

    for convo, phases in msg_orders.items():
        power1, power2 = convo.split("-")

        for phase, msg_logs in phases.items():
            power1_orders = end_phase_orders[phase][power1]
            power2_orders = end_phase_orders[phase][power2]
            results = {power1: power1_orders, power2: power2_orders}
            msg_logs["end_phase_orders"] = results
            phases[phase] = msg_logs

        msg_orders[convo] = phases

    return msg_orders


def filter_persuations(message_orders):
    filtered = {}

    for convo, phases in message_orders.items():
        filtered[convo] = {}
        power1, power2 = convo.split("-")

        for phase, msg_logs in phases.items():
            if phase[-1] != "M":
                continue

            power1_start = sorted(msg_logs[0][power1])
            power1_end = sorted(msg_logs["end_phase_orders"][power1])

            power2_start = sorted(msg_logs[0][power2])
            power2_end = sorted(msg_logs["end_phase_orders"][power2])

            if power1_start == power1_end and power2_start == power2_end:
                continue
            else:
                filtered[convo][phase] = msg_logs

    return filtered


def filter_location(mapping, data, state_history, mention_country=True):
    filtered = {}

    for convo, phases in data.items():
        power1, power2 = convo.split("-")
        filtered[convo] = {}

        for phase, msg_logs in phases.items():
            if phase[-1] != "M":
                continue

            curr_msg_logs = {}
            curr_msg_logs["mentioned"] = []
            influence_history = state_history[phase]["influence"]

            start_of_phase_orders = msg_logs.pop(0)
            end_of_phase_orders = msg_logs.pop("end_phase_orders")

            # get difference between start and end of phase orders
            power1_start = set(start_of_phase_orders[power1])
            power1_end = set(end_of_phase_orders[power1])

            power2_start = set(start_of_phase_orders[power2])
            power2_end = set(end_of_phase_orders[power2])

            power1_end_diff = sorted(list(power1_end.difference(power1_start)))
            power2_end_diff = sorted(list(power2_end.difference(power2_start)))

            power1_start_diff = sorted(list(power1_start.difference(power1_end)))
            power2_start_diff = sorted(list(power2_start.difference(power2_end)))

            if len(power1_end_diff) == 0 and len(power2_end_diff) == 0:
                continue

            curr_msg_logs["start"] = {}
            curr_msg_logs["end"] = {}
            curr_msg_logs["messages"] = list(msg_logs.values())

            if len(power1_start_diff) > 0:
                curr_msg_logs["start"][power1] = power1_start_diff
            if len(power2_start_diff) > 0:
                curr_msg_logs["start"][power2] = power2_start_diff

            if len(power1_end_diff) > 0:
                curr_msg_logs["end"][power1] = power1_end_diff
            if len(power2_end_diff) > 0:
                curr_msg_logs["end"][power2] = power2_end_diff

            for _, msg in msg_logs.items():
                if isinstance(msg, dict) and "message" in msg.keys():
                    split_msg = split_sentence(msg["message"].lower())

                    for word in split_msg:
                        for loc, variations in mapping.items():
                            # if the mentioned location is reflected in the orders
                            are_locs_in_orders = [
                                loc.upper() in order
                                for order in power1_end_diff + power2_end_diff
                            ]

                            if word == loc.lower() and (
                                len(are_locs_in_orders) > 0 and any(are_locs_in_orders)
                            ):
                                curr_msg_logs["mentioned"].append(loc)
                            for variation in variations:
                                if word == variation.lower() and (
                                    len(are_locs_in_orders) > 0
                                    and any(are_locs_in_orders)
                                ):
                                    curr_msg_logs["mentioned"].append(loc)

                        if mention_country:
                            for power, variation in power_mapping.items():
                                influence = influence_history[power.upper()]

                                are_locs_in_orders = [
                                    loc.upper() in order
                                    for order in power1_end_diff + power2_end_diff
                                    for loc in influence
                                ]

                                if (
                                    word == power
                                    and power
                                    not in [
                                        power1.lower(),
                                        power2.lower(),
                                    ]
                                    and (
                                        len(are_locs_in_orders) > 0
                                        and any(are_locs_in_orders)
                                    )
                                ):
                                    curr_msg_logs["mentioned"].append(power)
                                if (
                                    word == variation
                                    and power
                                    not in [
                                        power1.lower(),
                                        power2.lower(),
                                    ]
                                    and (
                                        len(are_locs_in_orders) > 0
                                        and any(are_locs_in_orders)
                                    )
                                ):
                                    curr_msg_logs["mentioned"].append(power)

            if len(curr_msg_logs["mentioned"]) > 0:
                filtered[convo][phase] = curr_msg_logs

    return filtered


def split_sentence(sentence):
    delimiters = [",", " ", "-", ";", "/", "!", "?", ".", ":", "'", '"']

    for delimiter in delimiters:
        sentence = " ".join(sentence.split(delimiter))

    return sentence.split()


def prettier(data):
    data_copy = {}

    for convo, phases in data.items():
        data_copy[convo] = {}

        for phase, msg_logs in phases.items():
            data_copy[convo][phase] = {}
            convo_msgs = []

            start = msg_logs.pop("start")
            end = msg_logs.pop("end")
            mentioned = list(set(msg_logs.pop("mentioned")))

            data_copy[convo][phase]["mentioned"] = mentioned
            data_copy[convo][phase]["start"] = start
            data_copy[convo][phase]["end"] = end

            for msg in msg_logs["messages"]:
                if "sender" in msg and "message" in msg:
                    convo_msgs.append(f'{msg["sender"]}: {msg["message"]}')

            data_copy[convo][phase]["messages"] = convo_msgs

    return data_copy


def llm(data):
    file = "persuation_txts/AIGame_0"
    sys_prompt = "The following is a conversation happened in a turn of diplomacy game containing two powers. Below lists their initial and final order as well as the messages. Determine if the order changed by a power corelates to being persuaded by the other power. \
Answer yes if the location mentioned is reflected in the orders; \
answer need more information if a power is but no locations are mentioned; \
answer no if the conversation does not involve persuasion/suggestion, if powers are stating their moves, if the other power did not take the suggestion, and if the change of orders are unrelated to the suggestion.\n\
###"
    prompt = ""

    for convo, phases in data.items():
        with open(file, "a") as f:
            f.write(f"{convo}\n")
        f.close()
        # text += f'{convo}\n'

        for phase, msg_logs in phases.items():
            with open(file, "a") as f:
                f.write(f"{phase}\n")
            f.close()
            # text += f'{phase}\n'

            start = msg_logs.pop("start")
            end = msg_logs.pop("end")
            mentioned = list(set(msg_logs.pop("mentioned")))

            with open(file, "a") as f:
                f.write(f"mentioned: ")
                f.write(", ".join(mentioned))
                f.write("\n")
            f.close()
            # text += f'mentioned: '
            # text += ', '.join(mentioned)
            # text += '\n'
            for power, orders in start.items():
                for order in orders:
                    prompt += f"{power} start: {order}\n"
                    # text += f'\t{power} start: {order}\n'

            text += "\n"

            for power, orders in end.items():
                for order in orders:
                    text += f"\t{power} final: {order}\n"

            for msg in msg_logs["messages"]:
                if "sender" in msg and "message" in msg:
                    text += f'{msg["sender"]}: {msg["message"]}\n'

            text += "\n"

    return text


def lies(output_file, message_history, annotated_messages, humans):
    output_path = f"lies/{output_file}.json"
    perceived_lies = []
    actual_lies = []
    perceived_lies_from_human = 0
    perceived_lies_from_cicero = 0
    actual_lies_count = 0
    total_msgs = 0
    perceived_and_actual = 0
    human_outgoing = 0
    human_incoming = 0
    human_incoming_and_outgoing = 0

    for phase, msgs in message_history.items():
        for msg in msgs:
            if msg['sender'] == 'omniscient_type' or msg['recipient'] == 'GLOBAL':
                continue
            total_msgs += 1
            if msg["sender"] in humans:
                human_outgoing += 1
            if msg["recipient"] in humans:
                human_incoming += 1
            if msg["sender"] in humans and msg["recipient"] in humans:
                human_incoming_and_outgoing += 1
            if msg["truth"] == "Lie":
                actual_lies.append(msg)
                actual_lies_count += 1
            if str(msg["time_sent"]) in annotated_messages:
                if annotated_messages[str(msg["time_sent"])] == "yes":
                    perceived_lies.append(msg)
                    if msg["sender"] in humans:
                        perceived_lies_from_human += 1
                    else:
                        perceived_lies_from_cicero += 1

                    if msg["truth"] == "Lie":
                        perceived_and_actual += 1
                        pass
                        #print(f'perceived and actual: {msg["message"]}')

    with open(output_path, "w") as f:
        json.dump(
            {"perceived_lies": perceived_lies, "actual_lies": actual_lies}, f, indent=4
        )

    return perceived_lies_from_human, perceived_lies_from_cicero, actual_lies_count, total_msgs, perceived_and_actual, human_outgoing, human_incoming, human_incoming_and_outgoing

def expect_to_do(output_file, log_history, order_history, humans):
    output_path = f'cicero_preds/{output_file}.json'
    output = {}
    expect_regex = r"I expect ([A-Z]+) to do: \((.*)\)"
    for phase, logs in log_history.items():
        if not phase.endswith("M"):
            continue
        if phase not in output:
            output[phase] = {}
            sorted_orders = {}
            for power, orders in order_history[phase].items():
                sorted_orders[power] = sorted(orders)
            output[phase]["actual"] = sorted_orders
            output[phase]["expected"] = {}
        for log in logs:
            m = re.search(expect_regex, log["message"])
            if m:
                sender = log["sender"]
                time_sent = log["time_sent"]
                recipient = m.group(1)
                if sender not in output[phase]['expected']:
                    output[phase]["expected"][sender] = {}
                orders = m.group(2).split(",")
                orders = list(map(lambda x: x.strip().replace("'", ""), orders))
                orders = list(filter(lambda x: x != "", orders))
                orders = sorted(orders)
                if (
                    recipient not in output[phase]["expected"][sender]
                    or output[phase]["expected"][sender][recipient][0] < time_sent
                ):
                    output[phase]["expected"][sender][recipient] = (
                        time_sent,
                        orders,
                    )
    with open(output_path, "w") as f:
        json.dump(output, f, indent=4)

    human_correct = 0
    human_total = 0
    cicero_correct = 0
    cicero_total = 0

    for phase, logs in output.items():
        expected = logs["expected"]
        actual = logs["actual"]

        for power, expectations in expected.items():
            for expected_power, arr in expectations.items():
                expected_orders = arr[1]
                actual_orders = actual[expected_power]
                if len(expected_orders) != len(actual_orders):
                    continue
                if expected_power in humans:
                    human_total += len(expected_orders)
                    for order in expected_orders:
                        if order in actual_orders:
                            human_correct += 1
                else:
                    cicero_total += len(expected_orders)
                    for order in expected_orders:
                        if order in actual_orders:
                            cicero_correct += 1

    print(f"human: {human_correct / human_total * 100}")
    print(f"cicero: {cicero_correct / cicero_total * 100}")
    return human_correct, human_total, cicero_correct, cicero_total
            

def simplify_orders(orders):
    add_order_regex = r'^([A-Z]+)\Wadded:\W([A-Z]\W[A-Z]{3})(.*)$'
    remove_order_regex = r'^([A-Z]+)\Wremoved:\W([A-Z]\W[A-Z]{3})(.*)'
    remove_all_orders_regex = r'^([A-Z]+)\Wremoved\Wits\Worders:$'
    final_orders = {}

    for _ , order_str in orders.items():
        if re.match(remove_all_orders_regex, order_str):
            power = re.match(remove_all_orders_regex, order_str).group(1)
            final_orders[power] = {}
        elif re.match(remove_order_regex, order_str):
            power = re.match(remove_order_regex, order_str).group(1)
            unit = re.match(remove_order_regex, order_str).group(2)
            unit_order = re.match(remove_order_regex, order_str).group(3)
            order = unit + unit_order

            if power in final_orders and order in final_orders[power]:
                del final_orders[power][unit]
        elif re.match(add_order_regex, order_str):
            power = re.match(add_order_regex, order_str).group(1)
            unit = re.match(add_order_regex, order_str).group(2)
            unit_order = re.match(add_order_regex, order_str).group(3)
            order = unit + unit_order

            if not power in final_orders:
                final_orders[power] = {unit: order}
            else:
                final_orders[power][unit] = order

    result = {}
    for power, orders in final_orders.items():
        result[power] = sorted(orders.values())

    return result

def human_intent_start_phase(output_file, data):
    output_path = f"human_intents/{output_file}.json"

    order_logs = all_order_logs(data)
    message_history = all_msgs(data)
    power_regex = r'^([A-Z]+)\W'

    initial_orders = {}
    first_msg_timestamps = {}

    for phase, logs in order_logs.items():
        if not phase.endswith("M"):
            continue
        if phase not in initial_orders:
            initial_orders[phase] = {}

        first_msg_timestamp_this_phase = {}
        initial_order_log_this_phase = {}

        for msg in message_history[phase]:
            sender = msg["sender"]
            if sender not in first_msg_timestamp_this_phase:
                first_msg_timestamp_this_phase[sender] = msg["time_sent"]
            elif msg['time_sent'] < first_msg_timestamp_this_phase[sender]:
                first_msg_timestamp_this_phase[sender] = msg["time_sent"]

        first_msg_timestamps[phase] = first_msg_timestamp_this_phase

        for timestamp, log in logs.items():
            if log.startswith("omniscient_type"):
                continue
            power = re.match(power_regex, log).group(1)

            if power not in first_msg_timestamp_this_phase or int(timestamp) <= int(first_msg_timestamp_this_phase[power]):
                initial_order_log_this_phase[timestamp] = log

            initial_orders[phase] = initial_order_log_this_phase

        initial_orders[phase] = simplify_orders(initial_orders[phase])

    with open(output_path, "w") as f:
        json.dump(initial_orders, f, indent=4)
    return initial_orders


############## main ##############


def main():
    # list of games to extract
    games = list(
        map(
            lambda x: game_dir + x,
            filter(lambda x: x.endswith(".json"), os.listdir(game_dir)),
        )
    )

    with open("mapping_province.json", "r") as f:
        mapping = json.load(f)

    scs = {}
    cicero_scs = {}
    is_bot_f1 = []
    precisions = []
    recalls = []
    human_powers = {}

    ht = 0
    hc = 0
    ct = 0
    cc = 0

    total_perceived_from_human = 0
    total_perceived_from_cicero = 0
    total_actual = 0
    total_count = 0
    total_perceived_and_actual = 0
    total_human_outgoing = 0
    total_human_incoming = 0
    total_human_incoming_and_outgoing = 0

    for game in games:
        with open(game, "r") as f:
            data = json.load(f)

        print(data["game_id"])
        if data["game_id"] == "beta_de_2":
            continue

        humans = human_players(data)
        ciceros = bot_players(data)
        if len(humans) + len(ciceros) != 7:
            print(data['game_id'])
            print('missing players')
            print(humans)
        is_bots = data["is_bot"]

        for human in humans:
            if human not in human_powers:
                human_powers[human] = 0
            human_powers[human] += 1

        perceived_lies_from_human, perceived_lies_from_cicero, actual_lies_count, total_msgs, perceived_and_actual, human_outgoing, human_incoming, human_incoming_and_outgoing = lies(data["game_id"], all_msgs(data), all_annotations(data), humans)
        total_perceived_from_human += perceived_lies_from_human
        total_perceived_from_cicero += perceived_lies_from_cicero
        total_actual += actual_lies_count
        total_count += total_msgs
        total_perceived_and_actual += perceived_and_actual
        total_human_outgoing += human_outgoing
        total_human_incoming += human_incoming
        total_human_incoming_and_outgoing += human_incoming_and_outgoing

        human_intent_start_phase(data["game_id"], data)
        human_correct, human_total, cicero_correct, cicero_total = expect_to_do(data["game_id"], all_logs(data), all_orders(data), humans)
        ht += human_total
        hc += human_correct
        ct += cicero_total
        cc += cicero_correct

        for power, predictions in is_bots.items():
            player = get_player_name(data, power)

            # f1 accracy for identifying bots
            ground_truth_set = set(ciceros)
            y_true = [power in ground_truth_set for power in sorted(predictions.keys())]
            y_pred = [predictions[power] for power in sorted(predictions.keys())]
            score = f1_score(y_true, y_pred, average="binary")
            is_bot_f1.append(score)
            precisions.append(precision_score(y_true, y_pred, average="binary"))
            recalls.append(recall_score(y_true, y_pred, average="binary"))
            print(f"{player}: {score}")

        for p in humans:
            # print(f"{p}: {get_player_name(data, p)}")

            if p not in scs:
                scs[p] = []

            scs[p].append(len(data["powers"][p]["centers"]))

        for p in ciceros:
            if p not in cicero_scs:
                cicero_scs[p] = []

            cicero_scs[p].append(len(data["powers"][p]["centers"]))

        msgs = all_msgs(data)
        sorted_msgs = msgs_by_time_sent(msgs)
        convos = message_channels(sorted_msgs, human_players(data))

        msg_orders = combine_msgs_orders(
            convos, all_order_logs(data), human_players(data)
        )

        cicero_start_of_phase_logs = start_phase_logs(data)

        with_cicero_start_phase_logs = add_start_phase_logs_to_msg_orders(
            msg_orders, cicero_start_of_phase_logs, bot_players(data)
        )

        end_phase_added = add_end_phase_orders_to_msg_orders(
            with_cicero_start_phase_logs, all_orders(data)
        )

        filtered = filter_persuations(end_phase_added)

        filtered_again = filter_location(mapping, filtered, get_state_history(data))

        prettified = prettier(copy.deepcopy(filtered_again))

        with open(f"persuations/{data['game_id']}.json", "w") as f:
            json.dump(
                prettified,
                f,
                indent=4,
            )
        f.close()

        print("\n")

    # sort hunan powers by value
    sorted_human_powers = {k: v for k, v in sorted(human_powers.items(), key=lambda item: item[1])}
    print(sorted_human_powers)
    
    print(f"human: {hc / ht * 100}")
    print(f"cicero: {cc / ct * 100}")
    # calculate supply centers for each power
    avg_scs = {k: (sum(v) / len(v)) for k, v in scs.items()}
    sorted_avg_scs = {k: v for k, v in sorted(avg_scs.items(), key=lambda item: item[0])}
    print(sorted_avg_scs)
    avg_cicero_scs = {k: (sum(v) / len(v)) for k, v in cicero_scs.items()}
    sorted_avg_cicero_scs = {k: v for k, v in sorted(avg_cicero_scs.items(), key=lambda item: item[0])}
    print('avg: ', sorted_avg_cicero_scs)
    elo = {}
    perf_elo = {}

    for game in games:
        with open(game, "r") as f:
            data = json.load(f)

        for p in humans:
            username = get_player_name(data, p)
            if username == 'human':
                continue
            perf = performance_mapping[username]

            # print(f"{p}: {get_player_name(data, p)}")

            if username not in elo:
                elo[username] = 0
            if perf not in perf_elo:
                perf_elo[perf] = 0

            diff = len(data["powers"][p]["centers"]) - avg_scs[p]

            elo[username] += diff
            if perf == 0:
                continue
            perf_elo[perf] += diff

    print({k:v for k, v in sorted(elo.items(), key=lambda item: item[1])})
    print({k:v for k, v in sorted(perf_elo.items(), key=lambda item: item[1])})
    print(f"perceived from human: {total_perceived_from_human}")
    print(f"perceived from cicero: {total_perceived_from_cicero}")
    print(f"actual: {total_actual}")
    print(f"total: {total_count}")
    print(f"perceived and actual: {total_perceived_and_actual}")
    print(f'perceived: {(total_perceived_from_human + total_perceived_from_cicero) / total_human_incoming * 100}')
    print(f'actual: {total_actual / total_human_outgoing * 100}')
    print(f'perceived and actual: {total_perceived_and_actual / total_human_incoming_and_outgoing * 100}')
    print(f'is_bot_f1: {sum(is_bot_f1) / len(is_bot_f1)}')
    print(f'precision: {sum(precisions) / len(precisions)}')
    print(f'recall: {sum(recalls) / len(recalls)}')

    """with open(game_dir + "AIGame_0.json", "r") as f:
        data = json.load(f)

    msgs = all_msgs(data)
    sorted_msgs = msgs_by_time_sent(msgs)
    convos = message_channels(sorted_msgs, human_players(data))

    msg_orders = combine_msgs_orders(
        convos, all_order_logs(data), human_players(data)
    )

    cicero_start_of_phase_logs = start_phase_logs(data)

    with_cicero_start_phase_logs = add_start_phase_logs_to_msg_orders(
        msg_orders, cicero_start_of_phase_logs, bot_players(data)
    )

    end_phase_added = add_end_phase_orders_to_msg_orders(
        with_cicero_start_phase_logs, all_orders(data)
    )

    filtered = filter_persuations(end_phase_added)

    filtered_again = filter_location(mapping, filtered, get_state_history(data))

    #llm(filtered_again)
    """


if __name__ == "__main__":
    main()
