import pygame
import random
from time import time
from time import sleep

# SOME USEFUL CONSTANTS
# Player and enemy Speed
PLAYER_SPEED = 20
ENEMY_SPEED = 10
ENEMY_MAX_SPEED = 30

# Homing strength
HOMING_STRENGTH = 5
MAX_HOMING_STRENGTH = 17

# Bullet speed
BULLET_SPEED = 15
MAX_BULLET_SPEED = 30

# Safe zone area
SAFE_ZONE = 10
MAX_SAFE_ZONE = 25

# Enemy Action States
ENEMY_IDLE = 0
ENEMY_ATTACKING = 1
ENEMY_RETREATING = 2
ENEMY_DODGE = 3
ENEMY_CHASE = 4

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
            print("player took damage")
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
            if self.movingLeft:
                if(self.pos[0] > 0):
                    self.move_left()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[0] += frame_movement[0]
            if self.movingRight:
                if(self.pos[0] < ((self.game.screen.get_size()[0]/2) - self.width)):
                    self.move_right()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[0] += frame_movement[0]
            if self.movingDown:
                if(self.pos[1] < self.game.screen.get_size()[1] - (self.height + 100)):
                    self.move_down()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[1] += frame_movement[1]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

        elif self.e_type == 'enemy':
            if self.movingUp:
                if(self.pos[1] > 0):
                    self.move_up()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[1] += frame_movement[1]
                else:
                    self.pos[1] = 0
            if self.movingLeft:
                if(self.pos[0] > 0):
                    self.move_left()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[0] += frame_movement[0]
            if self.movingRight:
                if(self.pos[0] < ((self.game.screen.get_size()[0]) - self.width)):
                    self.move_right()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[0] += frame_movement[0]
            if self.movingDown:
                if(self.pos[1] < self.game.screen.get_size()[1] - (self.height + 100)):
                    self.move_down()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[1] += frame_movement[1]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]
            
        elif self.e_type == 'bullet':
            if(self.pos[0] < 200000):
                self.pos[0] += self.velocity[0]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]



    def render(self, surface: pygame.Surface):
        surface.blit(self.img, self.pos)

class EnemyEntity(PhysicsEntity):

    # ENEMY ACTIONS, SUCH AS IDLING, ATTACKING AND RETREATING
    def __init__(self, game, e_type, pos, size, img: pygame.Surface):
        super().__init__(game, e_type, pos, size, img)
        self.action_state = ENEMY_IDLE
        self.action_state_locked = False
        self.timer = False
        self.dodge_start_time = 0

    def set_action_state(self, state: int):
        self.action_state = state

    def lock_action_state(self):
        self.action_state_locked = True

    def unlock_action_state(self):
        self.action_state_locked = False


    def dodge(self):
        self.lock_action_state()

        self.movingLeft = False
        self.movingRight = False

        if self.rect.x is not (self.game.screen.get_size()[0] - self.width):
            self.pos[0] = self.game.screen.get_size()[0] - self.width

        if self.action_state == ENEMY_DODGE:
            time_to_wait = float(3)
            if not self.timer:
                self.dodge_start_time = time()
                self.timer = True
            self.movingUp = False
            self.movingLeft = False
            self.movingRight = False
            self.movingLeft = False

            print(str(time() - self.dodge_start_time) + ", " + str(time_to_wait))

            if (time() - self.dodge_start_time) >= time_to_wait:
                self.timer = False
                self.unlock_action_state()
                self.set_action_state(ENEMY_IDLE)
            else:
                if len(self.game.bullets) > 0:
                    for e in self.game.bullets:
                        if ((self.rect.y + self.height/2) < (e.rect.y + e.height/2) and (e.rect.y + e.height/2) < (self.rect.y + self.height + 60)) or (self.rect.y + self.height + 30) >= self.game.screen.get_size()[1] - 100:
                            print("Bullet close to enemy")
                            self.movingDown = False
                            self.movingUp = True
                            sleep(0.5)
                            self.movingUp = False
                            sleep(0.15)
                            self.timer = False
                            self.unlock_action_state()
                            self.set_action_state(ENEMY_IDLE)
                        if ((self.rect.y - 60) < e.rect.y and e.rect.y < (self.rect.y + self.height/2)) or (self.rect.y < ((self.height/2) + 15)):
                            print("Bullet close to enemy")
                            self.movingUp = False
                            self.movingDown = True
                            sleep(0.5)
                            self.movingDown = False
                            sleep(0.15)
                            self.timer = False
                            self.unlock_action_state()
                            self.set_action_state(ENEMY_IDLE)
                else:
                    pass
                print("neither")
        self.unlock_action_state()

    def chase(self, e: PhysicsEntity):
        self.lock_action_state()
        if self.action_state == ENEMY_CHASE:
            if self.pos[0] > e.pos[0]:
                    self.movingRight = False
                    self.movingLeft = True
            elif self.pos[0] < e.pos[0]:
                self.movingLeft = False
                self.movingRight = True
            
            if self.pos[1] > e.pos[1]:
                self.movingDown = False
                self.movingUp = True
            elif self.pos[1] < e.pos[1]:
                self.movingUp = False
                self.movingDown = True

            if self.collided(e):
                self.action_state = ENEMY_RETREATING

    def enemy_idle(self):
        self.movingLeft = False
        self.movingRight = False
        if self.e_type == 'enemy':
            if self.action_state != ENEMY_IDLE:
                return
            
            self.lock_action_state()
            
            sleep(0.5)
            
            if self.action_state == ENEMY_IDLE:

                if self.rect.x is not (self.game.screen.get_size()[0] - self.width):
                    self.pos[0] = self.game.screen.get_size()[0] - self.width

                rand_num = random.randint(1, 20)
                if rand_num in range(1, 5):
                    print("MOVING DOWN")
                    self.game.prev_rand = rand_num
                    if self.rect.y <= 15:
                        self.movingUp = False
                        self.movingDown = True
                        self.lock_action_state()
                        sleep(0.2)
                        self.unlock_action_state()
                    else:
                        if self.movingDown:
                            self.movingDown = False
                        self.movingUp = True
                        self.lock_action_state()
                        sleep(0.2)
                        self.unlock_action_state()
                    
                elif rand_num in range (6, 10):
                    print("MOVING UP")
                    self.game.prev_rand = rand_num
                    if self.rect.y > self.game.screen.get_size()[1] - (100 + 100 + 5):
                        pass
                    if self.movingUp:
                        self.movingUp = False
                    self.movingDown = True
                    self.lock_action_state()
                    sleep(0.2)
                    self.unlock_action_state()
                elif rand_num in range(11, 16):
                    if self.action_state is ENEMY_IDLE:
                        print("IDLE TO DODGE")
                        self.game.prev_rand = rand_num
                        self.unlock_action_state()
                        self.set_action_state(ENEMY_DODGE)
                    return
                elif rand_num in range(17, 19):
                    print("IDLE TO ATTACKING")
                    self.unlock_action_state()
                    self.set_action_state(ENEMY_ATTACKING)
                    sleep(0.1)
                    return
                
                else:
                    if self.game.prev_rand == rand_num:
                        self.unlock_action_state()
                    else:
                        self.game.prev_rand = rand_num
                        self.movingUp = False
                        self.movingDown = False
                        self.unlock_action_state()
                        sleep(0.2)
        self.unlock_action_state()
        #print(self.action_state_locked)

    def enemy_attack(self):
        if self.e_type == 'enemy':
            self.lock_action_state()
            if self.rect.x > self.game.e_player.rect.x:
                print("bruh")
                self.movingRight = False
                self.movingLeft = True
            elif self.rect.x < self.game.e_player.rect.x:
                print("rlly")
                self.movingLeft = False
                self.movingRight = True
            else:
                print("HUUHHHH???")

            if(self.rect.x < (min(SAFE_ZONE + self.game.wave, MAX_SAFE_ZONE) * self.game.screen.get_size()[0]/100)):
                print("SAFE ZONE")
                self.movingUp = False
                self.movingDown = False
                self.movingRight = False
                self.movingLeft = True
                if (self.rect.x < 10): # and (self.rect.y != self.game.e_player.rect.y):
                    print("lock in")
                    self.unlock_action_state()
                    self.set_action_state(ENEMY_RETREATING)
                    return
                if (self.collided(self.game.e_player)):
                    print("player hit")
                    self.game.e_player.take_damage()
                    self.unlock_action_state()
                    self.set_action_state(ENEMY_RETREATING)
                    return

            else:
                self.lock_action_state()
                print("not in safe zone")

                if (self.rect.x < 10): # and (self.rect.y != self.game.e_player.rect.y):
                    print("lock in")
                    self.unlock_action_state()
                    self.set_action_state(ENEMY_RETREATING)
                    return
                if (self.collided(self.game.e_player)):
                    print("player hit")
                    self.game.e_player.take_damage()
                    self.unlock_action_state()
                    self.set_action_state(ENEMY_RETREATING)
                    return

                if abs(self.game.e_player.rect.y - self.rect.y) < min(MAX_HOMING_STRENGTH, HOMING_STRENGTH + self.game.wave):
                    self.movingUp = False
                    self.movingDown = False
                    self.rect.y = self.game.e_player.rect.y
                if self.rect.y > self.game.e_player.rect.y:
                    print("come on")
                    self.movingDown = False
                    self.movingUp = True
                elif self.rect.y < self.game.e_player.rect.y:
                    print("just work")
                    self.movingUp = False
                    self.movingDown = True
        self.unlock_action_state()
        self.set_action_state(ENEMY_ATTACKING)

    def enemy_retreat(self):
        self.lock_action_state()
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False

        if self.rect.x < (self.game.screen.get_size()[0] - self.width):
            self.movingUp = False
            self.movingDown = False
            self.movingLeft = False
            self.movingRight = True

        if self.rect.x >= (self.game.screen.get_size()[0] - self.width):
            self.movingUp = False
            self.movingDown = False
            self.movingLeft = False
            #self.movingRight = False
            if random.randint(1, 2) == 1:
                print("2 TO 0")
                self.unlock_action_state()
                self.set_action_state(ENEMY_IDLE)
                return
            else:
                print("2 TO 3")
                self.unlock_action_state()
                self.set_action_state(ENEMY_DODGE)
                return
        self.unlock_action_state()