import pygame
from sprites import *
from config import *
from container import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('trebuc.ttf', 32)
        self.running = True

        self.inmenu = False #Is user in menu screen
        self.inmerchant = False

        #if displaying battle zone
        self.in_battle = False

        #battle choice
        self.battle_input = -1

        #if displaying dialog over zone
        self.in_dialog = False

        #index of player currently visible from party
        self.top_character = 0

        #list of Players for party
        self.party = []

        #LIST OF BATTLE ENEMIES
        self.mobs = []

        #list of CLICKABLE MENU SPRITES
        self.menuboxes = []
        self.merchantboxes = []

        #if there is a sprite on the cursor
        self.oncursor = False

        #list of dialog NPCs in the current zone, empty and reload when zoning
        self.dialognpc = []
        #list of items in chests or available for PU in the zone, empty and reload when zoning
        self.items = []

        #index of current merchant to display and buy goods
        self.current_merchant = -1

        #keep last zone for inmenu
        self.lastzone = 0

        #set battle timers
        #self.playertimer = pygame.event.custom_type()
        self.mobtimer = pygame.event.custom_type()

        #sprite sheets
        self.character_spritesheet = BSpritesheet('img/character.png')    
        self.items_spritesheet = BSpritesheet('img/itemsprites.bmp')    
        #self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = BSpritesheet('img/enemy.png')
        self.attack_spritesheet = BSpritesheet('img/attack.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.go_background = pygame.image.load('img/gameover.png')
        self.temp_spritesheet = WSpritesheet('img/bigsheet.png')
        self.menu_background = pygame.image.load('img/menu.png')
        self.npc_spritesheet = WSpritesheet('img/charsprites.jpg')
        #self.npc_spritesheet = BSpritesheet('img/npcss.png')
        self.npc_textsheet = WSpritesheet('img/textsheet.png')

    def new(self):
        # a new game starts
        self.playing = True
        
        #CLASS TO HOLD INFO NEEDED FOR CAMERA AND ZONE LOADING
        self.current_zone = Zone()   
        self.current_zone.id = FRANTIKSHUT
        self.current_zone.x = FRANTIKSHUTMAXX
        self.current_zone.y = FRANTIKSHUTMAXY

        # ALL SPRITES TO BE DRAWN MUST GO HERE
        self.all_sprites = pygame.sprite.LayeredUpdates()
        #SPRITES FOR COLLISION AND GROUPING TYPES
        self.playersprite = pygame.sprite.LayeredUpdates()
        self.blocks  = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.zonelines = pygame.sprite.LayeredUpdates()
        #SPRITES FOR GROUPING TYPES TOGETHER
        self.battle = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        self.text = pygame.sprite.LayeredUpdates()
        self.item_sprites = pygame.sprite.LayeredUpdates()
        self.menu_sprites = pygame.sprite.LayeredUpdates()
        #self.attacks = pygame.sprite.LayeredUpdates()

        #CREATE PLAYER AND ADD TO PARTY
        #self.party.append(Player(self, 10, 10))
        self.party.append(CharacterSheet(self, 10, 10))
        self.createTilemap(self.current_zone.id)
        
        #DIALOG
        self.in_dialog = False
        #save values from COLLIDED NPC
        self.dialogindex = -1
        self.dialoglength = -1

        #initialize clickable MENU sprite list
        temp = 1
        while temp < NUMOFMENUITEMS:
            self.menuboxes.append(StaticSprite(self, 0, 0, 0, 0, INIT_LAYER))
            temp += 1

        temp = 1
        while temp < NUMOFMERCHANTSLOTS:
            self.merchantboxes.append(Item(self, 0, 0, BLANK))
            temp += 1        
        
    def showDialog(self, dialog):
        tempx = 1
        #ERASE SHOWING TEXT
        for sprite in self.text:
            sprite.kill()
        
        #IF DIALOG IS OVER, KILL SPRITES
        if dialog == "kill":
            self.in_dialog = False
        else:
            for x in dialog:
                TextSprite(self, tempx, 1, x)
                tempx += CHARACTER_SPACING #SPACING BETWEEN CHARACTERS

    def createTilemap(self, map):
        if map == FRANTIKSHUT:
            self.dialognpc.clear()
            self.items.clear()
            for i, row in enumerate(map):
                for j, column in enumerate(row):
                    StaticSprite(self, j, i, FRANTIKGROUNDX, FRANTIKGROUNDY, GROUND_LAYER)
                    if column == "B":
                        StaticSprite(self, j, i, FRANTIKWALLX, FRANTIKWALLY, BLOCK_LAYER)
                    if column == "Z":
                        StaticSprite(self, j, i, ZONELINEX, ZONELINEY, ZONE_LAYER)
                    if column == "C":
                        StaticSprite(self, j, i, FRANTIKBEDAX, FRANTIKBEDAY, BLOCK_LAYER)
                    if column == "D":
                        StaticSprite(self, j, i, FRANTIKBEDBX, FRANTIKBEDBY, BLOCK_LAYER)
                    if column == "R":
                        StaticSprite(self, j, i, KELETHINPOTX, KELETHINPOTY, BLOCK_LAYER)
                    if column == "O":
                        self.items.append(ItemBlock(self, j, i, KELETHINPOTX, KELETHINPOTY, POTION))
                    if column == "G":
                        self.items.append(ItemBlock(self, j, i, CHESTX, CHESTY,  SWORD))
                    if column == "N":
                        self.dialognpc.append(DialogNPC(self, j, i, NPCX, NPCY, DIALOGNPC_LAYER, QUESTNPC))
                    if column == "S":
                        self.dialognpc.append(DialogNPC(self, j, i, NPCX, NPCY, DIALOGNPC_LAYER, NEXTNPC))
                    if column == "P": 
                        self.party[self.top_character].x = j
                        self.party[self.top_character].y = i

        elif map == KELETHINMAIN:
            self.dialognpc.clear()
            for i, row in enumerate(map):
                for j, column in enumerate(row):
                    StaticSprite(self, j, i, FRANTIKGROUNDX, FRANTIKGROUNDY, GROUND_LAYER)
                    if column == "B":
                        StaticSprite(self, j, i, FRANTIKWALLX, FRANTIKWALLY, BLOCK_LAYER)
                    if column == "Z":
                        StaticSprite(self, j, i, ZONELINEX, ZONELINEY, ZONE_LAYER)
                    if column == "M":
                        StaticSprite(self, j, i, MERCHANTSTANDX, MERCHANTSTANDY, BLOCK_LAYER)
                    if column == "N":
                        StaticSprite(self, j, i, MERCHANTSTANDX + TILESIZE, MERCHANTSTANDY, BLOCK_LAYER)
                    if column == "G":
                        self.dialognpc.append(DialogNPC(self, j, i, MERCHANTAX, MERCHANTAY, DIALOGNPC_LAYER, MERCHANT))
                    if column == "E":
                        AnimatedSprite(self, j, i)
                    if column == "P":
                        self.party[self.top_character].x = j
                        self.party[self.top_character].y = i

        elif map == KELETHINBATTLE:
            #self.mobs.clear()
            for i, row in enumerate(map):
                for j, column in enumerate(row):                    
                    StaticSprite(self, j, i, BATTLEGROUNDX, BATTLEGROUNDY, GROUND_LAYER)
                    if column == "A":
                        StaticSprite(self, j, i, BATTLEWALLX, BATTLEWALLY, BLOCK_LAYER)
                    if column == "B":
                        StaticSprite(self, j, i, FRANTIKWALLX, FRANTIKWALLY, BLOCK_LAYER)
                    if column == "E": #create sprite and add to battle list
                        self.mobs.append(MobSheet(self, j, i))
                    if column == "P":
                        self.party[self.top_character].x = j
                        self.party[self.top_character].y = i
        
        elif map == MAINMENU:
            #empty the sprite groups
            self.all_sprites.empty()
            self.blocks.empty()
            self.enemies.empty()
            self.zonelines.empty()

            print ("Length is ", self.menuboxes.__len__())
            for i, row in enumerate(map):
                for j, column in enumerate(row):
                    StaticSprite(self, j, i, MAINMENUGROUNDX, MAINMENUGROUNDY, GROUND_LAYER)
                    if column == "A":
                        StaticSprite(self, j, i, MAINMENUWALLX, MAINMENUWALLY, BLOCK_LAYER)
                    ## THESE CLICKABLE SPRITES HAVE TO BE PUT INTO THE MAP IN A SPECIFIC ORDER FOR COLLISION
                    if column == "E":
                        self.menuboxes[EXIT] = StaticSprite(self, j, i, EXITBUTTONX, EXITBUTTONY, TEXT_LAYER)
                    if column == "G":
                        self.menuboxes[CHARACTER] = StaticSprite(self, j, i, CHARACTERBUTTONX, CHARACTERBUTTONY, TEXT_LAYER)
                    if column == "Q":
                        self.menuboxes[SPELLS] = StaticSprite(self, j, i, SPELLSBUTTONX, SPELLSBUTTONY, TEXT_LAYER)

        elif map == MERCHANTMENU:
            for i, row in enumerate(map):
                for j, column in enumerate(row):
                    StaticSprite(self, j+10, i, MAINMENUGROUNDX, MAINMENUGROUNDY, GROUND_LAYER)
                    if column == "A":
                        StaticSprite(self, j+10, i, MAINMENUWALLX, MAINMENUWALLY, BLOCK_LAYER)
                        #LOOK IN MERCHANT AND DISPLAY FOR SALE ITEMS

            #current merchant pulled from 'E' collision with DialogNPC
            merchantint = 0 #temp var
            while merchantint < self.dialognpc[self.current_merchant].itemsforsale.__len__():
                self.merchantboxes[merchantint] = (Item(self, 12, 1+merchantint, self.dialognpc[self.current_merchant].itemsforsale[merchantint]))
                #self.menuboxes.append(Item(self, 12, 1+merchantint, self.dialognpc[self.current_merchant].itemsforsale[merchantint]))
                merchantint += 1

        elif map == CHARACTERMENU:
            #empty the sprite groups
            self.all_sprites.empty()
            self.blocks.empty()
            self.text.empty()
            #self.menuboxes.clear()
            slidecounter = INVBOXA
            for i, row in enumerate(map):
                for j, column in enumerate(row):
                    StaticSprite(self, j, i, MAINMENUGROUNDX, MAINMENUGROUNDY, GROUND_LAYER)
                    if column == "A":
                        StaticSprite(self, j, i, MAINMENUWALLX, MAINMENUWALLY, BLOCK_LAYER)
                    ## THESE CLICKABLE SPRITES HAVE TO BE PUT INTO THE MAP EACH TIME BC CLEARING SPRITES
                    if column == "E":
                        self.menuboxes[EXIT] = StaticSprite(self, j, i, EXITBUTTONX, EXITBUTTONY, MENU_LAYER)
                    if column == "G":
                        self.menuboxes[CHARACTER] = StaticSprite(self, j, i, CHARACTERBUTTONX, CHARACTERBUTTONY, MENU_LAYER)
                    if column == "Q":
                        self.menuboxes[SPELLS] = StaticSprite(self, j, i, SPELLSBUTTONX, SPELLSBUTTONY, MENU_LAYER)
                    if column == "H":
                        self.menuboxes[HEAD] = StaticSprite(self, j, i, HEADSLOTX, HEADSLOTY, GEAR_LAYER)
                        #SHOWING ITEM IN THIS GEAR SLOT - SEEMS LIKE I'M REDRAWING TOO MUCH MAYBE ?
                        tempid = self.party[self.top_character].gear[HEAD].id
                        self.party[self.top_character].gear[HEAD] = Item(self, j, i, tempid)        
                    if column == "C":
                        self.menuboxes[CHEST] = StaticSprite(self, j, i, CHESTSLOTX, CHESTSLOTY, GEAR_LAYER)
                    if column == "R":
                        self.menuboxes[ARMS] = StaticSprite(self, j, i, ARMSSLOTX, ARMSSLOTY, GEAR_LAYER)
                    if column == "L":
                        self.menuboxes[LEGS] = StaticSprite(self, j, i, LEGSSLOTX, LEGSSLOTY, GEAR_LAYER)
                    if column == "F":
                        self.menuboxes[FEET] = StaticSprite(self, j, i, FEETSLOTX, FEETSLOTY, GEAR_LAYER)
                    if column == "P":
                        self.menuboxes[PRIMARY] = StaticSprite(self, j, i, PRIMARYSLOTX, PRIMARYSLOTY, GEAR_LAYER)
                    if column == "S":
                       self.menuboxes[SECONDARY] = StaticSprite(self, j, i, SECONDARYSLOTX, SECONDARYSLOTY, GEAR_LAYER)
                    if column == "U":
                        self.menuboxes[SHIFTLEFT] = StaticSprite(self, j, i, SHIFTLEFTX, SHIFTLEFTY, GEAR_LAYER)
                    if column == "Z":
                       self.menuboxes[SHIFTRIGHT] = StaticSprite(self, j, i, SHIFTRIGHTX, SHIFTRIGHTY, GEAR_LAYER)
                    if column == "V":
                        self.menuboxes[slidecounter] = StaticSprite(self, j, i, TILESIZE, 0, INVBAR_LAYER)
                        slidecounter += 1
                       #self.menuboxes[INVSLIDER] = StaticSprite(self, j, i, BLANKSLOTX, BLANKSLOTY, INVBAR_LAYER)
                    if column == "M":
                        StaticSprite(self, j, i, MAINMENUWALLX, MAINMENUWALLY, BLOCK_LAYER)
                    if column == "B":
                        StaticSprite(self, j, i, MAINMENUGROUNDX, MAINMENUGROUNDY, GROUND_LAYER)
            
            ## NOW DRAW ITEMS IN INVENTORY OVER THE [SLIDECOUNTER] SLOTS
            for i in range(self.party[self.top_character].inventory.__len__()):
                tempid = self.party[self.top_character].inventory[i].id
                if tempid > 0:
                    self.party[self.top_character].inventory[i] = Item(self, 4 + i, 16, tempid)
            #force draw new sprites
            #self.draw()
            #self.update()
            

#Roll a Natural 20 on the dice.
#Roll the dice again with all the exact same bonuses that were applied to the Natural 20 roll.
#If the attack roll from Step 2 is a hit, roll your damage twice and add the result of both rolls together.
#If the attack roll from Step 2 is a miss, you did not get a crit. However, because you rolled a Natural 20, you still successfully made a normal attack. Roll for damage!
#Congratulations!(!)
    def checkVitals(self, team):
        isAlive = False
        if team == PLAYERS:
            for i in range(self.party.__len__()):
                if self.party[i].hp >= 0:
                    isAlive = True
                    
                if not isAlive:
                    print("Your party has died!")
                    self.endBattle()

        if team == MOBS:
            for i in range(self.mobs.__len__()):
                if self.mobs[i].hp > 0:
                    isAlive = True
            
            if not isAlive:
                print ("The enemy is defeated!")
                self.endBattle()

            #deadcounter = 0
            #for i in range(self.mobs.__len__()):
                #if self.mobs[i].hp <=0:
                    #print ("enemy killed")
                    #self.mobs[i].kill() #kill sprite
                    #deadcounter += 1
                    #if self.mobs.__len__() < 1:
                        #print("You are victorious!")
                        #self.endBattle()
            #if deadcounter == self.mobs.__len__():
                #print("You are victorious!")
                #self.endBattle()
                
    def playerAttack(self, mob):
        print("Player attacking!")
        temproll = random.randint(1, 20)
        if temproll == 20:
            print ("Natural 20, critical chance!")
            if (temproll + self.party[0].atkbonus) > mob.ac:
                #random the damage die for the weapon
                temproll2 = random.randint(1,self.party[0].gear[PRIMARY].atk)
                #crit the damage
                temproll2 *= 2
                # show damage being done to mob
                print("Player does", temproll2 + self.party[0].atkbonus, "damage")
                mob.hp -=  temproll2 + self.party[0].atkbonus + self.party[0].strmod
        elif temproll == 1:
            print ("Natural 1, critical miss!")
            #miss the enemy
        else:
            print ("Rolled a ", temproll)
            if (temproll + self.party[0].atkbonus) > mob.ac:
                #random the damage die for the weapon
                temproll2 = random.randint(1,self.party[0].gear[PRIMARY].atk)
                # show damage being done to mob
                print("Player does", temproll2 + self.party[0].atkbonus, "damage")
                mob.hp -=  temproll2 + self.party[0].atkbonus + self.party[0].strmod

    def mobAttack(self, player):
        for i in range(self.mobs.__len__()):
            print ("Enemy ", i+1, "is attacking")
            temproll = random.randint(1, 20)
            if temproll == 20:
                print ("Enemy Natural 20, critical chance!")
            elif temproll == 1:
                print ("Enemy Natural 1, critical miss!")
            else:
                print ("Rolled a ", temproll)
                if (temproll + self.mobs[i].atkbonus) > player.ac:
                    #random the damage die for the weapon
                    temproll2 = random.randint(1,self.party[0].gear[PRIMARY].atk)
                    # show damage being done to mob
                    print("Enemy does", temproll2 + self.party[0].atkbonus, "damage")
                    player.hp -=  temproll2 + self.party[0].atkbonus + self.party[0].strmod
    
    def endBattle(self):
        #stop timers
        pygame.time.set_timer(self.party[0].playertimer, 0)       
        pygame.time.set_timer(self.mobtimer, 0)
        self.in_battle = False
        self.battle.empty()
        self.all_sprites.empty()
        self.mobs.clear()
        self.all_sprites.add(self.playersprite)
        self.current_zone.id = KELETHINMAIN
        self.createTilemap(self.current_zone.id)

    def startBattle(self):
        #show a "cursor" at starting mob
        #use keys to move cursor to mob to attack
        #only show & select sprites that aren't killed
        battlecursorx = self.mobs[0].x + 20
        battlecursory = self.mobs[0].y 
        self.menuboxes.append(StaticSprite(self, battlecursorx, battlecursory, POINTERX, POINTERY, GEAR_LAYER))
        #force draw new sprites
        self.draw()
        self.update()
        #flag in battle
        self.in_battle = True

        #set timers - use inits to offset
        pygame.time.set_timer(self.party[0].playertimer, 200)       
        #pygame.time.set_timer(self.mobtimer, 300)
        #from here timer events take over, until battle is over
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.inmenu:
                    i = 1
                    while i < self.menuboxes.__len__():
                        if self.menuboxes[i].rect.collidepoint(mouse_pos):
                            #if hitting the exit button
                            if i == EXIT:
                                self.inmenu = False
                                #empty the sprite groups
                                self.all_sprites.empty()
                                self.blocks.empty()
                                self.text.empty()
                                #remove images from menu clickables
                                temp = 1
                                while temp < NUMOFMENUITEMS:
                                    self.menuboxes.append(StaticSprite(self, 0, 0, 0, 0, INIT_LAYER))
                                    temp += 1
                                #self.menuboxes.clear()
                                #re-add player to all_sprites group
                                self.all_sprites.add(self.playersprite)
                                #go back to zone
                                self.current_zone.id = self.lastzone
                                self.createTilemap(self.current_zone.id)
                            elif i == CHARACTER:
                                self.createTilemap(CHARACTERMENU)
                            elif i == ARMS:
                                print("Picking Up - Arms")
                            elif i == HEAD:
                                if not self.oncursor:
                                    #IF THERE IS AN EQUIPPED ITEM, PICK IT UP
                                    print ("Picking Up - Head Slot")
                                    self.oncursor = True
                                    pygame.mouse.set_visible(False) 
                                    #get mouse pos for cursor sprite
                                    tempcoord = pygame.mouse.get_pos()
                                    #PUT ITEM FROM HEAD SLOT ON CURSOR
                                    self.menuboxes[CURSOR] = Item(self, tempcoord[0], tempcoord[1], self.party[self.top_character].gear[HEAD].id)
                                else:
                                    print("Dropping Into Head Slot")
                                    self.menuboxes[CURSOR].kill()
                                    self.menuboxes[CURSOR] = StaticSprite(self, 0, 0, 0, 0, GROUND_LAYER)
                                    pygame.mouse.set_visible(True)
                                    self.oncursor = False
                            elif i == INVBOXA:
                                if not self.oncursor: #TRY TO PICK UP FROM THAT SLOT
                                    print("Box Fresh !")
                                else:#TRY TO PUT SOMETHING HERE
                                    pass
                        i += 1
                elif self.inmerchant:
                    i = 0
                    while i < self.merchantboxes.__len__():
                        if self.merchantboxes[i].rect.collidepoint(mouse_pos):
                            if not self.oncursor:
                                if self.party[self.top_character].coin < self.merchantboxes[i].value:
                                    print ("You don't have enough money.")
                                else:
                                    print ("Picking Up Merchant Item")
                                    #TAKE COIN FOR THE PURCHASE
                                    self.party[self.top_character].coin -= self.merchantboxes[i].value
                                    self.oncursor = True
                                    pygame.mouse.set_visible(False) 
                                    #get mouse pos for cursor sprite
                                    tempcoord = pygame.mouse.get_pos()
                                    #PULL ITEM FROM INDEX WHERE YOU'RE CLICKING (UHHHH HOW ????) DO DISPLAY ITEM
                                    self.menuboxes[CURSOR] = Item(self, tempcoord[0], tempcoord[1], self.dialognpc[self.current_merchant].itemsforsale[i])
                            else:
                                print("Dropping Into Merchant")
                                self.menuboxes[CURSOR].kill()
                                #self.menuboxes[CURSOR] = StaticSprite(self, 0, 0, 0, 0, GROUND_LAYER)
                                pygame.mouse.set_visible(True)
                                self.oncursor = False
                        i += 1

            elif event.type == self.mobtimer:
                self.mobAttack(self.party[self.top_character])
                self.checkVitals(PLAYERS)

            elif event.type == self.party[0].playertimer:
                #set timer to 0 until player enters action
                pygame.time.set_timer(self.party[0].playertimer, 0)
                print ("Enter Player Input")
                #wait for player input, then do that to whichever mob is chosen
                #self.playerAttack(self.mobs[1])
                #self.checkVitals(MOBS)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

            elif event.type == pygame.KEYUP and self.in_battle:
                if event.key == pygame.K_g:
                    print ("g pressed - Attacking !")
                    self.playerAttack(self.mobs[0])
                    self.checkVitals(MOBS)
                    pygame.time.set_timer(self.party[0].playertimer, 200) 

                elif event.key == pygame.K_h:
                    print ("h pressed")
                    self.battle_input = 2

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e and not self.in_dialog:
                    #player is pressing action key so we look for item / npc and take appropriate action

                    #check through dialog NPCs and display text as necessary
                    tempint = 0
                    while tempint < self.dialognpc.__len__(): #go through each NPC in list
                        if pygame.sprite.collide_rect_ratio(1.1)(self.party[self.top_character], self.dialognpc[tempint]):
                            print("Hit NPC")
                            self.in_dialog = True #we are now in a dialog
                            #set temp info to pass along to if indialog
                            self.tempindex = 0
                            self.templength = self.dialognpc[tempint].dialoglength
                            self.tempdialog = self.dialognpc[tempint].dialog
                            self.showDialog(self.tempdialog[self.tempindex])
                            #IF THIS DIALOG IS A MERCHANT, ALSO DISPLAY WINDOW WITH ITEMS FOR SALE
                            if self.dialognpc[tempint].id == MERCHANT:
                                self.inmerchant = True
                                self.current_merchant = tempint #save index offset into dialog npc list
                                self.createTilemap(MERCHANTMENU)
                        tempint += 1

                    #check if the block has an item in it
                    tempint = 0
                    while tempint < self.items.__len__(): #go through each item spot in list
                        if pygame.sprite.collide_rect_ratio(1.05)(self.party[self.top_character], self.items[tempint]):
                            print("looking through items")
                            if self.items[tempint].hasitem: #put item into inventory
                                self.items[tempint].hasitem = False #item is removed
                                # FIND FIRST SPOT THAT HAS A 0 ID, THEN ADD TO THAT SPOT
                                for n in range (self.party[self.top_character].inventory.__len__()):
                                    if self.party[self.top_character].inventory[n].id == 0:
                                        self.party[self.top_character].inventory[n] = (Item(self, 0, 0, self.items[tempint].itemid))
                                        break
                                    
                                #display name of item at end of intentory (length - 1)
                                print("You picked up a ",self.party[self.top_character].inventory[self.party[self.top_character].inventory.__len__() - 1].name)
                        tempint += 1  

                elif event.key == pygame.K_e and self.in_dialog:
                    #when a player is in a dialog, continue on or exit
                    self.tempindex += 1 #increase to next index
                    print("Is", self.templength, ">", self.tempindex)
                    #if there's still dialog, keep displaying
                    if self.templength > self.tempindex:
                        print ("Next dialog")
                        #call the next line, and do so until over
                        self.showDialog(self.tempdialog[self.tempindex])
                
                    else:
                        print("End of dialog.")
                        #reset the index and length counter
                        self.tempindex = self.templength = -1
                        self.in_dialog = False
                        self.inmerchant = False
                        #input -1 into showDialog to end dialog mode
                        self.showDialog("kill")
                   
    def update(self):
        #if there's something on the cursor, update to the mouse position
        #must grab rect.center or will get tuple error
        if self.oncursor:
            self.menuboxes[CURSOR].rect.center = pygame.mouse.get_pos()
        self.all_sprites.update()
        

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #main game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def menu(self):       
        self.lastzone = self.current_zone.id
        #empty the sprite groups
        self.all_sprites.empty()
        self.blocks.empty()
        self.enemies.empty()
        self.zonelines.empty()

        self.createTilemap(MAINMENU)
        #force draw new sprites
        self.draw()
        self.update()

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        title = self.font.render('Awesome Game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Begin', 32)
        #create loop for intro screen, not into main loop yet
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
        
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
        
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

class Zone():
    name = ""
    description = ""
    id = 0 #zoneid for createTilemap
    maxx = 0 #max Player x location for zone
    maxy = 0 #max Player y location for zone
    

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()