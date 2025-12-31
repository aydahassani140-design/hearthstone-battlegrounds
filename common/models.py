# models.py
# Hearthstone Clone Project

# common/models.py
from dataclasses import dataclass, field
from typing import List, Optional
import uuid

@dataclass
class Card:
    """
    مشخصات ثابت یک کارت (تمپلیت اولیه)
    مثل چیزی که در کارخانه روی مقوا چاپ شده و تغییر نمی‌کند.
    """
    card_id: str
    name: str
    tier: int
    base_attack: int
    base_health: int
    minion_type: str  # Beast, Demon, Undead, Neutral
    keywords: List[str] = field(default_factory=list) # Taunt, Reborn, Deathrattle
    img_path: str = ""

@dataclass
class MinionInstance:
    """
    مینیونی که الان زنده است و در بازی حضور دارد.
    این از روی Card ساخته می‌شود اما جان و حمله‌اش در جنگ تغییر می‌کند.
    """
    instance_id: str
    card_id: str
    attack: int
    health: int
    max_health: int
    keywords: List[str]
    # وضعیت‌های خاص (Buffs & States)
    is_golden: bool = False
    divine_shield: bool = False
    reborn: bool = False
    taunt: bool = False
    windfury: bool = False
    
    # موقعیت گرافیکی (برای اینکه UI بداند کجا رسمش کند)
    slot_index: int = -1 

@dataclass
class Player:
    """
    اطلاعات کامل یک بازیکن (چه خودمان، چه ۳ حریف دیگر)
    """
    player_id: str
    hero_name: str
    hp: int = 40
    gold: int = 3
    max_gold: int = 10
    tavern_tier: int = 1
    tavern_upgrade_cost: int = 5
    
    # لیست کارت‌های در دست (Hand)
    hand: List[MinionInstance] = field(default_factory=list)
    # لیست کارت‌های در زمین (Board)
    board: List[MinionInstance] = field(default_factory=list)
    
    # ویژگی‌های خاص بازی
    freeze_shop: bool = False
    graveyard: List[MinionInstance] = field(default_factory=list) # لیست مرده‌ها (برای هیرو پاور سیلواناس)

@dataclass
class Shop:
    """
    وضعیت فروشگاه (Tavern)
    """
    slots: List[Optional[MinionInstance]] = field(default_factory=list)
    frozen: bool = False