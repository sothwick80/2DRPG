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

        #list of dialog NPCs
        self.dialoglist = []

        #set battle timers
        self.playertimer = pygame.event.custom_type()
        self.mobtimer = pygame.event.custom_type()

        #sprite sheets
        self.character_spritesheet = BSpritesheet('img/character.png')        
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

        #drawing layers
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.playersprite = pygame.sprite.LayeredUpdates()
        self.blocks  = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.zonelines = pygame.sprite.LayeredUpdates()
        self.battle = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        self.dialognpc = pygame.sprite.LayeredUpdates()
        self.text = pygame.sprite.LayeredUpdates()
        self.items = pygame.sprite.LayeredUpdates()

        #CREATE PLAYER AND ADD TO PARTY
        #self.party.append(Player(self, 10, 10))
        self.party.append(CharacterInfo(self, 10, 10))
        self.createTilemap(self.current_zone.id)

        #DIALOG
        self.in_dialog = False
        #save values from hit NPC
        self.dialogindex = -1
        self.dialoglength = -1
        #new game, show first dialogs

    def showDialog(self, dialog):
        tempx = 1
        #get rid of any previous text
        for sprite in self.text:
            sprite.kill()
        
        if dialog == "kill": #if dialog is over
            self.in_dialog = False
        else:
            for x in dialog:
                TextSprite(self, tempx, 1, x)
                tempx += CHARACTER_SPACING #SPACING BETWEEN CHARACTERS

    def createTilemap(self, map):
        if map == FRANTIKSHUT:
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
                        Item(self, j, i, KELETHINPOTX, KELETHINPOTY, POTION)
                    if column == "G":
                        Item(self, j, i, CHESTX, CHESTY,  SWORD)
                    if column == "N":
                        self.dialoglist.append(DialogNPC(self, j, i, NPCX, NPCY, DIALOGNPC_LAYER, QUESTNPC))
                    if column == "S":
                        self.dialoglist.append(DialogNPC(self, j, i, NPCX, NPCY, DIALOGNPC_LAYER, NEXTNPC))
                    #if column == "E":
                        #AnimatedSprite(self, j, i)
                    if column == "P": 
                        self.party[self.top_character].x = j
                        self.party[self.top_character].y = i

        if map == KELETHINMAIN:
            for i, row in enumerate(map):
                for j, column in enumerate(row):
                    StaticSprite(self, j, i+KELETHINMAINOFFSET, FRANTIKGROUNDX, FRANTIKGROUNDY, GROUND_LAYER)
                    if column == "B":
                        StaticSprite(self, j, i+KELETHINMAINOFFSET, FRANTIKWALLX, FRANTIKWALLY, BLOCK_LAYER)
                    if column == "Z":
                        StaticSprite(self, j, i+KELETHINMAINOFFSET, ZONELINEX, ZONELINEY, ZONE_LAYER)
                    if column == "C":
                        StaticSprite(self, j, i+KELETHINMAINOFFSET, FRANTIKBEDAX, FRANTIKBEDAY, BLOCK_LAYER)
                    if column == "D":
                        StaticSprite(self, j, i+KELETHINMAINOFFSET, FRANTIKBEDBX, FRANTIKBEDBY, BLOCK_LAYER)
                    if column == "R":
                        StaticSprite(self, j, i+KELETHINMAINOFFSET, KELETHINPOTX, KELETHINPOTY, BLOCK_LAYER)
                    if column == "E":
                        AnimatedSprite(self, j, i+KELETHINMAINOFFSET)
                    if column == "P":
                        self.party[self.top_character].x = j
                        self.party[self.top_character].y = i+KELETHINMAINOFFSET

        if map == KELETHINBATTLE:
            self.mobs.clear()
            for i, row in enumerate(map):
                for j, column in enumerate(row):                    
                    StaticSprite(self, j, i, BATTLEGROUNDX, BATTLEGROUNDY, GROUND_LAYER)
                    if column == "A":
                        StaticSprite(self, j, i, BATTLEWALLX, BATTLEWALLY, BLOCK_LAYER)
                    if column == "B":
                        StaticSprite(self, j, i, BATTLEWALLX + TILESIZE, BATTLEWALLY, BLOCK_LAYER)
                    if column == "C":
                        StaticSprite(self, j, i, BATTLEWALLX, BATTLEWALLY + TILESIZE, BLOCK_LAYER)
                    if column == "D":
                        StaticSprite(self, j, i, BATTLEWALLX + TILESIZE, BATTLEWALLY + TILESIZE, BLOCK_LAYER)
                    if column == "M":
                        StaticSprite(self, j, i, BATTLEMENUWALLX, BATTLEMENUWALLY, BLOCK_LAYER)
                    if column == ",":
                        StaticSprite(self, j, i, BATTLEMENUBACKX, BATTLEMENUWALLY, BLOCK_LAYER)
                    if column == "E": #create sprite and add to battle list
                        self.mobs.append(BattleMob(self, j, i))
                    if column == "P":
                        self.party[self.top_character].x = j
                        self.party[self.top_character].y = i

    #mytimer = pygame.event.custom_type()
    #pygame.time.set_timer(mytimer, 400)

    #while True:
    #    for event in pygame.event.get():
    #       if event.type == mytimer:
                # Do Something
    def checkVitals(self, team):
        
        if team == PLAYERS:
            isAlive = False
            for i in range(self.party.__len__()):
                if self.party[i].hp >= 0:
                    isAlive = True
                    
                if not isAlive:
                    print("Your party has died!")
                    self.endBattle()

        if team == MOBS:
            deadcounter = 0
            for i in range(self.mobs.__len__()):
                if self.mobs[i].hp <=0:
                    deadcounter += 1
            if deadcounter == self.mobs.__len__():
                print("You are victorious!")
                self.endBattle()

    def playerAttack(self, mob):
        print("Player attacking!")
        mob.hp -= 1

    def mobAttack(self, player):
        for i in range(self.mobs.__len__()):
            print ("Enemy ", i+1, "is attacking")
            #each mob does 1 damage to player
            player.hp -= 1
    
    def endBattle(self):
        #stop timers
        pygame.time.set_timer(self.playertimer, 0)       
        pygame.time.set_timer(self.mobtimer, 0)
        self.in_battle = False
        self.battle.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.playersprite)
        self.current_zone.id = KELETHINMAIN
        self.createTilemap(self.current_zone.id)

    def startBattle(self):
        #force draw new sprites
        self.draw()
        self.update()
        #flag in battle
        self.in_battle = True

        #start up player timer
        #pygame.time.set_timer(self.playertimer, 400)
        
        #set timers - use inits to offset
        pygame.time.set_timer(self.playertimer, 350)       
        pygame.time.set_timer(self.mobtimer, 300)

        #from here timer events take over, until battle is over
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            elif event.type == self.mobtimer:
                self.mobAttack(self.party[self.top_character])
                self.checkVitals(PLAYERS)

            elif event.type == self.playertimer:
                #wait for player input, then do that to whichever mob is chosen
                self.playerAttack(self.mobs[1])
                self.checkVitals(MOBS)
            
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
                    self.battle_input = 1
                elif event.key == pygame.K_h:
                    self.battle_input = 2

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e and not self.in_dialog:
                    #check if NPC has dialog
                    for sprite in self.dialoglist:                        
                        hits = pygame.sprite.spritecollide(self.party[self.top_character], self.dialoglist, False, pygame.sprite.collide_rect_ratio(2.0))

                    #if collide AND there's dialog
                        if hits:
                            print("Hit NPC")
                            self.in_dialog = True
                            #grab sprite info, can't grab on next dialog
                            self.tempindex = 0
                            self.templength = sprite.dialoglength
                            self.tempdialog = sprite.dialog
                            self.showDialog(self.tempdialog[self.tempindex])
                            hits = False
                        else:
                            print("No Hit on NPC")
                    #check if the block has an item in it
                    for sprite in self.items:
                        hits = pygame.sprite.spritecollide(self.party[self.top_character], self.items, False, pygame.sprite.collide_rect_ratio(2.0))    
                        if hits:
                            print("looking through items")
                            if sprite.hasitem: #put item into inventory
                                self.party[self.top_character].inventory.append(sprite)
                                sprite.hasitem = False #item is removed
                                #display name of item at end of intentory (length - 1)
                                print("You picked up a ",self.party[self.top_character].inventory[self.party[self.top_character].inventory.__len__() - 1].name)
                            break    

                elif event.key == pygame.K_e and self.in_dialog:
                    self.tempindex += 1 #increase to next index
                    print("Is", self.templength, ">", self.tempindex)
                    if self.templength > self.tempindex:
                        print ("Next dialog")
                        #call the next line, and do so until over
                        self.showDialog(self.tempdialog[self.tempindex])
                
                    else:
                        print("End of dialog.")
                        #reset the index and length counter
                        self.tempindex = self.templength = -1
                        self.in_dialog = False
                        #input -1 into showDialog to end dialog mode
                        self.showDialog("kill")
                   
    def update(self):
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

    def charactersheet(self):
        self.inmenu = True
        exit_button = Button(20, 25, 90, 30, WHITE, BLACK, 'Back', 32)
        character_button = Button(130, 25, 180, 30, WHITE, BLACK, 'Character', 32)
        inventory_button = Button(320, 25, 180, 30, WHITE, BLACK, 'Inventory', 32)
        quest_button = Button(520, 25, 150, 30, WHITE, BLACK, 'Quests', 32)


        while self.inmenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False #quits to another screen
                    self.inmenu = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if exit_button.is_pressed(mouse_pos, mouse_pressed):    
                self.inmenu = False

            self.screen.blit(self.menu_background, (0, 0))
            self.screen.blit(exit_button.image, exit_button.rect)
            self.screen.blit(character_button.image, character_button.rect)
            self.screen.blit(inventory_button.image, inventory_button.rect)
            self.screen.blit(quest_button.image, quest_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

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