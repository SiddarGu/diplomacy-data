import os, json, re
import numpy as np
import matplotlib.pyplot as plt

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

    total_humans = {}
    total_bots = {}
    human_msg_cnt = {}
    bot_msg_cnt = {}
    human_token_cnt = {}
    bot_token_cnt = {}

    with open("mapping_province.json", "r") as f:
        mapping = json.load(f)

    for game in games:

        with open(game, "r") as f:
            data = json.load(f)

        message_history = data["message_history"]
        state_history = data['state_history']


        human_players = get_human_players(data)
        bot_players = get_bot_players(data)


        for phase, messages in message_history.items():
            if phase[-1] != "M":
                continue
            phase_centers = state_history[phase]["centers"]

            if phase not in human_msg_cnt:
                human_msg_cnt[phase] = 0
            if phase not in bot_msg_cnt:
                bot_msg_cnt[phase] = 0
            if phase not in total_humans:
                total_humans[phase] = 0
            if phase not in total_bots:
                total_bots[phase] = 0
            if phase not in human_token_cnt:
                human_token_cnt[phase] = 0
            if phase not in bot_token_cnt:
                bot_token_cnt[phase] = 0

            players_alive = [power for power, centers in phase_centers.items() if len(centers) > 0]
            humans_alive = [power for power in human_players if power in players_alive]
            bots_alive = [power for power in bot_players if power in players_alive]

            total_humans[phase] += len(humans_alive)
            total_bots[phase] += len(bots_alive)

            for message in messages:
                if message['sender'] in humans_alive:
                    human_msg_cnt[phase] += 1
                    human_token_cnt[phase] += len(message['message'])
                elif message['sender'] in bots_alive:
                    bot_msg_cnt[phase] += 1
                    bot_token_cnt[phase] += len(message['message'])

    avg_human_msg_by_phase = np.array([human_msg_cnt[phase] / total_humans[phase] for phase in human_msg_cnt])
    avg_bot_msg_by_phase = np.array([bot_msg_cnt[phase] / total_bots[phase] for phase in bot_msg_cnt])
    
    avg_human_token_by_phase = np.array([human_token_cnt[phase] / total_humans[phase] for phase in human_token_cnt])
    avg_bot_token_by_phase = np.array([bot_token_cnt[phase] / total_bots[phase] for phase in bot_token_cnt])

    #plt.plot(avg_human_msg_by_phase, label="human")
    #plt.plot(avg_bot_msg_by_phase, label="bot")

    #plt.plot(avg_human_token_by_phase, label="human")
    #plt.plot(avg_bot_token_by_phase, label="bot")

    ratio = avg_bot_msg_by_phase / avg_human_msg_by_phase 
    token_ratio = avg_bot_token_by_phase / avg_human_token_by_phase
    plt.plot(ratio, label="msg ratio")
    plt.plot(token_ratio, label="char ratio")

    xticks = [phase[0] + phase[-3:] for phase in human_msg_cnt]
    plt.xticks(range(len(xticks)), xticks)
    plt.legend()
    plt.show()


    #for phase, cnt in human_msg_cnt.items():
    #    print(f"average human message count in {phase}: {round(cnt / total_humans[phase], 2)}")
    #    print(f"average bot message count in {phase}: {round(bot_msg_cnt[phase] / total_bots[phase], 2)}")

if __name__ == "__main__":
    main()
