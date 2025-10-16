import pygame 
import random 
import numpy as np 
 
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
 
        # Generate sounds in memory 
        self.sound_paddle = self.generate_sound(600) 
        self.sound_wall = self.generate_sound(800) 
        self.sound_score = self.generate_sound(1000) 
 
    def generate_sound(self, frequency=440, duration=0.15, volume=0.5): 
        """Generates a simple sine wave sound effect.""" 
        sample_rate = 44100 
        t = np.linspace(0, duration, int(sample_rate * duration), False) 
        wave = np.sin(frequency * t * 2 * np.pi) 
        wave = (wave * 32767).astype(np.int16) 
        sound = pygame.mixer.Sound(buffer=wave) 
        sound.set_volume(volume) 
        return sound 
 
    def move(self): 
        self.x += self.velocity_x 
        self.y += self.velocity_y 
 
        # Bounce off top/bottom 
        if self.y <= 0: 
            self.y = 0 
            self.velocity_y *= -1 
            self.sound_wall.play() 
        elif self.y + self.height >= self.screen_height: 
            self.y = self.screen_height - self.height 
            self.velocity_y *= -1 
            self.sound_wall.play() 
 
    def check_collision(self, player, ai): 
        """Checks collision with paddles and plays sound.""" 
        # Player paddle 
        if self.rect().colliderect(player.rect()) and self.velocity_x < 0: 
            self.x = player.rect().right 
            self.velocity_x *= -1 
            self.sound_paddle.play() 
            offset = (self.y + self.height / 2) - (player.y + player.height / 2) 
            self.velocity_y += offset * 0.05 
 
        # AI paddle 
        elif self.rect().colliderect(ai.rect()) and self.velocity_x > 0: 
            self.x = ai.rect().left - self.width 
            self.velocity_x *= -1 
            self.sound_paddle.play() 
            offset = (self.y + self.height / 2) - (ai.y + ai.height / 2) 
            self.velocity_y += offset * 0.05 
 
    def reset(self): 
        self.x = self.original_x 
        self.y = self.original_y 
        self.velocity_x *= -1 
        self.velocity_y = random.choice([-3, 3]) 
 
    def rect(self): 
        return pygame.Rect(self.x, self.y, self.width, self.height)