import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, img: pygame.Surface):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.img = pygame.transform.scale(img, size)
        self.velocity = [0, 0]
        self.width = size[0]
        self.height = size[1]
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False
        
    def move_right(self):
        if(self.pos[0] < self.game.screen.get_size()[0] - self.width):
            self.pos[0] += self.velocity[0]
    
    def move_left(self):
        if(self.pos[0] > 0):
            self.pos[0] -= self.velocity[0]
    
    def move_up(self):
        if(self.pos[1] > 0):
            self.pos[1] -= self.velocity[1]
    
    def move_down(self):
        if(self.pos[1] < self.game.screen.get_size()[1] - self.height):
            self.pos[1] += self.velocity[1]

    def set_x_velocity(self, n):
        self.velocity[0] = n 
    
    def set_y_velocity(self, n):
        self.velocity[1] = n 

    def update(self):
        
        if self.movingUp:
            self.move_up()
        if self.movingLeft:
            self.move_left()
        if self.movingRight:
            self.move_right()
        if self.movingDown:
            self.move_down()

        if self.e_type == 'player':
            pass
        if self.e_type == 'bullet':
            
            self.velocity[0] = 5

        frame_movement = (self.velocity[0], self.velocity[1])
        #self.pos[0] += frame_movement[0]
        #self.pos[1] += frame_movement[1]

    def render(self, surface: pygame.Surface):
        surface.blit(self.img, self.pos)