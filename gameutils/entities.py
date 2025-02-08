import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, img: pygame.Surface):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.img = pygame.transform.scale(img, size)
        if(self.e_type == 'bullet'):
            self.velocity = [5, 0]
        else:
            self.velocity = [0, 0]
        self.width = size[0]
        self.height = size[1]
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False

    def __del__(self):
        print(f"Object {self.e_type} destroyed")

    def out_of_bounds(self) -> bool:
        if(self.pos[0] > 0 and self.pos[0] < (self.game.screen.get_size()[0] - self.width) and self.pos[1] > 0 and self.pos[1] < self.game.screen.get_size()[1] - self.height):
            return False
        print(f"{self.e_type} Out of Bounds!")
        return True

    def reset_velocity(self):
        self.velocity = [0, 0]
        
    def move_right(self):
        self.velocity[0] = 10
    
    def move_left(self):
        if(self.pos[0] > 0):
            self.velocity[0] = -10
    
    def move_up(self):
        if(self.pos[1] > 0):
            self.velocity[1] = -10
    
    def move_down(self):
        self.velocity[1] = 10

    def set_x_velocity(self, n):
        self.velocity[0] = n 
    
    def set_y_velocity(self, n):
        self.velocity[1] = n 

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
                if(self.pos[1] < self.game.screen.get_size()[1] - self.height):
                    self.move_down()
                    frame_movement = (self.velocity[0], self.velocity[1])
                    self.pos[1] += frame_movement[1]
        elif self.e_type == 'bullet':
            if(self.pos[0] < 2000000):
                self.pos[0] += self.velocity[0]


    def render(self, surface: pygame.Surface):
        surface.blit(self.img, self.pos)