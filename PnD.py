# All the necessary library imports for the game
import pygame ; import numpy as np ; import math ; import random
# All necessary .py archives
import menus

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


# Group variable
allChars = pygame.sprite.Group()

class char(pygame.sprite.Sprite):
    def __init__(self, image, hp, atk, defP, speed, coords):
        pygame.sprite.Sprite.__init__(self)
        self.hp = hp;
        self.atk = atk;
        self.defP = defP;
        self.speed = speed;
        self.image = image;
        self.image = pygame.transform.scale(self.image, (100, 100));
        self.rect = self.image.get_rect() ;
        self.rect = self.rect.move(coords);
        screen.blit(self.image, coords);
        self.explain(image);

    def explain(self, image):
        print(f'Nome: {image}, Speed: {self.speed}, HP: {self.hp}, def: {self.defP}, atk: {self.atk}')
        



# Class for the PVE mode required on the PDF
class pve():
    def selectScreen(self):     
        # Background image loand and calls fade effect on it
        self.bgimage = pygame.image.load('Images\\Backgrounds\\BackgroundPve1.png').convert();
        self.bgimage.set_alpha(0);
        screen.blit(self.bgimage, (0, 0));
        menus.fade.backgroundFade(self.bgimage, 'out', 5);

        self.listHeroes = [];

        # List of menu buttons variables
        self.listHeroesTypes = ['Paladin', 'Monk', 'Ranger', 'Cleric', 'Mage']
        self.listButtonsImages = ['Paladin.png', 'Monk.png', 'Ranger.png', 'Cleric.png', 'Mage.png'];
        self.listButtonsCords = [(150, 150), (425, 150), (700, 150), (285, 415), (565, 415)]; self.dictButtons = {};

        self.midBlack = pygame.image.load('Images\\Backgrounds\\BackgroundOptions.png').convert_alpha();
        self.midBlack.set_alpha(255);
        self.teamScreen(0)

    def teamScreen(self, index):
        screen.blit(self.midBlack, (75, 75));
        self.drawButtons(index);

    def updatePveMode(self, index):
        global screenType;

        screen.blit(self.bgimage, (0, 0));
        if (len(self.listHeroes) < 3):
            self.teamScreen(index);
        else:
            screenType = 'Combat';

    def drawButtons(self, indexIdle):
        self.dictButtons = {};

        # Blit() menu buttons onto the screen and save them on a dictionary
        for i in range(len(self.listHeroesTypes)):
            key = self.listHeroesTypes[i] + '.png';
            buttonImage = pygame.image.load(f'Images\\Players\\{self.listHeroesTypes[i]}\\{(self.listHeroesTypes[i] + '.png')}').convert_alpha();
            buttonImage = pygame.transform.scale(buttonImage, (150, 150))
            imageRect = buttonImage.get_rect();
            imageRect = imageRect.move(self.listButtonsCords[i]);
            if (key not in self.dictButtons):
                self.dictButtons[key] = imageRect;
            screen.blit(buttonImage, self.listButtonsCords[i]);

    def combatScreen(self):
        allChars.update()
        allChars.draw(screen)
        # self.skillBar();

    def createHeroes(self):
        coords = [(250, 220), (200, 420), (250, 620)];
        for i in range(len(self.listHeroes)):
            Image = pygame.image.load(f'Images\\Players\\{self.listHeroes[i]}\\{(self.listHeroes[i] + '.png')}').convert_alpha();
            Image = pygame.transform.scale(Image, (70, 70));
            imageRect = Image.get_rect();
            imageRect = imageRect.move(coords[i]);
            allChars.add(char(Image, 50, 10, 5, (random.randrange(1, 10)), coords[i]));

    def createEnemys(self):
        coords = [(724, 320), (724, 520)];
        for i in range(2):
            Image = pygame.image.load(f'Images\\Monsters\\Skull.png').convert_alpha();
            imageRect = Image.get_rect();
            imageRect = imageRect.move(coords[i]);
            allChars.add(char(Image, 50, 10, 5, (random.randrange(1, 10)), coords[i]));

    def skillBar():
        pass


# Call the screen that will be loaded according to the button clicked
def updateScreenType(typeButton):
    global running;
    global screenType;
    global lastScreenType;

    print(typeButton)

    if (typeButton == 'playButton.png'):
        screenType = 'PlayMode';
        menus.fade.backgroundFade(True, 'in', 25);
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
        menus.fade.musicFade('out');
        menus.fade.backgroundFade(True, 'in', 3);
    elif (typeButton == 'setaE.png'):
        screenType = lastScreenType
        if lastScreenType == 'Menu':
            menus.fade.backgroundFade(True, 'in', 25);
            menus.fade.backgroundFade(Menu.bgimage, 'out', 25);
            Menu.menuScreen;
    elif (typeButton == 'pvpButton.png'):
        return
    elif (typeButton == 'pveButton.png'):
        screenType = 'PVE'
        menus.fade.backgroundFade(True, 'in', 25);
        Pve.selectScreen();
    
    

# Necessary class variables for general access
Play = menus.play();
Menu = menus.menu();
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
    oneTime = 0;

    # Cooldown variables for delay
    lastTick = pygame.time.get_ticks();

    while running:
    
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;
                menus.fade.musicFade('out');
                menus.fade.backgroundFade(True, 'in', 3);
            
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
                                    screenType == key;   
                                updateScreenType(key);
                elif (screenType == 'PVE'):
                    for (key, value) in Pve.dictButtons.items():
                        if (value.collidepoint(mouse_pos)):
                            if (value == Pve.dictButtons[key]):
                                selectSound.play();
                                if (key != screenType):
                                    screenType == key;
                                if (key in Pve.dictButtons):
                                    if (Pve.listHeroesTypes[list(Pve.dictButtons).index(key)] not in Pve.listHeroes) and (len(Pve.listHeroes) < 3):
                                        Pve.listHeroes.append(Pve.listHeroesTypes[list(Pve.dictButtons).index(key)]);
                                            
                            
                                
                                    
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
        elif (screenType == 'Combat'):
            if oneTime == 0:
                Pve.createHeroes();
                Pve.createEnemys();
                oneTime = 1;
            Pve.combatScreen();
            print(allChars)

        

        # RENDER YOUR GAME HERE
        
        pygame.display.set_caption(screenType)
        pygame.display.flip(); # Update game screen
        clock.tick(60);  # limits FPS to 60

    pygame.quit();


main();
