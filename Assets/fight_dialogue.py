"""
This module has a class to display dialogue during any boss fight
The text is displayed in a text bubble and appears 1 letter at a time
"""
import pygame
import os
pygame.init()

screen = pygame.display.set_mode((800, 600))

class FightDialouge:
    def __init__(self, text):  # takes the text to be displayed as a parameter
        # loads the images and text fonts
        absolute_path = os.path.dirname(__file__)
        speech_bubble = pygame.image.load(os.path.join(absolute_path, "Images/conversation.png"))
        self.speech_bubble = pygame.transform.scale_by(speech_bubble, 0.15)
        self.text_font = pygame.font.Font("freesansbold.ttf", 16)
        self.unwrapped = text

    # implementation of text wrapping around the text bubble
    def textwrap(self):
        text = self.unwrapped.split()  # splits the text into an array of words 
        self.text = list()
        line = ""
        for word in text:
            if not(line):
                line = word
            else:
                newline = line + " " + word  # concatenates words to form a string
                if self.text_font.size(newline)[0] <= 250:
                    line = newline
                else:  # if the size of string exceeds the required width, this string is appended to the array
                    self.text.append(line)
                    line = word
            if word == text[-1]:
                self.text.append(line)
        # this esentially creates an array with each element representing a line of text corresponding to the width of the text bubble

    def execute(self, boss):  # main function
        self.textwrap()
        current_line = self.text[0]  # gets the 1st line of text
        lines_drawn = list()  # an array to store the lines of text which have been fully drawn onto the screen
        i=0  # a variable representing the length of the current line of text to be drawn, used in slicing. This is incremented after every iteration of the loop to give the impression of characters appearing one at a time
        while self.text:  # main loop
            # fills background and draw speech bubble
            screen.fill((0, 0, 0))
            boss.draw_boss_and_health()
            screen.blit(self.speech_bubble, (400, 10))
            current_height = 35  # height from which the 1st text line starts
            for line in lines_drawn:  # draws the text lines which have been fully drawn onto the screen in their correct position. The current_height variable is incremented by 20 to move to the next line
                text = self.text_font.render(line, True, (0, 0, 0))
                screen.blit(text, (420, current_height))
                current_height += 20
            
            # renders and draws the leftmost i characters of the currrent line
            text = self.text_font.render(current_line[:i], True, (0, 0, 0)) 
            screen.blit(text, (420, current_height))
            pygame.time.delay(30)  # a time delay to give impression of 1 character appearing at a time
            if current_line[:i] == current_line:  # if the whole line has been drawn, then
                lines_drawn.append(self.text.pop(0))  # the line is removed from the array storing all the lines of text. It is appended to the array storing the lines of text which have been fully drawn
                i = 0  # the number of characters to be drawn from the next text line is reset to 1
                if self.text:
                    current_line = self.text[0]  # the current line to be drawn is updated
            else:
                i += 1  # if the full line is drawn, i is incremented to draw 1 more character from the line

            pygame.display.update()



