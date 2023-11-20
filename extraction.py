import os, json, re

game_dir = "./human_games/"
POWERS = ["AUSTRIA", "ENGLAND", "FRANCE", "GERMANY", "ITALY", "RUSSIA", "TURKEY"]
order_log_regex = r"([A-Z]+)\W(.*)"


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


def num_phases(data):
    """
    get number of phases played in the game

    :param data: dictionary of game data after json.load
    :return: integer of number of phases played
    """
    return len(data["state_history"])


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


def message_channels(data):
    """
    get conversations between players

    :param data: a dictionary of messages, with phase as key and list of messages as value
    :return: a dictionary of messages, with {POWER1}-{POWER2} as key and {phase: {time_sent: msg_obj}} as value
    """
    convos = {}

    for power1 in POWERS:
        for power2 in POWERS:
            if power1 != power2:
                sorted_powers = sorted([power1, power2])
                convo_key = sorted_powers[0] + "-" + sorted_powers[1]

                if convo_key not in convos:
                    convos[convo_key] = {}

    for phase in data:
        for time_sent, msg in data[phase].items():
            sender = msg["sender"]
            recipient = msg["recipient"]

            if sender not in POWERS or recipient not in POWERS:
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
                for time_sent, msg_order in sorted(power_msg_logs[power].items()):
                    if isinstance(msg_order, str):
                        cache[time_sent] = power_msg_logs[power].pop(time_sent)
                    else:
                        reduced_orders = reduce_duplicate_orders(cache)[power]
                        initial_orders[power] = reduced_orders
                        cache = {}
                        break

                if len(cache) > 0:
                    reduced_orders = reduce_duplicate_orders(cache)[power]
                    initial_orders[power] = reduced_orders

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
                current_phase_logs[log_sender] = list(stripped_orders)

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
                    start_of_phase_orders[power1] = cicero_logs[power1]

                if power2 in bots and power2 in cicero_logs:
                    start_of_phase_orders[power2] = cicero_logs[power2]

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


############## main ##############


def main():
    # list of games to extract
    games = list(
        map(
            lambda x: game_dir + x,
            filter(lambda x: x.endswith(".json"), os.listdir(game_dir)),
        )
    )

    for game in games:
        with open(game, "r") as f:
            data = json.load(f)

        print(data["game_id"])
        msgs = all_msgs(data)
        sorted_msgs = msgs_by_time_sent(msgs)
        convos = message_channels(sorted_msgs)

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

        with open("test.json", "w") as f:
            json.dump(
                filtered,
                f,
                indent=4,
            )

        print("\n")
        break


if __name__ == "__main__":
    main()
