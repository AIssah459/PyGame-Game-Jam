# Example file showing a basic pygame "game loop"
import pygame
from pygame.mixer import music
from pygame.event import Event
from time import sleep
import random
from threading import Thread
from gameutils.imgutils import load_image, load_image_no_convert, load_sound, load_music
from gameutils.entities import PhysicsEntity, EnemyEntity
from gameutils.entities import ENEMY_IDLE, ENEMY_ATTACKING, ENEMY_RETREATING, ENEMY_DODGE, ENEMY_CHASE

DEFAULT_SCREEN_RESOLUTION = (1280, 720)

HARDCORE_LEVEL = 20
HARDCORE_MODE = pygame.USEREVENT + 1
RELOAD_TIME = 2
PLAYER_HEIGHT = 75
PLAYER_WIDTH = 100
STARTING_POS = (0, (DEFAULT_SCREEN_RESOLUTION[1]/2 - PLAYER_HEIGHT/2))
NUM_ENEMIES = 1
SPAWN_POWERUP_CHANCE = 30
DUMMY_PLAYER_PATH = 'Dummies/dummy_player-remove-bg.png'

class Game:
    # pygame setup
    def __init__(self):
        self.running = True
        self.music_playing = False

        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.scene = 1
        
        self.hardcore_mode = False
        self.screen = pygame.display.set_mode(DEFAULT_SCREEN_RESOLUTION)
        pygame.display.set_caption("Sample Title")
        self.clock = pygame.time.Clock()
        self.reloading = False
        self.spawning_enemy = False
        self.spawning_powerup = False
        self.menu_blinking = False

        #ASSETS

        self.songs = ['menu-music-beginning.mp3', 'menu-music-looped.mp3', 'battle-music.mp3', 'battle-music-hardcore.mp3']

        pygame.mixer.music.set_volume(0.3)

        self.assets = {
            'player-img': load_image_no_convert('shipv1.png'),
            'enemy-img': load_image_no_convert('enemy1.png'),
            'bullet-img': load_image_no_convert('Dummies/dummy-bullet.gif'),
            'power-up': load_image('minigun.png'),
            'background-img': load_image('gamebackground.png'),
            'bullet-sound': load_sound('Dummies/laser-shot-ingame-230500.mp3'),
            'enemy-take-dmg-sound': load_sound('Dummies/01._damage_grunt_male.wav'),
            'enemy-death-sound': load_sound('Dummies/explosion.wav'),
            'player-dmg-sound': load_sound('Dummies/whip.wav'),
            'reload-sound': load_sound('Dummies/gun_reload_lock_or_click_sound.mp3'),
        }

        # ASSET MANAGEMENT

        self.assets['power-up'].set_colorkey('black')

        self.assets['bullet-sound'].set_volume(0.2)
        self.assets['enemy-death-sound'].set_volume(0.2)

        self.e_player = PhysicsEntity(self, 'player', STARTING_POS, (PLAYER_WIDTH, PLAYER_HEIGHT), pygame.transform.rotate(self.assets['player-img'], 270))
        self.wave = 1
        self.score = 0
        self.bullets = []
        self.magazine = 5
        self.enemies = []
        self.magazine_text_offset = 0
        self.powerups = []

        self.score_text = f"SCORE: {self.score}"
        self.magazine_text = f"BULLETS: {self.magazine}"
        self.wave_text = f"WAVE: {self.wave}"
        self.menu_text = f"PRESS ANY KEY TO PLAY"
        self.prev_rand = 0

        self.score_text_surface = pygame.Surface((0, 0))
        self.magazine_text_surface = pygame.Surface((0, 0))
        self.wave_text_surface = pygame.Surface((0, 0))

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def reset_battle(self):

        #RECORD SCRATCH!!!
        self.stop_music()

        self.e_player.pos = list(STARTING_POS)

        self.wave = 1
        self.hardcore_mode = False
        self.score = 0
        self.e_player.health = 5
        self.magazine = 5
        self.prev_rand = 0
        
        load_music(self.songs[2])

        self.score_text = f"SCORE: {self.score}"
        self.magazine_text = f"BULLETS: {self.magazine}"
        self.wave_text_surface = f"WAVE: {self.wave}"

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
        self.screen.blit(self.magazine_text_surface, (0, self.screen.get_size()[1] - self.magazine_text_surface.get_size()[1]))

    def display_wave_text(self):
        my_font = pygame.font.SysFont('SF Pro', 100)
        self.wave_text_surface = my_font.render(self.wave_text, False, 'red')
        self.screen.blit(self.wave_text_surface, (self.screen.get_size()[0]/2 - (self.wave_text_surface.get_size()[0]/2), 0))

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
        self.assets['reload-sound'].play()
        if not self.e_player.powered_up:
            sleep(RELOAD_TIME)
        self.magazine = 5
        self.magazine_text = f"BULLETS: {self.magazine}"
        self.reloading = False

    def spawn_enemy(self, num_enemtes):
        self.spawning_enemy = True
        sleep(1)
        for i in range(num_enemtes):
            if len(self.enemies) < (self.wave // 3) + 1:
                self.enemies.append(EnemyEntity(self, 'enemy', (self.screen.get_size()[0] - 100, random.randint(0, self.screen.get_size()[1] - (100 + 100))), (100, 100), self.assets['enemy-img']))
        self.spawning_enemy = False

    def spawn_powerup(self):
        self.spawning_powerup = True
        sleep(1)
        self.powerups.append(PhysicsEntity(self, 'powerup', (min(self.screen.get_size()[0]/2 - 15, random.randint(30, self.screen.get_size()[0]/2 - 15)), random.randint(100, self.screen.get_size()[1] - 100)), (55, 55), self.assets['power-up']))
        sleep(10)
        if len(self.powerups) > 0:
            self.powerups.pop()
        self.spawning_powerup = False
    
    def handle_key_input(self, e: pygame.event):
        if(e.type == pygame.KEYDOWN):
            if e.key == pygame.K_q:
                pygame.mixer.music.stop()
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

    def menu_music(self):
        load_music(self.songs[1])
        pygame.mixer.music.play(-1)
        self.music_playing = True

    def hardcore_music(self):
        print("HARDCORE MUSIIIIIIC")
        self.hardcore_mode = True
        load_music(self.songs[3])
        pygame.mixer.music.play(-1)
        self.music_playing = True

    def menu_blink(self):
        self.menu_blinking = True
        self.menu_text = f"PRESS ANY KEY TO PLAY"
        sleep(1)
        self.menu_text = ""
        sleep(1)
        self.menu_blinking = False

    def menu(self):
        self.screen.fill('black')
        self.display_menu_text()
        if not self.menu_blinking:
            Thread(target=self.menu_blink).start()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.stop_music()
                self.scene = 2
                

    def battle(self):

        if self.wave == HARDCORE_LEVEL:
            pygame.event.post(Event(HARDCORE_MODE))

        if len(self.enemies) < 1 and not self.spawning_enemy:
            Thread(target=self.spawn_enemy, args=[1]).start()

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.handle_key_input(event)
            if event.type == HARDCORE_MODE:
                        print("AHHHHHHHHHHHHH")
                        if not self.hardcore_mode:
                            self.stop_music()
                            self.hardcore_mode = True
                        if not self.music_playing:
                            Thread(target=self.hardcore_music).start()
                            print("music not playing")

        # fill the screen with a color to wipe away anything from last frame
        #self.screen.fill("black")
        self.render_background()
        self.display_score()
        self.display_magazine_text()
        self.display_wave_text()

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
                self.assets['enemy-death-sound'].play()
                if len(self.enemies) <= 0:
                    self.wave += 1
                    self.wave_text = f"WAVE: {self.wave}"
                
                self.score += 1
                
                self.score_text = f"SCORE: {self.score}"
                if not self.spawning_enemy and len(self.enemies) == 0:
                    if self.wave < HARDCORE_LEVEL:
                        Thread(target=self.spawn_enemy, args=[(self.wave // 3) + 1]).start()
                    else:
                        Thread(target=self.spawn_enemy, args=[7]).start()
                self.e_player.invincible = True

            #print(enemy.action_state)
            match enemy.action_state:
                case 1:
                    print("[" + str(enemy.rect.x) + ", " + str(enemy.rect.y) + "]")
                    # print(enemy.action_state)
                    if not enemy.action_state_locked:
                        self.e_player.invincible = False
                        #Thread(target=enemy.enemy_attack).start()
                        enemy.enemy_attack()

                case 2:
                    # print(enemy.action_state)
                    if not enemy.action_state_locked:
                        self.e_player.invincible = True
                        Thread(target=enemy.enemy_retreat).start()

                    else:
                        print("LOCKED")

                case 3:
                    # print(enemy.action_state)
                    if not enemy.action_state_locked:
                        Thread(target=enemy.dodge).start()

                case 0:
                    if enemy.action_state_locked == False:
                        self.e_player.invincible = False
                        Thread(target=enemy.enemy_idle).start()

                case _:
                    pass

        #HANDLE BULLET RENDERING AND COLLISION DETECTION
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update()
                bullet.render(self.screen)
                if bullet.out_of_bounds() and len(self.bullets) > 0 and bullet in self.bullets:
                    self.bullets.remove(bullet) 
                for enemy in self.enemies:
                    if bullet.collided(enemy):
                        if enemy.action_state is not ENEMY_RETREATING:
                            #print("HE WASNT RETREATING " + str(enemy.action_state))
                            enemy.take_damage()
                            # print("HIT!")
                        if len(self.bullets) > 0 and bullet in self.bullets:
                            self.bullets.remove(bullet)

        #HANDLE POWER UP LOGIC
        if len(self.powerups) > 0:
            for powerup in self.powerups:
                powerup.update()
                powerup.render(self.screen)
                if powerup.collided(self.e_player):
                    if not self.e_player.powered_up:
                        Thread(target=self.e_player.power_up).start()
                    if powerup in self.powerups:
                        self.powerups.remove(powerup)
                for enemy in self.enemies:
                    if powerup.collided(enemy) and enemy.action_state is not ENEMY_RETREATING:
                        if len(self.powerups) > 0 and powerup in self.powerups:
                            self.powerups.remove(powerup)

        #POWERUP SPAWNING
        spawn_powerup = random.randint(1, 100)
        if spawn_powerup < SPAWN_POWERUP_CHANCE and len(self.powerups) < 1 and not self.spawning_powerup:
            Thread(target=self.spawn_powerup).start()

    def run(self):
        while self.running:
            if self.scene == 1:
                if not self.music_playing:
                    Thread(target=self.menu_music).start()
                self.menu()
                pygame.display.update()
                self.clock.tick(24)  # limits FPS to 24
            elif self.scene == 2:
                #self.test_battle()
                if not self.music_playing:
                    load_music(self.songs[2])
                    pygame.mixer.music.play(-1)
                    self.music_playing = True
                self.battle()
                pygame.display.update()
                self.clock.tick(24)  # limits FPS to 24
    pygame.quit()

Game().run()