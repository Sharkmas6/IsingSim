from MainAlgo import *
import pygame
import pygame.freetype  # text and fonts
pygame.init()

# GLOBAL COLORS
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
GREY = pygame.Color("azure3")

# SCREEN SETTINGS
GAME_FONT = pygame.freetype.SysFont(None, 20)
WIDTH = 500
HEIGHT = 500
InfoSize = 1.32
FPS = 120


class InteractiveIsing(Lattice):
    def __init__(self, NDims=2, NSpins=20, pUpInnit=0.5, rng=None, B=0, J=1, kT=1, Evo=None,
                WIDTH=500, HEIGHT=500, FPS=60, infoSize=1.3):
        super().__init__(NDims, NSpins, pUpInnit, rng, B, J, kT, Evo)
        self.dx = int(WIDTH / NSpins)
        self.dy = int(HEIGHT / NSpins)
        self.fps = FPS
        self.infoSize = infoSize
        # setup drawing window
        self.background = pygame.display.set_mode([WIDTH*infoSize, HEIGHT])
        self.background.fill(GREY)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.background.blit(self.screen, (0, 0))


    def mainLoop(self):
        # draw initial lattice
        self.updateLat()

        # Run until the user asks to quit
        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                running = self.handleEvent(event, running)

            # run iteration and update
            self.RunIter()
            self.updateLat()

            # limit framerate and flip
            pygame.time.Clock().tick(self.fps)
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def handleEvent(self, event, running):
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # specifically escape key
            if event.key == pygame.K_ESCAPE:
                running = False
            # in/decrease magnetic field if u/j pressed
            if event.key == pygame.K_u:
                self.B += 1
            elif event.key == pygame.K_j:
                self.B -= 1
            # in/decrease temperature if t/g pressed
            if event.key == pygame.K_t:
                self.kT += 1
            elif event.key == pygame.K_g:
                if self.kT > 1: self.kT -= 1

        return running

    def updateLat(self):
        #todo CHANGE TO DRAW LATTICE ON SURFACE, .DRAW INSTEAD OF MAKING NEW FILLED SURFACES
        self.background.fill(GREY)
        self.background.blit(self.screen, (0, 0))
        # draw spins
        for row in range(self.NSpins):
            for col in range(self.NSpins):
                val = BLACK if self.lattice[row, col] == 1 else WHITE
                surf = pygame.Surface((self.dx, self.dy))
                surf.fill(val)
                surf_centre = (self.dx*col, self.dy*row)
                self.screen.blit(surf, surf_centre)

        # insert text
        text_surface, rect = GAME_FONT.render(f"B: {self.B}", (0, 0, 0), GREY)
        self.background.blit(text_surface, (WIDTH * 1.01, HEIGHT * 0.01))
        text_kT, rect = GAME_FONT.render(f"kT: {self.kT}", (0, 0, 0), GREY)
        self.background.blit(text_kT, (WIDTH * 1.01, HEIGHT * 0.01 + self.dy))
        text_surface, rect = GAME_FONT.render(f"m: {self.GetAvgMagnetisation()}", (0, 0, 0), GREY)
        self.background.blit(text_surface, (WIDTH * 1.01, HEIGHT * 0.01 + self.dy*2))
        text_surface, rect = GAME_FONT.render(f"E: {self.GetAvgEnergy()}", (0, 0, 0), GREY)
        self.background.blit(text_surface, (WIDTH * 1.01, HEIGHT * 0.01 + self.dy*3))

        # controls
        controls_title, rect = GAME_FONT.render(f"Controls:", (0, 0, 0), GREY)
        controls_B, rect = GAME_FONT.render(r"B up/down: U/J", (0, 0, 0), GREY)
        controls_kT, rect = GAME_FONT.render(r"T up/down: T/G", (0, 0, 0), GREY)
        controls_quit, rect = GAME_FONT.render(r"Quit: ESCAPE", (0, 0, 0), GREY)
        self.background.blit(controls_title, (WIDTH * 1.01, HEIGHT - self.dy*4))
        self.background.blit(controls_B, (WIDTH * 1.01, HEIGHT - self.dy*3))
        self.background.blit(controls_kT, (WIDTH * 1.01, HEIGHT - self.dy*2))
        self.background.blit(controls_quit, (WIDTH * 1.01, HEIGHT - self.dy*1))

        self.background.blit(self.screen, (0, 0))

        return None

# run
game = InteractiveIsing(WIDTH=WIDTH, HEIGHT=HEIGHT, FPS=FPS, infoSize=InfoSize)
game.mainLoop()