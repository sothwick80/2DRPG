import pygame
from config import *
from sprites import *

class CharacterInfo(Player):
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

        self.hp = self.mp = self.init = 0

        #inventory starts at 1, not 0 --- WHY??????
        self.inventory = []
        self.gear = [NUMBEROFGEARSLOTS]

    #any time gear is equipped, unequipped, debuffs, buffs, etc
    def calculate_stats(self):
        pass
    
    #use a skill or ability
    def skill_ability(self):
        pass

    def get_attack(self):
        pass

    def get_defend(self):
        pass

class Item(ItemBlockSprite):
    def __init__(self, game, x, y, pixx, pixy, index):
        ItemBlockSprite.__init__(self, game, x, y, pixx, pixy)
        #this block has an item!
        self.hasitem = True
        self.itemid = index
        self.name = "" #name of the item
        self.description = "" #description of item
        self.equip = False #if equippable, if not put in inventory directly
        self.effect = 0 #if item has an effect
        
        if self.itemid == POTION:
            self.name = "Potion of Minor Relief" #name of the item
            self.description = "This potion heals a small boo boo" #description of item
            self.equip = False #if equippable, if not put in inventory directly
            self.effect = MINORRELIEF #if item has an effect
        elif self.itemid == SWORD:
            self.name = "Rusty Sword" #name of the item
            self.description = "Barely a sword." #description of item
            self.equip = True #if equippable, if not put in inventory directly
            self.effect = 0

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
