import os, json, re
import numpy as np

game_dir = "./human_games/"
POWERS = ["AUSTRIA", "ENGLAND", "FRANCE", "GERMANY", "ITALY", "RUSSIA", "TURKEY"]

power_mapping = {
    "russia": "rus",
    "austria": "aus",
    "england": "eng",
    "france": "fra",
    "germany": "ger",
    "italy": "ita",
    "turkey": "tur",
}

def get_human_players(data):
    """
    get all human players in the game

    :param data: dictionary of game data after json.load
    :return: a list of powers that does not have cicero prefix usernames
    """
    bots = get_bot_players(data)
    humans = []

    for power in POWERS:
        if power not in bots:
            humans.append(power)

    return humans

def get_bot_players(data):
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

def main():
    games = list(
        map(
            lambda x: game_dir + x,
            filter(lambda x: x.endswith(".json"), os.listdir(game_dir)),
        )
    )

    with open("mapping_province.json", "r") as f:
        mapping = json.load(f)

    for game in games:
        with open(game, "r") as f:
            data = json.load(f)

        messages_flattened = []

        message_history = data["message_history"]

        human_players = get_human_players(data)
        bot_players = get_bot_players(data)

        human_msg_cnt = {}
        bot_msg_cnt = {}

        for _, messages in message_history.items():
            for message in messages:
                messages_flattened.append(message)

        for message in messages_flattened:
            phase = message["phase"]
            if phase[-1] != "M":
                continue
            sender = message["sender"]
            if sender in human_players:
                if phase not in human_msg_cnt:
                    human_msg_cnt[phase] = 1
                else:
                    human_msg_cnt[phase] += 1
            elif sender in bot_players:
                if phase not in bot_msg_cnt:
                    bot_msg_cnt[phase] = 1
                else:
                    bot_msg_cnt[phase] += 1

        human_msg_avg = {}
        bot_msg_avg = {}

        for phase, cnt in human_msg_cnt.items():
            human_msg_avg[phase] = round(cnt / len(human_players), 2)

        for phase, cnt in bot_msg_cnt.items():
            bot_msg_avg[phase] = round(cnt / len(bot_players), 2)
                

        with open(f"stats/{data['game_id']}.json", "w") as f:
            json.dump(
                {
                    "human_msg_avg": human_msg_avg,
                    "bot_msg_avg": bot_msg_avg,
                },
                f,
                indent=4,
            )

if __name__ == "__main__":
    main()
