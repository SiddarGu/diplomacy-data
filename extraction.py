import os, json, re
game_dir = './games/'
POWERS = ['AUSTRIA', 'ENGLAND', 'FRANCE', 'GERMANY', 'ITALY', 'RUSSIA', 'TURKEY']
order_log_regex = r'([A-Z]+)\W(.*)'

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
    all_powers = data['powers']

    for power in all_powers:
        power_controllers = all_powers[power]['controller']

        for controller in power_controllers.values():
            if controller not in bots and controller.startswith('cicero'):
                bots.append(power)

    return bots

def num_phases(data):
    """
    get number of phases played in the game

    :param data: dictionary of game data after json.load
    :return: integer of number of phases played
    """ 
    return len(data['state_history'])

def num_phases_with_msg(data):
    """
    get number of phases with messages in the game

    :param data: dictionary of game data after json.load
    :return: integer of number of phases with messages, which should be the same or less than num_phases
    """ 

    cnt = 0
    message_history = data['message_history']

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
    return data['log_history']

def all_orders(data):
    """
    get the final orders for each power for each phase in the game

    :param data: dictionary of game data after json.load

    :return: a dictionary of logs, with phase as key and {power: [orders]} as value
    """ 
    return data['order_history']

def all_stances(data):
    """
    get the player stances for each power for each phase in the game
    stance ranges from 1 to 5, with 1 being very hostile and 5 being very friendly
    :param data: dictionary of game data after json.load

    :return: a dictionary of stances, with phase as key and {power: {stance_power: stance}} as value
    """ 

    return data['stance_history']

def perceived_bots(data):
    """
    get the player perceptions of the bots
    :param data: dictionary of game data after json.load

    :return: a dictionary with phase as key and {power: {stance_power: bool}} as value
    """ 

    return data['is_bot_history']

def all_order_logs(data):
    """
    get the logs of orders for each player for each phase in the game
    :param data: dictionary of game data after json.load

    :return: a dictionary with phase as key and {str(time_sent): log} as value
    """ 

    return data['order_log_history']

def all_msgs(data):
    """
    get all messages in the game

    :param data: dictionary of game data after json.load
    :return: a dictionary of messages, with phase as key and list of messages as value
    """ 

    return data['message_history']

def all_annotations(data):
    """
    get all annotations in the game

    :param data: dictionary of game data after json.load
    :return: a dictionary of annotations, with phase as key and list of annotations as value
    """ 

    return data['annotated_messages']

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
            if msg['sender'] in humans:
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
    #msgs_by_phase = all_msgs(data)
    #humans = human_players(data)

    for phase in data:
        curr_phase_msgs = []

        for msg in data[phase]:
            if msg['recipient'] in humans:
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
    #humans = human_players(data)

    for phase in msgs_from_humans_by_phase:
        curr_phase_msgs = []
        
        for msg in msgs_from_humans_by_phase[phase]:
            if msg['recipient'] in humans:
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
            if msg['truth'] is not None and msg['truth'] == 'Lie':
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
            if msg['time_sent'] in time_sents:
                msg['annotation'] = annotations[str(msg['time_sent'])]
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
            if msg['annotation'] == 'yes':
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
    msgs = {}
    
    for phase in data:
        curr_phase_msgs = data[phase]
        sorted_msgs = {}

        for msg in curr_phase_msgs:
            time_sent = msg['time_sent']
            sender = msg['sender']
            recipient = msg['recipient']
            message = msg['message']
            truth = msg['truth']
            annotation = msg['annotation'] if 'annotation' in msg else None

            sorted_msgs[time_sent] = {
                'sender': sender,
                'recipient': recipient,
                'message': message,
                'truth': truth,
                'annotation': annotation
            }

        sorted_msgs = {k: v for k, v in sorted(sorted_msgs.items(), key=lambda item: item[0])}
        msgs[phase] = sorted_msgs

    return msgs
    

def combine_msgs_orders(data):
    """
    combine messages and orders by time_sent

    :param data: dictionary of game data after json.load
    :return: a dictionary of order logs, with phase as key and {power: {time_sent: log}} as value
    """ 

    pass


############## main ##############

def main():
    # list of games to extract
    games = list(map(lambda x: game_dir + x, filter(lambda x: x.endswith('.json'), os.listdir(game_dir))))

    for game in games:
        with open(game, 'r') as f:
            data = json.load(f)

        print(data['game_id'])
        humans = human_players(data)
        annotations = all_annotations(data)
        print('human players: ', humans)
        print('bot players: ', bot_players(data))
        print('number of phases: ', num_phases(data))
        print('number of phases with messages: ', num_phases_with_msg(data))
        all_messages = all_msgs(data)
        print('all messages: ', len(all_messages))
        print('messages from humans: ', len(msgs_from_humans(all_messages, humans)))
        print('messages to humans: ', len(msgs_to_humans(all_messages, humans)))
        print('messages from humans to humans: ', len(msgs_from_to_humans(all_messages, humans)))
        print('human lies: ', len(human_lies(all_messages, humans)))
        print('annotated messages: ', len(annotated_msgs(all_messages, annotations, humans)))
        print('perceived lies: ', len(perceived_lies(all_messages, annotations, humans)))
        logs = all_logs(data)
        orders = all_orders(data)
        stances = all_stances(data)
        is_bot = perceived_bots(data)
        order_logs = all_order_logs(data)
        print('\n')
        print(order_logs_by_country(data))
        break

if __name__ == '__main__':
    main()