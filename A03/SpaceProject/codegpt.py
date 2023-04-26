```python
import pygame
import random

# Initialize pygame
pygame.init()

# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Create the wormhole sprite
wormhole_image = pygame.image.load("wormhole.png").convert_alpha()
wormhole_rect = wormhole_image.get_rect()

# Generate a random position for the wormhole
wormhole_rect.x = random.randint(0, screen_width - wormhole_rect.width)
wormhole_rect.y = random.randint(0, screen_height - wormhole_rect.height)

# Create the wormhole sprite object
wormhole_sprite = pygame.sprite.Sprite()
wormhole_sprite.image = wormhole_image
wormhole_sprite.rect = wormhole_rect

# Add the wormhole sprite to the sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(wormhole_sprite)

# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw all sprites
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
```


Here's an example code that shows how you can animate a list of images using Python:

```python
import pygame

# Initialize Pygame
pygame.init()

# Set the size of the window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

# Set the frames per second (FPS) of the animation
FPS = 30

# Create a window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Animation Example")

# Load a list of images
images = ["image1.png", "image2.png", "image3.png"]
current_image = 0
max_images = len(images)

# Set the clock for the FPS
clock = pygame.time.Clock()

# Start the animation loop
while True:
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Draw the current image on the window
    current_image_path = images[current_image]
    current_image_surface = pygame.image.load(current_image_path)
    window.blit(current_image_surface, (0, 0))

    # Check if we need to change images
    current_image += 1
    if current_image >= max_images:
        current_image = 0

    # Update the display
    pygame.display.update()

    # Pause the animation for the FPS
    clock.tick(FPS)
```

This code loads a list of images and then displays each image in the list in order, animating the images at the specified frames per second. You can adjust the `images` array to contain the list of images you want to animate, and adjust `FPS` to set the speed of the animation.