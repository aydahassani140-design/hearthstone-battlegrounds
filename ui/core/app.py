# app.py
# Hearthstone Clone Project
# ui/core/app.py
import pygame
import sys
import os
from ui.core.config import *
from services.engine import GameEngine
from data.minions_data import CARD_DB

class App:
    def __init__(self):
        print("Initializing Pygame...")
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hearthstone - Leader View")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 22, bold=True)

        self.engine = GameEngine()
        self.images = {}
        self.load_assets()

    def load_assets(self):
        print("Loading assets from disk...")
        for card_id, data in CARD_DB.items():
            if os.path.exists(data.img_path):
                try:
                    img = pygame.image.load(data.img_path)
                    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
                    self.images[card_id] = img
                except: pass
            else:
                print(f"Warning: Missing {data.img_path}")

    def run(self):
        print("Game Loop Started!")
        while True:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: self.engine.switch_phase()
                elif event.key == pygame.K_r: self.engine.refresh_shop(self.engine.players["p1"])

    def handle_click(self, pos):
        mx, my = pos
        if self.engine.phase == "RECRUIT":
            if 120 <= my <= 120 + CARD_HEIGHT:
                idx = int((mx - 50) // (CARD_WIDTH + GAP))
                self.engine.buy_minion("p1", idx)
            if mx > SCREEN_WIDTH - 150 and my < 60:
                self.engine.refresh_shop(self.engine.players["p1"])

    def draw(self):
        self.screen.fill(COLORS["BACKGROUND"])
        if self.engine.phase == "RECRUIT": self.draw_recruit()
        elif self.engine.phase == "COMBAT": self.draw_combat()

    def draw_recruit(self):
        p = self.engine.players["p1"]
        info = f"Turn: {self.engine.turn} | Gold: {p.gold}/{p.max_gold}"
        self.screen.blit(self.title_font.render(info, True, COLORS["TEXT_GOLD"]), (20, 20))
        
        # Shop
        for i, m in enumerate(self.engine.shop.slots):
            rect = pygame.Rect(50 + i*(CARD_WIDTH+GAP), 120, CARD_WIDTH, CARD_HEIGHT)
            if m: self.draw_card(m, rect)
            else: pygame.draw.rect(self.screen, COLORS["CARD_EMPTY"], rect, 2)

        # Hand
        for i, m in enumerate(p.hand):
            rect = pygame.Rect(50 + i*(CARD_WIDTH+GAP), 600, CARD_WIDTH, CARD_HEIGHT)
            self.draw_card(m, rect)

    def draw_combat(self):
        self.screen.fill((60, 20, 20))
        txt = self.title_font.render("COMBAT MODE (Press SPACE)", True, COLORS["TEXT_WHITE"])
        self.screen.blit(txt, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

    def draw_card(self, minion, rect):
        if minion.card_id in self.images:
            self.screen.blit(self.images[minion.card_id], rect)
        else:
            pygame.draw.rect(self.screen, (100, 100, 150), rect)
        
        col = COLORS["CARD_GOLDEN"] if minion.is_golden else COLORS["CARD_BORDER"]
        pygame.draw.rect(self.screen, col, rect, 3)