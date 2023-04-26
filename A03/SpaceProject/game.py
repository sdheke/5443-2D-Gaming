import pygame
from rich import json
import sys

from models import Asteroid, Spaceship, NPC, Wormhole1, Wormhole2, Damage_bar, Explosion
from utils import get_random_position, load_sprite, print_text, load_sound, mykwargs


import pygame
import math
import random
from pygame.math import Vector2
from comms import CommsSender, CommsListener
from manager import commsManager

from urllib.request import urlopen

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

time_elapse = 500

pygame.mixer.init()

pygame.mixer.music.load("sounds/song21.mp3")

# Add the ships to a list
ships = ["space_ship1", "space_ship2", "space_ship3", "space_ship4", "space_ship5", "space_ship6", "space_ship7", "space_ship8", "space_ship9", "space_ship10"]
display_time = 1000  # Time in milliseconds to display each image

# def callback(ch, method, properties, body):
#     """This method gets run when a message is received. You can alter it to
#     do whatever is necessary.
#     """
#     #body = body.decode("utf-8")
#     print(body)


class Spacers:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        """
        To Run: py/python __main__.py game-01 player-01
        """
        url = "https://terrywgriffin.com/current_usage.json"
        response = urlopen(url)
        data_json = json.loads(response.read())
        if len(data_json['players']) >= 10:
            print(data_json['players'])
            print("max users exceed!")
            exit(111)

        args, kwargs = mykwargs(sys.argv)

        queue = kwargs.get("queue", None)
        playerId = kwargs.get("player", None)
        creds = {
            "exchange": queue,
            "port": "5672",
            "host": "terrywgriffin.com",
            "user": playerId,
            "password": playerId + "2023!!!!!",
        }

        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("BackgroundSupernovaLarge", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.hit = load_sound("ExplodeKG")
        self.explosion = load_sound("CrashKG")
        self.taunt = load_sound("Funny-16")
        self.spawn = load_sound("SpawnKG")
        self.teleport = load_sound("TeleportKG")
        #self.song = pygame.mixer.music.load("sounds/song21.wav")
        pygame.mixer.music.play(-1)
        self.targets = []
        self.asteroids = []
        self.bullets = []
        self.blackholes = []
  
        self.wormhole2 = Wormhole1(self.screen)
        self.wormhole3 = Wormhole2(self.screen)
        self.damage_bar = Damage_bar(self.screen)
        self.npc = NPC((random.randrange(10, 790, 1), random.randrange(10, 790, 1)), self.bullets.append, random.choice(ships), self.targets)
        self.enemies = []

        self.manager = commsManager(self.bullets.append)
        localSpaceShip = Spaceship((400,300),self.bullets.append, None,
           id=playerId,creds=creds, callback= self.manager.callBack)
        
        self.manager.addPlayer(None, player=localSpaceShip, localPlayer=True)

        self.spaceship = localSpaceShip
        # Griffin changed this to 1 so it would only generate 1 asteroid :)
        for _ in range(2):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))
        
        # if len(self.blackholes) == 0:
        #     self.blackholes.append(Wormhole1(self.screen))

        if len(self.enemies) == 0:
            #self.targets.append(self.npc)
            self.targets.append(self.spaceship)
            self.enemies.append(NPC((random.randrange(10, 790, 1), random.randrange(10, 790, 1)), self.bullets.append, random.choice(ships), self.targets))

    def main_loop(self, status):
        global time_elapse
        running = status
        while running:
            self._handle_input()
            self._process_game_logic()
            self._draw()
        
            time_elapse -= 1

            if time_elapse == 0 and self.message != "You Won!" and self.message != "You lost!":
                # if len(self.enemies) == 0:
                #     self.targets.append(self.spaceship)
                #     self.targets.append(self.npc)
                self.spawn.play()
                self.enemies.append(NPC((random.randrange(10, 790, 1), random.randrange(10, 790, 1)), self.bullets.append, random.choice(ships), self.targets))
                time_elapse = 500

    def _init_pygame(self):

        pygame.init()
        
        pygame.display.set_caption("Spacers")

        # self.listener = CommsListener(callback)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
                self.spaceship.sendData()
            if is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
                self.spaceship.sendData()
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
                self.spaceship.sendData()
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.decelerate()
                self.spaceship.sendData()
            if is_key_pressed[pygame.K_b]:
                self.spaceship.brake()
                self.spaceship.sendData()
                

    def _process_game_logic(self):

        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            self.damage_bar.update(self.spaceship.damage, self.spaceship.kills)
            if self.spaceship.damage >= 100:
                    self.spaceship = None
                    self.explosion.play()
                    self.message = "You lost!"
            if self.spaceship is not None:
                for asteroid in self.asteroids:
                    #print(asteroid)
                    if self.spaceship.collides_with(asteroid):
                        self.hit.play()
                        self.spaceship.damage += 10
                        #self.damage_bar.update(self.spaceship.damage)
                        self.asteroids.remove(asteroid)
                        asteroid.split()
                        break

                    elif self.spaceship.damage >= 100:
                        self.explode.update(self.spaceship.position)
                        self.spaceship = None
                        self.spaceship.explode(self.screen)
                        # self.explosion.play()
                        self.message = "You lost!"

        for enemy in self.enemies:
            enemy.choose_target()
            enemy.follow_target()
            enemy.shoot()
            if len(self.enemies) > 0:
                if enemy.damage >= 100:
                    self.enemies.remove(enemy)
                    self.spaceship.kills += 1
                    self.explosion.play()
                if len(self.enemies) > 0:
                    for asteroid in self.asteroids:
                        if enemy.collides_with(asteroid):
                            self.hit.play()
                            enemy.damage += 10
                            self.asteroids.remove(asteroid)
                            asteroid.split()

                        # elif enemy.damage >= 100:
                        #     self.enemies.remove(enemy)
                        #     self.explosion.play()
                
        if self.wormhole3:
            self.wormhole3.update()
            if self.wormhole2:
                self.wormhole2.update()
                
                #Teleporting the spaceship
                if self.wormhole3.available:
                    if self.spaceship and self.spaceship.collides_withPos(self.wormhole2,Vector2(self.wormhole2.pos1.x + 40, self.wormhole2.pos1.y + 40)):
                        self.wormhole2.available = False
                        self.spaceship.position = Vector2(self.wormhole3.pos2.x + 40 - 32,self.wormhole3.pos2.y + 40 - 32)
                        self.spaceship.velocity = Vector2(0,0)
                        self.teleport.play()

                if self.wormhole2.available:
                    if self.spaceship and self.spaceship.collides_withPos(self.wormhole3,Vector2(self.wormhole3.pos2.x + 40 ,self.wormhole3.pos2.y + 40)):
                        self.wormhole3.available = False
                        self.spaceship.position = Vector2(self.wormhole2.pos1.x + 40 - 32,self.wormhole2.pos1.y + 40 - 32)
                        self.spaceship.velocity = Vector2(0, 0)
                        self.teleport.play()
                        


        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

            # if bullet.belongTo == "player" and bullet.collides_with(self.npc):
            #     self.npc.damage += 5
            #     self.hit.play()
            #     self.bullets.remove(bullet)
            #     break

            if self.spaceship and bullet.belongTo == "npc" and bullet.collides_with(self.spaceship):
                self.spaceship.damage += 5
                self.hit.play()
                self.bullets.remove(bullet)

        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.belongTo == "player" and bullet.collides_with(enemy):
                    enemy.damage += 5
                    self.hit.play()
                    self.bullets.remove(bullet)
                    break

        if len(self.enemies) == 0:
            self.message = "You Won!"

        # if not self.npc and self.spaceship:
        #     self.message = "You won!"

    def _draw(self):
        global time_elapse
        self.screen.blit(self.background, (0,0))
        for game_object in self._get_game_objects():
            #print(game_object)
            game_object.draw(self.screen)

        if self.wormhole2:
            self.wormhole2.draw(self.screen)

        if self.wormhole3:
            self.wormhole3.draw(self.screen)

        if self.damage_bar:
            self.damage_bar
        else:
            self.damage_bar.update(100, self.spaceship.kills)

        for enemy in self.enemies:
            if enemy:
                enemy.damage_bar(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        # if self.npc:
        #     game_objects.append(self.npc)

        for enemy in self.enemies:
            if enemy:
                game_objects.append(enemy)

        return game_objects
    
    def _map_scroll(self):
        # self.spaceship.rect = self.spaceship.get_rect()
        # self.background.rect = self.background.get_rect()
        
        # if self.spaceship.rect.x > self.screen.get_width() / 2:
        #     self.background.rect.x += self.spaceship.speed

        # if self.spaceship.rect.x < self.screen.get_width() / 2:
        #     self.background.rect.x -= self.spaceship.speed
        
        # if self.spaceship.rect.y > self.screen.get_height() / 2:
        #     self.background.rect.y += self.spaceship.speed

        # if self.spaceship.rect.y < self.screen.get_height() / 2:
        #     self.background.rect.y -= self.spaceship.speed
        pass