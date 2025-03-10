import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Directions (x, y)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        """Initialize the Snake with default position, direction, and score."""
        self.head = [GRID_WIDTH // 2, GRID_HEIGHT // 2]
        self.body = [[self.head[0], self.head[1]],
                     [self.head[0]-1, self.head[1]],
                     [self.head[0]-2, self.head[1]]]
        self.direction = RIGHT
        self.score = 0

    def change_direction(self, direction):
        """Change the snake's direction based on user input, preventing 180 degree turns."""
        if direction == 'UP' and self.direction != DOWN:
            self.direction = UP
        if direction == 'DOWN' and self.direction != UP:
            self.direction = DOWN
        if direction == 'LEFT' and self.direction != RIGHT:
            self.direction = LEFT
        if direction == 'RIGHT' and self.direction != LEFT:
            self.direction = RIGHT

    def move(self):
        """Move the snake by adding a new head and removing the tail."""
        new_head = [self.head[0] + self.direction[0], self.head[1] + self.direction[1]]
        self.body.insert(0, new_head)
        self.head = new_head
        self.body.pop()

    def grow(self):
        """Grow the snake by adding a new head without removing the tail."""
        new_head = [self.head[0] + self.direction[0], self.head[1] + self.direction[1]]
        self.body.insert(0, new_head)
        self.head = new_head
        self.score += 1

    def check_collision(self):
        """Check if snake collides with walls or itself."""
        if self.head[0] < 0 or self.head[0] >= GRID_WIDTH or self.head[1] < 0 or self.head[1] >= GRID_HEIGHT:
            return True
        if self.head in self.body[1:]:
            return True
        return False

    def draw(self, screen):
        """Draw the snake on the screen."""
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Coin:
    def __init__(self):
        """Initialize the coin with a random position."""
        self.position = [random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)]

    def respawn(self):
        """Respawn the coin at a new random position."""
        self.position = [random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)]

    def draw(self, screen):
        """Draw the coin on the screen."""
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Game:
    def __init__(self):
        """Initialize the game with snake, coin, and game over status."""
        self.snake = Snake()
        self.coin = Coin()
        self.game_over = False

    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction('RIGHT')

    def update(self):
        """Update game state each frame."""
        self.snake.move()

        # Check collision with coin
        if self.snake.head == self.coin.position:
            self.snake.grow()
            self.coin.respawn()

        # Check collision with walls or itself
        if self.snake.check_collision():
            self.game_over = True

    def draw(self, screen):
        """Draw all game objects on the screen."""
        screen.fill(BLACK)
        self.snake.draw(screen)
        self.coin.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.snake.score}', True, WHITE)
        screen.blit(text, (10, 10))

    def run(self):
        """Run the game loop."""
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')

        clock = pygame.time.Clock()

        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw(screen)
            pygame.display.update()
            clock.tick(10)  # Adjust the speed of the game

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
