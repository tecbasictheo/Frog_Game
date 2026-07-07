import pygame
#import helper.py as helper
from random import randint
from button import button

# making the mainscreen
def menu:
    def main_menu():
        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("FROG GAME", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                                 text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                    text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
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

            main_menu()

# making the classes
class Frog:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y

# should move - use bo
    def event(self, event):
        if event.type == QUIT:
            self.running = False

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.running = False

        if self.state == 'START':
            if event.type == KEYDOWN and event.key == K_RETURN:
                self.state = 'PLAYING'

        if self.state == 'PLAYING':
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.frog.move(angle += 1)

            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.frog.move(1, 0)
            if event.type == KEYDOWN and event.key == K_UP:
                self.frog.move(0, -1)
            if event.type == KEYDOWN and event.key == K_DOWN:
                self.frog.move(0, 1)