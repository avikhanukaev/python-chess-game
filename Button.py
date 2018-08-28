import pygame
from TextHandler import TextHandler
from Consts import Colors, Fonts
from typing import Callable, List


class Button:
    """
    This class responsible for buttons functionality
    """

    def __init__(self, top_x: int, top_y: int, title: str, operation: Callable, arguments: List, dest: pygame.Surface):
        """
        Default c'tor
        :param top_x: int, x coordinate for display
        :param top_y: int, y coordinate for display
        :param title: str, the caption of the button
        :param operation: Callable, the operation that should be performed when button is pressed
        :param arguments: List, the list of arguments to be passed to the operation.
        :param dest: pygame.Surface, the surface to blit on the button.
        """
        self.__top_x = top_x
        self.__top_y = top_y
        self.__title = title
        self.__operation = operation
        self.__arguments = arguments
        self.destination = dest
        self.__text_handler = TextHandler(Fonts['Regular'], Colors['BLACK'], 20, dest)
        self.__w, self.__h = self.__text_handler.get_text_rect(title)[2:]
        self.__w += 5
        self.__h += 5

    def display(self) -> None:
        """
        Shows the button on the screen.
        :return: None
        """
        pygame.draw.rect(self.destination, Colors['BLACK'],
        [self.__top_x, self.__top_y, self.__w, self.__h], 1)
        self.__text_handler.display_message(self.__top_x + 2, self.__top_y + 2, self.__title)
        pygame.display.update()

    def is_pressed(self) -> bool:
        """
        Checks whether the button was pressed.
        :return: True, if and only if the mouse click was inside the button borders (= mouse click on button).
        """
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.__top_x <= mouse_x <= self.__top_x + self.__w and \
                self.__top_y <= mouse_y <= self.__top_y + self.__h:
                return True
        return False

    def perform_operation(self):
        self.__operation(self.__arguments[0])
