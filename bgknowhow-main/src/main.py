# src/main.py

import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game_engine import GameEngine
from src.asset_loader import AssetManager
from src.ui_renderer import UIRenderer
from src.combat_engine import CombatEngine
from src.models import Player


RED = (200, 50, 50)
GREEN = (50, 200, 50)
PURPLE_TIER = (150, 50, 200)
YELLOW_COMBAT = (200, 200, 50)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sylvanas Battlegrounds - Team Project Phase 1")
    clock = pygame.time.Clock()

    
    engine = GameEngine()
    engine.player2 = Player("AI_Opponent")  # Mock Player برای تست Combat
    
    engine.player2.board = [m for m in engine.player2.board]  

    assets = AssetManager()
    renderer = UIRenderer(screen, assets)

    
    buttons = {
        "upgrade": {"rect": pygame.Rect(600, 5, 180, 50), "color": PURPLE_TIER},
        "refresh": {"rect": pygame.Rect(800, 5, 120, 50), "color": GREEN},
        "end_turn": {"rect": pygame.Rect(950, 5, 150, 50), "color": RED},
        "combat": {"rect": pygame.Rect(1120, 5, 150, 50), "color": YELLOW_COMBAT}
    }

    running = True
    while running:
        
        buttons["upgrade"]["text"] = f"Upgrade ({engine.player.upgrade_cost}g)"
        buttons["refresh"]["text"] = "Refresh (1g)"
        buttons["end_turn"]["text"] = "End Turn"
        buttons["combat"]["text"] = "Start Combat"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                
                if event.button == 1:
                    
                    if buttons["upgrade"]["rect"].collidepoint(pos):
                        engine.upgrade_tavern()
                    elif buttons["refresh"]["rect"].collidepoint(pos):
                        engine.refresh_shop()
                    elif buttons["end_turn"]["rect"].collidepoint(pos):
                        engine.start_next_turn()
                    elif buttons["combat"]["rect"].collidepoint(pos):
                        
                        combat = CombatEngine(engine.player, engine.player2, seed=12345)
                        combat.perform_combat()
                        print("=== Combat Finished ===")
                        print(f"{engine.player.name} HP: {combat.p1.hp}")
                        print(f"{engine.player2.name} HP: {combat.p2.hp}")

                        
                        engine.player.board = []
                        engine.player2.board = []

                    
                    for card in engine.player.shop[:]:
                        if card.rect.collidepoint(pos):
                            engine.buy_minion(card)

                    
                    for card in engine.player.hand[:]:
                        if card.rect.collidepoint(pos):
                            engine.play_minion(card)

                
                elif event.button == 3:
                    for card in engine.player.shop:
                        if card.rect.collidepoint(pos):
                            engine.toggle_freeze(card)

        
        renderer.draw_game(engine.player, buttons)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
