import pygame

class Minion:
    def __init__(self, data):
        self.name = data.get("name", "Unknown")
        self.attack = data.get("attack", 0)
        self.health = data.get("health", 0)
        self.keywords = data.get("keywords", [])
        self.cost = data.get("cost", 3)
        self.is_frozen = False
        self.is_golden = data.get("is_golden", False)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.auras = data.get("auras", [])  # برای Auraهایی مثل Rivendare

class Player:
    def __init__(self, name="Sylvanas"):
        self.name = name
        self.hp = 40
        self.turn = 1
        self.gold = 3
        self.max_gold = 3
        self.tavern_tier = 1
        self.upgrade_cost = 5
        self.hand = []
        self.board = []
        self.shop = []
        self.discover_queue = []  # برای Triple/Discover