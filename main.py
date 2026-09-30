import pygame
from launcher import Menu


def main() -> None:
    pygame.init()
    menu = Menu()
    menu.run()


if __name__ == "__main__":
    main()
    pygame.quit()