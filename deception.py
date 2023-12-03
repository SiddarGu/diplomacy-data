import os, json, re

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
        annotated_messages = data["annotated_messages"]
        perceived_lie_timestamps = [int(k) for k, v in annotated_messages.items() if v == "yes"]

        for _, messages in message_history.items():
            for message in messages:
                messages_flattened.append(message)

        perceived_lies = [m for m in messages_flattened if m["time_sent"] in perceived_lie_timestamps]
        outgoing_lies = [m for m in messages_flattened if m['truth'] and m['truth'] == 'Lie']


        with open(f"deceptions/{data['game_id']}.json", "w") as f:
            json.dump(
                {
                    "perceived_lies": perceived_lies,
                    "outgoing_lies": outgoing_lies,
                },
                f,
                indent=4,
            )

if __name__ == "__main__":
    main()
