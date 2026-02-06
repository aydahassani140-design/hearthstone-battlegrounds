# src/models.py

import pygame

class Minion:
    def __init__(self, data):
        self.name = data.get("name")
        self.attack = data.get("attack", 0)
        self.health = data.get("health", 0)
        self.keywords = data.get("keywords", [])
        self.cost = 3
        self.is_frozen = False
        self.rect = pygame.Rect(0, 0, 110, 150)

class Player:
    def __init__(self, name="Sylvanas"):
        self.name = name
        self.hp = 40
        self.turn = 1
        self.gold = 3
        self.max_gold = 3
        self.tavern_tier = 1
        self.upgrade_cost = 5
        self.hand = []   # List of Minion objects
        self.board = []  # List of Minion objects
        self.shop = []   # List of Minion objects