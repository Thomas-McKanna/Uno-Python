import pygame

LOGO = pygame.image.load('assets/uno_logo.png')
DASH = pygame.image.load('assets/Dashed_Border.png')
DECK = pygame.image.load('assets/Deck.png')

CARD_IMAGE_DICT = {
    # Blue Cards
    'BLUE_0': pygame.image.load('assets/Blue_0.png'),
    'BLUE_1': pygame.image.load('assets/Blue_1.png'),
    'BLUE_2': pygame.image.load('assets/Blue_2.png'),
    'BLUE_3': pygame.image.load('assets/Blue_3.png'),
    'BLUE_4': pygame.image.load('assets/Blue_4.png'),
    'BLUE_5': pygame.image.load('assets/Blue_5.png'),
    'BLUE_6': pygame.image.load('assets/Blue_6.png'),
    'BLUE_7': pygame.image.load('assets/Blue_7.png'),
    'BLUE_8': pygame.image.load('assets/Blue_8.png'),
    'BLUE_9': pygame.image.load('assets/Blue_0.png'),
    'BLUE_DRAW': pygame.image.load('assets/Blue_Draw.png'),
    'BLUE_REVERSE': pygame.image.load('assets/Blue_Reverse.png'),
    'BLUE_SKIP': pygame.image.load('assets/Blue_Skip.png'),
    # Green Cards
    'GREEN_0': pygame.image.load('assets/Green_0.png'),
    'GREEN_1': pygame.image.load('assets/Green_1.png'),
    'GREEN_2': pygame.image.load('assets/Green_2.png'),
    'GREEN_3': pygame.image.load('assets/Green_3.png'),
    'GREEN_4': pygame.image.load('assets/Green_4.png'),
    'GREEN_5': pygame.image.load('assets/Green_5.png'),
    'GREEN_6': pygame.image.load('assets/Green_6.png'),
    'GREEN_7': pygame.image.load('assets/Green_7.png'),
    'GREEN_8': pygame.image.load('assets/Green_8.png'),
    'GREEN_9': pygame.image.load('assets/Green_0.png'),
    'GREEN_DRAW': pygame.image.load('assets/Green_Draw.png'),
    'GREEN_REVERSE': pygame.image.load('assets/Green_Reverse.png'),
    'GREEN_SKIP': pygame.image.load('assets/Green_Skip.png'),
    # Red Cards
    'RED_0': pygame.image.load('assets/Red_0.png'),
    'RED_1': pygame.image.load('assets/Red_1.png'),
    'RED_2': pygame.image.load('assets/Red_2.png'),
    'RED_3': pygame.image.load('assets/Red_3.png'),
    'RED_4': pygame.image.load('assets/Red_4.png'),
    'RED_5': pygame.image.load('assets/Red_5.png'),
    'RED_6': pygame.image.load('assets/Red_6.png'),
    'RED_7': pygame.image.load('assets/Red_7.png'),
    'RED_8': pygame.image.load('assets/Red_8.png'),
    'RED_9': pygame.image.load('assets/Red_0.png'),
    'RED_DRAW': pygame.image.load('assets/Red_Draw.png'),
    'RED_REVERSE': pygame.image.load('assets/Red_Reverse.png'),
    'RED_SKIP': pygame.image.load('assets/Red_Skip.png'),
    # Yellow Cards
    'YELLOW_0': pygame.image.load('assets/Yellow_0.png'),
    'YELLOW_1': pygame.image.load('assets/Yellow_1.png'),
    'YELLOW_2': pygame.image.load('assets/Yellow_2.png'),
    'YELLOW_3': pygame.image.load('assets/Yellow_3.png'),
    'YELLOW_4': pygame.image.load('assets/Yellow_4.png'),
    'YELLOW_5': pygame.image.load('assets/Yellow_5.png'),
    'YELLOW_6': pygame.image.load('assets/Yellow_6.png'),
    'YELLOW_7': pygame.image.load('assets/Yellow_7.png'),
    'YELLOW_8': pygame.image.load('assets/Yellow_8.png'),
    'YELLOW_9': pygame.image.load('assets/Yellow_0.png'),
    'YELLOW_DRAW': pygame.image.load('assets/Yellow_Draw.png'),
    'YELLOW_REVERSE': pygame.image.load('assets/Yellow_Reverse.png'),
    'YELLOW_SKIP': pygame.image.load('assets/Yellow_Skip.png'),
    # Other Cards
    'WILD': pygame.image.load('assets/Wild.png'),
    'WILD_DRAW': pygame.image.load('assets/Wild_Draw.png')
}
