# Example file showing a basic pygame "game loop"
import pygame
from gameutils.imgutils import load_image, load_image_no_convert, load_sound
from gameutils.entities import PhysicsEntity

class Game:
    # pygame setup
    def __init__(self):
        self.devmode = True
        pygame.init()
        self.resolution = (1280, 720)
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("PyGame-Game-Jam")
        self.clock = pygame.time.Clock()
        self.gravity = False

        self.assets = {
            'player-img': load_image_no_convert('Dummies/dummy_player-removebg-preview.png'),
            'bullet-img': load_image_no_convert('Dummies/dummy-bullet.gif'),
            'background-img': load_image('Dummies/dummy-background-space-3.jpeg'),
            'bullet-sound': load_sound('Dummies/laser-shot-ingame-230500.mp3')
        }
        self.e_player = PhysicsEntity(self, 'player', (0, 20), (100, 75), self.assets['player-img'])
        self.bullets = []

    def render_background(self):
        background = pygame.transform.scale(self.assets['background-img'], self.screen.get_size())
        self.screen.blit(background, (0, 0))

    def shoot_bullet(self):
        if len(self.bullets) < 3:
            bullet = PhysicsEntity(self, 'bullet', (self.e_player.pos[0] + self.e_player.width, self.e_player.pos[1]), (50, 50), self.assets['bullet-img'])
            bullet.img.set_colorkey('black')
            self.bullets.append(bullet)
            self.assets['bullet-sound'].play()
            
    
    def handle_key_input(self, e: pygame.event):
        if(e.type == pygame.KEYDOWN):
            if(self.devmode):
                pass
            if e.key == pygame.K_b:
                self.shoot_bullet()
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
        #self.e_player.set_x_velocity(50)
        #self.e_player.set_y_velocity(100)
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

