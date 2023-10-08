# All the necessary library imports for the game
import pygame
import numpy as np
import math

# pygame setup required variables
pygame.init();
screen = pygame.display.set_mode((1024, 768), pygame.NOFRAME);
screen.fill((0, 0, 0));
screenType = 'Menu'; lastScreenType = screenType;
clock = pygame.time.Clock();

# Priority variable for running code
running = True;
dictButtons = {};

# Sound mixer initializing and simple configuration
pygame.mixer.init();
pygame.mixer.music.set_volume(0);
# Necessary sound variables
selectSound = pygame.mixer.Sound('Sounds\\selectSound.mp3');

# Test if mixer was initialized
if (pygame.mixer.get_init() != True):
    pygame.mixer.init();


# Base colors


# Gives a fade effect to the screen in and out 
class fade():

    def backgroundFade(bgimage, type, value):
        # Cooldown variables for delay
        lastTick = pygame.time.get_ticks();
        cooldownFade = 30;

        # Fade effect on background when game ends
        if (type == 'in'):
            fade = 0;
            ckey = pygame.Surface((screen.get_width(), screen.get_height()), flags = pygame.SRCALPHA).convert();
            ckey.fill((0, 0, 0));
            while (fade < 256):
                if ((pygame.time.get_ticks() - lastTick)  >=  cooldownFade):
                    lastTick = pygame.time.get_ticks();
                    ckey.set_alpha(fade);
                    fade += value;
                    screen.blit(ckey, (0, 0));
                    pygame.display.flip()

        # Fade effect on background when game starts
        elif (type == 'out'):
            fade = 0;
            while (fade < 256):
                if ((pygame.time.get_ticks() - lastTick)  >=  cooldownFade):
                    lastTick = pygame.time.get_ticks();
                    bgimage.set_alpha(fade);
                    fade += value;
                    screen.blit(bgimage, (0, 0));
                    pygame.display.flip()
        
    # Gives a fade effect on the music when game starts and ends
    def musicFade(type):
        # Cooldown variables for delay
        lastTick = pygame.time.get_ticks();
        cooldownMusic = 60;

        # Fade effect on music when game starts
        if (type == 'in'):
            volume = 0.01;
            while (volume < 0.41):
                if ((pygame.time.get_ticks() - lastTick)  >=  cooldownMusic):
                    lastTick = pygame.time.get_ticks();
                    pygame.mixer.music.set_volume(volume);
                    volume += 0.01;
        
        # Fade effect on music when game ends
        elif (type == 'out'):
            volume = 0.4;
            while (volume > 0):
                if ((pygame.time.get_ticks() - lastTick)  >=  cooldownMusic):
                    lastTick = pygame.time.get_ticks();
                    pygame.mixer.music.set_volume(volume);
                    volume -= 0.01;

# Class that would make the menu screen entirely
class menu():

    def __init__(self):
        # Music mixer start and calls fade effect on it
        pygame.mixer.music.load('Sounds\\MenuStart.mp3');
        pygame.mixer.music.play(-1); 
        fade.musicFade('in'); 
        self.menuScreen;

    def menuScreen(self):
        self.frameIndex = 0;   

        # Background image loand and calls fade effect on it
        self.bgimage = pygame.image.load('Images\\Backgrounds\\BackgroundMenu.png').convert();
        self.bgimage.set_alpha(0);
        screen.blit(self.bgimage, (0, 0));
        fade.backgroundFade(self.bgimage, 'out', 5);
                
        self.logo = pygame.image.load('Images\\Assets\\logo.png').convert_alpha();
        screen.blit(self.logo, (294, 0));

        # List of menu buttons variables
        self.listButtonsImages = ['playButton.png', 'shopButton.png', 'MenuButtons.png', 'quitButton.png', 'optionsButton.png'];
        self.listButtonsCords = [(385, 389), (385, 494), (385, 599), (20, 700), (919, 42)]; self.dictButtons = {};

        Menu.drawButtons();
        Menu.drawTorches();
    
    # Update the entirely menu
    def updateMenu(self):
        screen.blit(self.bgimage, (0, 0));
        screen.blit(self.logo, (294, 0));

        Menu.drawButtons();

        # Get the next torch sprite
        self.torchImage = self.listTorchesImages[self.frameIndex];
 
        # Shows up the torch sprite onto the screen
        screen.blit(self.torchImage, self.listTorchesCords[0]);
        screen.blit(self.torchImage, self.listTorchesCords[1]);
        if (self.frameIndex >= 5):
            self.frameIndex = 0;
        self.frameIndex += 1;

    # Draw the buttons on the screen
    def drawButtons(self):
        self.dictButtons;
        
        # Blit() menu buttons onto the screen and save them on a dictionary
        for i in range(len(self.listButtonsImages)):
            key = self.listButtonsImages[i];
            buttonImage = pygame.image.load(f'Images\\Buttons\\{self.listButtonsImages[i]}').convert_alpha();
            if (i == 3):
                buttonImage = pygame.transform.scale(buttonImage, (120, 50));
            imageRect = buttonImage.get_rect();
            imageRect = imageRect.move(self.listButtonsCords[i]);
            if (key not in self.dictButtons):
                self.dictButtons[key] = imageRect;
            screen.blit(buttonImage, self.listButtonsCords[i]);

    # Draw the torches on the screen
    def drawTorches(self):
        # Functinon to load torch animation in menu screen
        self.listTorchesNames = ['torch1.png', 'torch2.png', 'torch3.png', 'torch4.png', 'torch5.png', 'torch6.png'];
        self.listTorchesCords = [(50, 180), (831, 180)];
        self.listTorchesImages = [];
        for i in self.listTorchesNames:
            self.torchImages = pygame.image.load(f'Images\\Assets\\Torch\\{i}').convert_alpha();
            self.torchImages = pygame.transform.scale(self.torchImages, (143, 143));
            self.listTorchesImages.append(self.torchImages);
                
# Class for load the play menu 
class play():
    def playScreen(self):

        self.bgimage = pygame.image.load('Images\\Backgrounds\\BackgroundPvMode.png').convert();
        self.bgimage.set_alpha(0);
        screen.blit(self.bgimage, (0, 0));
        fade.backgroundFade(self.bgimage, 'out', 5);

        # List of menu buttons variables
        self.listButtonsImages = ['pveButton.png', 'pvpButton.png', 'optionsButton.png', 'setaE.png'];
        self.listButtonsCords = [(150, 600), (621, 600), (919, 42), (43, 42)]; self.dictButtons = {};

        # Functinon to load slime animation in menu screen
        self.listSlimeNames = ['Slime1.png', 'Slime2.png', 'Slime3.png', 'Slime4.png'];
        self.listSlimeCords = [(246, 530)];
        self.listSlimeImages = [];

        for i in self.listSlimeNames:
            SlimeImages = pygame.image.load(f'Images\\Monsters\\Slime\\Idle\\{i}').convert_alpha();
            self.listSlimeImages.append(SlimeImages);
        
        # Functinon to load slime animation in menu screen
        self.listKnightNames = ['Knight1.png', 'Knight2.png', 'Knight3.png', 'Knight4.png', 'Knight5.png', 'Knight6.png', 'Knight7.png', 'Knight8.png', 'Knight9.png', 'Knight10.png'];
        self.listKnightCords = [(697, 455)];
        self.listKnightImages = [];

        for i in self.listKnightNames:
            KnightImages = pygame.image.load(f'Images\\Players\\Knight\\Run\\{i}').convert_alpha();
            self.listKnightImages.append(KnightImages);

        self.scroll = 0;
        self.tiles = math.ceil(screen.get_width() / self.bgimage.get_width()) + 1;

        self.drawButtons();
        self.drawIdles(0, 0);

    def drawButtons(self):
        self.dictButtons;

        # Blit() menu buttons onto the screen and save them on a dictionary
        for i in range(len(self.listButtonsImages)):
            key = self.listButtonsImages[i];
            buttonImage = pygame.image.load(f'Images\\Buttons\\{self.listButtonsImages[i]}').convert_alpha();
            imageRect = buttonImage.get_rect();
            imageRect = imageRect.move(self.listButtonsCords[i]);
            if (key not in self.dictButtons):
                self.dictButtons[key] = imageRect;
            screen.blit(buttonImage, self.listButtonsCords[i]);
    
    def drawIdles(self, indexS, indexK):
        SlimeImages = self.listSlimeImages[indexS];
        screen.blit(SlimeImages, self.listSlimeCords[0]);
        KnightImages = self.listKnightImages[indexK];
        screen.blit(KnightImages, self.listKnightCords[0]);

    # Update the torch animatioon to the next sprite
    def updatePlayMode(self, index1, index2):

        self.drawButtons();
        self.drawIdles(index1, index2);
        
# Class for the PVE mode required on the PDF
class pve():
    def selectScreen(self):     
        # Background image loand and calls fade effect on it
        self.bgimage = pygame.image.load('Images\\Backgrounds\\BackgroundPve1.png').convert();
        self.bgimage.set_alpha(0);
        screen.blit(self.bgimage, (0, 0));
        fade.backgroundFade(self.bgimage, 'out', 5);

        self.listHeroes = [];

        # List of menu buttons variables
        self.listHeroesTypes = ['Barbarian', 'Monk', 'Ranger', 'Cleric', 'Mage']
        self.listButtonsImages = ['Barbarian0.png', 'Monk0.png', 'Ranger0.png', 'Cleric0.png', 'Mage0.png'];
        self.listButtonsCords = [(150, 150), (425, 150), (700, 150), (285, 415), (565, 415)]; self.dictButtons = {};

        self.midBlack = pygame.image.load('Images\\Backgrounds\\BackgroundOptions.png').convert_alpha();
        self.midBlack.set_alpha(255);
        self.teamScreen(0)

    def teamScreen(self, index):
        screen.blit(self.midBlack, (75, 75));
        self.drawButtons(index);

    def updatePveMode(self, index):
        screen.blit(self.bgimage, (0, 0));
        if (len(self.listHeroes) < 3):
            self.teamScreen(index);
        else:
            self.combatScreen()

    def drawButtons(self, indexIdle):
        self.dictButtons = {};

        # Blit() menu buttons onto the screen and save them on a dictionary
        for i in range(len(self.listHeroesTypes)):
            key = self.listHeroesTypes[i] + '0.png';
            buttonImage = pygame.image.load(f'Images\\Players\\{self.listHeroesTypes[i]}\\{(self.listHeroesTypes[i] + str(indexIdle) + '.png')}').convert_alpha();
            imageRect = buttonImage.get_rect();
            imageRect = imageRect.move(self.listButtonsCords[i]);
            if (key not in self.dictButtons):
                self.dictButtons[key] = imageRect;
            screen.blit(buttonImage, self.listButtonsCords[i]);

    def combatScreen(self):
        print(self.listHeroes)
        self.updateAnimations();
        self.skillBar();


# Call the screen that will be loaded according to the button clicked
def updateScreenType(typeButton):
    global running;
    global screenType;
    global lastScreenType;

    print(typeButton)

    if (typeButton == 'playButton.png'):
        screenType = 'PlayMode';
        fade.backgroundFade(True, 'in', 25);
        Play.playScreen();
    elif (typeButton == 'shopButton.png'):
        return
        # Shop.interface();
    elif (typeButton == 'MenuButtons.png'):
        return
    elif (typeButton == 'optionsButton.png'):
        return
    elif (typeButton == 'quitButton.png'):
        running = False;
        fade.musicFade('out');
        fade.backgroundFade(True, 'in', 3);
    elif (typeButton == 'setaE.png'):
        screenType = lastScreenType
        if lastScreenType == 'Menu':
            fade.backgroundFade(True, 'in', 25);
            fade.backgroundFade(Menu.bgimage, 'out', 25);
            Menu.menuScreen;
    elif (typeButton == 'pvpButton.png'):
        return
    elif (typeButton == 'pveButton.png'):
        screenType = 'PVE'
        fade.backgroundFade(True, 'in', 25);
        Pve.selectScreen();
    
    

# Necessary class variables for general access
Play = play();
Menu = menu();
Pve = pve();

def main():
    # Global variables
    global running;
    global screenType;
    global lastScreenType;
    global selectSound;

    # Shows the game menu when execute
    Menu.menuScreen();
    
    indexIdle1 = 0;
    indexIdle2 = 0;
    indexIdle3 = 0;
    contTime = 0;

    # Cooldown variables for delay
    lastTick = pygame.time.get_ticks();

    while running:
    
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;
                fade.musicFade('out');
                fade.backgroundFade(True, 'in', 3);
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos(); # Now it will have the coordinates of click point
                if (screenType == 'Menu'):
                    for (key, value) in Menu.dictButtons.items():
                        if (value.collidepoint(mouse_pos)):
                            selectSound.play();
                            if (value == Menu.dictButtons[key]):              
                                if (key != screenType):
                                    screenType == key
                                updateScreenType(key);
                elif (screenType == 'PlayMode'):
                    for (key, value) in Play.dictButtons.items():
                        if (value.collidepoint(mouse_pos)):
                            selectSound.play();
                            if (value == Play.dictButtons[key]):
                                if (key != screenType):
                                    screenType == key       
                                updateScreenType(key);
                elif (screenType == 'PVE'):
                    for (key, value) in Pve.dictButtons.items():
                        if (value.collidepoint(mouse_pos)):
                            if (value == Pve.dictButtons[key]):
                                selectSound.play();
                                if (key != screenType):
                                    screenType == key
                                if (key in Pve.dictButtons):
                                    if (Pve.listHeroesTypes[list(Pve.dictButtons).index(key)] not in Pve.listHeroes) and (len(Pve.listHeroes) < 3):
                                        Pve.listHeroes.append(Pve.listHeroesTypes[list(Pve.dictButtons).index(key)])
                            
                                
                                    
        if (screenType == 'Menu'):
            if ((pygame.time.get_ticks() - lastTick)  >=  180):
                lastTick = pygame.time.get_ticks();
                Menu.updateMenu();
        elif (screenType == 'PlayMode'):
            Play.scroll -= 5;
            if (contTime == 5):
                for i in range(0, Play.tiles):
                    screen.blit(Play.bgimage, (i * Play.bgimage.get_width() + Play.scroll, 0))
                if (abs(Play.scroll) > Play.bgimage.get_width()):
                    Play.scroll = 0;
                contTime = 0;
            Play.drawButtons();
            if ((pygame.time.get_ticks() - lastTick)  >=  60):
                lastTick = pygame.time.get_ticks();
                Play.updatePlayMode(indexIdle1, indexIdle2);
                if (indexIdle1 >= 3):
                    indexIdle1 = 0;
                if (indexIdle2 >= 9):
                    indexIdle2 = 0;
                indexIdle1 += 1;
                indexIdle2 += 1;
            contTime += 1;
        elif (screenType == 'PVE'):
            if ((pygame.time.get_ticks() - lastTick)  >=  240):
                lastTick = pygame.time.get_ticks();
                if (indexIdle3 >= 4):
                    indexIdle3 = 0;
                Pve.updatePveMode(indexIdle3);
                indexIdle3 += 1;

        # RENDER YOUR GAME HERE
        
        pygame.display.set_caption(screenType)
        pygame.display.flip(); # Update game screen
        clock.tick(60);  # limits FPS to 60

    pygame.quit();


main();