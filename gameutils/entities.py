import pygame

PLAYER_SPEED = 20
ENEMY_SPEED = 10

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, img: pygame.Surface):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.img = pygame.transform.scale(img, size)
        if self.e_type == 'bullet':
            self.velocity = [20, 0]
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
            self.velocity[0] = ENEMY_SPEED
    
    #Move Entity left by a certain speed
    def move_left(self):
        if(self.pos[0] > 0):
            if(self.e_type == 'player'):
                self.velocity[0] = -(PLAYER_SPEED)
            elif(self.e_type == 'enemy'):
                self.velocity[0] = -(ENEMY_SPEED)
    
    #Move Entity up by a certain speed
    def move_up(self):
        if(self.pos[1] > 0):
            if(self.e_type == 'player'):
                self.velocity[1] = -(PLAYER_SPEED)
            elif(self.e_type == 'enemy'):
                self.velocity[1] = -(ENEMY_SPEED)

    #Move Entity down by a certain speed
    def move_down(self):
        if(self.e_type == 'player'):
            self.velocity[1] = PLAYER_SPEED
        elif(self.e_type == 'enemy'):
            self.velocity[1] = ENEMY_SPEED

    def set_x_velocity(self, n):
        self.velocity[0] = n 
    
    def set_y_velocity(self, n):
        self.velocity[1] = n

    def take_damage(self):
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