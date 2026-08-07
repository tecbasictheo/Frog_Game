import pygame, sys
from Buttons import Button
#from frog import event

pygame.init()

screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Menu")
font = pygame.font.SysFont('cambria', 20)
BG = pygame.image.load("../media/background.png")

def get_font(size):
    return pygame.font.SysFont('cambria', size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black") #how to change background - reload background
        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        screen.blit(PLAY_TEXT, PLAY_RECT) # here background plus text

        PLAY_BACK = Button(image=None, pos=(640, 460), text_input= "BACK", font = get_font(30), base_color= "White", hover_color= "Black")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        #for quit game - put in froggame later
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def levels():
    while True:
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black") #how to change background - reload background
        LEVELS_TEXT = get_font(45).render("This is the Level screen.", True, "White")
        LEVELS_RECT = LEVELS_TEXT.get_rect(center=(640, 260))
        screen.blit(LEVELS_TEXT, LEVELS_RECT) # here background plus text

        LEVELS_BACK = Button(image=None, pos=(640, 460), text_input= "BACK", font = get_font(30), base_color= "White", hover_color= "Black")
        LEVELS_BACK.changeColor(LEVEL_MOUSE_POS)
        LEVELS_BACK.update(screen)

        #for quit game - put in froggame later
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVELS_BACK.checkForInput(LEVEL_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def options(): # use return to go back
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(60).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hover_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

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
        screen.blit(BG, (0, 0)) # add background here

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("Jumping Frog", True, "green")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 150))
        ME_TEXT = get_font(15).render("By Theodora 🐸", True, "pink")
        ME_RECT = ME_TEXT.get_rect(center= (1200, 700))

        PLAY_BUTTON = Button(image=None, pos = (200, 250),  text_input="PLAY", font=get_font(35), base_color="#d7fcd4",  hover_color= "white")   #missing button design
        OPTIONS_BUTTON = Button(image=None, pos = (200, 400), text_input="Options", font=get_font(35), base_color="#d7fcd4",  hover_color= "white")   #missing button design
        QUIT_BUTTON = Button(image=None, pos = (200, 550), text_input="Quit", font=get_font(35), base_color="#d7fcd4",  hover_color= "white")   #missing button design
        LEVELS_BUTTON = Button(image=None, pos = (200, 450), text_input="Levels", font=get_font(35), base_color="#d7fcd4",  hover_color= "white")   #missing button design
        HIGHSCORE_BUTTON = Button(image=None, pos = (200, 350),  text_input="Highscore", font=get_font(35), base_color="#d7fcd4",  hover_color= "white")   #missing button design
        # add text input         PLAY_BUTTON = Button(image=pygame.image.load("../media/"), pos = (640, 250),  text_input="PLAY", font=get_font(75), base_color="#d7fcd4",  hovering_color= "white")   #missing button design

        screen.blit(pygame.image.load("../media/background.png"), (0, 0)) #-> where does that come from
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(ME_TEXT, ME_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON,LEVELS_BUTTON, HIGHSCORE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

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

main_menu()