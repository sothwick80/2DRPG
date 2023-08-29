import pygame
from config import *
from sprites import *

#PUTS A CHARACTERSHEET OVERLAY ONTO THE PLAYER CLASS ALLOWING D&D STYLE ADVENTURES
class CharacterSheet(Player):
    def __init__(self, game, x, y):
        Player.__init__(self, game, x, y)
        self.game = game
        self.name = self.description = ""
        self.jobclass = 0
        
        #default starting stats
        self.lvl = 1
        self.exp = 0
        #str governs attack damage, weight limit
        self.str = self.strmod = 0
        #vitality governs hit points, hit points regen & constitution saves
        self.vit = self.vitmod = 0
        #dexterity governs chance to hit & reflex saves
        self.dex = self.dexmod = 0
        #intelligence governs lore, search, spell power & mind saves
        self.int = self.intmod = 0
        #spirit governs mana points, mana regen
        self.spr = self.sprmod = 0
        self.atkbonus = 0
        self.hp = self.mp = self.init = 0
        self.ac = 10 + self.dexmod #+ gear
        
        self.coin = 10
        self.inventory = []
        #self.gear = []
        self.playertimer = pygame.event.custom_type()

        #INITIALIZE LISTS inventory starts at 1
        self.temp = 1
        while self.temp < NUMOFINVENTORYSLOTS:
            self.inventory.append(Item(self.game, 0, 0, BLANK))
            self.temp += 1

        #give a sword to pretend battle
        #self.gear[PRIMARY] = Item(self.game, 10, 10, SWORD)
        self.inventory[PRIMARY] = Item(self.game, 10, 10, SWORD)
        self.inventory[HEAD] = Item(self.game, 10, 10, SHIRT)

        ##  BUT THEN HOW DO I DRAW LATER, RE- ADD??
        for sprite in self.game.item_sprites:
            sprite.kill()
        
    #any time gear is equipped, unequipped, debuffs, buffs, etc
    def calculate_stats(self):
        self.str = self.inventory[HEAD].str + self.inventory[ARMS].str + self.inventory[CHEST].str + self.inventory[LEGS].str + self.inventory[FEET].str + self.inventory[PRIMARY].str + self.inventory[SECONDARY].str
        self.strmod = self.str // 5 #str mod 5 for str modifier

        self.vit = self.inventory[HEAD].vit + self.inventory[ARMS].vit + self.inventory[CHEST].vit + self.inventory[LEGS].vit + self.inventory[FEET].vit + self.inventory[PRIMARY].vit + self.inventory[SECONDARY].vit
        self.vitmod = self.vit // 5 #str mod 5 for str modifier

        self.dex = self.inventory[HEAD].dex + self.inventory[ARMS].dex + self.inventory[CHEST].dex + self.inventory[LEGS].dex + self.inventory[FEET].dex + self.inventory[PRIMARY].dex + self.inventory[SECONDARY].dex
        self.dexmod = self.dex // 5 #str mod 5 for str modifier

        self.int = self.inventory[HEAD].int + self.inventory[ARMS].int + self.inventory[CHEST].int + self.inventory[LEGS].int + self.inventory[FEET].int + self.inventory[PRIMARY].int + self.inventory[SECONDARY].int
        self.intmod = self.int // 5 #str mod 5 for str modifier

        self.spr = self.inventory[HEAD].spr + self.inventory[ARMS].spr + self.inventory[CHEST].spr + self.inventory[LEGS].spr + self.inventory[FEET].spr + self.inventory[PRIMARY].spr + self.inventory[SECONDARY].spr
        self.sprmod = self.spr // 5 #str mod 5 for str modifier

        self.hp = 10 + self.vitmod + (5 * self.lvl)
        #calculate level
        
    
    #use a skill or ability
    def skill_ability(self):
        pass

    def display_stats(self):
        self.game.showDialog(10, 2, "HP: ")
        self.game.showDialog(12, 2, str(self.hp))
        self.game.showDialog(10, 3, "Str: ")
        self.game.showDialog(12, 3, str(self.str))
        self.game.showDialog(10, 4, "Vit: ")
        self.game.showDialog(12, 4, str(self.vit))
        self.game.showDialog(10, 5, "Dex: ")
        self.game.showDialog(12, 5, str(self.dex))
        self.game.showDialog(10, 6, "Int: ")
        self.game.showDialog(12, 6, str(self.int))
        self.game.showDialog(10, 7, "Spr: ")
        self.game.showDialog(12, 7, str(self.spr))
        
        

class MobSheet(Enemy):
    def __init__(self, game, x, y):
        Enemy.__init__(self, game, x, y)
        
        self.lvl = 1

        self.str = 5
        self.strmod = 0
        self.vit = 5
        self.vitmod = 0
        self.dex = 5
        self.dexmod = 0
        self.int = 5
        self.intmod = 0
        self.spr = 5
        self.sprmod = 0

        self.hp = 10
        self.ac = 10 + self.dexmod #+ gear ac
        self.mp = 10
        self.init = 0

        self.atkbonus = 0

        #inventory starts at 1, not 0 --- WHY??????
        self.inventory = [1] #mob drops an item
        self.coin = random.randint(1, 10) #mob has 1-10 gold
        self.gear = []

        self.temp = 1
        while self.temp < NUMOFGEARSLOTS:
            self.gear.append(Item(self.game, 0, 0, BLANK))
            self.temp += 1

        #give a sword to pretend battle
        #self.gear[PRIMARY] = Item(self.game, 0, 0, SWORD)


#an interactible, impassible block that holds the ID of an item which is then created in the inventory
class ItemBlock(StaticSprite):
    def __init__(self, game, x, y, pixx, pixy, index):
        StaticSprite.__init__(self, game, x, y, pixx, pixy, BLOCK_LAYER)
        #this block has an item!
        self.hasitem = True
        #item reference to plug into Item() to return an item to player
        self.itemid = index

class DialogNPC(StaticSprite):
    def __init__(self, game, x, y, pixx, pixy, layer, index):
        StaticSprite.__init__(self, game, x, y, pixx, pixy, layer)
        
        self.id = index
        self.hasdialog = False
        self.dialog = []
        self.dialogindex = -1 #for dialog IF statement
        self.dialoglength = -1 #how many dialogs there are

        #list of item IDs to be sold
        self.itemsforsale = []

        if index == QUESTNPC:
            self.hasdialog = True
            #set universal dialog indices
            self.dialogindex = 0
            self.dialoglength = 2
            self.dialog.append("Your uncle is waiting outside")
            self.dialog.append("Grab your sword and tunic and go help him")
        
        elif index == NEXTNPC:
            self.hasdialog = False
            #set universal dialog indices
            self.dialogindex = 0
            self.dialoglength = 1
            self.dialog.append("Can you even read this, brah?")

        elif index == MERCHANT:
            self.hasdialog = True
            self.dialogindex = 0
            self.dialoglength = 1
            self.dialog.append("Welcome to my Shop")
            self.itemsforsale = [SWORD, SHIRT, POTION]
            #build inventory & set pricing
            #self.itemsforsale.append(Item(self.game, 10, 10, SWORD))
            #self.itemsforsale.append(Item(self.game, 12, 10, SHIRT))
            #show interactable blocks that remove gold as per items value