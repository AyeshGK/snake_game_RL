import pygame 
import random
from enum import Enum
from collections import namedtuple



pygame.init()
font = pygame.font.Font('arial.ttf',25)

BLOCK_SIZE = 20
SPEED = 10

# RGB color
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')


class SnakeGame:
    def __init__(self,w=640,h=480):
        self.width = w
        self.height = h

        #  screen init 
        self.dispaly = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        # game init 
        self.direction = Direction.RIGHT
        self.head = Point(self.width/2,self.height/2)
        self.snake= [
                        self.head,
                        Point(self.head.x-BLOCK_SIZE,self.head.y),
                        Point(self.head.x-(2*BLOCK_SIZE),self.head.y)
                    ]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0,(self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # collect use input 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
        
        # move
        self._move(self.direction)
        self.snake.insert(0,self.head)

        # check if game over
        game_over = False
        if self._is_collision() :
            game_over = True
            return game_over,self.score

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        

        # update the state of the game
        self._update_snake_ui()
        self.clock.tick(SPEED)

        # game over 
        return game_over, self.score

    def _update_snake_ui(self):
        self.dispaly.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.dispaly,GREEN,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.dispaly,WHITE,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE),1)

        pygame.draw.rect(self.dispaly,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))

        text = font.render("Score: "+str(self.score),True,WHITE)
        self.dispaly.blit(text,[0,0])

        pygame.display.flip()

    def _move(self,direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x,y)

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True

        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

if __name__ == '__main__':
    game = SnakeGame()
    while True:
        game_over,score = game.play_step()
        if game_over == True:
            break

    print('Final Score',score)
    
    pygame.quit()