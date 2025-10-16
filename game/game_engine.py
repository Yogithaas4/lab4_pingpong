import pygame 
from .paddle import Paddle 
from .ball import Ball 
 
WHITE = (255, 255, 255) 
 
class GameEngine: 
    def __init__(self, width, height, winning_score=5): 
        self.width = width 
        self.height = height 
        self.paddle_width = 10 
        self.paddle_height = 100 
 
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height) 
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, 
self.paddle_height) 
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height) 
 
        self.player_score = 0 
        self.ai_score = 0 
        self.font = pygame.font.SysFont("Arial", 30) 
        self.large_font = pygame.font.SysFont("Arial", 60) 
 
        self.game_over = False 
        self.winning_score = winning_score  # now dynamic 
 
    def handle_input(self): 
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_w]: 
            self.player.move(-10, self.height) 
        if keys[pygame.K_s]: 
            self.player.move(10, self.height) 
 
    def update(self): 
        if self.game_over: 
            return 
 
        self.ball.move() 
        self.ball.check_collision(self.player, self.ai) 
 
        # Scoring logic 
        if self.ball.x <= 0: 
            self.ai_score += 1 
            self.ball.sound_score.play() 
            self.ball.reset() 
        elif self.ball.x >= self.width: 
            self.player_score += 1 
            self.ball.sound_score.play() 
            self.ball.reset() 
 
        # AI tracking 
        self.ai.auto_track(self.ball, self.height) 
 
        # Check game over 
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score: 
            self.game_over = True 
 
    def render(self, screen): 
        screen.fill((0, 0, 0)) 
        pygame.draw.rect(screen, WHITE, self.player.rect()) 
        pygame.draw.rect(screen, WHITE, self.ai.rect()) 
        pygame.draw.ellipse(screen, WHITE, self.ball.rect()) 
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, 
self.height)) 
 
        # Scores 
        player_text = self.font.render(str(self.player_score), True, WHITE) 
        ai_text = self.font.render(str(self.ai_score), True, WHITE) 
        screen.blit(player_text, (self.width // 4, 20)) 
        screen.blit(ai_text, (self.width * 3 // 4, 20)) 
 
    def show_game_over(self, screen): 
        """Displays Game Over screen until restart or quit""" 
        screen.fill((0, 0, 0)) 
        winner = "Player Wins!" if self.player_score > self.ai_score else "AI Wins!" 
        text = self.large_font.render(winner, True, (255, 255, 255)) 
        msg = self.font.render("Press R to Restart or ESC to Quit", True, (200, 200, 200)) 
 
        screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 
50)) 
        screen.blit(msg, (self.width // 2 - msg.get_width() // 2, self.height // 2 + 30)) 
        pygame.display.flip() 
 
        waiting = True 
        while waiting: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    return False 
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE: 
                        pygame.quit() 
                        return False 
                    elif event.key == pygame.K_r: 
                        return True