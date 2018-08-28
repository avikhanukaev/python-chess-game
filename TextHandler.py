import pygame


class TextHandler:
    def __init__(self, font_path, font_color, font_size, dest):
        self.__font = pygame.font.Font(font_path, font_size)
        self.__color = font_color
        self.__size = font_size
        self.destination = dest
        self.__text_surface = None
    
    def display_message(self, top_x, top_y, message_text):
        text_surface = self.render_text(message_text)
        self.destination.blit(text_surface, (top_x, top_y))
        pygame.display.update()

    def render_text(self, message_text):
        return self.__font.render(message_text, True, self.__color)

    def get_text_rect(self, message_text):
        return self.render_text(message_text).get_rect()