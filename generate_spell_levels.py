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

def scroll_not_yet_read(scroll_name):
    for scroll in tier_0_scroll_list:
        if scroll_name == scroll:
            return False
    for scroll in tier_1_scroll_list:
        if scroll_name == scroll:
            return False
    for scroll in tier_2_scroll_list:
        if scroll_name == scroll:
            return False
    for scroll in tier_3_scroll_list:
        if scroll_name == scroll:
            return False
    return True

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
                if ( jo["id"] == "spell_scroll_tier_0" ):
                    for scroll in jo["items"]:
                        if scroll_not_yet_read(scroll[0]):
                            tier_0_scroll_list.append(scroll[0])
                if ( jo["id"] == "spell_scroll_tier_1" ):
                    for scroll in jo["items"]:
                        if scroll_not_yet_read(scroll[0]):
                            tier_1_scroll_list.append(scroll[0])
                if ( jo["id"] == "spell_scroll_tier_2" ):
                    for scroll in jo["items"]:
                        if scroll_not_yet_read(scroll[0]):
                            tier_2_scroll_list.append(scroll[0])
                if ( jo["id"] == "spell_scroll_tier_3" ):
                    for scroll in jo["items"]:
                        if scroll_not_yet_read(scroll[0]):
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
                  "id": str(jo["id"]),
                  "safe_id": str(jo["id"]).replace("-", "_"),
                  "level": -1,
                  "name": str(jo["name"]),
                  "description": str(jo["description"])
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
        "dynamic_line": "<u_val:sorcerer_level_" + str( level ) + "_spells_known> / <u_val:sorcerer_level_" + str( level ) + "_spells_known_slots> level " + str( level ) + " spells known.",
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
            "condition": { "math": [ "u_used_spell_slot_for_" + spell["safe_id"], "==", "0" ] },
            "text": "Learn " + spell["name"] + " ( level "+ str(spell["level"]) + " )",
            "topic": "TALK_SORCERER_LEARN_SPELL_" + spell["id"] + "_at_level_" + str( level )
            }
            main_topic["responses"].append(response)
            new_other_topic = {
                "type": "talk_topic",
                "id": "TALK_SORCERER_LEARN_SPELL_" + spell["id"] + "_at_level_" + str( level ),
                "dynamic_line": spell["name"] + ": " + spell["description"],
                "responses": [
                  {
                    "text": "Select Spell.",
                    "topic": "TALK_SORCERER_MENU_MAIN",
                    "effect": [
                      { "math": [ "u_val('spell_level', 'spell: " + spell["id"] + "')", "=", "u_current_sorcerer_level" ] },
                      { "math": [ "u_used_spell_slot_for_"+spell["safe_id"], "=", str( max( level, 0.5 ) ) ] },
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
    with open(path + "/learn_spells_level_" + str( level ) + ".json", mode="wt") as f:
        f.write(json.dumps(all_topics, indent=2))

def write_forget_spell():
    main_topic = {
        "type": "talk_topic",
        "id": "TALK_SORCERER_FORGET_SPELL",
        "dynamic_line": "Pick a spell to forget",
        "responses": [
            { "text": "Go Back.", "topic": "TALK_SORCERER_MENU_MAIN" },
            { "text": "Quit.", "topic": "TALK_DONE" }
            ]
        }
    for spell in spell_data:
        response = {
            "condition": { "math": [ "u_used_spell_slot_for_"+spell["safe_id"], ">", "0" ] },
            "text": "Forget " + spell["name"] + " ( level <u_val:used_spell_slot_for_" + spell["safe_id"] + "> )",
            "topic": "TALK_SORCERER_MENU_MAIN",
            "effect": [
                { "math": [ "u_val('spell_level', 'spell: " + spell["id"] + "')", "=", "-1" ] },
                { "run_eoc_with": "EOC_sorcerer_forget_spell_refund_slots", "variables": { "forgotten_spell_level": { "u_val": "used_spell_slot_for_"+spell["safe_id"] } } },
                { "math": [ "u_used_spell_slot_for_"+spell["safe_id"], "=", "0" ] },
                { "math": [ "u_sorcerer_forget_spell_charge", "--" ] }
            ]
        }
        main_topic["responses"].append(response)
    path = "generated_code/"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    with open(path + "/forget_spells.json", mode="wt") as f:
        f.write(json.dumps(main_topic, indent=2))

def write_level_up_spells():
    main_topic = {
        "type": "effect_on_condition",
        "id": "EOC_level_up_sorcerer_spells",
        "effect": []
        }
    for spell in spell_data:
        effect = {
            "run_eocs": {
              "id": "sorcerer_level_up_"+spell["safe_id"],
              "condition": { "math": [ "u_used_spell_slot_for_"+spell["safe_id"], ">", "0" ] },
              "effect": [ { "math": [ "u_val('spell_level', 'spell: " + spell["id"] + "')", "=", "max(u_current_sorcerer_level, u_val('spell_level', 'spell: " + spell["id"] + "') )" ] } ]
            }
        }
        main_topic["effect"].append(effect)
    path = "generated_code/"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    with open(path + "/level_up_spells.json", mode="wt") as f:
        f.write(json.dumps(main_topic, indent=2))

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

write_forget_spell()
write_level_up_spells()

input(".")