# CSCE 31903 Programming Paradigms
# Fall 2025
# Assignment 7 starter code
# Name: Gavin Henderson
# Date: December 4th, 2025
# Desc: Link Game in Python

import pygame
import time
import json
import math

from pygame.locals import*
from time import sleep


class Sprite():
    def __init__(self, x, y, w, h, image):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = 1
        self.valid = True
        self.image = pygame.image.load(image)

    #all of the templates for child classes to implement
    # these methods do nothing in the parent class
    def update(self, model):
        pass

    def draw(self, screen_object, scrollX, scrollY):
        pass

    def manage_collision(self, other):
        pass

    def get_img(self):
        pass

    def to_string(self):
        pass

    # for the starter code, we assume that all Sprites of a certain
    # type are the same size, and thus don't need w and h saved
    # However, it would be very easy to add more attributes to be 
    # saved here!

    #we will let the child classes implement this method
    #this is the same as what we did in Java and makes more sense to me
    def marshal(self):
        pass
    
    def collision_detection(self, other):
        if self != other:
            other_left = other.x
            other_right = other.x + other.w
            other_top = other.y
            other_bottom = other.y + other.h

            if (self.x + self.w > other_left and self.x < other_right and self.y + self.h > other_top and self.y < other_bottom):
                return other
        
        return None
    
    #no abstract methods so these are defaults
    #child classes will return true for respective type
    def is_tree(self):
        return False
    
    def is_link(self):
        return False
    
    def is_treasure_chest(self):
        return False
    
    def is_boomerang(self):
        return False
    
    def is_cucco(self):
        return False

class Link(Sprite):
    
    def __init__(self):
        super().__init__(100, 100, 40, 50, "images/link1.png")
        self.frame = 0
        self.speed = 10
        self.direction = "down"
        self.px = self.x
        self.py = self.y

        self.rupee_score = 0

        #load in link images 
        self.link_down = []
        self.link_up = []
        self.link_left = []
        self.link_right = []

        if self.link_down == []:
            try:
                for i in range(1, 6):
                    file_name = "images/link" + str(i) + ".png"
                    self.link_down.append(pygame.image.load(file_name))
                for i in range(12, 17):
                    file_name = "images/link" + str(i) + ".png"
                    self.link_left.append(pygame.image.load(file_name))
                for i in range(23, 28):
                    file_name = "images/link" + str(i) + ".png"
                    self.link_right.append(pygame.image.load(file_name))
                for i in range(34, 39):
                    file_name = "images/link" + str(i) + ".png"
                    self.link_up.append(pygame.image.load(file_name))
            except:
                print("Error loading in images for link")

    def draw(self, screen_object, scrollX, scrollY):
        link_img = None
        match self.direction:
            case "down":
                link_img = self.link_down[self.frame]
            case "up":
                link_img = self.link_up[self.frame]
            case "left": 
                link_img = self.link_left[self.frame]
            case "right":
                link_img = self.link_right[self.frame]
        
        if link_img is not None:
            #transform the image as pygame's .blit() method doesnt take w and h as parameters
            #change the img size so that it accurately reflects the image being drawn
            scaled_img = pygame.transform.scale(link_img, (self.w, self.h))

            screen_object.blit(scaled_img, (self.x - scrollX, self.y - scrollY))

    def get_img(self):
        link_img = None

        match self.direction:
            case "down":
                link_img = self.link_down[self.frame]
            case "up":
                link_img = self.link_up[self.frame]
            case "left": 
                link_img = self.link_left[self.frame]
            case "right":
                link_img = self.link_right[self.frame]

        return link_img
    
    #getters and setters for links px and py
    def get_px(self):
        return self.px
    
    def get_py(self):
        return self.py
    
    def set_px(self, x):
        self.px = x

    def set_py(self, y):
        self.py = y

    #set direction and create frame changers
    def set_direction(self, dir):
        self.direction = dir

    def update_frame(self):
        self.frame = (self.frame + 1) % 5

    #movement functions for link
    def move_up(self):
        self.set_direction("up")
        self.y -= self.speed
        self.update_frame()
    
    def move_down(self):
        self.set_direction("down")
        self.y += self.speed
        self.update_frame()

    def move_left(self):
        self.set_direction("left")
        self.x -= self.speed
        self.update_frame()

    def move_right(self):
        self.set_direction("right")
        self.x += self.speed
        self.update_frame()

    def manage_collision(self, other):
        if (other.is_tree()):
            prev_right = self.px + self.w
            prev_left = self.px
            prev_top = self.py
            prev_bottom = self.py + self.h

            if (prev_right <= other.x):
                self.x = other.x - self.w
            elif (prev_left >= other.x + other.w):
                self.x = other.x + other.w
            elif (prev_bottom <= other.y):
                self.y = other.y - self.h
            elif (prev_top >= other.y + other.h):
                self.y = other.y + other.h
        
        if (other.is_treasure_chest()):
            chest = other
            if (chest.opened == True):
                if (chest.countdown <= 75):
                    self.rupee_score += 1
                    return
                self.x = self.px
                self.y = self.py
    
    def update(self, model):
        #doesn't need to do anything
        return True
    
    def marshal(self):
        return None
    
    def to_string(self):
        return "Link is at (" + str(self.x) + ", " + str(self.y) + ") facing " + self.direction + " on frame " + str(self.frame)
    
    def is_link(self):
        return True
    




class Tree(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y, 60, 75, "images/tree.png")

    def draw(self, screen_object, scroll_x, scroll_y):
        #scale tree so width and height are accurate and draw tree with screen_object
        scaled_tree = pygame.transform.scale(self.image, (self.w, self.h))
        screen_object.blit(scaled_tree, (self.x - scroll_x, self.y - scroll_y))

    def get_img(self):
        return self.image
    
    def marshal(self):
        return {
            "x" : self.x,
            "y" : self.y,
            "w" : self.w,
            "h" : self.h,
            "type": "tree"
            }

    def unmarshal(self, data):
        self.x = data['x']
        self.y = data['y']
        self.w = data['w']
        self.h = data['h']

    def to_string(self):
        return "Tree (x,y) = (" + str(self.x) + ", " + str(self.y) + "), w = " + str(self.w) + ", h = " + str(self.h)
    
    def update(self, model):
        return True
    
    def manage_collision(self, other):
        return None
    
    def is_tree(self):
        return True
    


class TreasureChest(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, "images/treasurechest.png")
        self.opened = False
        self.countdown = 0

        self.opened_img = pygame.image.load("images/rupee.png")

    def get_img(self):
        return self.image
    
    def draw(self, screen_object, scroll_x, scroll_y):
        if (self.opened):
            scaled_img = pygame.transform.scale(self.opened_img, (self.w, self.h))
            screen_object.blit(scaled_img, (self.x - scroll_x, self.y - scroll_y))
        else:
            scaled_img = pygame.transform.scale(self.image, (self.w, self.h))
            screen_object.blit(scaled_img, (self.x - scroll_x, self.y - scroll_y))

    def update(self, model):
        if (self.opened):
            self.countdown -= 1
            if (self.countdown <= 0):
                return False
        
        return True
    
    def manage_collision(self, other):
        if (other.is_link() or other.is_boomerang()):
            if (self.opened == False):
                self.opened = True
                self.countdown = 80
            else:
                if (self.countdown < 75):
                    if (other.is_link() or other.is_boomerang()):
                        self.countdown = 1 #gets rid of chest on the next frame

    def marshal(self):
        return{
            "x" : self.x,
            "y" : self.y,
            "w" : self.w,
            "h" : self.h,
            "type" : "TreasureChest"
        }
    
    def unmarshal(self, data):
        self.x = data["x"]
        self.y = data["y"]
        self.w = data["w"]
        self.h = data["h"]
    
    def to_string(self):
        return "TreasureChest (x,y) = (" + str(self.x) + ", " + str(self.y) + "), w = " + str(self.w) + ", h = " + str(self.h) + ", opened = " + str(self.opened) + ", countdown = " + str(self.countdown)

    def is_treasure_chest(self):
        return True

    
class Boomerang(Sprite):

    def __init__(self, x, y, direction):
        super().__init__(x, y, 20, 20, "images/boomerang1.png")
        self.direction = direction
        self.speed = 15
        self.frame = 0
        self.alive = True

        self.boomerang_imgs = []

        if (self.boomerang_imgs == []):
            try:
                for i in range(1,5):
                    filename = "images/boomerang" + str(i) + ".png"
                    self.boomerang_imgs.append(pygame.image.load(filename))
            except:
                print("Couldn't load in boomerang images")
    
    def draw(self, screen_object, scroll_x, scroll_y):
        boomerang_img = self.boomerang_imgs[self.frame]
        if boomerang_img is not None:
            scaled_img = pygame.transform.scale(boomerang_img, (self.w, self.h))
            screen_object.blit(scaled_img, (self.x - scroll_x, self.y - scroll_y))

    def update(self, model):
        if (self.direction == 'up'):
            self.y -= self.speed
        elif (self.direction == 'down'):
            self.y += self.speed
        elif (self.direction == 'left'):
            self.x -= self.speed
        elif (self.direction == 'right'):
            self.x += self.speed

        self.update_frame()
        return self.alive
    
    def manage_collision(self, other):
        if (other.is_tree() or other.is_treasure_chest()):
            self.alive = False

    def get_img(self):
        return self.boomerang_imgs[self.frame]
    
    def update_frame(self):
        self.frame = (self.frame + 1) % 4

    def marshal(self):
        return None
    
    def to_string(self):
        return "Boomerang (x,y) = (" + str(self.x) + ", " + str(self.y) + "), w = " + str(self.w) + ", h = " + str(self.h) + ", direction = " + self.direction + ", speed = " + str(self.speed)
    
    def is_boomerang(self):
        return True

        

    

        
    


class Model():
    filename = "map.json"
    
    def __init__(self):
        self.load_map()

    def load_map(self):
        # reset the fish count if we're loading (or reloading)
        # the map
        Fish.reset_fish()
        
        self.sprites = []
        # example of adding a hardcoded fish
        self.sprites.append(Fish(200,100,Fish.FISH_WIDTH, Fish.FISH_HEIGHT))
        
        # example of reading through the map.json file
        # and loading fishes and the turtle's location
        # open the json map and pull out the individual lists of sprite objects
        with open(Model.filename) as file:
            data = json.load(file)
            #get the lists . as "fishes" and "butterflies" from the map.json file
            fishes = data["fishes"]
            butterflies = data["butterflies"]
            #get turtle data out - these are individual
            #attributes, not a list
            turtlex = data["turtlex"]
            turtley = data["turtley"]
        file.close()
        
        #create turtle using saved attributes
        self.turtle = Turtle(turtlex, turtley)
        self.sprites.append(self.turtle)

        #for each entry inside the fishes list, pull the key:value pair out and create 
        #a new Fish object with (x,y,w,h)
        for entry in fishes:
            self.sprites.append(Fish(entry["x"], entry["y"], Fish.FISH_WIDTH, Fish.FISH_HEIGHT))

    def save_map(self):
        # create lists for each type of sprite you want to save
        fishes = []
        butterflies = []

        # go through all of the sprites, saving them into the 
        # appropriate lists
        for s in self.sprites:
            if s.is_fish():
                fishes.append(s.marshal())
            elif s.is_butterfly():
                butterflies.append(s.marshal())

        # create the dictionary of sprites, split by what types
        # they are - fishes and butterflies are lists, while 
        # turtlex and turtley are singular attributes
        map_to_save = {
            "fishes": fishes,
            "butterflies": butterflies,
            "turtlex": self.turtle.x,
            "turtley": self.turtle.y
        }

        # Save to file
        with open(Model.filename, "w") as f:
            json.dump(map_to_save, f)

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def clear_map(self):
        self.sprites.clear()
        self.sprites.append(self.turtle)
        # calling a static method - notice the lack of 'self'
        Fish.reset_fish()

    # pos was passed as the mouse position tuple - pos[0] is x, 
    # pos[1] is y
    def add_fish(self, pos):
        self.sprites.append(Fish(pos[0], pos[1]))

class View():
    def __init__(self, model):
        SCREEN_SIZE = (800,600)
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 32)
        self.model = model

    def update(self):
        # change background color if the user is in edit_mode
        if Controller.edit_mode:
            self.screen.fill([146, 203, 146]) #light green
        else:
            self.screen.fill([72, 152, 72]) #dark forest green

        # draw sprites to the screen
        for sprite in self.model.sprites:
            LOCATION = (sprite.x, sprite.y)
            SIZE = (sprite.w, sprite.h)
            self.screen.blit(pygame.transform.scale(sprite.image, SIZE), LOCATION)

        # add text to the screen
        # Default font, size 32
        font = pygame.font.SysFont(None, 32)   
        text_string = "There are " + str(Fish.num_fish) + " fish on the screen!"
        PURPLE_COLOR = (160, 32, 240)
        text_surface = font.render(text_string, True, PURPLE_COLOR)
        TEXT_LOCATION = (250, 10)
        self.screen.blit(text_surface, TEXT_LOCATION)
        
        # update display screen
        pygame.display.flip()

class Controller():
    edit_mode = False
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.keep_going = True

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    self.keep_going = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if Controller.edit_mode:
                    # add a fish at using the "overloaded" constructor
                    self.model.add_fish(pygame.mouse.get_pos())
            elif event.type == pygame.KEYUP: #this is keyReleased!
                if event.key == K_c:
                    self.model.clear_map()
                    print("Map cleared and game reset")
                if event.key == K_e:
                    Controller.edit_mode = not Controller.edit_mode
                if event.key == K_l:
                    self.model.load_map()
                    print("Map loaded")
                if event.key == K_s:
                    self.model.save_map()
                    print("Map saved")
        keys = pygame.key.get_pressed()
        # turtle's movement function changed to be closer related
        # to Link
        if keys[K_LEFT]:
            self.model.turtle.move("left")
        if keys[K_RIGHT]:
            self.model.turtle.move("right")
        if keys[K_UP]:
            self.model.turtle.move("up")
        if keys[K_DOWN]:
            self.model.turtle.move("down")

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
pygame.font.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye!")