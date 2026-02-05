# src/game_engine.py
import json
import random
import pygame # برای ساخت Rect
from src.models import Minion, Player

class GameEngine:
    def __init__(self):
        self.player = Player()
        with open("data/minions.json", "r") as f:
            self.minion_pool = json.load(f)
        self.refresh_shop()

    def start_next_turn(self):
        self.player.turn += 1
        self.player.max_gold = min(10, 2 + self.player.turn)
        self.player.gold = self.player.max_gold
        if self.player.upgrade_cost > 0: self.player.upgrade_cost -= 1
        self.refresh_shop()

    def refresh_shop(self):
        shop_size = 3 + (self.player.tavern_tier // 2)
        self.player.shop = []
        available_minions = self.minion_pool.get(f"tier{self.player.tavern_tier}", [])
        if not available_minions: available_minions = self.minion_pool["tier1"] # Fallback

        for i in range(shop_size):
            minion = Minion(random.choice(available_minions))
            minion.rect = pygame.Rect(100 + (i * 130), 120, 110, 150)
            self.player.shop.append(minion)

    def upgrade_tavern(self):
        if self.player.gold >= self.player.upgrade_cost and self.player.tavern_tier < 6:
            self.player.gold -= self.player.upgrade_cost
            self.player.tavern_tier += 1
            self.player.upgrade_cost = 5 + self.player.tavern_tier

    def buy_minion(self, minion):
        if self.player.gold >= minion.cost and len(self.player.hand) < 10:
            self.player.gold -= minion.cost
            self.player.shop.remove(minion)
            self.player.hand.append(minion)
            self._update_hand_positions()

    def play_minion(self, minion):
        if len(self.player.board) < 7:
            self.player.hand.remove(minion)
            self.player.board.append(minion)
            self._update_hand_positions()
            self._update_board_positions()

    def _update_hand_positions(self):
        for i, m in enumerate(self.player.hand): m.rect.topleft = (100 + (i * 130), 320)

    def _update_board_positions(self):
        for i, m in enumerate(self.player.board): m.rect.topleft = (100 + (i * 130), 520)