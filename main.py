import pygame
from game.game_engine import GameEngine

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Clock
clock = pygame.time.Clock()
FPS = 60

def choose_winning_score(screen):
    """Display menu to choose winning score (3, 5, or 7)."""
    font = pygame.font.SysFont("Arial", 40)
    small_font = pygame.font.SysFont("Arial", 25)

    selecting = True
    selected_score = None

    while selecting:
        # Draw background and text
        screen.fill((0, 0, 0))
        title = font.render("Choose Winning Score", True, (255, 255, 255))
        msg = small_font.render("Press 3, 5, or 7 to select", True, (200, 200, 200))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # stop if window closed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    selected_score = 3
                    selecting = False
                elif event.key == pygame.K_5:
                    selected_score = 5
                    selecting = False
                elif event.key == pygame.K_7:
                    selected_score = 7
                    selecting = False

    return selected_score

def main():
    running = True
    winning_score = choose_winning_score(SCREEN)
    if winning_score is None:
        return  # exit cleanly if window is closed in menu

    engine = GameEngine(WIDTH, HEIGHT, winning_score)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle game over
        if engine.game_over:
            result = engine.show_game_over(SCREEN)
            if not result:
                running = False
                break
            else:
                winning_score = choose_winning_score(SCREEN)
                if winning_score is None:
                    running = False
                    break
                engine = GameEngine(WIDTH, HEIGHT, winning_score)
                continue

        # Normal gameplay
        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
