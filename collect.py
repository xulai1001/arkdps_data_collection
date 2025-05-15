#encoding: utf-8
import os, json
from termcolor import colored
from parse import parse_dict, ParseObject, MyEncoder

GAMEDATA_DIR = "./ArknightsGameData/zh_CN/gamedata/excel/"
AKDATA_DIR = "./customdata/"

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        ret = json.load(f)
        print(f"载入 {filename} -> {len(ret)} Items.")
        return ret
        
def pick(dic, keys):
    k = dic.keys() & keys
    return { x: dic[x] for x in k }
        
CHAR_DATA = load_json(GAMEDATA_DIR + "character_table.json")
EQUIP_DATA = load_json(GAMEDATA_DIR + "battle_equip_table.json")
UNIEQUIP_DATA = load_json(GAMEDATA_DIR + "uniequip_table.json")
SKILL_DATA = load_json(GAMEDATA_DIR + "skill_table.json")
TAGS = load_json(AKDATA_DIR + "dps_specialtags.json")
ANIM_DATA = load_json(AKDATA_DIR + "dps_anim.json")
OPTS = load_json(AKDATA_DIR + "dps_options.json")
TRANSFORM = load_json("transform.json")

def collect_skill(char):
    ids = [x["skillId"] for x in char["skills"]]
    ret = { id: SKILL_DATA[id] for id in ids}
    return ret

def collect_equip(char_id):
    ret = None
    if UNIEQUIP_DATA["charEquip"].get(char_id, None):
        ret = {}
        for id in UNIEQUIP_DATA["charEquip"][char_id]:
            data = pick(UNIEQUIP_DATA["equipDict"][id], ["uniEquipId", "uniEquipName", "charId", "typeIcon", "itemCost"])
            data["battle"] = EQUIP_DATA.get(id, {})
            print(id)
            ret[id] = data
            
    return ret

def collect_custom(char_id, prior_data): 
    ret = { "options": None, "spec": None, "anim": None }
    spec = {}
    # dps_options.json
    if OPTS["char"].get(char_id, None): 
        ret["options"] = {
            "tags": OPTS["char"][char_id],
            "cond_info": OPTS["cond_info"].get(char_id, None)
        }
    # dps_specialtags.json
    if prior_data.get("skill", None):
        for skill_id in prior_data["skill"].keys():
            if TAGS.get(skill_id, None):
                spec[skill_id] = TAGS[skill_id]
    if prior_data.get("equip", None):
        for equip_id in prior_data["equip"].keys():
            if TAGS.get(equip_id, None):
                spec[equip_id] = TAGS[equip_id]
    talent_part = char_id.replace("char_", "tachr_")
    talents = prior_data["char"]["talents"]
    trait = prior_data["char"]["trait"]
    if talents:
        for i in range(0, len(talents)):
            talent_id = f"{talent_part}_{i+1}"
            if TAGS.get(talent_id, None):
                spec[talent_id] = TAGS[talent_id]
    if trait:
        talent_id = f"{talent_part}_trait"
        if TAGS.get(talent_id, None):
            spec[talent_id] = TAGS[talent_id]
    if TAGS.get(char_id, None): 
        spec[char_id] = TAGS[char_id]
    ret["spec"] = spec
    # dps_anim.json
    if ANIM_DATA.get(char_id, None):
        ret["anim"] = ANIM_DATA[char_id]
    return ret

def collect(char_id, char): 
    ret = {}
    char_data = pick(char, ["name", "description", "itemObtainApproach", "isSpChar", "rarity",
        "profession", "subProfessionId", "trait", "phases", "skills",
        "talents", "potentialRanks", "favorKeyFrames", "allSkillLvlup"])

    # filter
    if not char_data["itemObtainApproach"]:
        return None
    else:
        print([v for v in pick(char_data, ["name", "profession", "subProfessionId"]).values()])
        ret["char"] = char_data
        ret["skill"] = collect_skill(char_data)
        ret["equip"] = collect_equip(char_id)
        ret["custom"] = collect_custom(k, ret)
        return ret

for k in CHAR_DATA.keys():
    print(colored(f"收集 {k}", "yellow"))
    ret = collect(k, CHAR_DATA[k])
    if ret:
        print(colored("清洗数据", "cyan"))
        result = parse_dict(TRANSFORM, ParseObject(ret))
        print(colored(f"保存 output/{k}.json", "green"))
        with open(f"output/{k}.json", "w", encoding="utf-8") as g:
            json.dump(result, g, ensure_ascii=False, indent=2, sort_keys=True, cls=MyEncoder)
