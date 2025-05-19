import pygame
import random
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 400
MOVEMENT_SPEED = 5
FONT_SIZE = 72
BLACK = pygame.Color('black')
RED = pygame.Color('red')
BLUE = pygame.Color('dodgerblue')
WHITE = pygame.Color('white')

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
    
    def move(self, x_change, y_change):
        self.rect.x = max(0, min(self.rect.x + x_change, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + y_change, SCREEN_HEIGHT - self.rect.height))

def create_sprite(color, width, height, group):
    sprite = Sprite(color, width, height)
    sprite.rect.x = random.randint(0, SCREEN_WIDTH - width)
    sprite.rect.y = random.randint(0, SCREEN_HEIGHT - height)
    group.add(sprite)
    return sprite

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sprite Collision")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Times New Roman", FONT_SIZE)
    
    # Try to load background, fallback to solid color
    try:
        background = pygame.transform.scale(pygame.image.load("b.jpg"), 
                                          (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(BLUE)
    
    # Create sprites
    all_sprites = pygame.sprite.Group()
    player = create_sprite(BLACK, 30, 20, all_sprites)
    target = create_sprite(RED, 30, 20, all_sprites)
    
    # Game state
    running = True
    won = False
    
    # Main game loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    running = False
                elif won and event.key == pygame.K_r:  # Restart game
                    all_sprites.empty()
                    player = create_sprite(BLACK, 30, 20, all_sprites)
                    target = create_sprite(RED, 30, 20, all_sprites)
                    won = False
        
        # Game logic
        if not won:
            keys = pygame.key.get_pressed()
            x_move = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * MOVEMENT_SPEED
            y_move = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * MOVEMENT_SPEED
            player.move(x_move, y_move)
            
            if pygame.sprite.collide_rect(player, target):
                all_sprites.remove(target)
                won = True
        
        # Rendering
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        
        if won:
            win_text = font.render("You Win!", True, WHITE)
            restart_text = font.render("Press R to restart", True, WHITE)
            screen.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) // 2,
                                   (SCREEN_HEIGHT - win_text.get_height()) // 2 - 40))
            screen.blit(restart_text, ((SCREEN_WIDTH - restart_text.get_width()) // 2,
                                     (SCREEN_HEIGHT - restart_text.get_height()) // 2 + 40))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()