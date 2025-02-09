import pygame
import random
from time import sleep

PLAYER_SPEED = 20
ENEMY_SPEED = 10
ENEMY_MAX_SPEED = 30
HOMING_STRENGTH = 5
MAX_HOMING_STRENGTH = 17
BULLET_SPEED = 15
MAX_BULLET_SPEED = 30
SAFE_ZONE = 10
MAX_SAFE_ZONE = 25

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, img: pygame.Surface):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.img = pygame.transform.scale(img, size)
        if self.e_type == 'bullet':
            self.velocity = [min(MAX_BULLET_SPEED, BULLET_SPEED + (self.game.wave/2)), 0]
        else:
            self.velocity = [0, 0]
        
        self.width = size[0]
        self.height = size[1]
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)

        if self.e_type == 'player':
            self.health = 5
            self.invincible = False
            self.taking_damage = False
        elif self.e_type == 'enemy':
            self.health = 5

        if self.e_type == 'enemy':
            self.idling = False
            self.idle = True
            self.attacking = False
            self.retreating = False

    def __del__(self):
        print(f"Object {self.e_type} destroyed")

    def out_of_bounds(self) -> bool:
        if(self.pos[0] > 0 and self.pos[0] < (self.game.screen.get_size()[0] - self.width) and self.pos[1] > 0 and self.pos[1] < self.game.screen.get_size()[1] - self.height):
            return False
        print(f"{self.e_type} Out of Bounds!")
        return True
    
    def collided(self, e):
        if self.rect.colliderect(e.rect):
            return True
        return False

    def reset_velocity(self):
        self.velocity = [0, 0]
        
    #Move Entity right by a certain speed
    def move_right(self):
        if(self.e_type == 'player'):
            self.velocity[0] = PLAYER_SPEED
        elif(self.e_type == 'enemy'):
            self.velocity[0] = min(ENEMY_MAX_SPEED, ENEMY_SPEED + ((self.game.wave - 1)/2))
    
    #Move Entity left by a certain speed
    def move_left(self):
        if(self.pos[0] > 0):
            if(self.e_type == 'player'):
                self.velocity[0] = -(PLAYER_SPEED)
            elif(self.e_type == 'enemy'):
                self.velocity[0] = -(min(ENEMY_MAX_SPEED, ENEMY_SPEED + ((self.game.wave - 1)/2)))
    
    #Move Entity up by a certain speed
    def move_up(self):
        if(self.pos[1] > 0):
            if(self.e_type == 'player'):
                self.velocity[1] = -(PLAYER_SPEED)
            elif(self.e_type == 'enemy'):
                self.velocity[1] = -(min(ENEMY_MAX_SPEED, ENEMY_SPEED + ((self.game.wave - 1)/2)))

    #Move Entity down by a certain speed
    def move_down(self):
        if(self.e_type == 'player'):
            self.velocity[1] = PLAYER_SPEED
        elif(self.e_type == 'enemy'):
            self.velocity[1] = min(ENEMY_MAX_SPEED, ENEMY_SPEED + ((self.game.wave - 1)/2))

    def set_x_velocity(self, n):
        self.velocity[0] = n 
    
    def set_y_velocity(self, n):
        self.velocity[1] = n

    def take_damage(self):
        if self.e_type == 'player':
            self.taking_damage = True
            sleep(0.3)
            self.taking_damage = False
            if self.game.wave < 50:
                self.health -= 1
            else:
                self.health -= 2
        elif self.e_type == 'enemy':
            self.health -= 1

    def update(self):
        if self.e_type == 'player':
            if self.movingUp:
                if(self.pos[1] > 0):
                    self.move_up()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[1] += frame_movement[1]
                    self.rect.y += frame_movement[1]
            if self.movingLeft:
                if(self.pos[0] > 0):
                    self.move_left()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[0] += frame_movement[0]
                    self.rect.x += frame_movement[0]
            if self.movingRight:
                if(self.pos[0] < ((self.game.screen.get_size()[0]/2) - self.width)):
                    self.move_right()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[0] += frame_movement[0]
                    self.rect.x += frame_movement[0]
            if self.movingDown:
                if(self.pos[1] < self.game.screen.get_size()[1] - (self.height + 100)):
                    self.move_down()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[1] += frame_movement[1]
                    self.rect.y += frame_movement[1]

        elif self.e_type == 'enemy':
            if self.movingUp:
                if(self.pos[1] > 0):
                    self.move_up()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[1] += frame_movement[1]
                    self.rect.y += frame_movement[1]
            if self.movingLeft:
                if(self.pos[0] > 0):
                    self.move_left()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[0] += frame_movement[0]
                    self.rect.x += frame_movement[0]
            if self.movingRight:
                if(self.pos[0] < ((self.game.screen.get_size()[0]) - self.width)):
                    self.move_right()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[0] += frame_movement[0]
                    self.rect.x += frame_movement[0]
            if self.movingDown:
                if(self.pos[1] < self.game.screen.get_size()[1] - (self.height + 100)):
                    self.move_down()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[1] += frame_movement[1]
                    self.rect.y += frame_movement[1]
            
        elif self.e_type == 'bullet':
            if(self.pos[0] < 200000):
                self.pos[0] += self.velocity[0]
                self.rect.x += self.velocity[0]



    def render(self, surface: pygame.Surface):
        surface.blit(self.img, self.pos)

class EnemyEntity(PhysicsEntity):

    # ENEMY ACTIONS, SUCH AS IDLING, ATTACKING AND RETREATING

    def enemy_idle(self):
        if self.e_type == 'enemy':
            if not self.idle:
                return
            sleep(0.5)
            self.idling = True
            self.retreating = False
            if self.idle:
                rand_num = random.randint(1, 10)
                if rand_num == (1 or 2 or 3):
                    self.game.prev_rand = rand_num
                    if self.pos[1] <= 15:
                        self.movingUp = False
                        self.movingDown = True
                    else:
                        if self.movingDown:
                            self.movingDown = False
                        self.movingUp = True
                elif rand_num == (3 or 4 or 5):
                    self.game.prev_rand = rand_num
                    if self.pos[1] > self.game.screen.get_size()[1] - (100 + 100 + 5):
                        pass
                    if self.movingUp:
                        self.movingUp = False
                    self.movingDown = True
                elif rand_num == (6 or 7 or 8 or 9):
                    self.idle = False
                    self.attacking = True
                    self.enemy_attack()
                
                else:
                    if self.game.prev_rand == rand_num:
                        pass
                    else:
                        self.game.prev_rand = rand_num
                        self.movingUp = False
                        self.movingDown = False
                        sleep(0.2)
            self.idling = False

    def enemy_attack(self):
        if self.e_type == 'enemy':
            self.idle = False
            self.retreating = False
            if self.pos[0] > self.game.e_player.pos[0]:
                self.movingRight = False
                self.movingLeft = True
            elif self.pos[0] < self.game.e_player.pos[0]:
                self.movingLeft = False
                self.movingRight = True

            if(self.pos[0] < (min(SAFE_ZONE + self.game.wave, MAX_SAFE_ZONE) * self.game.screen.get_size()[0]/100)):
                self.movingUp = False
                self.movingDown = False
                self.movingRight = False
                self.movingLeft = True
                if (self.pos[0] < 25) and (self.pos[1] is not self.game.e_player.pos[1]):
                    self.attacking = False
                    self.retreating = True
                if (self.collided(self.game.e_player)):
                    self.attacking = False
                    self.retreating = True

            else:
                if abs(self.game.e_player.pos[1] - self.pos[1]) < min(MAX_HOMING_STRENGTH, HOMING_STRENGTH + self.game.wave):
                    self.movingUp = False
                    self.movingDown = False
                    self.pos[1] = self.game.e_player.pos[1]
                if self.pos[1] > self.game.e_player.pos[1]:
                    self.movingDown = False
                    self.movingUp = True
                elif self.pos[1] < self.game.e_player.pos[1]:
                    self.movingUp = False
                    self.movingDown = True

    def enemy_retreat(self):
        if self.e_type == 'enemy':
            self.idle = False
            self.movingUp = False
            self.movingDown = False
            self.movingLeft = False
            self.movingRight = False

            if self.pos[0] < (self.game.screen.get_size()[0] - self.width):
                self.movingRight = True

            if self.pos[0] >= (self.game.screen.get_size()[0] - self.width):
                self.movingRight = False
                self.retreating = False