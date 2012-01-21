import pygame
import random
from pygame.locals import *
from pygame.color import THECOLORS

dim = (1200, 900)

def main():
    pygame.init()
    screen = pygame.display.set_mode(dim)
    bg = screen.convert()
    bg.fill(THECOLORS["black"])
    screen.blit(bg, (0,0))
    pygame.display.update()


    clock = pygame.time.Clock()
    boxes = []
    box = Box(bg, dim, (4,4), boxes)
    boxes.append(box)
    timer = 0
    running = True
    while running:
        if timer > 100:
            boxes.append(Box(bg, dim, (4,4), boxes))
            timer = 0
        for box in boxes:
            box.update()

        screen.blit(bg, (0,0))
        pygame.display.flip()
        clock.tick(35)
        timer += 1
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

class Box:
    MAX_V = 3 
    def __init__(self, bg, screen_dim , size, box_list):
        self.box_list = box_list
        self.leader = False
        self.bg = bg
        self.prob = 0.1
        self.action_radius = random.randint(25,75) 
        self.screen_dim = screen_dim
        self.x = screen_dim[0]/2
        self.y = screen_dim[1]/2
        self.width = size[0]
        self.height = size[1]
        self.center_x = self.x+self.width/2
        self.center_y = self.y+self.height/2
        self.vx = random.randint(-self.MAX_V,self.MAX_V)
        self.vy = random.randint(-self.MAX_V,self.MAX_V)
        self.color = THECOLORS["green"]
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.neighbors = []
        self.update_neighbors()

    def update(self):
        self.update_neighbors()
        pygame.draw.rect(self.bg, THECOLORS["black"], self.rect)
        if random.random() < self.prob:
            self.vx += random.randint(-1,1)
            self.vy += random.randint(-1,1)

        if len(self.neighbors) > 0:
            leader = []

            for neighbor in self.neighbors:
                if neighbor.leader: 
                    leader.append(neighbor)
            if self.leader: leader.append(self)

            if len(leader) == 0:
                a = random.randint(-1, len(self.neighbors)-1)
                if a == -1:
                    self.leader = True
                else:
                    self.neighbors[a].leader = True
            elif len(leader) > 1:
                for i in range(1,len(leader)):
                    if len(leader[i-1].neighbors) <= len(leader[i].neighbors):
                        leader[i-1].leader = False
                
                    
            else:
                if leader[0] != self:
                    self.vx = leader[0].vx 
                    self.vy = leader[0].vy 

        else:
           self.leader = False

        if self.vx > self.MAX_V:
                self.vx = self.MAX_V
        elif self.vx < -self.MAX_V:
                self.vx = -self.MAX_V
        if self.vy > self.MAX_V:
                self.vy = self.MAX_V
        elif self.vy < -self.MAX_V:
                self.vy = -self.MAX_V

        new_x , new_y = self.x + self.vx, self.y + self.vy
        bound_x = new_x + self.width + self.action_radius
        bound_y = new_y + self.height + self.action_radius

        if bound_x >= self.screen_dim[0] or new_x-self.action_radius <= 0:
            self.vx *= -1
        else:
            self.x = new_x
        if bound_y >= self.screen_dim[1] or new_y-self.action_radius <= 0:
            self.vy *= -1
        else:
            self.y = new_y

        self.center_x = self.x+self.width/2
        self.center_y = self.y+self.height/2

        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        if self.leader:
            self.color = THECOLORS["blue"]
        else:
            self.color = THECOLORS["green"]
        pygame.draw.rect(self.bg, self.color, self.rect)

    def update_neighbors(self):
        self.neighbors = []
        for box in self.box_list:
            if box is not self and box.center_x > self.center_x-self.action_radius and \
                box.center_x < self.center_x+self.action_radius and \
                box.center_y > self.center_y-self.action_radius and \
                box.center_y < self.center_y+self.action_radius:
                self.neighbors.append(box)





if __name__ ==  '__main__': main()
