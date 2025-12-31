# minions_data.py
# Hearthstone Clone Project

# data/minions_data.py
import uuid
from common.models import Card, MinionInstance

# --- لیست ۱۸ مینیون فاز اول (طبق داکیومنت) ---

CARD_DB = {
    # --- BEETLE TRIBE (سوسک‌ها) ---
    "BG_TOKEN_BEETLE": Card("BG_TOKEN_BEETLE", "Beetle", 1, 1, 1, "Beast", [], "assets/minions/beetle.png"),
    
    "BG31_803": Card(
        card_id="BG31_803", 
        name="Buzzing Vermin", 
        tier=1, base_attack=1, base_health=2, 
        minion_type="Beast", 
        keywords=["Taunt", "Deathrattle"], 
        img_path="assets/minions/BG31_803.png"
    ),
    "BG31_801": Card(
        card_id="BG31_801", 
        name="Forest Rover", 
        tier=2, base_attack=3, base_health=2, 
        minion_type="Beast", 
        keywords=["Battlecry", "Deathrattle"], 
        img_path="assets/minions/BG31_801.png"
    ),
    "BG27_084": Card(
        card_id="BG27_084", 
        name="Sprightly Scarab", 
        tier=2, base_attack=2, base_health=1, 
        minion_type="Beast", 
        keywords=["Battlecry", "Reborn"], 
        img_path="assets/minions/BG27_084.png"
    ),
    "BG31_809": Card(
        card_id="BG31_809", 
        name="Turquoise Skitterer", 
        tier=3, base_attack=3, base_health=4, 
        minion_type="Beast", 
        keywords=["Deathrattle"], 
        img_path="assets/minions/BG31_809.png"
    ),
    "BG31_807": Card(
        card_id="BG31_807", 
        name="Nest Swarmer", 
        tier=4, base_attack=4, base_health=4, 
        minion_type="Beast", 
        keywords=["Deathrattle"], 
        img_path="assets/minions/BG31_807.png"
    ),
    "BGS_078": Card(
        card_id="BGS_078", 
        name="Monstrous Macaw", 
        tier=3, base_attack=5, base_health=3, 
        minion_type="Beast", 
        keywords=["Trigger"], 
        img_path="assets/minions/BGS_078.png"
    ),

    # --- DEMON TRIBE (دیمن‌ها) ---
    "BGS_004": Card(
        card_id="BGS_004", 
        name="Wrath Weaver", 
        tier=1, base_attack=1, base_health=3, 
        minion_type="Neutral", 
        keywords=["Trigger"], 
        img_path="assets/minions/BGS_004.png"
    ),
    "BGS_044": Card(
        card_id="BGS_044", 
        name="Imp Mama", 
        tier=6, base_attack=6, base_health=10, 
        minion_type="Demon", 
        keywords=["Taunt", "Deathrattle"], 
        img_path="assets/minions/BGS_044.png"
    ),
    "BG29_140": Card(
        card_id="BG29_140", 
        name="False Implicator", 
        tier=3, base_attack=1, base_health=1, 
        minion_type="Demon", 
        keywords=["EndTurn"], 
        img_path="assets/minions/BG29_140.png"
    ),
    "BG31_874": Card(
        card_id="BG31_874", 
        name="Furious Driver", 
        tier=4, base_attack=4, base_health=5, 
        minion_type="Demon", 
        keywords=["Battlecry"], 
        img_path="assets/minions/BG31_874.png"
    ),
    "BG21_005": Card(
        card_id="BG21_005", 
        name="Famished Felbat", 
        tier=6, base_attack=9, base_health=5, 
        minion_type="Demon", 
        keywords=["EndTurn"], 
        img_path="assets/minions/BG21_005.png"
    ),

    # --- UNDEAD TRIBE (آنددها) ---
    "BG28_300": Card(
        card_id="BG28_300", 
        name="Harmless Bonehead", 
        tier=1, base_attack=0, base_health=2, 
        minion_type="Undead", 
        keywords=["Deathrattle"], 
        img_path="assets/minions/BG28_300.png"
    ),
    "BG25_010": Card(
        card_id="BG25_010", 
        name="Handless Forsaken", 
        tier=2, base_attack=2, base_health=1, 
        minion_type="Undead", 
        keywords=["Deathrattle"], 
        img_path="assets/minions/BG25_010.png"
    ),
    "BG25_011": Card(
        card_id="BG25_011", 
        name="Nerubian Deathswarmer", 
        tier=2, base_attack=1, base_health=3, 
        minion_type="Undead", 
        keywords=["Battlecry"], 
        img_path="assets/minions/BG25_011.png"
    ),
    "BG25_008": Card(
        card_id="BG25_008", 
        name="Eternal Knight", 
        tier=2, base_attack=3, base_health=1, 
        minion_type="Undead", 
        keywords=["StartOfCombat"], 
        img_path="assets/minions/BG25_008.png"
    ),
    "BG25_009": Card(
        card_id="BG25_009", 
        name="Eternal Summoner", 
        tier=6, base_attack=8, base_health=1, 
        minion_type="Undead", 
        keywords=["Reborn", "Deathrattle"], 
        img_path="assets/minions/BG25_009.png"
    ),
    "BG30_129": Card(
        card_id="BG30_129", 
        name="Catacomb Crasher", 
        tier=5, base_attack=5, base_health=5, 
        minion_type="Undead", 
        keywords=["Trigger"], 
        img_path="assets/minions/BG30_129.png"
    ),
    "BG25_354": Card(
        card_id="BG25_354", 
        name="Titus Rivendare", 
        tier=5, base_attack=1, base_health=7, 
        minion_type="Neutral", 
        keywords=["Aura"], 
        img_path="assets/minions/BG25_354.png"
    ),
}

def create_minion(card_id: str) -> MinionInstance:
    """
    وظیفه: تبدیل یک کارت خشک و خالی به یک موجود زنده در بازی
    """
    if card_id not in CARD_DB:
        raise ValueError(f"Card {card_id} not found in DB")
        
    template = CARD_DB[card_id]
    
    return MinionInstance(
        instance_id=str(uuid.uuid4()),
        card_id=card_id,
        attack=template.base_attack,
        health=template.base_health,
        max_health=template.base_health,
        keywords=template.keywords.copy(),
        taunt="Taunt" in template.keywords,
        reborn="Reborn" in template.keywords,
        divine_shield="Divine Shield" in template.keywords,
        windfury="Windfury" in template.keywords
    )