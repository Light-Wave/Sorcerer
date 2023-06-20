import os
import json

tier_0_scroll_list = []
tier_1_scroll_list = []
tier_2_scroll_list = []
tier_3_scroll_list = []
tier_0_spell_list = []
tier_1_spell_list = []
tier_2_spell_list = []
tier_3_spell_list = []
spell_data = []

def read_item_group(path):
    change = False
    with open(path, "r", encoding="utf-8") as json_file:
        try:
            json_data = json.load(json_file)
        except json.JSONDecodeError:
            failures.add(
                "Json Decode Error at:\n" + path
            )
            return None
        for jo in json_data:
            if isinstance(jo, dict):
                if (
                    jo["id"] == "spell_scroll_tier_0"
                ):
                    for scroll in jo["items"]:
                        tier_0_scroll_list.append(scroll[0])
                if (
                    jo["id"] == "spell_scroll_tier_1"
                ):
                    for scroll in jo["items"]:
                        tier_1_scroll_list.append(scroll[0])
                if (
                    jo["id"] == "spell_scroll_tier_2"
                ):
                    for scroll in jo["items"]:
                        tier_2_scroll_list.append(scroll[0])
                if (
                    jo["id"] == "spell_scroll_tier_3"
                ):
                    for scroll in jo["items"]:
                        tier_3_scroll_list.append(scroll[0])
    return

def read_spell_scrolls(path):
    change = False
    with open(path, "r", encoding="utf-8") as json_file:
        try:
            json_data = json.load(json_file)
        except json.JSONDecodeError:
            failures.add(
                "Json Decode Error at:\n" + path
            )
            return None
        for jo in json_data:
            if isinstance(jo, dict):
                for scroll_name in tier_0_scroll_list:
                    if (
                        "id" in jo and jo["id"] == scroll_name
                    ):
                        tier_0_spell_list.append(jo["use_action"]["spells"][0])
                for scroll_name in tier_1_scroll_list:
                    if (
                        "id" in jo and jo["id"] == scroll_name
                    ):
                        tier_1_spell_list.append(jo["use_action"]["spells"][0])
                for scroll_name in tier_2_scroll_list:
                    if (
                        "id" in jo and jo["id"] == scroll_name
                    ):
                        tier_2_spell_list.append(jo["use_action"]["spells"][0])
                for scroll_name in tier_3_scroll_list:
                    if (
                        "id" in jo and jo["id"] == scroll_name
                    ):
                        tier_3_spell_list.append(jo["use_action"]["spells"][0])
    return

def read_spell_data(path):
    change = False
    with open(path, "r", encoding="utf-8") as json_file:
        try:
            json_data = json.load(json_file)
        except json.JSONDecodeError:
            failures.add(
                "Json Decode Error at:\n" + path
            )
            return None
        for jo in json_data:
            if isinstance(jo, dict) and "id" in jo and "name" in jo and "description" in jo:
                difficulty = int(jo["difficulty"] if "difficulty" in jo else 0)
                new_spell_data = {
                  "id": jo["id"],
                  "level": -1,
                  "name": jo["name"],
                  "description": jo["description"]
                }
                for spell_name in tier_0_spell_list:
                    if (
                        jo["id"] == spell_name
                    ):
                        if difficulty <= 1:
                            new_spell_data["level"] = 0
                        elif difficulty <= 4:
                            new_spell_data["level"] = 1
                        else:
                            new_spell_data["level"] = 2
                        spell_data.append(new_spell_data)
                for spell_name in tier_1_spell_list:
                    if (
                        jo["id"] == spell_name
                    ):
                        new_spell_data["tier"] = 1
                        if difficulty <= 4:
                            new_spell_data["level"] = 3
                        else:
                            new_spell_data["level"] = 4
                        spell_data.append(new_spell_data)
                for spell_name in tier_2_spell_list:
                    if (
                        jo["id"] == spell_name
                    ):
                        new_spell_data["tier"] = 2
                        if difficulty <= 5:
                            new_spell_data["level"] = 5
                        else:
                            new_spell_data["level"] = 6
                        spell_data.append(new_spell_data)
                for spell_name in tier_3_spell_list:
                    if (
                        jo["id"] == spell_name
                    ):
                        new_spell_data["tier"] = 3
                        if difficulty <= 5:
                            new_spell_data["level"] = 7
                        else:
                            new_spell_data["level"] = 8
                        spell_data.append(new_spell_data)
    return

def write_learn_spell(level):
    main_topic = {
        "type": "talk_topic",
        "id": "TALK_SORCERER_LEARN_SPELL_" + str( level ),
        "dynamic_line": "<u_val:u_sorcerer_level_" + str( level ) + "_spells_known> / <u_val:u_sorcerer_level_" + str( level ) + "_spells_known_slots> level " + str( level ) + " spells known.",
        "speaker_effect": { "effect": { "math": [ "curent_spell_slot", "=", str( level ) ] } },
        "responses": [
            { "text": "Go Back.", "topic": "TALK_SORCERER_MENU_MAIN" },
            { "text": "Quit.", "topic": "TALK_DONE" }
            ]
        }
    all_topics = []
    for spell in spell_data:
        if int(spell["level"]) <= level:
            response = {
            "condition": { "math": [ "u_used_spell_slot_for_"+str(spell["id"]), "==", "0" ] },
            "text": "Learn " + str(spell["name"]) + " ( level "+str( spell["level"] )+" )",
            "topic": "TALK_SORCERER_LEARN_SPELL_" + str(spell["id"]) + "_at_level_" + str( level )
            }
            main_topic["responses"].append(response)
            new_other_topic = {
                "type": "talk_topic",
                "id": "TALK_SORCERER_LEARN_SPELL_" + str(spell["id"]) + "_at_level_" + str( level ),
                "dynamic_line": str(spell["name"]) + ": " + str(spell["description"]),
                "responses": [
                  {
                    "text": "Select Spell.",
                    "topic": "TALK_SORCERER_MENU_MAIN",
                    "effect": [
                      { "math": [ "u_val('spell_level', 'spell: " + str(spell["name"]) + "')", "=", "u_current_sorcerer_level" ] },
                      { "math": [ "u_used_spell_slot_for_"+str(spell["id"]), "=", str( max( level, 0.5 ) ) ] },
                      { "math": [ "u_sorcerer_level_"+str(level)+"_spells_known", "++" ] },
                    ]
                  },
                  { "text": "Go Back.", "topic": "TALK_SORCERER_MENU_MAIN" },
                  { "text": "Quit.", "topic": "TALK_DONE" }
                ]
            }
            all_topics.append(new_other_topic)
    all_topics.append(main_topic)
    path = "generated_code/learn_spell"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    with open(path + "/_learn_spells_level_" + str( level ) + ".json", mode="wt") as f:
        f.write(json.dumps(all_topics, indent=2))

read_item_group("../../data/mods/Magiclysm/itemgroups/spellbooks.json")
read_spell_scrolls("../../data/mods/Magiclysm/items/spell_scrolls.json")

for root, directories, filenames in os.walk("../../data/mods/Magiclysm/Spells"):
    for filename in filenames:
        path = os.path.join(root, filename)
        if path.endswith(".json"):
            read_spell_data(path)

            
spell_data = sorted(spell_data, key=lambda x: x["level"], reverse = True)

for number in range(0,10):
    write_learn_spell(number)


input(".")