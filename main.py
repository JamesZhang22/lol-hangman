import sys
 
import pygame
from pygame.locals import *

import requests
import json
import random

from typing import Tuple, List

# Colors
BLACK = (0, 0, 0)
BLACK2 = (60, 60, 60)
GRAY = (199, 199, 199)
GRAY2 = (225, 225, 225)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREENYELLOW = (6, 220, 49)
GREENYELLOW2 = (82, 223, 110)
LIGHTGREEN = (111, 250, 111)
RED = (255, 0, 0)
ORANGE = (255, 111, 0)
LIGHTBLUE = (135, 206, 250)
LIGHTORANGE = (246, 148, 36)
LIGHTRED = (250, 70, 70)

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('monospace', 100)
myfont2 = pygame.font.SysFont('monospace', 70)
myfont3 = pygame.font.SysFont('monospace', 30)
myfont4 = pygame.font.SysFont('monospace', 50)
myfont5 = pygame.font.SysFont('monospace', 120)

timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, 1000)

size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Hangman")
clock = pygame.time.Clock()

pygame.mouse.set_cursor(*pygame.cursors.diamond)

# Letter Dictionary
letters = {
    1: 'a',
    2: 'b',
    3: 'c',
    4: 'd',
    5: 'e',
    6: 'f',
    7: 'g',
    8: 'h',
    9: 'i',
    10: 'j',
    11: 'k',
    12: 'l',
    13: 'm',
    14: 'n',
    15: 'o',
    16: 'p',
    17: 'q',
    18: 'r',
    19: 's',
    20: 't',
    21: 'u',
    22: 'v',
    23: 'w',
    24: 'x',
    25: 'y',
    26: 'z',
    27: ' ',
    28: "'"
}


class Button:
    """Parent class for all buttons in game."""
    def __init__(self, text: str, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Creates a Button.

        Args:
            text (str): word displayed on button.
            x (int): x-location.
            y (int): y-location.
            width (int): width of button.
            height (int): height of button
            color (Tuple[int, int, int]): color of button.
            hold_color (Tuple[int, int, int]): holds the initial color of the button.
            color2 (Tuple[int, int, int]): color of button when hovered on.
            rect (pygame.Rect): Rect of the button.
        """
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hold_color = color
        self.color2 = color
        self.rect = pygame.Rect(x, y, width, height)

    def is_hover(self, mouse_pos: Tuple[int, int]) -> None:
        """Checks if the mouse is hovering over the button and changes the color if so.

        Args:
            mouse_pos (Tuple[int, int]): current position of mouse.
        """
        if self.rect.collidepoint(mouse_pos):
            self.color = self.color2
        else:
            self.color = self.hold_color
    

class StartButton(Button):
    """Start Button."""
    def __init__(self, text: str, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Creates the start/play button.

        Args:
            text (str): word displayed on button.
            x (int): x-location.
            y (int): y-location.
            width (int): width of button.
            height (int): height of button
            color (Tuple[int, int, int]): color of button.
            hold_color (Tuple[int, int, int]): holds the initial color of the button.
            color2 (Tuple[int, int, int]): color of button when hovered on.
            rect (pygame.Rect): Rect of the button.
            play (bool): button clicked on?
        """
        super().__init__(text, x, y, width, height, color)
        self.color2 = LIGHTGREEN
        self.play = False

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the button.

        Args:
            screen (pygame.Surface): display screen to draw on.
        """
        text = myfont.render(self.text, False, WHITE)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text, (380, 280))
        
    def update(self, pos: Tuple[int, int]) -> None:
        """Checks if the button is clicked on.

        Args:
            pos (Tuple[int, int]): mouse position.
        """
        if self.rect.collidepoint(pos):
            self.play = True


class EasyButton(Button):
    """Easy Difficulty Button."""
    def __init__(self, text: str, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Creates easy difficulty game mode button.

        Args:
            text (str): word displayed on button.
            x (int): x-location.
            y (int): y-location.
            width (int): width of button.
            height (int): height of button
            color (Tuple[int, int, int]): color of button.
            hold_color (Tuple[int, int, int]): holds the initial color of the button.
            color2 (Tuple[int, int, int]): color of button when hovered on.
            rect (pygame.Rect): Rect of the button.
        """
        super().__init__(text, x, y, width, height, color)
        self.color2 = GREENYELLOW2

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the button.

        Args:
            screen (pygame.Surface): display screen to draw on.
        """
        text = myfont2.render(self.text, False, WHITE)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text, (70, 450))

    def update(self, pos: Tuple[int, int]) -> None:
        """Checks if the button is clicked on, if so run game loop on easy difficulty.

        Args:
            pos (Tuple[int, int]): current mouse position.
        """
        if self.rect.collidepoint(pos):
            game('EASY')


class MediumButton(Button):
    """Medium Difficulty Button."""
    def __init__(self, text: str, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Creates medium difficulty game mode button.

        Args:
            text (str): word displayed on button.
            x (int): x-location.
            y (int): y-location.
            width (int): width of button.
            height (int): height of button
            color (Tuple[int, int, int]): color of button.
            hold_color (Tuple[int, int, int]): holds the initial color of the button.
            color2 (Tuple[int, int, int]): color of button when hovered on.
            rect (pygame.Rect): Rect of the button.
        """
        super().__init__(text, x, y, width, height, color)
        self.color2 = LIGHTORANGE

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the button.

        Args:
            screen (pygame.Surface): display screen to draw on.
        """
        text = myfont2.render(self.text, False, WHITE)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text, (440, 450))

    def update(self, pos: Tuple[int, int]) -> None:
        """Checks if the button is clicked on, if so run game loop on medium difficulty.

        Args:
            pos (Tuple[int, int]): current mouse position.
        """
        if self.rect.collidepoint(pos):
            game('MEDIUM')


class HardButton(Button):
    """Hard Difficulty Button."""
    def __init__(self, text: str, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Creates hard difficulty game mode button.

        Args:
            text (str): word displayed on button.
            x (int): x-location.
            y (int): y-location.
            width (int): width of button.
            height (int): height of button
            color (Tuple[int, int, int]): color of button.
            hold_color (Tuple[int, int, int]): holds the initial color of the button.
            color2 (Tuple[int, int, int]): color of button when hovered on.
            rect (pygame.Rect): Rect of the button.
        """
        super().__init__(text, x, y, width, height, color)
        self.color2 = LIGHTRED

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the button.

        Args:
            screen (pygame.Surface): display screen to draw on.
        """
        text = myfont2.render(self.text, False, WHITE)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text, (770, 450))

    def update(self, pos: Tuple[int, int]) -> None:
        """Checks if the button is clicked on, if so run game loop on hard difficulty.

        Args:
            pos (Tuple[int, int]): current mouse position.
        """
        if self.rect.collidepoint(pos):
            game('HARD')


class SpecialGame(Button):
    """Special button for special gamemode."""
    def __init__(self, text: str, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Creates special difficulty game mode button.

        Args:
            text (str): word displayed on button.
            x (int): x-location.
            y (int): y-location.
            width (int): width of button.
            height (int): height of button
            color (Tuple[int, int, int]): color of button.
            hold_color (Tuple[int, int, int]): holds the initial color of the button.
            color2 (Tuple[int, int, int]): color of button when hovered on.
            rect (pygame.Rect): Rect of the button.
            pressed (bool): if button is pressed
            pressed_t (bool) : if text button is pressed
            current_text (str): text user inputs with keyboard
            text_box_rect (pygame.Rect); Rect of the text box
        """
        super().__init__(text, x, y, width, height, color)
        self.pressed = False
        self.pressed_t = False
        self.color2 = BLACK2
        self.current_text = ''
        self.text_box_rect = pygame.Rect(860, 220, 100, 30)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the button.

        Args:
            screen (pygame.Surface): display screen to draw on.
        """
        text = myfont3.render(self.text, False, WHITE)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text, (880, 155))

        if self.pressed:
            if self.pressed_t:
                pygame.draw.rect(screen, RED, self.text_box_rect)
                text2 = myfont3.render(self.current_text, True, WHITE)
                screen.blit(text2, (900, 220))
            else:
                pygame.draw.rect(screen, BLACK, self.text_box_rect)
                text2 = myfont3.render(self.current_text, True, WHITE)
                screen.blit(text2, (900, 220))
            

    def is_pressed(self, pos: Tuple[int, int]) -> None:
        """Checks if the special button is pressed.

        Args:
            pos (Tuple[int, int]): current mouse position.

        Returns:
            bool: True if the button is clicked and false if not clicked.
        """
        if self.rect.collidepoint(pos):
            self.pressed = True

    def is_pressed_text(self, pos: Tuple[int, int]) -> None:
        """Checks if the text box is pressed.

        Args:
            pos (Tuple[int, int]): current mouse position.

        Returns:
            bool: True if the button is clicked and false if not clicked.
        """
        if self.text_box_rect.collidepoint(pos):
            self.pressed_t = True


class MenuButton(Button):
    """Menu Button."""
    def __init__(self, text: str, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Creates the menu button on game over screen.

        Args:
            text (str): word displayed on button.
            x (int): x-location.
            y (int): y-location.
            width (int): width of button.
            height (int): height of button
            color (Tuple[int, int, int]): color of button.
            hold_color (Tuple[int, int, int]): holds the initial color of the button.
            color2 (Tuple[int, int, int]): color of button when hovered on.
            rect (pygame.Rect): Rect of the button.
        """
        super().__init__(text, x, y, width, height, color)
        self.color2 = GRAY2

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the button.

        Args:
            screen (pygame.Surface): display screen to draw on.
        """
        text = myfont3.render(self.text, False, WHITE)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text, (465, 360))

    def is_pressed(self, pos: Tuple[int, int]) -> bool:
        """Checks if the menu button is pressed.

        Args:
            pos (Tuple[int, int]): current mouse position.

        Returns:
            bool: True if the button is clicked and false if not clicked.
        """
        if self.rect.collidepoint(pos):
            return True
        else:
            return False


class ResultButton(Button):
    """Results Button."""
    def __init__(self, text: str, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        """Creates the results button on the game over screen.

        Args:
            text (str): word displayed on button.
            x (int): x-location.
            y (int): y-location.
            width (int): width of button.
            height (int): height of button
            color (Tuple[int, int, int]): color of button.
            hold_color (Tuple[int, int, int]): holds the initial color of the button.
            color2 (Tuple[int, int, int]): color of button when hovered on.
            rect (pygame.Rect): Rect of the button.
        """
        super().__init__(text, x, y, width, height, color)
        self.color2 = GRAY2

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the button.

        Args:
            screen (pygame.Surface): display screen to draw on.
        """
        text = myfont3.render(self.text, False, WHITE)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(text, (437, 240))

    def is_pressed(self, pos: Tuple[int, int]) -> bool:
        """Checks if the results button is pressed.

        Args:
            pos (Tuple[int, int]): current mouse position.

        Returns:
            bool: True if the button is clicked and false if not clicked.
        """
        if self.rect.collidepoint(pos):
            return True
        else:
            return False
        
    def print_out(self) -> None:
        """Generates a .txt and a .json file with the results of the game.
        """
        with open("results.txt", "w") as f:
            f.write(f"Word: {Words.GUESS_WORD}\n")
            f.write(f"Total Guesses: {word.guesses}\n")
            f.write(f"Correct Guesses: {word.guesses - word.incorrect_guesses}\n")
            f.write(f"Incorrect Guesses: {word.incorrect_guesses}\n")
            if word.won is True:
                f.write(f"Succesfully Guess Word")
            if word.lost is True:
                f.write(f"Failed to Guess Word")

        data = {
            'Word': Words.GUESS_WORD,
            'Total Guesses': word.guesses,
            'Correct Guesses': word.guesses - word.incorrect_guesses,
            'Incorrect Guesses': word.incorrect_guesses
        }
        if word.won is True:
            data['Guessed Word'] = True
        if word.lost is True:
            data['Guessed Word'] = False
        
        with open("results.json", "w") as f:
            json.dump(data, f, indent=4)
    

class Keyboard():
    """Keyboard."""
    def __init__(self, letter: str, x: int, y: int) -> None:
        """Creates a single letter on the keyboard.

        Args:
            letter (str): letter on key.
            x (int): x-location
            y (int): y-location
            letter_rect (pygame.Rect): Rect of the key
            selected (bool): is button clicked on?
        """
        self._x = x
        self._y = y
        self._letter = letter
        self._letter_rect = pygame.Rect(x, y, 40, 40)
        self._selected = False

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the key.

        Args:
            screen (pygame.Surface): screen to draw on.
        """
        if self._selected == False:
            pygame.draw.rect(screen, BLACK, self._letter_rect, 5)
            text = myfont3.render(self._letter, False, BLACK)
            screen.blit(text, (self._x + 10, self._y))
        elif self._selected == True:
            pygame.draw.rect(screen, GREEN, self._letter_rect, 5)
            text = myfont3.render(self._letter, False, GREEN)
            screen.blit(text, (self._x + 10, self._y))

    def update(self, pos: Tuple[int, int]) -> str:
        """Checks if the key is clicked on.

        Args:
            pos (Tuple[int, int]): current mouse position.

        Returns:
            str: key that was clicked on.
        """
        if self._letter_rect.collidepoint(pos) and self._selected is False:
            self._selected = True
            word.guesses += 1
            return self._letter

    def get_positions(self) -> Tuple[int, int]:
        """Get the position.

        Returns:
            Tuple[int, int]: location of the key.
        """
        return (self._x, self._y)
    
    def set_position(self, new_x: int, new_y: int) -> None:
        """Change position of key.

        Args:
            new_x (int): new x-location
            new_y (int): new y-location
        """
        self._x = new_x
        self._y = new_y

    def get_letter(self) -> str:
        """Get the letter on key.

        Returns:
            str: letter on key.
        """
        return self.letter

    def set_letter(self, new_letter: str) -> None:
        """Set new letter on key.

        Args:
            new_letter (str): new letter.
        """
        self._letter = new_letter

    def get_rect(self) -> pygame.Rect:
        """Get the Rect of the key.

        Returns:
            pygame.Rect: Rect of the key.
        """
        return self._letter_rect

    def set_rect(self, new_rect: pygame.Rect) -> None:
        """Change the Rect of key.

        Args:
            new_rect (pygame.Rect): new Rect.
        """
        self._letter_rect = new_rect

    def get_is_selected(self) -> bool:
        """Get the state of the button.

        Returns:
            bool: True if selected, false otherwise.
        """
        return self._selected

    def set_is_selected(self, selected: bool) -> None:
        """Change the state of the button.

        Args:
            selected (bool): new state of button.
        """
        self._selected = selected
        

class Words():
    """Words to guess."""

    GUESS_WORD = ''

    def __init__(self) -> None:
        """Creates and sets up the word to guess.

            Args:
                word_list (List): list of all possible words to guess
                guesses (int): total guesses made.
                correct_guesses (int): total correct guesses made.
                incorrect_guesses (int): total incorrect guesses made.
                lost (bool): if user lost
                won (bool): if user won
        """
        self.word_list = []
        
        request = requests.get('https://raw.githubusercontent.com/ngryman/lol-champions/master/champions.json')
        words = request.json()
        for word in words:
            if '&' in word['name']:
                self.word_list.append('nunu')
            else:
                self.word_list.append(word['name'].lower())
        self.guesses = 0
        self.correct_guesses = 0
        self.incorrect_guesses = 0
        self.lost = False
        self.won = False

    def get_difficulty(self, index: int) -> int:
        """Gets the difficulty of the word.

        Args:
            index (int): index in the word_list.

        Returns:
            int: difficulty of the word based on lenght and uniqueness.
        """
        # count unique words
        unique = set(self.word_list[index])
        uniqe_letters = len(unique)

        return (len(self.word_list[index])*0.5) + uniqe_letters

    def sort(self) -> None:
        """Bubble sort algorithm to sort the words from lowest to highest difficulty.
        """
        for num in range(len(self.word_list) - 1):
            i = 0
            swapped = False

            while i + 1 < len(self.word_list) - num:
                first = self.word_list[i]
                second = self.word_list[i + 1]
                first_diff = self.get_difficulty(i)
                second_diff = self.get_difficulty(i + 1)

                if first_diff > second_diff:
                    self.word_list[i] = second
                    self.word_list[i + 1] = first
                    swapped = True
                
                i += 1

            if swapped is False:
                break
        return 

    def filter_by_letter(self, letter: str) -> List[str]:
        """Filter the word list by a certain letter so that no word has that letter.

        Args:
            letter (str): unwanted letter.

        Returns:
            List[int]: list of words without that letter.
        """
        filtered_list = []

        for word in self.word_list:
            if letter not in word:
                filtered_list.append(word)
        
        return filtered_list

    def get_word(self, difficulty: str) -> None:
        """Get a random word from word_list based on game difficulty.

        Args:
            difficulty (str): difficulty of the game.
        """
        if difficulty == 'EASY':
            rand_index = random.randint(0, 50)
            Words.GUESS_WORD = self.word_list[rand_index]
        elif difficulty == 'MEDIUM':
            rand_index = random.randint(51, 101)
            Words.GUESS_WORD = self.word_list[rand_index]
        elif difficulty == 'HARD':
            rand_index = random.randint(102, 151)
            Words.GUESS_WORD = self.word_list[rand_index]
        elif len(difficulty) == 1:
            filtered_list = self.filter_by_letter(difficulty)
            rand_index = random.randint(0, len(filtered_list) - 1)
            Words.GUESS_WORD = filtered_list[rand_index]
        
        self.current_word = list('_ '*len(Words.GUESS_WORD))

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the word to guess.

        Args:
            screen (pygame.Surface): screen to draw on.
        """
        text = myfont4.render(''.join(self.current_word), True, BLACK)
        screen.blit(text, (300, 200))

    def update_word(self, letter_to_show: str) -> None:
        """Update to state of the game aswell as the words shwon if they are guessed.

        Args:
            letter_to_show (str): letter the user guessed.
        """
        if self.incorrect_guesses == 6:
            self.lost = True
        if '_' not in self.current_word:
            self.won = True
        if letter_to_show not in Words.GUESS_WORD:
            self.incorrect_guesses += 1
        for i, letter in enumerate(list(Words.GUESS_WORD)):
            if letter == letter_to_show:
                self.current_word[i*2] = letter
                self.current_word[(i*2)+1] = ' '
                self.correct_guesses += 1
        # print(self.guesses, self.correct_guesses, self.incorrect_guesses)


class HangMan():
    """Hangman images."""
    def __init__(self) -> None:
        """Creates the hangman for the game

        Args:
            stand (pygame.image): stand for hangman
            head (pygame.image): headof hangman
            body (pygame.image): body of hangman
            left_arm (pygame.image): left arm of hangman
            right_arm (pygame.image): right arm of hangman
            left_leg (pygame.image): left leg of hangman
            right_leg (pygame.image): right leg of hangman
            current_img (pygame.image): current state of hangman
        """
        self.stand = pygame.image.load('Images/Hangman1.png')
        self.head = pygame.image.load('Images/Hangman2.png')
        self.body = pygame.image.load('Images/Hangman3.png')
        self.left_arm = pygame.image.load('Images/Hangman4.png')
        self.right_arm = pygame.image.load('Images/Hangman5.png')
        self.left_leg = pygame.image.load('Images/Hangman6.png')
        self.right_leg = pygame.image.load('Images/Hangman7.png')
        self.current_img = pygame.image.load('Images/Hangman1.png')

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the current state of hangman.

        Args:
            screen (pygame.Surface): screen to draw on.
        """
        screen.blit(self.current_img, (70, 70))
        if word.incorrect_guesses == 1:
            self.current_img = pygame.image.load('Images/Hangman2.png')
        elif word.incorrect_guesses == 2:
            self.current_img = pygame.image.load('Images/Hangman3.png')
        elif word.incorrect_guesses == 3:
            self.current_img = pygame.image.load('Images/Hangman4.png')
        elif word.incorrect_guesses == 4:
            self.current_img = pygame.image.load('Images/Hangman5.png')
        elif word.incorrect_guesses == 5:
            self.current_img = pygame.image.load('Images/Hangman6.png')
        elif word.incorrect_guesses == 6:
            self.current_img = pygame.image.load('Images/Hangman7.png')
        else:
            self.current_img = pygame.image.load('Images/Hangman1.png')


# Objects/Instance Creation
start_button = StartButton('PLAY', 350, 285, 300, 100, GREEN)
special_button = SpecialGame('???', 860, 150, 100, 50, BLACK)
easy_button = EasyButton('EASY', 50, 440, 200, 100, GREENYELLOW)
medium_button = MediumButton('MED', 400, 440, 200, 100, ORANGE)
hard_button = HardButton('HARD', 750, 440, 200, 100, RED)
menu_button = MenuButton('Menu', 435, 350, 130, 50, GRAY)
result_button = ResultButton('Results', 435, 230, 130, 50, GRAY)

hangman = HangMan()
word = Words()
word.sort()

keyboard_buttons = []
for key, value in letters.items():
    if key < 14:
        letter = Keyboard(value, (key*50) + 140, 400)
        keyboard_buttons.append(letter)
    elif 14 <= key < 27:
        letter = Keyboard(value, ((key-13)*50) + 140, 470)
        keyboard_buttons.append(letter)
    else:
        letter = Keyboard(value, (key-13)*50 - 230, 540)
        keyboard_buttons.append(letter)

# Written by Rabbid76
# https://replit.com/@Rabbid76/PyGame-TransparentShapes#main.py
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)
# ------------------


# Menus
def main_menu() -> None:
    """Main menu loop.
    """
    typed_letter = False
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = event.pos
                start_button.update(mouse_position)
                if start_button.play:
                    easy_button.update(mouse_position)
                    medium_button.update(mouse_position)
                    hard_button.update(mouse_position)
                    special_button.is_pressed(mouse_position)
                    if special_button.pressed:
                        special_button.is_pressed_text(mouse_position)

            if event.type == pygame.MOUSEMOTION:
                mouse_position = event.pos
                start_button.is_hover(mouse_position)
                easy_button.is_hover(mouse_position)
                medium_button.is_hover(mouse_position)
                hard_button.is_hover(mouse_position)
                special_button.is_hover(mouse_position)

            if event.type == pygame.KEYDOWN and special_button.pressed_t is True:
                if event.key == pygame.K_BACKSPACE:
                    special_button.current_text = special_button.current_text[0:-1]
                    typed_letter = False
                elif event.key == pygame.K_RETURN and typed_letter is True:
                    game(special_button.current_text)
                elif len(special_button.current_text) < 1 and event.key != pygame.K_RETURN:
                    special_button.current_text += event.unicode
                    typed_letter = True


        screen.fill(GRAY)

        # Draw code
        title_text = myfont5.render('HANGMAN', True, WHITE)
        screen.blit(title_text, (250, -10))

        hangman_img = pygame.image.load('Images/Hangman.png')
        hangman_img = pygame.transform.scale(hangman_img, (200, 200))
        screen.blit(hangman_img, (400, 100))

        start_button.draw(screen)
        if start_button.play is True:
            easy_button.draw(screen)
            medium_button.draw(screen)
            hard_button.draw(screen)
            special_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def game(difficulty: str) -> None:
    """Game loop.

    Args:
        difficulty (str): difficulty of game.
    """
    if difficulty == 'EASY':
        countdown = 120
    elif difficulty == 'MEDIUM':
        countdown = 60
    elif difficulty == 'HARD':
        countdown = 30
    elif len(difficulty) == 1:
        countdown = 45
    count_text = myfont3.render(str(countdown), True, BLACK)

    word.get_word(difficulty)
    for letter in keyboard_buttons:
        letter._selected = False
    word.guesses = 0
    word.correct_guesses = 0
    word.incorrect_guesses = 0
    word.lost = False
    word.won = False
    # print(Words.GUESS_WORD)
    
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if word.lost is False and word.won is False:
                    mouse_position = event.pos
                    for letter in keyboard_buttons:
                        pressed = letter.update(mouse_position)
                        try:
                            word.update_word(pressed)
                        except TypeError:
                            pass
                elif word.lost is True or word.won is True:
                    mouse_position = event.pos
                    if menu_button.is_pressed(mouse_position):
                        done = True
                    if result_button.is_pressed(mouse_position):
                        result_button.print_out()

            if event.type == pygame.MOUSEMOTION:
                mouse_position = event.pos
                menu_button.is_hover(mouse_position)
                result_button.is_hover(mouse_position)

            if event.type == timer_event and word.lost is False and word.won is False:
                c = BLACK
                if countdown == 1:
                    word.lost = True
                    c = RED
                elif countdown <= 10:
                    c = RED
                countdown -= 1
                count_text = myfont3.render(str(countdown), True, c)
    
        screen.fill(GRAY)
    
        # Draw code
        hangman.draw(screen)
        word.draw(screen)

        for letter in keyboard_buttons:
            letter.draw(screen)

        if word.lost:
            text = myfont.render('LOST', False, RED)
            screen.blit(text, (380, 50))
        if word.won:
            text = myfont.render('WON', False, GREEN)
            screen.blit(text, (400, 50))
        if word.lost is True or word.won is True:
            draw_rect_alpha(screen, (0, 0, 0, 127), (0, 0, 1000, 600))
            draw_circle_alpha(screen, (255, 255, 255, 127), (500, 300), 150)
            menu_button.draw(screen)
            result_button.draw(screen)
        
        screen.blit(count_text, (930, 0))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()