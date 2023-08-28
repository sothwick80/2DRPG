# #WINDOW AND MAP DEFINES ##
WIN_WIDTH = 800
WIN_HEIGHT = 600

TILESIZE = 32
FPS = 60

#UNIQUE SIZE FOR THE INVENTORY BAR UNTIL I CAN FIGURE OUT HOW TO WITH SPRITES

DIALOGNPC_LAYER = 11
TEXT_LAYER = 10
GEAR_LAYER = 9
INVBAR_LAYER = 8
MENU_LAYER = 7
ZONE_LAYER = 6
PLAYER_LAYER = 5
NPC_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1
INIT_LAYER = 0

PLAYER_SPEED = 3
ENEMY_SPEED = 2

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

PLAYERS = 2
MOBS = 3

TEXTWIDTH = 100
TEXTHEIGHT = 85

## DIALOG DEFINES ##
CHARACTER_SPACING = 0.4

## GEAR DEFINES ##
NUMOFMENUITEMS = 20 #TOTAL AMOUNT OF CLICKABLE ITEMS IN MENU
NUMOFGEARSLOTS = 7
NUMOFINVENTORYSLOTS = 25
NUMOFMERCHANTSLOTS = 4
PRIMARY = 1
SECONDARY = 2
HEAD = 3
CHEST = 4
ARMS = 5
LEGS = 6
FEET = 7
## MENU SPRITES TO BE INDEXED AFTER EQUIPPABLE SLOTS
## VERY IFFY - NEED TO BE LOADED IN THE CORRECT ORDER
EXIT = 8
CHARACTER = 9
SPELLS = 10
SHIFTLEFT = 11
SHIFTRIGHT = 12
CURSOR = 13
INVBOXA = 14
INVBOXB = 15
INVBOXC = 16
INVBOXD = 17


MERCHANTONE = 14
MERCHANTTWO = 15
MERCHANTTHREE = 16




## ITEM DEFINES ##
BLANK = 0
POTION = 1
SWORD = 2
SHIRT = 3
COIN = 4
INVENTORY = 5

POTIONX = 128
POTIONY = 160
SWORDX = 768
SWORDY = 320
SHIRTX = 416
SHIRTY = 288

## EFFECT DEFINES ##
MINORRELIEF = 1

QUESTNPC = 1
NEXTNPC = 2
MERCHANT = 3

MERCHANTAX = 96
MERCHANTAY = 0
MERCHANTBX = 192
MERCHANTBY = 0


KELETHINMAIN = [
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'B.................................B',
'B......MN.........................B',
'B......G..........................B',
'B.................................B',
'B.................................B',
'B.................................B',
'B.................................B',
'B.................................B',
'B.................................B',
'Z.P...............................B',
'Z.................................B',
'B...............E.................B',
'B.................................B',
'B.................................B',
'B.................................B',
'B.................................B',
'B.................................B',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]
KELETHINMAINOFFSET = -8

MERCHANTSTANDX = 768
MERCHANTSTANDY = 1728


FRANTIKSHUT = [
'BBBBBBBBBBBBBBBBBBBBBBBBB',
'B.......................B',
'B.......................B',
'B...RRORR..........S....B',
'B...R...R...G...........B',
'B...R...R...............B',
'B.......................B',
'B.......................Z',
'B......................NZ',
'B...........RRR.........B',
'B.............R.........B',
'B.............R.........B',
'B...........RRR.........B',
'B.......................B',
'B...P..C................B',
'B......D................B',
'B.......................B',
'B.......................B',
'BBBBBBBBBBBBBBBBBBBBBBBBB',
]

NPCX = 0
NPCY = 0

CHESTX = 224
CHESTY = 0

ENEMYX = 3
ENEMYY = 2

#JUST HALF SCREEN SIZE FOR NOW, CALCULATE LATER ON
FRANTIKSHUTMAXX = 400
FRANTIKSHUTMAXY = 300

## FRANTIK'S HUT AND KELETHIN SPRITES ##

FRANTIKBEDAX = 608
FRANTIKBEDAY = 1408
FRANTIKBEDBX = 608
FRANTIKBEDBY = 1440
FRANTIKGROUNDX = 0
FRANTIKGROUNDY = 128
FRANTIKWALLX = 0
FRANTIKWALLY = 160
KELETHINPOTX = 160
KELETHINPOTY = 992
ZONELINEX = 192
ZONELINEY = 960

KELETHINBATTLE = [
'AAAAAAAAAAAAAAAAAAAAAAAAA',
'A.......................A',
'A.......................A',
'A.......................A',
'A.................P.....A',
'A.......................A',
'A.......................A',
'A...E...................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'BBBBBBBBBBBBBBBBBBBBBBBBB',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'BBBBBBBBBBBBBBBBBBBBBBBBB',
]

BATTLEGROUNDX = 544
BATTLEGROUNDY = 320
#BATTLE WALL IS 4 TILES (2X2), THESE ARE TOP LEFT COORDS
BATTLEWALLX = 512
BATTLEWALLY = 352
BATTLEMENUWALLX = 832
BATTLEMENUWALLY = 0
BATTLEMENUBACKX = 192
BATTLEMENUBACKY = 128

'''
CHARACTERMENU = [
'AAAAAAAAAAAAAAAAAAAAAAAAA',
'AE...G...Q..............A',
'A.......................A',
'A.......................A',
'A..........H............A',
'A.......................A',
'A.......C.....R.........A',
'A.......................A',
'A....L...........F......A',
'A.......................A',
'A.......P.....S.........A',
'A.......................A',
'A.......................A',
'A.......................A',
'AAAAAAAAAAAAAAAAAAAAAAAAA',
'A.......................A',
'A.ZV.V.V..............U.A',
'A.......................A',
'AAAAAAAAAAAAAAAAAAAAAAAAA',
]
'''

CHARACTERMENU = [
'AAAAAAAAAAAAAAAAAAAAAAAAA',
'A.E...Q.................A',
'A................H......A',
'A.......................A',
'A...MMMMM......C....R...A',
'A...MBBBM...............A',
'A...MBBBM......L....F...A',
'A...MBBBM...............A',
'A...MBBBM......P....S...A',
'A...MBBBM...............A',
'A...MMMMM...............A',
'A.......................A',
'A.......................A',
'A.......................A',
'AAAAAAAAAAAAAAAAAAAAAAAAA',
'A.......................A',
'A.Z.VVVV.........U......A',
'A.......................A',
'AAAAAAAAAAAAAAAAAAAAAAAAA',
]

MAINMENUWALLX = 512
MAINMENUWALLY = 0
MAINMENUGROUNDX = 480
MAINMENUGROUNDY = 64

#COORDS FOR CLICKALE MEU SPRITES
PRIMARYSLOTX = 0
PRIMARYSLOTY = SECONDARYSLOTY = HEADSLOTY = CHESTSLOTY = ARMSSLOTY = LEGSSLOTY = FEETSLOTY = SHIFTLEFTY = SHIFTRIGHTY = 120
POINTERY = 120
SECONDARYSLOTX = 41
HEADSLOTX = 82
CHESTSLOTX = 123
ARMSSLOTX = 164
LEGSSLOTX = 205
FEETSLOTX = 246
SHIFTLEFTX = 287
SHIFTRIGHTX = 328
BLANKSLOTX = 0
BLANKSLOTY = 166
POINTERX = 411
EXITBUTTONX = 0
EXITBUTTONY = 32
CHARACTERBUTTONX = 101
CHARACTERBUTTONY = 32
SPELLSBUTTONX = 199
SPELLSBUTTONY = 32

MAINMENU = [
'AAAAAAAAAAAAAAAAAAAAAAAAA',
'AE...G...Q..............A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'A.......................A',
'AAAAAAAAAAAAAAAAAAAAAAAAA',
]

#SHOULD SHOW CHARACTER SCREEN AS WELL
MERCHANTMENU = [
'AAAAA',
'A...A',
'A...A',
'A...A',
'A...A',
'AAAAA',
]