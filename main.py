import pygame
from pygame.locals import *
import sys
import os
from menu import menu, Speed

pygame.init()
pygame.mixer.init()

# Game dimensions
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 20
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        
        # Initialize sound (create a simple beep sound if no sound file exists)
        self.bounce_sound = self.create_bounce_sound()
        self.score_sound = self.create_score_sound()
        
        # Game objects
        self.player_paddle = pygame.Rect(WIDTH - 30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ai_paddle = pygame.Rect(15, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        
        # Game state
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.Font(None, 74)
        self.clock = pygame.time.Clock()
        
        # Ball speed will be set based on menu selection
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        
    def create_bounce_sound(self):
        """Create a simple bounce sound programmatically"""
        try:
            # Create a simple beep sound
            sample_rate = 22050
            duration = 0.1
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * pygame.math.sin(2 * pygame.math.pi * 440 * i / sample_rate)
                arr.append([int(wave), int(wave)])
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            return sound
        except:
            # If sound creation fails, return None
            return None
    
    def create_score_sound(self):
        """Create a simple score sound programmatically"""
        try:
            sample_rate = 22050
            duration = 0.3
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 2048 * pygame.math.sin(2 * pygame.math.pi * 220 * i / sample_rate)
                arr.append([int(wave), int(wave)])
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            return sound
        except:
            return None
    
    def play_sound(self, sound):
        """Play sound if it exists"""
        if sound:
            try:
                sound.play()
            except:
                pass
    
    def reset_ball(self):
        """Reset ball to center with random direction"""
        self.ball.center = (WIDTH//2, HEIGHT//2)
        # Randomize initial direction
        import random
        self.ball_speed_x *= random.choice([-1, 1])
        self.ball_speed_y = random.choice([-abs(self.ball_speed_y), abs(self.ball_speed_y)])
    
    def update_ai_paddle(self):
        """AI paddle movement"""
        ai_speed = 6
        
        # AI follows the ball with some lag for realistic gameplay
        if self.ai_paddle.centery < self.ball.centery - 10:
            if self.ai_paddle.bottom < HEIGHT:
                self.ai_paddle.y += ai_speed
        elif self.ai_paddle.centery > self.ball.centery + 10:
            if self.ai_paddle.top > 0:
                self.ai_paddle.y -= ai_speed
    
    def handle_collisions(self):
        """Handle ball collisions"""
        # Top and bottom walls
        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.ball_speed_y *= -1
            self.play_sound(self.bounce_sound)
        
        # Left wall (AI scores)
        if self.ball.left <= 0:
            self.player_score += 1
            self.play_sound(self.score_sound)
            self.reset_ball()
        
        # Right wall (Player scores)
        if self.ball.right >= WIDTH:
            self.ai_score += 1
            self.play_sound(self.score_sound)
            self.reset_ball()
        
        # Paddle collisions
        if self.ball.colliderect(self.player_paddle) and self.ball_speed_x > 0:
            self.ball_speed_x *= -1
            self.play_sound(self.bounce_sound)
            # Add some variation to the ball direction based on where it hits the paddle
            hit_pos = (self.ball.centery - self.player_paddle.centery) / (PADDLE_HEIGHT / 2)
            self.ball_speed_y += hit_pos * 2
        
        if self.ball.colliderect(self.ai_paddle) and self.ball_speed_x < 0:
            self.ball_speed_x *= -1
            self.play_sound(self.bounce_sound)
            # Add some variation to the ball direction
            hit_pos = (self.ball.centery - self.ai_paddle.centery) / (PADDLE_HEIGHT / 2)
            self.ball_speed_y += hit_pos * 2
        
        # Keep ball speed reasonable
        if abs(self.ball_speed_y) > 10:
            self.ball_speed_y = 10 if self.ball_speed_y > 0 else -10
    
    def draw_escape_menu(self):
        """Draw the escape menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Menu box
        menu_width, menu_height = 300, 200
        menu_x = WIDTH // 2 - menu_width // 2
        menu_y = HEIGHT // 2 - menu_height // 2
        
        pygame.draw.rect(self.screen, (40, 40, 40), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), 3)
        
        # Title
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, menu_y + 30))
        self.screen.blit(title_text, title_rect)
        
        return menu_x, menu_y, menu_width, menu_height
    
    def draw_menu_option(self, text, x, y, width, height, selected=False):
        """Draw a menu option button"""
        color = (100, 100, 255) if selected else (60, 60, 60)
        border_color = (255, 255, 255) if selected else (150, 150, 150)
        text_color = (255, 255, 255)
        
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2)
        
        option_font = pygame.font.Font(None, 36)
        option_text = option_font.render(text, True, text_color)
        text_rect = option_text.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(option_text, text_rect)
    
    def show_escape_menu(self):
        """Show the escape menu and handle input"""
        menu_options = ["Resume", "New Game", "Quit"]
        selected_option = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "resume"
                    elif event.key == K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == K_RETURN:
                        if selected_option == 0:  # Resume
                            return "resume"
                        elif selected_option == 1:  # New Game
                            return "new_game"
                        elif selected_option == 2:  # Quit
                            return "quit"
            
            # Redraw the game state
            self.draw()
            
            # Draw escape menu
            menu_x, menu_y, menu_width, menu_height = self.draw_escape_menu()
            
            # Draw menu options
            button_width = 200
            button_height = 30
            button_x = WIDTH // 2 - button_width // 2
            start_y = menu_y + 70
            
            for i, option in enumerate(menu_options):
                button_y = start_y + i * 40
                selected = (i == selected_option)
                self.draw_menu_option(option, button_x, button_y, button_width, button_height, selected)
            
            # Instructions
            inst_font = pygame.font.Font(None, 24)
            inst_text = inst_font.render("Use UP/DOWN to select, ENTER to confirm, ESC to resume", True, (200, 200, 200))
            inst_rect = inst_text.get_rect(center=(WIDTH // 2, menu_y + menu_height - 20))
            self.screen.blit(inst_text, inst_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def draw(self):
        """Draw all game objects"""
        self.screen.fill((0, 0, 0))
        
        # Draw paddles
        pygame.draw.rect(self.screen, (255, 255, 255), self.player_paddle)
        pygame.draw.rect(self.screen, (255, 255, 255), self.ai_paddle)
        
        # Draw ball
        pygame.draw.ellipse(self.screen, (255, 255, 255), self.ball)
        
        # Draw center line
        for i in range(0, HEIGHT, 20):
            pygame.draw.rect(self.screen, (255, 255, 255), (WIDTH//2 - 2, i, 4, 10))
        
        # Draw scores
        player_text = self.font.render(str(self.player_score), True, (255, 255, 255))
        ai_text = self.font.render(str(self.ai_score), True, (255, 255, 255))
        
        self.screen.blit(player_text, (WIDTH//2 + 50, 50))
        self.screen.blit(ai_text, (WIDTH//2 - 100, 50))
        
        # Draw labels
        label_font = pygame.font.Font(None, 36)
        player_label = label_font.render("PLAYER", True, (200, 200, 200))
        ai_label = label_font.render("AI", True, (200, 200, 200))
        
        self.screen.blit(player_label, (WIDTH//2 + 50, 100))
        self.screen.blit(ai_label, (WIDTH//2 - 100, 100))
        
        pygame.display.flip()
    
    def reset_game(self, speed_setting):
        """Reset the game state for a new game"""
        self.player_score = 0
        self.ai_score = 0
        
        # Set ball speed based on menu selection
        speed_map = {
            Speed.SLOW: 4,
            Speed.MEDIUM: 7,
            Speed.FAST: 10
        }
        base_speed = speed_map[speed_setting]
        self.ball_speed_x = base_speed
        self.ball_speed_y = base_speed // 2
        
        self.reset_ball()
    
    def run(self, speed_setting):
        """Main game loop"""
        self.reset_game(speed_setting)
        
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        # Show escape menu
                        menu_result = self.show_escape_menu()
                        if menu_result == "quit":
                            running = False
                        elif menu_result == "new_game":
                            # Show menu again to select speed
                            new_speed = menu()
                            self.reset_game(new_speed)
                        # If "resume", just continue the game loop
            
            # Handle player input
            keys = pygame.key.get_pressed()
            if keys[K_UP] and self.player_paddle.top > 0:
                self.player_paddle.y -= 8
            if keys[K_DOWN] and self.player_paddle.bottom < HEIGHT:
                self.player_paddle.y += 8
            
            # Update AI
            self.update_ai_paddle()
            
            # Update ball
            self.ball.x += self.ball_speed_x
            self.ball.y += self.ball_speed_y
            
            # Handle collisions
            self.handle_collisions()
            
            # Draw everything
            self.draw()
            
            # Control frame rate
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    """Main function to start the game"""
    # Show menu and get speed selection
    speed_selection = menu()
    
    # Create and run the game
    game = PongGame()
    game.run(speed_selection)

if __name__ == "__main__":
    main()
