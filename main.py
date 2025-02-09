# Example file showing a basic pygame "game loop"
import pygame
from time import sleep
import random
from threading import Thread
from gameutils.imgutils import load_image, load_image_no_convert, load_sound
from gameutils.entities import PhysicsEntity, EnemyEntity

DEFAULT_SCREEN_RESOLUTION = (1280, 720)
RELOAD_TIME = 2
PLAYER_HEIGHT = 75
PLAYER_WIDTH = 100
STARTING_POS = (0, (DEFAULT_SCREEN_RESOLUTION[1]/2 - PLAYER_HEIGHT/2))
NUM_ENEMIES = 1

class Game:
    # pygame setup
    def __init__(self):
        self.devmode = True
        self.running = True
        pygame.init()
        self.scene = 1
        pygame.font.init()
        self.screen = pygame.display.set_mode(DEFAULT_SCREEN_RESOLUTION)
        pygame.display.set_caption("PyGame-Game-Jam")
        self.clock = pygame.time.Clock()
        self.gravity = False
        self.reloading = False
        self.spawning_enemy = False

        self.assets = {
            'player-img': load_image_no_convert('Dummies/dummy_player-removebg-preview.png'),
            'enemy-img': load_image_no_convert('Dummies/dummy-enemy-removebg-preview.png'),
            'bullet-img': load_image_no_convert('Dummies/dummy-bullet.gif'),
            'background-img': load_image('Dummies/dummy-background-space-3.jpeg'),
            'bullet-sound': load_sound('Dummies/laser-shot-ingame-230500.mp3')
        }
        self.e_player = PhysicsEntity(self, 'player', STARTING_POS, (PLAYER_WIDTH, PLAYER_HEIGHT), self.assets['player-img'])
        self.wave = 1
        self.score = 0
        self.bullets = []
        self.magazine = 5
        self.enemies = []
        self.magazine_text_offset = 0

        self.score_text = f"SCORE: {self.score}"
        self.magazine_text = f"BULLETS: {self.magazine}"
        self.menu_text = f"PRESS ANY KEY TO PLAY"
        self.prev_rand = 0

    def reset_battle(self):
        self.wave = 1
        self.score = 0
        self.e_player.health = 5
        self.magazine = 5
        self.prev_rand = 0

        self.e_player.pos = list(STARTING_POS)

        self.score_text = f"SCORE: {self.score}"
        self.magazine_text = f"BULLETS: {self.magazine}"

        if len(self.bullets) > 0:
            for bullet in self.bullets:
                self.bullets.remove(bullet)
        if len(self.enemies) > 0:
            for enemy in self.enemies:
                self.enemies.remove(enemy)

    
    def display_menu_text(self):
        my_font = pygame.font.SysFont('SF Pro', 100)
        self.menu_text_surface = my_font.render(self.menu_text, False, 'red')
        self.screen.blit(self.menu_text_surface, ((self.screen.get_size()[0]/2 - self.menu_text_surface.get_size()[0]/2), self.screen.get_size()[1]/2 - self.menu_text_surface.get_size()[1]/2)) 

    #SCORE AND MAGAZINE INFORMATION
    def display_score(self):
        my_font = pygame.font.SysFont('SF Pro', 100)
        self.score_text_surface = my_font.render(self.score_text, False, 'red')
        self.screen.blit(self.score_text_surface, (500, self.screen.get_size()[1] - self.score_text_surface.get_size()[1]))

    def display_magazine_text(self):
        my_font = pygame.font.SysFont('SF Pro', 100)
        self.magazine_text_surface = my_font.render(self.magazine_text, False, 'red')
        self.magazine_text_offset = self.magazine_text_surface.get_size()[1]
        self.screen.blit(self.magazine_text_surface, (0, self.screen.get_size()[1] - self.magazine_text_surface.get_size()[1]))

    def render_background(self):
        background = pygame.transform.scale(self.assets['background-img'], self.screen.get_size())
        self.screen.blit(background, (0, 0))

    #PLAYER ACTIONS, SUCH AS SHOOTING BULLETS AND RELOADING

    def shoot_bullet(self):
        if len(self.bullets) < 5 and self.magazine > 0:
            e_bullet = PhysicsEntity(self, 'bullet', (self.e_player.pos[0] + self.e_player.width, self.e_player.pos[1]), (50, 50), self.assets['bullet-img'])
            e_bullet.img.set_colorkey('black')
            self.bullets.append(e_bullet)
            self.assets['bullet-sound'].play()

    def reload(self):  
        self.magazine_text = "RELOADING"
        self.reloading = True 
        sleep(RELOAD_TIME)
        self.magazine = 5
        self.magazine_text = f"BULLETS: {self.magazine}"
        self.reloading = False

    def spawn_enemy(self, num_enemtes):
        self.spawning_enemy = True
        sleep(1)
        for i in range(num_enemtes):
            if len(self.enemies) < (self.wave // 10) + 1:
                self.enemies.append(EnemyEntity(self, 'enemy', (self.screen.get_size()[0] - 100, random.randint(0, self.screen.get_size()[1] - (100 + 100))), (100, 100), self.assets['enemy-img']))
        self.spawning_enemy = False
    
    def handle_key_input(self, e: pygame.event):
        if(e.type == pygame.KEYDOWN):
            if(self.devmode):
                pass
            if e.key == pygame.K_q:
                sleep(3)
                if len(self.bullets) > 0:
                    for bullet in self.bullets:
                        self.bullets.remove(bullet)
                if len(self.enemies) > 0:
                    for enemy in self.enemies:
                        self.enemies.remove(enemy)
                self.reset_battle()
                self.scene = 1
            if e.key == pygame.K_b:
                if(self.magazine == 0 and self.reloading == False):
                    Thread(target=self.reload).start()
                else:
                    if(len(self.bullets) < 5 and self.magazine > 0 and self.reloading == False):
                        self.shoot_bullet()
                        self.magazine -= 1
                        self.magazine_text = f"BULLETS: {self.magazine}"
            if e.key == pygame.K_UP:
                self.e_player.movingDown = False
                self.e_player.movingUp = True
            if e.key == pygame.K_LEFT:
                self.e_player.movingRight = False
                self.e_player.movingLeft = True
            if e.key == pygame.K_RIGHT:
                self.e_player.movingLeft = False
                self.e_player.movingRight = True
            if e.key == pygame.K_DOWN:
                self.e_player.movingUp = False
                self.e_player.movingDown = True
        if(e.type == pygame.KEYUP):
            if e.key == pygame.K_UP:
                self.e_player.movingUp = False
            if e.key == pygame.K_LEFT:
                self.e_player.movingLeft = False
            if e.key == pygame.K_RIGHT:
                self.e_player.movingRight = False
            if e.key == pygame.K_DOWN:
                self.e_player.movingDown = False

    def menu(self):
        self.screen.fill('white')
        self.display_menu_text()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.scene = 2

    def battle(self):
        if len(self.enemies) < 1 and not self.spawning_enemy:
            Thread(target=self.spawn_enemy, args=[1]).start()
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.handle_key_input(event)

        # fill the screen with a color to wipe away anything from last frame
        #self.screen.fill("black")
        self.render_background()
        self.display_score()
        self.display_magazine_text()

        # HANDLE PLAYER LOGIC
        self.e_player.update()
        self.e_player.render(self.screen)
        if self.e_player.health <= 0:
            sleep(3)
            self.reset_battle()
            if len(self.bullets) > 0:
                for bullet in self.bullets:
                    self.bullets.remove(bullet)
            if len(self.enemies) > 0:
                for enemy in self.enemies:
                    self.enemies.remove(enemy)
            self.scene = 1

        #HANDLE ENEMY LOGIC
        for enemy in self.enemies:
            enemy.update()
            enemy.render(self.screen)
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                if len(self.enemies) <= 0:
                    self.wave += 1
                
                self.score += 1
                
                self.score_text = f"SCORE: {self.score}"
                if not self.spawning_enemy and len(self.enemies) == 0:
                    if self.wave < 50:
                        Thread(target=self.spawn_enemy, args=[(self.wave // 10) + 1]).start()
                    else:
                        Thread(target=self.spawn_enemy, args=[5]).start()
            if enemy.collided(self.e_player):
                if not self.e_player.invincible:
                    if not self.e_player.taking_damage:
                        Thread(target=self.e_player.take_damage).start()
                enemy.attacking = False
                enemy.retreating = True
                self.e_player.invincible = True
            if enemy.attacking:
                self.e_player.invincible = False
                enemy.idle = False
                enemy.retreating = False
                enemy.enemy_attack()
            elif enemy.retreating:
                self.e_player.invincible = True
                enemy.idle = False
                enemy.attacking = False
                enemy.enemy_retreat()
                enemy.idle = True
            elif enemy.idle:
                self.e_player.invincible = False
                enemy.attacking = False
                enemy.retreating = False
                if not enemy.idling:
                    enemy.idling = True
                    Thread(target=enemy.enemy_idle).start()

        #HANDLE BULLET RENDERING AND COLLISION DETECTION
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update()
                bullet.render(self.screen)
                for enemy in self.enemies:
                    if bullet.collided(enemy):
                        # enemy.idle = False
                        if not enemy.retreating:
                            enemy.take_damage()
                            # print("HIT!")
                            if enemy.health < 3 :
                                enemy.attacking = True
                                enemy.idle = False
                        if len(self.bullets) > 0 and bullet in self.bullets:
                            self.bullets.remove(bullet)
                        
                if bullet.out_of_bounds() and len(self.bullets) > 0 and bullet in self.bullets:
                    self.bullets.remove(bullet)                    
    
    def run(self):
        while self.running:
            if self.scene == 1:
                self.menu()
                pygame.display.update()
                self.clock.tick(24)  # limits FPS to 60
            elif self.scene == 2:
                self.battle()
                pygame.display.update()
                self.clock.tick(24)  # limits FPS to 60
    pygame.quit()

Game().run()