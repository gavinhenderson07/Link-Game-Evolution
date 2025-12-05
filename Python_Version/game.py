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

    def reset_frame(self):
        self.frame = 0

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
    

class Cucco(Sprite):

    num_cuccos = 0
    num_hits = 0
    angry = False
    dissapeared = 0
    link_x = 0
    link_y = 0

    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, "images/cucco1.png")

        #variables of specific cucco
        self.xdir = 1
        self.ydir = 1
        self.speed = 5
        self.angry_speed = 10
        self.frame = 0
        self.attached_to_link = False
        self.attached_timer = 20
        self.cooldown_timer = 0
        

        self.happy_right = []
        self.happy_left = []
        self.angry_left = []
        self.angry_right = []

        try:
            self.happy_left.append(pygame.image.load("images/cucco1.png"))
            self.happy_left.append(pygame.image.load("images/cucco2.png"))
            self.happy_right.append(pygame.image.load("images/cucco3.png"))
            self.happy_right.append(pygame.image.load("images/cucco4.png"))

            self.angry_left.append(pygame.image.load("images/angrycucco1.png"))
            self.angry_left.append(pygame.image.load("images/angrycucco2.png"))
            self.angry_right.append(pygame.image.load("images/angrycucco3.png"))
            self.angry_right.append(pygame.image.load("images/angrycucco4.png"))
        except:
            print("Error loading in Cucco images")

    def draw(self, screen_object, scroll_x, scroll_y):
        current_img = None

        if not Cucco.angry:
            if self.xdir < 0:
                current_img = self.happy_left[self.frame]
            else:
                current_img = self.happy_right[self.frame]
        else:
            if self.xdir < 0:
                current_img = self.angry_left[self.frame]
            else:
                current_img = self.angry_right[self.frame]

        if current_img is not None:
            scaled_img = pygame.transform.scale(current_img, (self.w, self.h))
            screen_object.blit(scaled_img, (self.x -scroll_x, self.y - scroll_y))
    
    def update(self, model):
        #first check if they are angry/one left and reset values accordingly
        if Cucco.num_cuccos <= 1 or Cucco.dissapeared >= 3:
            Cucco.angry = False
            Cucco.num_hits = 0
            Cucco.dissapeared = 0

            self.attached_to_link = False
            self.attached_timer = 10

        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

        if Cucco.num_hits >= 5 and Cucco.num_cuccos > 1 and not Cucco.angry:
            Cucco.angry = True
        
        #if theyre not angry move them and update frame
        if not Cucco.angry:
            self.x += self.xdir * self.speed
            self.y += self.ydir * self.speed

            self.frame = (self.frame + 1) % 2
            #if angry, track down link
        else:
            if self.attached_to_link:
                self.attached_timer -= 1
                if self.attached_timer <= 0:

                    #check for the last cucco and return true
                    if Cucco.num_cuccos <= 1:
                        Cucco.angry = False
                        Cucco.num_hits = 0
                        Cucco.dissapeared = 0

                        self.attached_to_link = False
                        self.attached_timer = 20
                        return True
                    Cucco.num_cuccos -= 1
                    Cucco.dissapeared += 1
                    #remove from sprites list
                    return False
            else:
                dx = Cucco.link_x - self.x
                dy = Cucco.link_y - self.y

                if dx < 0:
                    self.xdir = -1
                else:
                    self.xdir = 1
                
                #find the distance to link using his location and cuccos
                #make them move towards him at the faster speed
                #move them to link until they are touching and update frame
                length = math.sqrt(dx*dx + dy*dy)
                if length < 0.001:
                    length = 0.001

                direction_to_go_x = dx / length
                direction_to_go_y = dy / length

                self.x += direction_to_go_x * self.angry_speed
                self.y += direction_to_go_y * self.angry_speed

                if length < 40:
                    self.attached_to_link = True

                self.frame = (self.frame + 1) % 2
        return True
    
    def manage_collision(self, other):
        #dont detect anything if its angry
        if Cucco.angry:
            return
        
        if other.is_tree() or other.is_treasure_chest() or other.is_link() or other.is_boomerang():
            
            # Check X side
            # If Cucco center is to the left of object center, bounce Left
            if (self.x + self.w/2) < (other.x + other.w/2):
                self.xdir = -1
                self.x -= 15 
            else:
                self.xdir = 1
                self.x += 15 

            # Check Y side
            if (self.y + self.h/2) < (other.y + other.h/2):
                self.ydir = -1
                self.y -= 15
            else:
                self.ydir = 1
                self.y += 15

            if other.is_link() or other.is_boomerang():
                if self.cooldown_timer == 0:
                    self.cooldown_timer = 15
                    Cucco.num_hits += 1
                    print("Hit! Total:", Cucco.num_hits)

    def get_img(self):
        return self.image
    
    def is_cucco(self):
        return True
    
    def marshal(self):
        return {
            "x" : self.x,
            "y" : self.y,
            "type" : "Cucco"
        }

    def unmarshal(self, data):
        self.x = data["x"]
        self.y = data["y"]


class TreasureChest(Sprite):

    RUPEE_COUNT = 0
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, "images/treasurechest.png")
        self.opened = False
        self.countdown = 0
        self.collected = False
        

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
                if (self.countdown < 75 and self.collected == False):
                    if (other.is_link() or other.is_boomerang()):
                        TreasureChest.RUPEE_COUNT += 1
                        self.collected = True
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
        if (other.is_tree() or other.is_treasure_chest() or other.is_cucco()):
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

    #create model static variables to hold screen and world size for scrolling use

    #keep values same as java for porting capability
    WORLD_WIDTH = 1400
    WORLD_HEIGHT = 1000

    #world_width world_height screen_width screen_height
    #these values come from this line in view:
    #SCREEN_SIZE = (800,600)
    #use same values for scrolling purpose
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 500

    
    def __init__(self):

        self.sprites = []
        self.can_add = []
        self.item_index = 0
        self.edit_mode = False

        self.link = Link()
        self.sprites.append(self.link)

        self.chest = TreasureChest(-100, -100)
        self.tree = Tree(-100, -100)

        self.ui_cucco = Cucco(-100, -100)
        

        self.can_add.append(self.tree)
        self.can_add.append(self.chest)
        self.can_add.append(self.ui_cucco)
    

        self.load_map()

        self.cucco = Cucco(250, 250)
        self.sprites.append(self.cucco)
        Cucco.num_cuccos = 1

    def load_map(self):
        
        #set cucco amoutn before loading in map
        Cucco.num_cuccos = 0
        #clear the list and add link first
        self.sprites = []
        self.sprites.append(self.link)


        
        #try to open the json file and throw exception in case of error
        #read file and add sprite according to the type
        try:
            with open(Model.filename, 'r') as file:
                data = json.load(file)

            #grab the loaded sprites from the data
            #if there is an issue, create empty list if no sprites are found to prevent crashes (precaution)
                loaded_sprites = data.get("sprites", [])

                for sprite in loaded_sprites:
                    if sprite["type"] == "tree":
                        t = Tree(0, 0)
                        t.unmarshal(sprite)
                        self.sprites.append(t)
                    
                    elif sprite["type"] == "TreasureChest":
                        c = TreasureChest(0, 0)
                        c.unmarshal(sprite)
                        self.sprites.append(c)

                    elif sprite["type"] == "Cucco":
                        c = Cucco(0,0)
                        c.unmarshal(sprite)
                        self.sprites.append(c)
        except Exception as e:
            print("Error loading in map from JSON:", e)

    def save_map(self):
        
        saved_sprites = []
        #loop through all the sprites but skip link as he is not saved
        for sprite in self.sprites:
            if sprite.is_link():
                continue
                
            saved_sprites.append(sprite.marshal())

        #create dictionary with the sprites key that saves the sprite list in its value
        data = {
            "sprites": saved_sprites
        }


        # Save to file
        with open(Model.filename, "w") as f:
            json.dump(data, f)

    def set_view(self, view):
        self.view = view

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        #loop through a copy of the list of sprites
        #when removing, remove from real list, but continue to 
        #loop through coped list to avoid skipping elements
        for sprite in self.sprites[:]:
            valid = sprite.update(self)

            #check for ghost sprites due to using a copied list
            if sprite not in self.sprites:
                continue

            if not valid:
                self.sprites.remove(sprite)
                continue

            #here can loop through regular list as we are not removing anything,
            #just checking for collisions
            for sprite2 in self.sprites:
                if (sprite is not sprite2):
                    if (sprite.collision_detection(sprite2) is not None):
                        sprite.manage_collision(sprite2)
                        sprite2.manage_collision(sprite)

        
        #create edge variables to work with
        right_edge = self.view.scroll_x + Model.SCREEN_WIDTH
        left_edge = self.view.scroll_x
        top_edge = self.view.scroll_y
        bottom_edge = self.view.scroll_y + Model.SCREEN_HEIGHT

        if (self.controller.key_right and self.link.x + self.link.w > right_edge):
            if (self.view.scroll_x < Model.WORLD_WIDTH - Model.SCREEN_WIDTH):
                self.view.set_scroll(self.view.scroll_x + Model.SCREEN_WIDTH, self.view.scroll_y)

                #place link in a visible spot on the next screen
                self.link.x = self.view.scroll_x + 5
        elif (self.controller.key_left and self.link.x < left_edge):
            if (self.view.scroll_x > 0):
                self.view.set_scroll(self.view.scroll_x - Model.SCREEN_WIDTH, self.view.scroll_y)

                self.link.x = Model.SCREEN_WIDTH - self.link.w -12
        elif(self.controller.key_down and self.link.y + self.link.h > bottom_edge):
            if(self.view.scroll_y < Model.WORLD_HEIGHT - Model.SCREEN_HEIGHT):
                self.view.set_scroll(self.view.scroll_x, self.view.scroll_y + Model.SCREEN_HEIGHT)

                self.link.y = self.view.scroll_y + 5
        elif(self.controller.key_up and self.link.y < top_edge):
            if (self.view.scroll_y > 0):
                self.view.set_scroll(self.view.scroll_x, self.view.scroll_y - Model.SCREEN_HEIGHT)

                self.link.y = Model.SCREEN_HEIGHT - self.link.h - 25

    def add_sprite(self, x, y):
        sprite = self.can_add[self.item_index]

        if (sprite.is_tree()):
            snapped_x = (x // 75) * 75
            snapped_y = (y // 75) * 75
            tree = Tree(snapped_x, snapped_y)
            
            if (self.is_area_colliding(tree) is not True):
                self.sprites.append(tree)
        elif(sprite.is_treasure_chest()):
            centered_x = x - (sprite.w // 2)
            centered_y = y - (sprite.h // 2)

            temp_chest = TreasureChest(centered_x, centered_y)

            if (self.is_area_colliding(temp_chest) is not True):
                self.sprites.append(temp_chest)
        elif (sprite.is_cucco()):
            centered_x = x - (sprite.w // 2)
            centered_y = y - (sprite.h // 2)
            t_cucco = Cucco(centered_x, centered_y)
            if (self.is_area_colliding(t_cucco) is not True):
                self.sprites.append(t_cucco)
                Cucco.num_cuccos += 1
            



    def is_area_colliding(self, s):
        for sprite in self.sprites:
            if (s.collision_detection(sprite) is not None):
                return True
            
        return False

    def is_sprite_at(self, x, y):
        for sprite in self.sprites:
            if (sprite.is_tree() or sprite.is_treasure_chest()):
                if (sprite.x == x and sprite.y == y):
                    return True
        
        return False
    
    def clear_map(self):
        for sprite in self.sprites[:]:
            if (sprite.is_tree() or sprite.is_treasure_chest() or sprite.is_cucco()):
                self.sprites.remove(sprite)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

    def set_item_index(self):
        self.item_index = (self.item_index + 1) % len(self.can_add)

    def throw_boomerang(self):

        link_x = self.link.x + (self.link.w // 2)
        link_y = self.link.y + (self.link.h // 2)

        #boomerang is 20 by 20 so subtract half to launch from center
        boom_x = link_x - 10
        boom_y = link_y - 10

        boomerang = Boomerang(boom_x, boom_y, self.link.direction)
        self.sprites.append(boomerang)



class View():
    def __init__(self, model):
        SCREEN_SIZE = (700,500)
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 32)
        self.model = model

        self.scroll_x = 0
        self.scroll_y = 0

        self.font = pygame.font.SysFont(None, 32)

    def update(self):
        # change background color if the user is in edit_mode
        if self.model.edit_mode:
            self.screen.fill([146, 203, 146]) #light green
        else:
            self.screen.fill([72, 152, 72]) #dark forest green

        # draw sprites to the screen
        for sprite in self.model.sprites:
            #changed this code as we used pygame.image.transform when lazy loading images
            #also since sprites have their own draw, we just call sprite.draw

            sprite.draw(self.screen, self.scroll_x, self.scroll_y)

        rupee_count = TreasureChest.RUPEE_COUNT

        display_str = "Rupees: " + str(rupee_count)


        surface = self.font.render(display_str, True, (255, 255, 255), None)
        self.screen.blit(surface, (550, 10))

        if self.model.edit_mode:
            pygame.draw.rect(self.screen, (0, 100, 0), (0, 0, 100, 100))
            item = self.model.can_add[self.model.item_index]
            item_img = item.get_img()

            #put the images 10 frames from top left corner
            #center the sprite being drawn so that it lays in the center of the rectangle
            scaled_img = pygame.transform.scale(item_img, (60, 60))
            img_x = (100-60) // 2
            img_y = (100-60) // 2
            self.screen.blit(scaled_img, (img_x, img_y))

        # update display screen
        pygame.display.flip()

    def set_scroll(self, x, y):
        self.scroll_x = x
        self.scroll_y = y

class Controller():
    
    
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

                elif event.key == K_SPACE:
                    self.model.throw_boomerang()

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.model.edit_mode:
                    pos = pygame.mouse.get_pos()

                    #see if the mouse click was in the top corner
                    if 0 <= pos[0] <= 100 and 0 <= pos[1] <= 100:
                        self.model.set_item_index()
                    else:
                        world_x = pos[0] + self.view.scroll_x
                        world_y = pos[1] + self.view.scroll_y

                        self.model.add_sprite(world_x, world_y)

            elif event.type == pygame.KEYUP: #this is keyReleased!
                if event.key == K_c:
                    if self.model.edit_mode is True:
                        self.model.clear_map()
                        print("Map cleared and game reset")

                if event.key == K_e:
                    self.model.toggle_edit_mode()

                if event.key == K_l:
                    self.model.load_map()
                    print("Map loaded")

                if event.key == K_s:
                    self.model.save_map()
                    print("Map saved")

        keys = pygame.key.get_pressed()
        #use variable names for scrolling reasons in model
        self.key_left = keys[K_LEFT]
        self.key_right = keys[K_RIGHT]
        self.key_up = keys[K_UP]
        self.key_down = keys[K_DOWN]

        if self.key_left:
            self.model.link.move_left()
        elif self.key_right:
            self.model.link.move_right()
        elif self.key_up:
            self.model.link.move_up()
        elif self.key_down:
            self.model.link.move_down()
        else:
            self.model.link.reset_frame()

        #update cucco link location after links movement
        Cucco.link_x = self.model.link.x
        Cucco.link_y = self.model.link.y

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
pygame.font.init()
m = Model()
v = View(m)
m.set_view(v)
c = Controller(m, v)
m.set_controller(c)
while c.keep_going:
    link = m.link
    link.set_px(link.x)
    link.set_py(link.y)
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye!")