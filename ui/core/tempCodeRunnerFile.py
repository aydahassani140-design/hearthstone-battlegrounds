# app.py
# Hearthstone Clone Project
# ui/core/app.py
import pygame
import sys
import os
from ui.core.config import *
# نکته: ما داریم از موتور لیدر (Engine) استفاده می‌کنیم
from services.engine import GameEngine
from data.minions_data import CARD_DB

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hearthstone - Player 2 UI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 20, bold=True)

        self.engine = GameEngine() # اتصال به منطق لیدر
        self.images = {}
        self.load_assets()

    def load_assets(self):
        # لود کردن عکس‌ها از پوشه‌ای که لیدر ساخته
        print("loading assets...")
        for card_id, data in CARD_DB.items():
            if os.path.exists(data.img_path):
                try:
                    img = pygame.image.load(data.img_path)
                    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
                    self.images[card_id] = img
                except: pass

    def run(self):
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
                if event.key == pygame.K_SPACE:
                    self.engine.switch_phase() # تغییر فاز جنگ/خرید
                elif event.key == pygame.K_r:
                    self.engine.refresh_shop(self.engine.players["p1"])

    def handle_click(self, pos):
        mx, my = pos
        if self.engine.phase == "RECRUIT":
            # منطق خرید (مختصات شاپ)
            if 120 <= my <= 120 + CARD_HEIGHT:
                idx = int((mx - 50) // (CARD_WIDTH + GAP))
                self.engine.buy_minion("p1", idx)

    def draw(self):
        self.screen.fill(COLORS["BACKGROUND"])
        if self.engine.phase == "RECRUIT":
            self.draw_recruit()
        elif self.engine.phase == "COMBAT":
            # فعلاً فقط متن جنگ را نشان می‌دهیم (تا نفر سوم منطقش را بنویسد)
            self.screen.fill((50, 20, 20))
            txt = self.title_font.render("COMBAT PHASE (Waiting for Logic...)", True, COLORS["TEXT_WHITE"])
            self.screen.blit(txt, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

    def draw_recruit(self):
        p = self.engine.players["p1"]
        # اطلاعات
        info = f"Gold: {p.gold} | Turn: {self.engine.turn}"
        self.screen.blit(self.title_font.render(info, True, COLORS["TEXT_GOLD"]), (20, 20))
        
        # رسم شاپ
        for i, m in enumerate(self.engine.shop.slots):
            rect = pygame.Rect(50 + i*(CARD_WIDTH+GAP), 120, CARD_WIDTH, CARD_HEIGHT)
            if m: self.draw_card(m, rect)
            else: pygame.draw.rect(self.screen, COLORS["CARD_EMPTY"], rect, 2)

        # رسم دست
        for i, m in enumerate(p.hand):
            rect = pygame.Rect(50 + i*(CARD_WIDTH+GAP), 600, CARD_WIDTH, CARD_HEIGHT)
            self.draw_card(m, rect)

    def draw_card(self, minion, rect):
        if minion.card_id in self.images:
            self.screen.blit(self.images[minion.card_id], rect)
        else:
            pygame.draw.rect(self.screen, (100, 100, 150), rect)
        
        # قاب دور کارت
        col = (255, 215, 0) if minion.is_golden else COLORS["CARD_BORDER"]
        pygame.draw.rect(self.screen, col, rect, 3)