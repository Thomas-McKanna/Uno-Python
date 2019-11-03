import pygame
from pkg_resources import resource_filename
assets_path = resource_filename('animation', 'assets')
LOGO = pygame.image.load(assets_path + '/Logo.png')
DASH = pygame.image.load(assets_path + '/Dashed_Border.png')
DECK = pygame.image.load(assets_path + '/Deck.png')
BDECK = pygame.image.load(assets_path + '/Bordered_Deck.png')
BLANK = pygame.image.load(assets_path + '/Blank.png')
FELT = pygame.image.load(assets_path + '/Green_Felt.jpg')
INSTRUCTIONS_LEFT = pygame.image.load(assets_path + '/instructions_left.png')
INSTRUCTIONS_RIGHT = pygame.image.load(assets_path + '/instructions_right.png')

CS_PROFS = [
    pygame.image.load(assets_path + '/gosnell.png'),
    pygame.image.load(assets_path + '/markowsky.png'),
    pygame.image.load(assets_path + '/mcmillin.png'),
    pygame.image.load(assets_path + '/morales.png'),
    pygame.image.load(assets_path + '/price.png'),
    pygame.image.load(assets_path + '/sabharwal.png')
]

# Used for choosing wildcard color
WILDWHEEL = {
    'BLUE': pygame.image.load(assets_path + '/Wildwheel_Blue.png'),
    'RED':  pygame.image.load(assets_path + '/Wildwheel_Red.png'),
    'YELLOW': pygame.image.load(assets_path + '/Wildwheel_Yellow.png'),
    'GREEN': pygame.image.load(assets_path + '/Wildwheel_Green.png')
}

WILDMORPH = {
    'BLUE_WILD': pygame.image.load(assets_path + '/Blue_Wild.png'),
    'RED_WILD': pygame.image.load(assets_path + '/Red_Wild.png'),
    'GREEN_WILD': pygame.image.load(assets_path + '/Green_Wild.png'),
    'YELLOW_WILD': pygame.image.load(assets_path + '/Yellow_Wild.png'),
}

CARDS = {
    # Blue Cards
    'BLUE_0': pygame.image.load(assets_path + '/Blue_0.png'),
    'BLUE_1': pygame.image.load(assets_path + '/Blue_1.png'),
    'BLUE_2': pygame.image.load(assets_path + '/Blue_2.png'),
    'BLUE_3': pygame.image.load(assets_path + '/Blue_3.png'),
    'BLUE_4': pygame.image.load(assets_path + '/Blue_4.png'),
    'BLUE_5': pygame.image.load(assets_path + '/Blue_5.png'),
    'BLUE_6': pygame.image.load(assets_path + '/Blue_6.png'),
    'BLUE_7': pygame.image.load(assets_path + '/Blue_7.png'),
    'BLUE_8': pygame.image.load(assets_path + '/Blue_8.png'),
    'BLUE_9': pygame.image.load(assets_path + '/Blue_9.png'),
    'BLUE_DRAW': pygame.image.load(assets_path + '/Blue_Draw.png'),
    'BLUE_REVERSE': pygame.image.load(assets_path + '/Blue_Reverse.png'),
    'BLUE_SKIP': pygame.image.load(assets_path + '/Blue_Skip.png'),
    # Green Cards
    'GREEN_0': pygame.image.load(assets_path + '/Green_0.png'),
    'GREEN_1': pygame.image.load(assets_path + '/Green_1.png'),
    'GREEN_2': pygame.image.load(assets_path + '/Green_2.png'),
    'GREEN_3': pygame.image.load(assets_path + '/Green_3.png'),
    'GREEN_4': pygame.image.load(assets_path + '/Green_4.png'),
    'GREEN_5': pygame.image.load(assets_path + '/Green_5.png'),
    'GREEN_6': pygame.image.load(assets_path + '/Green_6.png'),
    'GREEN_7': pygame.image.load(assets_path + '/Green_7.png'),
    'GREEN_8': pygame.image.load(assets_path + '/Green_8.png'),
    'GREEN_9': pygame.image.load(assets_path + '/Green_9.png'),
    'GREEN_DRAW': pygame.image.load(assets_path + '/Green_Draw.png'),
    'GREEN_REVERSE': pygame.image.load(assets_path + '/Green_Reverse.png'),
    'GREEN_SKIP': pygame.image.load(assets_path + '/Green_Skip.png'),
    # Red Cards
    'RED_0': pygame.image.load(assets_path + '/Red_0.png'),
    'RED_1': pygame.image.load(assets_path + '/Red_1.png'),
    'RED_2': pygame.image.load(assets_path + '/Red_2.png'),
    'RED_3': pygame.image.load(assets_path + '/Red_3.png'),
    'RED_4': pygame.image.load(assets_path + '/Red_4.png'),
    'RED_5': pygame.image.load(assets_path + '/Red_5.png'),
    'RED_6': pygame.image.load(assets_path + '/Red_6.png'),
    'RED_7': pygame.image.load(assets_path + '/Red_7.png'),
    'RED_8': pygame.image.load(assets_path + '/Red_8.png'),
    'RED_9': pygame.image.load(assets_path + '/Red_9.png'),
    'RED_DRAW': pygame.image.load(assets_path + '/Red_Draw.png'),
    'RED_REVERSE': pygame.image.load(assets_path + '/Red_Reverse.png'),
    'RED_SKIP': pygame.image.load(assets_path + '/Red_Skip.png'),
    # Yellow Cards
    'YELLOW_0': pygame.image.load(assets_path + '/Yellow_0.png'),
    'YELLOW_1': pygame.image.load(assets_path + '/Yellow_1.png'),
    'YELLOW_2': pygame.image.load(assets_path + '/Yellow_2.png'),
    'YELLOW_3': pygame.image.load(assets_path + '/Yellow_3.png'),
    'YELLOW_4': pygame.image.load(assets_path + '/Yellow_4.png'),
    'YELLOW_5': pygame.image.load(assets_path + '/Yellow_5.png'),
    'YELLOW_6': pygame.image.load(assets_path + '/Yellow_6.png'),
    'YELLOW_7': pygame.image.load(assets_path + '/Yellow_7.png'),
    'YELLOW_8': pygame.image.load(assets_path + '/Yellow_8.png'),
    'YELLOW_9': pygame.image.load(assets_path + '/Yellow_9.png'),
    'YELLOW_DRAW': pygame.image.load(assets_path + '/Yellow_Draw.png'),
    'YELLOW_REVERSE': pygame.image.load(assets_path + '/Yellow_Reverse.png'),
    'YELLOW_SKIP': pygame.image.load(assets_path + '/Yellow_Skip.png'),
    # Other Cards
    'WILD_WILD': pygame.image.load(assets_path + '/Wild.png'),
    'WILD_WILD_DRAW': pygame.image.load(assets_path + '/Wild_Draw.png')
}
