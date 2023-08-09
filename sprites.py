import pygame
from config import *
import math
import random

#for spritesheet with white bg
class WSpritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(WHITE)
        return sprite

#for shpritesheet with black bg    
class BSpritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.playersprite
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        
    
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_zoneline()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    #inputcounter = 0
    #showingtext = False

    def movement(self):
        keys = pygame.key.get_pressed()
        if self.game.in_dialog or self.game.in_battle:
            pass
        else:
            if keys[pygame.K_a]:
                #IF PLAYER IS AT EDGE, DON'T MOVE THE SPRITES
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
                self.x_change -= PLAYER_SPEED
                self.facing = 'left'
            if keys[pygame.K_d]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
                self.x_change += PLAYER_SPEED
                self.facing = 'right'
            if keys[pygame.K_w]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED
                self.y_change -= PLAYER_SPEED
                self.facing = 'up'
            if keys[pygame.K_s]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED
                self.y_change += PLAYER_SPEED
                self.facing = 'down'
            if keys[pygame.K_i]:
                self.game.inmenu = True
                self.game.menu()

    def collide_zoneline(self):
        hits = pygame.sprite.spritecollide(self, self.game.zonelines, False)
        if hits:
            #empty the sprite groups
            self.game.all_sprites.empty()
            self.game.blocks.empty()
            self.game.enemies.empty()
            self.game.zonelines.empty()
            #re-add player to all_sprites group
            self.game.all_sprites.add(self.game.playersprite)
            if self.game.current_zone.id == FRANTIKSHUT:
                self.game.current_zone.id = KELETHINMAIN
            elif self.game.current_zone.id == KELETHINMAIN:
                self.game.current_zone.id = FRANTIKSHUT
            
            self.game.createTilemap(self.game.current_zone.id)

    ### BATTLE SCREEN
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            #empty the sprite groups - new map will add 
            self.game.all_sprites.empty()
            self.game.blocks.empty()
            self.game.enemies.empty()
            self.game.zonelines.empty()

            #add player to sprite group for drawing
            self.game.all_sprites.add(self.game.playersprite)

            #select and call new map
            if self.game.current_zone.id == KELETHINMAIN or FRANTIKSHUT:
                self.game.current_zone.id = KELETHINBATTLE
                           
            self.game.createTilemap(self.game.current_zone.id)
            self.game.startBattle()

            
            #pygame.time.delay(250)
            #while self.game.in_battle:
            """  
            #get first round inits
            for i in range(self.game.mobs.__len__()):
                    self.game.mobs[i].init = random.randint(1, 20) + self.game.mobs[i].dexmod
                    print(self.game.mobs[i].init)
            self.init = random.randint(1, 20) + self.dexmod
            print(self.init)
                
            #until everyone has a turn
            while self.turns < (self.game.mobs.__len__() + 1):
            #set everyone's init
                for i in range(self.game.mobs.__len__()):   #get first init
                    if self.game.mobs[i].init > self.tempspot:
                        self.tempspot = i

                #check highest init
                if self.game.mobs[self.tempspot].init > self.init:
                    print("Enemy attacks")
                    self.hp -= 1
                    self.game.mobs[self.tempspot].init = 0 #make that enemy init 0
                else:
                    print ("Player attacks")
                    #getplayerinput()
                    pygame.event.wait()
                    if self.game.battle_input == 1:
                        self.game.mobs[self.tempspot].hp -= 1
                        #self.waitingforaction = False
                        self.game.battle_input = -1
                    elif self.game.battle_input == 2:
                        self.game.mobs[self.tempspot].hp -= 5
                        #self.waitingforaction = False
                        self.game.battle_input = -1
                        
                    self.init = 0


                if self.hp <= 0:
                    print("You Die!")
                    self.game.in_battle = False
                    self.turns += 100 #if you're dead, end the round
                elif self.game.mobs[self.tempspot].hp <= 0:
                    print("You killed an enemy!")
                    self.game.in_battle = False
                    for i in range(self.game.mobs.__len__()):   
                        if self.game.mobs[i].hp > 0:
                            self.game.in_battle = True
                            print("still some to kill")
                #any enemies left alive?  keep battle going
                self.turns += 1

            self.turns = 0
            print ("Round over")
            #self.inbattle = False
             
            self.game.battle.empty()
            self.game.all_sprites.empty()
            self.game.all_sprites.add(self.game.playersprite)
            self.game.current_zone.id = KELETHINMAIN
            self.game.createTilemap(self.game.current_zone.id)
            """

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction =='y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

#Sprites that contain items
#class ItemBlockSprite(pygame.sprite.Sprite):
#    def __init__(self, game, x, y, pixx, pixy):
#        self.game = game
#        self._layer = BLOCK_LAYER
        
#        self.x = x * TILESIZE
#        self.y = y * TILESIZE
#        self.width = TILESIZE  
 #       self.height = TILESIZE

#        self.groups = self.game.all_sprites, self.game.blocks
#        self.image = self.game.temp_spritesheet.get_sprite(pixx, pixy, self.width, self.height)

#        pygame.sprite.Sprite.__init__(self, self.groups)
#       self.rect = self.image.get_rect()
#        self.rect.x = self.x
 #       self.rect.y = self.y

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self. y

        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        


    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement (self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate (self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.battle
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self. y


    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement (self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate (self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

#non-moving, interactable sprites
class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y, pixx, pixy, layer):
        self.game = game
        self._layer = layer
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE  
        self.height = TILESIZE

        #impassible by player
        if layer == BLOCK_LAYER: #all_sprites for display, blocks for collision
            self.groups = self.game.all_sprites, self.game.blocks
            self.image = self.game.temp_spritesheet.get_sprite(pixx, pixy, self.width, self.height)
        #transport player to connected zone on collision
        elif layer == ZONE_LAYER:
            self.groups = self.game.all_sprites, self.game.zonelines
            self.image = self.game.temp_spritesheet.get_sprite(pixx, pixy, self.width, self.height)
        #characters of text for dialog
        elif layer == TEXT_LAYER: ## make into spritesheet for dialog
            self.groups = self.game.all_sprites, self.game.text
            #self.width = 98
            #self.height = 60
            self.image = self.game.npc_textsheet.get_sprite(pixx, pixy, 100, 85)
        elif layer == GEAR_LAYER:
            self.groups = self.game.all_sprites, self.game.text
            self.image = self.game.npc_textsheet.get_sprite(pixx, pixy, 40, 47)
        elif layer == DIALOGNPC_LAYER: 
            self.groups = self.game.all_sprites, self.game.blocks#, self.game.dialognpc - can I use hasdialog flag??
            self.image = self.game.enemy_spritesheet.get_sprite(ENEMYX, ENEMYY, self.width, self.height)
            #NPClist.append(dialog_npc) - to check through and get dialog
        else: #GROUND_LAYER
            self.groups = self.game.all_sprites
            self.image = self.game.temp_spritesheet.get_sprite(pixx, pixy, self.width, self.height)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class TextSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y, char):
        self.game = game
        #DISPLAY GROUPS
        self.groups = self.game.all_sprites, self.game.text
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE / 2  
        self.height = TILESIZE / 2

        if char == 'A':
            self.image = self.game.npc_textsheet.get_sprite(0, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'a':
            self.image = self.game.npc_textsheet.get_sprite(0, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'B':
            self.image = self.game.npc_textsheet.get_sprite(17, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'b':
            self.image = self.game.npc_textsheet.get_sprite(17, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'C':
            self.image = self.game.npc_textsheet.get_sprite(33, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'c':
            self.image = self.game.npc_textsheet.get_sprite(33, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'D':
            self.image = self.game.npc_textsheet.get_sprite(50, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'd':
            self.image = self.game.npc_textsheet.get_sprite(50, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'E':
            self.image = self.game.npc_textsheet.get_sprite(67, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'e':
            self.image = self.game.npc_textsheet.get_sprite(67, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'F':
            self.image = self.game.npc_textsheet.get_sprite(85, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'f':
            self.image = self.game.npc_textsheet.get_sprite(85, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'G':
            self.image = self.game.npc_textsheet.get_sprite(101, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'g':
            self.image = self.game.npc_textsheet.get_sprite(101, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'H':
            self.image = self.game.npc_textsheet.get_sprite(119, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'h':
            self.image = self.game.npc_textsheet.get_sprite(119, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'I':
            self.image = self.game.npc_textsheet.get_sprite(136, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'i':
            self.image = self.game.npc_textsheet.get_sprite(136, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'J':
            self.image = self.game.npc_textsheet.get_sprite(152, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'j':
            self.image = self.game.npc_textsheet.get_sprite(152, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'K':
            self.image = self.game.npc_textsheet.get_sprite(170, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'k':
            self.image = self.game.npc_textsheet.get_sprite(170, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'L':
            self.image = self.game.npc_textsheet.get_sprite(187, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'l':
            self.image = self.game.npc_textsheet.get_sprite(187, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'M':
            self.image = self.game.npc_textsheet.get_sprite(203, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'm':
            self.image = self.game.npc_textsheet.get_sprite(203, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'N':
            self.image = self.game.npc_textsheet.get_sprite(221, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'n':
            self.image = self.game.npc_textsheet.get_sprite(221, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'O':
            self.image = self.game.npc_textsheet.get_sprite(238, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'o':
            self.image = self.game.npc_textsheet.get_sprite(238, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'P':
            self.image = self.game.npc_textsheet.get_sprite(254, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'p':
            self.image = self.game.npc_textsheet.get_sprite(254, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'Q':
            self.image = self.game.npc_textsheet.get_sprite(271, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'q':
            self.image = self.game.npc_textsheet.get_sprite(271, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'R':
            self.image = self.game.npc_textsheet.get_sprite(289, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'r':
            self.image = self.game.npc_textsheet.get_sprite(289, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'S':
            self.image = self.game.npc_textsheet.get_sprite(305, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 's':
            self.image = self.game.npc_textsheet.get_sprite(305, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'T':
            self.image = self.game.npc_textsheet.get_sprite(323, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 't':
            self.image = self.game.npc_textsheet.get_sprite(323, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'U':
            self.image = self.game.npc_textsheet.get_sprite(340, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'u':
            self.image = self.game.npc_textsheet.get_sprite(340, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'V':
            self.image = self.game.npc_textsheet.get_sprite(356, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'v':
            self.image = self.game.npc_textsheet.get_sprite(356, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'W':
            self.image = self.game.npc_textsheet.get_sprite(373, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'w':
            self.image = self.game.npc_textsheet.get_sprite(373, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'X':
            self.image = self.game.npc_textsheet.get_sprite(391, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'x':
            self.image = self.game.npc_textsheet.get_sprite(391, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'Y':
            self.image = self.game.npc_textsheet.get_sprite(408, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'y':
            self.image = self.game.npc_textsheet.get_sprite(408, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == 'Z':
            self.image = self.game.npc_textsheet.get_sprite(425, 0, TILESIZE / 2, TILESIZE / 2)
        elif char == 'z':
            self.image = self.game.npc_textsheet.get_sprite(425, 16, TILESIZE / 2, TILESIZE / 2)
        elif char == '.':
            self.image = self.game.npc_textsheet.get_sprite(442, 32, TILESIZE / 2, TILESIZE / 2)
        elif char == ',':
            self.image = self.game.npc_textsheet.get_sprite(459, 32, TILESIZE / 2, TILESIZE / 2)
        else:
            self.image = self.game.npc_textsheet.get_sprite(442, 0, TILESIZE / 2, TILESIZE / 2)

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#from tutorial
class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('trebuc.ttf', fontsize)
        self.content = content
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:  #index 0 - LMB, index 1 RMB, index 2 MMB
                return True
            return False
        return False

#from tutorial
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]
        

    def update(self):
        self.animate()
        self.collide()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing


        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
            
        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

