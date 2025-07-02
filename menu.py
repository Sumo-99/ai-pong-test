import pygame
import sys

pygame.init()

# Enum for speed
class Speed:
    SLOW = 'slow'
    MEDIUM = 'medium'
    FAST = 'fast'

def draw_menu(screen, speed):
    font = pygame.font.Font(None, 74)
    title_text = font.render("PONG", True, (255, 255, 255))
    screen.blit(title_text, (screen.get_width()//2 - title_text.get_width()//2, 50))
    
    subtitle_font = pygame.font.Font(None, 48)
    subtitle_text = subtitle_font.render("Select Ball Speed", True, (255, 255, 255))
    screen.blit(subtitle_text, (screen.get_width()//2 - subtitle_text.get_width()//2, 120))

    # Speed options
    option_font = pygame.font.Font(None, 36)
    colors = {Speed.SLOW: (255, 100, 100), Speed.MEDIUM: (255, 255, 100), Speed.FAST: (100, 255, 100)}
    y_positions = {Speed.SLOW: 200, Speed.MEDIUM: 250, Speed.FAST: 300}
    labels = {Speed.SLOW: "Slow", Speed.MEDIUM: "Medium (Recommended)", Speed.FAST: "Fast"}

    for s in [Speed.SLOW, Speed.MEDIUM, Speed.FAST]:
        color = colors[s]
        y = y_positions[s]
        label = labels[s]
        
        # Draw selection box
        rect = pygame.Rect(150, y - 5, 300, 40)
        if s == speed:
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
        else:
            pygame.draw.rect(screen, (50, 50, 50), rect)
            pygame.draw.rect(screen, color, rect, 2)
        
        # Draw text
        text_color = (0, 0, 0) if s == speed else color
        text = option_font.render(label, True, text_color)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Instructions
    inst_font = pygame.font.Font(None, 24)
    inst_text1 = inst_font.render("Use UP/DOWN arrows to select", True, (200, 200, 200))
    inst_text2 = inst_font.render("Press ENTER to start", True, (200, 200, 200))
    screen.blit(inst_text1, (screen.get_width()//2 - inst_text1.get_width()//2, 380))
    screen.blit(inst_text2, (screen.get_width()//2 - inst_text2.get_width()//2, 410))

def menu():
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Pong - Menu")

    speed = Speed.MEDIUM
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        draw_menu(screen, speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return speed
                if event.key == pygame.K_UP:
                    if speed == Speed.MEDIUM:
                        speed = Speed.SLOW
                    elif speed == Speed.FAST:
                        speed = Speed.MEDIUM
                if event.key == pygame.K_DOWN:
                    if speed == Speed.SLOW:
                        speed = Speed.MEDIUM
                    elif speed == Speed.MEDIUM:
                        speed = Speed.FAST

        pygame.display.flip()
        clock.tick(30)
