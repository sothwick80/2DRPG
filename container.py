import pygame
from config import *
from sprites import *

class CharacterSheet(Player):
    def __init__(self, game, x, y):
        Player.__init__(self, game, x, y)
        self.name = self.description = ""
        self.jobclass = 0
        
        #default starting stats
        self.lvl = 1
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
        #inventory starts at 1, not 0 --- WHY??????
        self.inventory = [NUMOFINVENTORYSLOTS]
        self.gear = [NUMBEROFGEARSLOTS]

        #give a sword to pretend battle
        self.gear[PRIMARY] = Item(SWORD)

    #any time gear is equipped, unequipped, debuffs, buffs, etc
    def calculate_stats(self):
        pass
    
    #use a skill or ability
    def skill_ability(self):
        pass

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

        self.gear = [NUMBEROFGEARSLOTS]

        #give a sword to pretend battle
        self.gear[PRIMARY] = Item(SWORD)




#Body of the items in inventory
class Item():
    def __init__(self, itemid):
        self.name = "" #name of the item
        self.description = "" #description of item
        self.pic = 0
        self.equip = False #if equippable, if not put in inventory directly
        self.effect = 0 #if item has an effect
        self.atk = 0
        self.ac = 0
        self.value = 0
        
        if itemid == POTION:
            self.name = "Potion of Minor Relief" #name of the item
            self.description = "This potion heals a small boo boo" #description of item
            self.equip = False #if equippable, if not put in inventory directly
            self.effect = MINORRELIEF #if item has an effect
            #get a pic for the item as well, put it here - sprite sheet but does it have to be a whole sprite?
        elif itemid == SWORD:
            self.name = "Rusty Sword" #name of the item
            self.description = "Barely a sword." #description of item
            self.equip = True #if equippable, if not put in inventory directly
            self.atk = 4 #attack die associated

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
        self.hasdialog = False
        self.dialog = []
        self.dialogindex = -1 #for dialog IF statement
        self.dialoglength = -1 #how many dialogs there are

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
