# src/game_engine.py

import json
import random
import pygame
import os

from src.models import Minion, Player

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # bgknowhow-main
PROJECT_ROOT = os.path.dirname(BASE_DIR)              # hearthstone-battlegrounds
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "minions.json")


class GameEngine:
    def __init__(self):
        self.player = Player()

        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                self.minion_pool = json.load(f)
        except FileNotFoundError:
            raise RuntimeError(f"minions.json not found!\nExpected at: {DATA_PATH}")

        self.refresh_shop(free=True)

    def start_next_turn(self):
        self.player.turn += 1
        self.player.max_gold = min(10, 2 + self.player.turn)
        self.player.gold = self.player.max_gold

        # تخفیف Upgrade
        if self.player.upgrade_cost > 2:
            self.player.upgrade_cost -= 1

        self.refresh_shop(free=True)

    def refresh_shop(self, free=False):
        """Refresh shop with freeze support"""
        if not free:
            if self.player.gold < 1:
                print("Not enough gold to refresh!")
                return
            self.player.gold -= 1

        shop_size = 3 + (self.player.tavern_tier // 2)
        new_shop = []

        # کارت‌های فریز شده حفظ شوند
        frozen_cards = [m for m in self.player.shop if m.is_frozen]

        # تعداد جای خالی که نیاز به جایگزینی دارد
        slots_to_fill = shop_size - len(frozen_cards)

        # کارت‌های قابل استفاده
        available = self.minion_pool.get(
            f"tier{self.player.tavern_tier}",
            self.minion_pool.get("tier1", [])
        )

        for _ in range(slots_to_fill):
            minion = Minion(random.choice(available))
            minion.rect = pygame.Rect(100 + len(new_shop + frozen_cards) * 130, 120, 110, 150)
            new_shop.append(minion)

        # ترکیب کارت‌های فریز و جدید
        self.player.shop = frozen_cards + new_shop
        self._update_shop_positions()

    def toggle_freeze(self, minion):
        minion.is_frozen = not minion.is_frozen

    def upgrade_tavern(self):
        if self.player.gold >= self.player.upgrade_cost and self.player.tavern_tier < 6:
            self.player.gold -= self.player.upgrade_cost
            self.player.tavern_tier += 1
            self.player.upgrade_cost = 5 + self.player.tavern_tier

    def buy_minion(self, minion):
        if self.player.gold < minion.cost:
            print(f"Not enough gold to buy {minion.name}!")
            return
        if len(self.player.hand) >= 10:
            print("Hand is full!")
            return

        self.player.gold -= minion.cost
        if minion in self.player.shop:
            self.player.shop.remove(minion)
        self.player.hand.append(minion)
        self._update_hand_positions()
        self._update_shop_positions()

    def play_minion(self, minion):
        if len(self.player.board) >= 7:
            print("Board is full!")
            return

        if minion in self.player.hand:
            self.player.hand.remove(minion)
        self.player.board.append(minion)
        self._update_hand_positions()
        self._update_board_positions()

    # موقعیت کارت‌ها
    def _update_hand_positions(self):
        for i, m in enumerate(self.player.hand):
            m.rect.topleft = (100 + i * 130, 320)

    def _update_board_positions(self):
        for i, m in enumerate(self.player.board):
            m.rect.topleft = (100 + i * 130, 520)

    def _update_shop_positions(self):
        for i, m in enumerate(self.player.shop):
            m.rect.topleft = (100 + i * 130, 120)
