import datetime
import socket
import time

import pygame
import sys
# create display window
from pygame import mixer
from Button import Button
from Connect import Connect
from TextBox import TextBox

errormsgtimer = datetime.datetime.now() + datetime.timedelta(seconds=3)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CHARLIMIT = 15
response = ""

SCALE = 1
mixer.init()
mixer.music.load('Hunter X Hunter - Opening 1 ｜ Departure!.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.1)
clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

# load button images
start_img = pygame.image.load('pics/real sign up.png').convert_alpha()
login_img = pygame.image.load('pics/real login.png').convert_alpha()
login2_img = pygame.image.load('pics/login.png').convert_alpha()
exit_img = pygame.image.load('pics/Exit.png').convert_alpha()
background_img = pygame.image.load('pics/background.png').convert_alpha()
back_img = pygame.image.load('pics/back.png').convert_alpha()
continue_img = pygame.image.load('pics/continue.png').convert_alpha()
muteMusic_img = pygame.image.load('pics/muteMusic.png').convert_alpha()
play_img = pygame.image.load('pics/Play.png').convert_alpha()
# creates buttons images
start_img = pygame.transform.scale(start_img, (350, 100))
login_img = pygame.transform.scale(login_img, (350, 100))
login2_img = pygame.transform.scale(login2_img, (200, 200))
exit_img = pygame.transform.scale(exit_img, (350, 100))
background_img = pygame.transform.scale(background_img, (1200, 800))
back_img = pygame.transform.scale(back_img, (50, 50))
continue_img = pygame.transform.scale(continue_img, (200, 200))
muteMusic_img = pygame.transform.scale(muteMusic_img, (100, 100))
play_img = pygame.transform.scale(play_img,(300,100))
# create button instances
signup_button = Button((SCREEN_WIDTH * 0.5) - (start_img.get_width() / 2),
                       (SCREEN_HEIGHT * 0.25) - (start_img.get_height() / 2), start_img, SCALE)
login_button = Button((SCREEN_WIDTH * 0.5) - (login_img.get_width() / 2),
                      (SCREEN_HEIGHT * 0.50) - (login_img.get_height() / 2), login_img, SCALE)
login2_button = Button((SCREEN_WIDTH * 0.125),
                       (SCREEN_HEIGHT * 0.60), login2_img, SCALE)
exit_button = Button((SCREEN_WIDTH * 0.5) - (exit_img.get_width() / 2),
                     (SCREEN_HEIGHT * 0.75) - (exit_img.get_height() / 2), exit_img, SCALE)
back_button = Button(0, 0, back_img, SCALE)
muteMusic = Button((SCREEN_WIDTH) - (muteMusic_img.get_width()),
                   (SCREEN_HEIGHT) - (muteMusic_img.get_height()), muteMusic_img, SCALE)
continue_button = Button((SCREEN_WIDTH * 0.125), (SCREEN_HEIGHT * 0.60), continue_img, SCALE)
play_button = Button((SCREEN_WIDTH * 0.125), (SCREEN_HEIGHT * 0.20), play_img, SCALE)

conn = Connect()
conn.connect()


def removeAllTextBoxes():
    for user in TextBox._textboxes:
        user.remove()


def errorMessage(string):
    font = pygame.font.Font(None, 32)
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(SCREEN_WIDTH - 500, 0, 500, 100))
    errormsg = font.render(string, False, (255, 255, 255))
    screen.blit(errormsg, ((SCREEN_WIDTH - errormsg.get_rect().width) - (500 - errormsg.get_rect().width) / 2, 50))
    pygame.display.flip()
    time.sleep(2)



def eventListener():
    for event in pygame.event.get():
        # if game was closed
        if event.type == pygame.QUIT:
            pygame.quit()
            # checks that if you have clicked on the box or outside of it
        if event.type == pygame.MOUSEBUTTONDOWN:
            for user in TextBox._textboxes:
                if user.rect.collidepoint(pygame.mouse.get_pos()):
                    user.active = True
                else:
                    user.active = False

        # checks if any button was pressed
        if event.type == pygame.KEYDOWN:
            for user in TextBox._textboxes:
                # short form for if active == true
                if user.active:
                    # ablitiy to backspace/delete, looks if backspace is pressed
                    if event.key == pygame.K_BACKSPACE:
                        print(user.text)
                        user.addText("delete", CHARLIMIT)
                    else:
                        # gets the specific key that was pressed and adds it to user_text, gets information
                        user.addText(event.unicode, CHARLIMIT)


def signup():
    user_textbox = TextBox(200, 32, int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT * 0.3), "USERNAME")
    pass_textbox = TextBox(200, 32, int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT * 0.4), "PASSWORD")
    confirmpass_textbox = TextBox(200, 32, int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT * 0.5), "CONFIRM PASSWORD")


    while True:
        screen.fill((0, 0, 0))
        eventListener()

        if back_button.draw(screen):
            removeAllTextBoxes()
            return 0

        user_textbox.makeTextBox(False, screen)
        pass_textbox.makeTextBox(True, screen)
        confirmpass_textbox.makeTextBox(True, screen)
        if continue_button.draw(screen):
            if confirmpass_textbox.text != pass_textbox.text:
                errorMessage("PASSWORDS DO NOT MATCH")
                pygame.display.flip()
                time.sleep(1.5)
            else:
                response = conn.send("~SIGNUP~ " + user_textbox.text + " " + pass_textbox.text)
            if response == "SUCCESSFUL SIGNUP":
                removeAllTextBoxes()
                return 0
            else:
                errorMessage(response)

        pygame.display.flip()
        clock.tick(60)


def login():
    user_textbox = TextBox(200, 32, int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT * 0.3), "USERNAME")
    pass_textbox = TextBox(200, 32, int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT * 0.4), "PASSWORD")


    while True:
        screen.fill((0, 0, 0))
        eventListener()

        if back_button.draw(screen):
            removeAllTextBoxes()
            return 0

        user_textbox.makeTextBox(False, screen)
        pass_textbox.makeTextBox(True, screen)

        if login2_button.draw(screen):
            print(user_textbox.text)
            response = conn.send("~LOGIN~ " + user_textbox.text + " " + pass_textbox.text)
            if response == "LOGIN SUCCESSFUL":
                removeAllTextBoxes()
                return 3
            else:
                errorMessage(response)

        pygame.display.flip()
        clock.tick(60)


def playScreen():

    while True:
        screen.fill((0, 50, 100))
        eventListener()
        if play_button.draw(screen):
            print()

        pygame.display.flip()





#                                                   MAIN SCREEN
# ***********************************************************************************************************************

def menuScreen():
    while True:
        screen.fill((0, 0, 0))
        screen.blit(background_img, (0, 0))

        if signup_button.draw(screen):
            return 1
            # sys.stdout.close()
        if login_button.draw(screen):
            return 2

        if exit_button.draw(screen):
            return -1
            # sys.stdout.close()
        if muteMusic.draw(screen):
            if mixer.music.get_volume() == 0:
                mixer.music.set_volume(0.1)
            else:
                mixer.music.set_volume(0)

        # event handler
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                sys.stdout.close()
                pygame.quit()

        pygame.display.update()
