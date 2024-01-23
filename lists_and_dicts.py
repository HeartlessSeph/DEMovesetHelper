from pathlib import Path

db_paths = {
    "motion_gmt": "puid.aston",
    "motion_bep": "puid.aston",
    "File Information": "Fighter Commander",
    "behavior_set": "puid.aston",
    "sound_cuesheet": "puid.aston",
    "asset_id": "asset_aston_ngen",
    "battle_ai_setting": "db.aston.en",
    "battle_tougijyo_nakama_skill": "db.aston.en",
    "battle_tougijyo_nakama_type": "db.aston.en",
    "battle_tougijyo_nakama_rarity": "db.aston.en",
    "ui_texture": "puid.aston",
    "character_npc_soldier_name_group": "db.aston.en",
    "character_model_model_data": "db.aston.en",
    "character_character_data": "db.aston.en",
    "particle": "puid.aston",
    "character": "puid.aston",
    "character_model": "puid.aston",
    "sound_voicer": "db.aston.en",
    "battle_ctrltype": "db.aston.en",
    "character_npc_soldier_personal_data": "db.aston.en",
    "battle_tougijyo_nakama_list": "db.aston.en",
    "battle_motion_set": "db.aston.en",
    "battle_command_set": "db.aston.en",
    "battle_command_set_puid": "puid.aston",
    "battle_action_info": "db.aston.en",
    "sound_finish_blow": "db.aston.en",
    "battle_charge_attack_info": "db.aston.en",
    "battle_motion_group": "db.aston.en",
    "motion_flag_info": "db.aston.en",
    "sound_voice_table": "db.aston.en"
}

file_names = \
    ["particle",
     "motion_gmt",
     "motion_bep",
     "File Information",
     "behavior_set",
     "sound_cuesheet",
     "asset_id",
     "battle_ai_setting",
     "battle_tougijyo_nakama_skill",
     "battle_tougijyo_nakama_type",
     "battle_tougijyo_nakama_rarity",
     "ui_texture",
     "character_npc_soldier_name_group",
     "character",
     "talk_param",
     "sound_category",
     "sound_se_all_id_to_id",
     "character_model"]

wfile_names = \
    ["battle_ctrltype",
     "sound_voicer",
     "character_model_model_data",
     "character_character_data",
     "character_npc_soldier_personal_data",
     "battle_tougijyo_nakama_list",
     "battle_motion_set",
     "battle_command_set",
     "battle_action_info",
     "sound_finish_blow",
     "battle_charge_attack_info",
     "battle_motion_group",
     "motion_flag_info",
     "sound_voice_table"
     ]

puid_auto_update = [
    {
        "search": "**/*.",
        "ext": "mbv",
        "file": "behavior_set",
        "puidpath": "MBV",
        "outpath": Path("motion") / "behavior",
        "update": True,
        "copy": False,
        "copy_search": "**/*.mbv"
    },
    {
        "search": "**/*.",
        "ext": "gmt",
        "file": "motion_gmt",
        "puidpath": "Motion",
        "outpath": Path("motion") / "gmt",
        "update": True,
        "copy": True,
        "copy_search": "**/*.gmt"
    },
    {
        "search": "**/*.",
        "ext": "bep",
        "file": "motion_bep",
        "puidpath": "Motion",
        "outpath": Path("motion") / "bep",
        "update": True,
        "copy": True,
        "copy_search": "**/*.bep"
    },
    {
        "search": "**/*.",
        "ext": "acb",
        "file": "sound_cuesheet",
        "puidpath": "Sound",
        "outpath": Path("sound"),
        "update": True,
        "copy": True,
        "copy_search": "**/*.acb"
    },
    {
        "search": "**/*.",
        "ext": "awb",
        "file": "sound_cuesheet",
        "puidpath": "Sound",
        "outpath": Path("stream"),
        "update": False,
        "copy": True,
        "copy_search": "**/*.awb"
    },
    {
        "search": "**/*.",
        "ext": "pib",
        "file": "particle",
        "puidpath": "Particle",
        "outpath": Path("particle"),
        "update": True,
        "copy": True,
        "copy_search": "*/"
    },
    {
        "search": "**/*.",
        "ext": "dds",
        "file": "ui_texture",
        "puidpath": "UI",
        "outpath": Path("ui.aston.en") / "texture",
        "update": True,
        "copy": True,
        "copy_search": "**/*.dds"
    }
]