# src/ui_renderer.py

import pygame

WHITE=(240,240,240); GRAY=(180,180,180); BLACK=(20,20,20); BLUE_FROZEN=(100,200,255)

class UIRenderer:
    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.assets = asset_manager

    def draw_card(self, minion):
        rect = minion.rect
        color = BLUE_FROZEN if minion.is_frozen else GRAY
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=8)
        
        name_txt = self.assets.font_small.render(minion.name[:12], True, BLACK)
        self.screen.blit(name_txt, (rect.x + 5, rect.y + 10))
        
        atk_txt = self.assets.font_small.render(f"ATK: {minion.attack}", True, (200, 0, 0))
        self.screen.blit(atk_txt, (rect.x + 10, rect.y + 120))
        
        hp_txt = self.assets.font_small.render(f"HP: {minion.health}", True, (0, 150, 0))
        self.screen.blit(hp_txt, (rect.x + 60, rect.y + 120))

    def draw_game(self, player, buttons):
        self.screen.fill(WHITE)
        
        info_text = f"Turn: {player.turn} | Gold: {player.gold}/{player.max_gold} | Tavern: Tier {player.tavern_tier}"
        self.screen.blit(self.assets.font_big.render(info_text, True, BLACK), (20, 10))

        for name, data in buttons.items():
            pygame.draw.rect(self.screen, data["color"], data["rect"], border_radius=8)
            txt = self.assets.font_small.render(data["text"], True, BLACK)
            self.screen.blit(txt, (data["rect"].x + 10, data["rect"].y + 15))

        for minion in player.shop: self.draw_card(minion)
        for minion in player.hand: self.draw_card(minion)
        for minion in player.board: self.draw_card(minion)