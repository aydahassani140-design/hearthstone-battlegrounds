# src/main.py
import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game_engine import GameEngine
from src.asset_loader import AssetManager
from src.ui_renderer import UIRenderer

# رنگ‌ها
RED=(200,50,50); GREEN=(50,200,50); PURPLE_TIER=(150,50,200)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sylvanas Battlegrounds - Team Project Phase 1")
    clock = pygame.time.Clock()

    engine = GameEngine()
    assets = AssetManager()
    renderer = UIRenderer(screen, assets)

    buttons = {
        "upgrade": {"rect": pygame.Rect(600, 5, 180, 50), "color": PURPLE_TIER},
        "refresh": {"rect": pygame.Rect(800, 5, 120, 50), "color": GREEN},
        "end_turn": {"rect": pygame.Rect(950, 5, 150, 50), "color": RED}
    }

    running = True
    while running:
        buttons["upgrade"]["text"] = f"Upgrade ({engine.player.upgrade_cost}g)"
        buttons["refresh"]["text"] = "Refresh (1g)"
        buttons["end_turn"]["text"] = "End Turn"

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if buttons["upgrade"]["rect"].collidepoint(pos): engine.upgrade_tavern()
                elif buttons["refresh"]["rect"].collidepoint(pos): engine.refresh_shop()
                elif buttons["end_turn"]["rect"].collidepoint(pos): engine.start_next_turn()
                
                for card in engine.player.shop[:]: engine.buy_minion(card) if card.rect.collidepoint(pos) else None
                for card in engine.player.hand[:]: engine.play_minion(card) if card.rect.collidepoint(pos) else None
        
        renderer.draw_game(engine.player, buttons)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()