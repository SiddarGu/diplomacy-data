import xlwings as xw
import json
import pandas as pd

POWERS = ["AUSTRIA", "ENGLAND", "ITALY", "RUSSIA", "TURKEY"]
COLUMNS = [
    "Phase",
    "Message",
    "Sender",
    "Recipient",
    "Sender Annotation",
    "Recipient Annotation",
    "Notes",
]
HUMANS = ["GERMANY", "FRANCE"]

CONVERSATIONS = {}

# a df for each conversation involving humans
for human in HUMANS:
    for power in POWERS:
        CONVERSATIONS[human + "-" + power] = pd.DataFrame(columns=COLUMNS)

CONVERSATIONS["FRANCE-GERMANY"] = pd.DataFrame(columns=COLUMNS)

GAME_NAME = "beta_de_2"
GAME_FILE = "games/" + GAME_NAME + ".json"

with open(GAME_FILE) as f:
    game = json.load(f)
    message_history = game["message_history"]
    annotated_messages = game["annotated_messages"]

for phase in message_history:
    current_phase_messages = message_history[phase]

    for message in current_phase_messages:
        sender = message["sender"]
        recipient = message["recipient"]
        time_sent = message["time_sent"]
        message_phase = message["phase"]
        text = message["message"]
        sender_annotation = message["truth"] if message["truth"] is not None else ""
        recipient_annotation = (
            annotated_messages[str(time_sent)] if str(time_sent) in annotated_messages else ""
        )

        # check if the conversation involves humans
        if (sender not in HUMANS and recipient not in HUMANS) or (
            sender == "GLOBAL" or recipient == "GLOBAL"
        ):
            continue
        # if between two humans
        elif sender in HUMANS and recipient in HUMANS:
            conversation = "FRANCE-GERMANY"
        # human and cicero
        else:
            if sender in HUMANS:
                conversation = sender + "-" + recipient
            else:
                conversation = recipient + "-" + sender

        CONVERSATIONS[conversation] = CONVERSATIONS[conversation].append(
            {
                "Phase": phase,
                "Message": text,
                "Sender": sender,
                "Recipient": recipient,
                "Sender Annotation": sender_annotation,
                "Recipient Annotation": recipient_annotation,
                "Notes": "",
            },
            ignore_index=True,
        )        

# to excel using ExcelWriter
writer = pd.ExcelWriter(GAME_NAME + ".xlsx", engine="xlsxwriter")

for conversation in CONVERSATIONS:
    CONVERSATIONS[conversation].to_excel(writer, sheet_name=conversation, index=False)

writer.save()
