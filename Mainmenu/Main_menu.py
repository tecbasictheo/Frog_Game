import pygame, sys
from Buttons import Button
from pygame_menu.font import get_font

#from frog import event

pygame.init()

screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Menu")
font = pygame.font.SysFont('cambria', 30)
BG = pygame.image.load("media/background.png")

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black") #how to change background - reload background
        '''PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)''' # here background plus text

        PLAY_BACK = Button(image=None, pos=(640, 260), text_input= "BACK", font = get_font(75), base_color= "White", hovering_color= "Black")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        #for quit game - put in froggame later
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu(): #Main Menu Screen
    pygame.display.set_caption("Main Menu")

    while True:
        SCREEN.blit(BG, (0, 0)) # add background here

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        MENU_TEXT_1 = get_font(100).render("By Theodora 🐸", True, "pink")
        MENU_RECT_1 = MENU_TEXT_1.get_rect('button right corner')

        PLAY_BUTTON = Button(image=pygame.image.load("media/"), pos = (640, 250), hovering_color= "white")   #missing button design
        OPTIONS_BUTTON = Button(image=pygame.image.load("media/"), pos = (640, 400), hovering_color= "white")   #missing button design
        QUIT_BUTTON = Button(image=pygame.image.load("media/"), pos = (640, 550), hovering_color= "white")   #missing button design
        LEVELS_BUTTON = Button(image=pygame.image.load("media/"), pos = (640, 450), hovering_color= "white")   #missing button design
        HIGHSCORE_BUTTON = Button(image=pygame.image.load("media/"), pos = (640, 350), hovering_color= "white")   #missing button design
        # add text input

        #SCREEN.blit(pygame.image.load("media/Main_menu.png"), (0, 0)) #-> where does that come from
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON,LEVELS_BUTTON, HIGHSCORE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
            if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                options()
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

        pygame.display.update()