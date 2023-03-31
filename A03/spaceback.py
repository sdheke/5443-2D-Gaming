import pygame
import random

pygame.init()
timer = pygame.time.Clock()
fps = 60

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Rock Game")

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Set up the fonts
# small_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 50)
# smaller_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 30)
# big_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 75)
# bigger_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 90)
        # Define the ships
ship1 = pygame.image.load("sprites/space_ship1.png")
ship2 = pygame.image.load("sprites/space_ship2.png")
ship3 = pygame.image.load("sprites/space_ship3.png")
ship4 = pygame.image.load("sprites/space_ship4.png")
ship5 = pygame.image.load("sprites/space_ship5.png")
ship6 = pygame.image.load("sprites/space_ship6.png")
ship7 = pygame.image.load("sprites/space_ship7.png")
ship8 = pygame.image.load("sprites/space_ship8.png")
ship9 = pygame.image.load("sprites/space_ship9.png")
ship10 = pygame.image.load("sprites/space_ship10.png")

# Add the ships to a list
ships = [ship1, ship2, ship3, ship4, ship5, ship6, ship7, ship8, ship9, ship10]

class Spaceship(pygame.sprite.Sprite):
    MANEUVERABILITY = 3

    def __init__(self):
        super().__init__()
        self.image = random.choice(ships)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.hitbox = self.rect.inflate(-20, -20)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.speed_x = 0
        self.speed_y = 0
    
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.speed_x -= 5
            self.rect.left = max(20, self.rect.left + self.speed_x)
        if key[pygame.K_RIGHT]:
            self.speed_x += 5
            self.rect.right = min(screen.get_height() - 20, self.rect.right + self.speed_x)
        if key[pygame.K_UP]:
            self.speed_y -= 5
            self.rect.top = max(20, self.rect.top + self.speed_y)
        if key[pygame.K_DOWN]:
            self.speed_y += 5
            self.rect.bottom = min(screen.get_width() - 20, self.rect.bottom + self.speed_y)
        
        # if direction == "left":
        #     self.speed_x -= 5
        # elif direction == "right":
        #     self.speed_x += 5
        # elif direction == "up":
        #     self.speed_y -= 5
        # elif direction == "down":
        #     self.speed_y += 5

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        self.angle = self.MANEUVERABILITY * sign
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

class SpaceRock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/asteroid.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)
    
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() / 2
        self.half_height = self.display_surface.get_height() / 2
        self.offset = pygame.math.Vector2()

    def draw(self, space1):

        self.offset.x = -space1.rect.x + self.half_width
        self.offset.y = -space1.rect.y + self.half_height
        
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)

# NEW_SPACE_ROCK = pygame.USEREVENT + 1
# pygame.time.set_timer(NEW_SPACE_ROCK, 1000)
background = pygame.image.load("sprites/BackgroundSupernova.png")
background_width = background.get_width()
background_height= background.get_height()
background_x = 0
background_y = 0

#Adding the spaceship and the space rock to the sprite groups
space1 = Spaceship()
spaceship = pygame.sprite.Group()
spaceship.add(space1)            
new_rock = SpaceRock()
space_rock_group = pygame.sprite.Group()
space_rock_group.add(new_rock)


running = True
while running:
    timer.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        space1.move()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_ESCAPE:
        #         running = False
        #     elif event.key == pygame.K_LEFT:
        #         space1.move("left")
        #     elif event.key == pygame.K_RIGHT:
        #         space1.move("right")
        #     elif event.key == pygame.K_UP:
        #         space1.move("up")
        #     elif event.key == pygame.K_DOWN:
        #         space1.move("down")
        # elif event.type == NEW_SPACE_ROCK:

    # Scroll the map
    # background_x -= 5
    # if background_x < -background.get_width():
    #     background_x = 0

    # Scroll the map based on the player position
    if space1.rect.x > screen.get_width() / 2:
        background_x -= space1.speed
    if space1.rect.x < screen.get_width() / 2:
        background_x += space1.speed
    if space1.rect.y > screen.get_height() / 2:
        background_y -= space1.speed
    elif space1.rect.y < screen.get_height() / 2:
        background_y += space1.speed

    # Keep the map within bounds
    if background_x < -background.get_width() + screen.get_width():
        background_x = -background.get_width() + screen.get_width()
    if background_x > 0:
        background_x = 0
    if background_y < -background.get_height() + screen.get_height():
        background_y = -background.get_height() + screen.get_height()
    elif background_y > 0:
        background_y = 0

    screen.blit(background, (background_x, background_y))

    spaceship.draw(screen)
    space_rock_group.draw(screen)

    spaceship.update()
    space_rock_group.update()

    pygame.display.update()


pygame.quit()
exit()
