# Example file showing a basic pygame "game loop"
import pygame
from time import sleep
from threading import Thread
from gameutils.imgutils import load_image, load_image_no_convert, load_sound
from gameutils.entities import PhysicsEntity

DEFAULT_SCREEN_RESOLUTION = (1280, 720)

class Game:
    # pygame setup
    def __init__(self):
        self.devmode = True
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(DEFAULT_SCREEN_RESOLUTION)
        pygame.display.set_caption("PyGame-Game-Jam")
        self.clock = pygame.time.Clock()
        self.gravity = False
        self.reloading = False

        self.assets = {
            'player-img': load_image_no_convert('Dummies/dummy_player-removebg-preview.png'),
            'bullet-img': load_image_no_convert('Dummies/dummy-bullet.gif'),
            'background-img': load_image('Dummies/dummy-background-space-3.jpeg'),
            'bullet-sound': load_sound('Dummies/laser-shot-ingame-230500.mp3')
        }
        self.e_player = PhysicsEntity(self, 'player', (0, 20), (100, 75), self.assets['player-img'])
        self.bullets = []
        self.magazine = 5

        self.magazine_text = f"BULLETS: {self.magazine}"

    def display_magazine_text(self):
        my_font = pygame.font.SysFont('Comic Sans MS', 100)
        text_surface = my_font.render(self.magazine_text, False, 'red')
        self.screen.blit(text_surface, (0, self.screen.get_size()[1] - text_surface.get_size()[1]))

    def render_background(self):
        background = pygame.transform.scale(self.assets['background-img'], self.screen.get_size())
        self.screen.blit(background, (0, 0))

    def shoot_bullet(self):
        if len(self.bullets) < 5 and self.magazine > 0:
            bullet = PhysicsEntity(self, 'bullet', (self.e_player.pos[0] + self.e_player.width, self.e_player.pos[1]), (50, 50), self.assets['bullet-img'])
            bullet.img.set_colorkey('black')
            self.bullets.append(bullet)
            self.assets['bullet-sound'].play()

    def reload(self):
        if len(self.bullets) == 0:  
            self.magazine_text = "RELOADING"
            self.reloading = True 
            sleep(1)
            self.magazine = 5
            self.magazine_text = f"BULLETS: {self.magazine}"
            self.reloading = False
            
    
    def handle_key_input(self, e: pygame.event):
        if(e.type == pygame.KEYDOWN):
            if(self.devmode):
                pass
            if e.key == pygame.K_b:
                if(self.magazine == 0 and self.reloading == False):
                    Thread(target=self.reload).start()
                else:
                    if(len(self.bullets) < 5 and self.magazine > 0 and self.reloading == False):
                        self.shoot_bullet()
                        self.magazine -= 1
                        self.magazine_text = f"BULLETS: {self.magazine}"
            if e.key == pygame.K_UP:
                self.e_player.movingUp = True
            if e.key == pygame.K_LEFT:
                self.e_player.movingLeft = True
            if e.key == pygame.K_RIGHT:
                self.e_player.movingRight = True
            if e.key == pygame.K_DOWN:
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

    def run(self):
        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.handle_key_input(event)

            # fill the screen with a color to wipe away anything from last frame
            #self.screen.fill("black")
            self.render_background()
            self.display_magazine_text()


            # RENDER YOUR GAME HERE
            self.e_player.update()
            self.e_player.render(self.screen)

            if len(self.bullets) > 0:
                for bullet in self.bullets:
                    bullet.update()
                    bullet.render(self.screen)
                    if(bullet.out_of_bounds()):
                        self.bullets.remove(bullet)
                    

            # flip() the display to put your work on screen
            # pygame.display.flip()
            pygame.display.update()

            self.clock.tick(60)  # limits FPS to 60

    pygame.quit()

Game().run()

