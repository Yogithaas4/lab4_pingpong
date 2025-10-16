import pygame
import random
import numpy as np
import os

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # ✅ Load your sound file with full path and debug
        sound_path = os.path.join("assets", "ping.wav")
        full_path = os.path.abspath(sound_path)
        print("📂 Current working directory:", os.getcwd())
        print("🔊 Trying to load:", full_path)

        if os.path.exists(full_path):
            try:
                self.sound_effect = pygame.mixer.Sound(full_path)
                self.sound_effect.set_volume(0.5)
                print("✅ Sound loaded successfully!")
            except Exception as e:
                print("❌ Failed to load sound:", e)
                self.sound_effect = None
        else:
            print("⚠️ Sound file not found at:", full_path)
            self.sound_effect = None

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            if self.sound_effect:
                self.sound_effect.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            if self.sound_effect:
                self.sound_effect.play()

    def check_collision(self, player, ai):
        # Player paddle
        if self.rect().colliderect(player.rect()) and self.velocity_x < 0:
            self.x = player.rect().right
            self.velocity_x *= -1
            if self.sound_effect:
                self.sound_effect.play()
            offset = (self.y + self.height / 2) - (player.y + player.height / 2)
            self.velocity_y += offset * 0.05

        # AI paddle
        elif self.rect().colliderect(ai.rect()) and self.velocity_x > 0:
            self.x = ai.rect().left - self.width
            self.velocity_x *= -1
            if self.sound_effect:
                self.sound_effect.play()
            offset = (self.y + self.height / 2) - (ai.y + ai.height / 2)
            self.velocity_y += offset * 0.05

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
