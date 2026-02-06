# src/ui_renderer.py

import pygame

WHITE=(240,240,240); GRAY=(180,180,180); BLACK=(20,20,20);

class UIRenderer:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

    def draw_card(self, m):
        pygame.draw.rect(self.screen, GRAY, m.rect, border_radius=8)
        pygame.draw.rect(self.screen, BLACK, m.rect, 2, border_radius=8)
        self.screen.blit(self.assets.font_small.render(m.name[:12], True, BLACK), (m.rect.x+6, m.rect.y+8))
        self.screen.blit(self.assets.font_small.render(f"{m.attack}/{m.health}", True, BLACK), (m.rect.x+10, m.rect.y+120))


    def draw(self, player, buttons):
        self.screen.fill(WHITE)
        info = f"Turn {player.turn} | Gold {player.gold}/{player.max_gold} | Tavern {player.tavern_tier}"
        self.screen.blit(self.assets.font_big.render(info, True, BLACK), (20,10))


        for b in buttons.values():
            pygame.draw.rect(self.screen, b['color'], b['rect'], border_radius=8)
            self.screen.blit(self.assets.font_small.render(b['text'], True, BLACK), (b['rect'].x+10, b['rect'].y+15))


        for m in player.shop + player.hand + player.board:
            self.draw_card(m)