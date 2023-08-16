# #WINDOW AND MAP DEFINES ##
WIN_WIDTH = 800
WIN_HEIGHT = 600

TILESIZE = 32
FPS = 60

GEAR_LAYER = 9
DIALOGNPC_LAYER = 8
TEXT_LAYER = 7
ZONE_LAYER = 6
PLAYER_LAYER = 5
NPC_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3
ENEMY_SPEED = 2

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

PLAYERS = 2
MOBS = 3

## DIALOG DEFINES ##
CHARACTER_SPACING = 0.4

## GEAR DEFINES ##
NUMOFMENUITEMS = 20 #MAKES 11 SPOTS, TOTAL AMOUNT OF CLICKABLE ITEMS IN MENU
NUMOFGEARSLOTS = 7
NUMOFINVENTORYSLOTS = 10
PRIMARY = 1
SECONDARY = 2
HEAD = 3
CHEST = 4
ARMS = 5
LEGS = 6
FEET = 7
## MENU SPRITES TO BE INDEXED AFTER EQUIPPABLE SLOTS
EXIT = 8
CHARACTER = 9
SPELLS = 10
SHIFTLEFT = 11
SHIFTRIGHT = 12
CURSOR = 13




## ITEM DEFINES ##
POTION = 1
SWORD = 2
SHIRT = 3
COIN = 4

## EFFECT DEFINES ##
MINORRELIEF = 1

QUESTNPC = 1
NEXTNPC = 2


KELETHINMAIN = [
'BBBBBBBBBBBBBBBBBBBBBBBBB',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.............E.........B',
'B.......................B',
'Z.P.....................B',
'Z.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B..................E....B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'B.......................B',
'BBBBBBBBBBBBBBBBBBBBBBBBB',
]

KELETHINMAINOFFSET = -8

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
MERCHANTAX = 96
MERCHANTAY = 0
MERCHANTBX = 192
MERCHANTBY = 0

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

MAINMENUWALLX = 512
MAINMENUWALLY = 0
MAINMENUGROUNDX = 480
MAINMENUGROUNDY = 64

#COORDS FOR CLICKALE MEU SPRITES
PRIMARYSLOTX = 0
PRIMARYSLOTY = SECONDARYSLOTY = HEADSLOTY = CHESTSLOTY = ARMSSLOTY = LEGSSLOTY = FEETSLOTY = SHIFTLEFTY = SHIFTRIGHTY = 120
BLANKSLOTY = POINTERY = 120
SECONDARYSLOTX = 41
HEADSLOTX = 82
CHESTSLOTX = 123
ARMSSLOTX = 164
LEGSSLOTX = 205
FEETSLOTX = 246
SHIFTLEFTX = 287
SHIFTRIGHTX = 328
BLANKSLOTX = 370
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