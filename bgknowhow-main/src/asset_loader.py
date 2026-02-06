# src/asset_loader.py

import pygame
import os

class AssetManager:
    def __init__(self):
        pygame.font.init()
        self.images = {}
        
        self.font_small = pygame.font.SysFont('Arial', 14, bold=True)
        self.font_big = pygame.font.SysFont('Arial', 22, bold=True)

    def get_image(self, name):
        if name in self.images: return self.images[name]
        path = os.path.join("images", "misc", name)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
        else:
            img = pygame.Surface((60,60)); img.fill((255,0,255))
        self.image[name] = img
        return img