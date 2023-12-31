# All the necessary library imports for the game
import pygame ; import numpy as np ; import math ; import random
# All necessary .py archives
import menus ;

# pygame setup required variables
pygame.init();
screen = pygame.display.set_mode((1024, 768), pygame.NOFRAME);
screen.fill((0, 0, 0));
screenType = 'Menu'; lastScreenType = screenType;
clock = pygame.time.Clock();

# Priority variable for running code
running = True;

# Sound mixer initializing and simple configuration
pygame.mixer.init();
pygame.mixer.music.set_volume(0);
# Necessary sound variables
selectSound = pygame.mixer.Sound('selectSound.mp3');

# Test if mixer was initialized
if (pygame.mixer.get_init() != True):
    pygame.mixer.init();

# Group variable
Heroes = pygame.sprite.Group();
Enemys = pygame.sprite.Group();
# Another variables
dictButtons = {};
turnDict = {};

# Char stats variable
# ((8-25), (8-25), (5-20), 'AP/AD')
mageStats = (9, 24, 6, 6, 'AP');
knightStats = (25, 11, 15, 12, 'AD');
monkStats = (19, 16, 9, 8, 'AD');
rangerStats = (14, 13, 12, 8, 'AD');
clericStats = (11, 9, 11, 13, 'AP');

class char(pygame.sprite.Sprite):
    def __init__(self, image, hp, atk, fdef, mdef, typeAtk, speed, coords, name):
        pygame.sprite.Sprite.__init__(self);
        self.id = name;
        self.hp = hp;
        self.maxHp = hp;
        self.atk = atk;
        self.fisicalDef = fdef;
        self.magicalDef = mdef;
        self.speed = speed;
        self.type = typeAtk;
        self.image = image;
        self.image = pygame.transform.scale(self.image, (70, 70));
        self.rect = self.image.get_rect() ;
        self.rect = self.rect.move(coords);
        screen.blit(self.image, coords);
        self.explain();

    def explain(self):
        print(f'Nome: {self.id}, Speed: {self.speed}, HP: {self.hp}, defT: {self.fisicalDef + self.magicalDef}, atk: {self.atk}')

    def getSpeed(self):
        return self.speed;


# Class for the PVE mode required on the PDF
class pve():
    def selectScreen(self):     
        # Background image loand and calls fade effect on it
        self.bgimage = pygame.image.load('BackgroundPve1.png').convert();
        self.bgimage.set_alpha(0);
        screen.blit(self.bgimage, (0, 0));
        menus.fade.backgroundFade(self.bgimage, 'out', 5);

        self.listHeroes = [];

        # List of menu buttons variables
        self.listHeroesTypes = ['Paladin', 'Monk', 'Ranger', 'Cleric', 'Mage'];
        self.listButtonsImages = ['Paladin.png', 'Monk.png', 'Ranger.png', 'Cleric.png', 'Mage.png'];
        self.listButtonsCords = [(150, 150), (425, 150), (700, 150), (285, 415), (565, 415)]; self.dictButtons = {};

        self.midBlack = pygame.image.load('BackgroundOptions.png').convert_alpha();
        self.midBlack.set_alpha(255);
        self.teamScreen();

    def teamScreen(self):
        screen.blit(self.midBlack, (75, 75));
        self.drawButtons();

    def updatePveMode(self, index):
        global screenType;

        screen.blit(self.bgimage, (0, 0));
        if (len(self.listHeroes) < 3):
            self.teamScreen();
        else:
            screenType = 'Combat';
            
    def drawButtons(self):
        self.dictButtons = {};

        # Blit() menu buttons onto the screen and save them on a dictionary
        for i in range(len(self.listHeroesTypes)):
            key = self.listHeroesTypes[i] + '.png';
            buttonImage = pygame.image.load(f'{key}').convert_alpha();
            buttonImage = pygame.transform.scale(buttonImage, (150, 150))
            imageRect = buttonImage.get_rect();
            imageRect = imageRect.move(self.listButtonsCords[i]);
            if (key not in self.dictButtons):
                self.dictButtons[key] = imageRect;
            screen.blit(buttonImage, self.listButtonsCords[i]);

    def combatScreen(self):
        Heroes.update() ; Enemys.update();
        Heroes.draw(screen) ; Enemys.draw(screen);
        # self.skillBar();

    def createHeroes(self):
        global knightStats ; global mageStats ; global rangerStats ; global monkStats ; global clericStats;
        coords = [(250, 220), (200, 420), (250, 620)];
        for i in range(len(self.listHeroes)):
            Image = pygame.image.load(f'{self.listButtonsImages[i]}').convert_alpha();
            Image = pygame.transform.scale(Image, (70, 70));
            imageRect = Image.get_rect();
            imageRect = imageRect.move(coords[i]);
            if (self.listHeroes[i] == 'Paladin'):
                Heroes.add(char(Image, knightStats, (random.randrange(1, 21)), coords[i], 'paladin'));
            elif (self.listHeroes[i] == 'Mage'):
                Heroes.add(char(Image, mageStats, (random.randrange(1, 21)), coords[i], 'mage'));
            elif (self.listHeroes[i] == 'Cleric'):
                Heroes.add(char(Image, clericStats, (random.randrange(1, 21)), coords[i], 'cleric'));
            elif (self.listHeroes[i] == 'Ranger'):
                Heroes.add(char(Image, rangerStats, (random.randrange(1, 21)), coords[i], 'ranger'));
            elif (self.listHeroes[i] == 'Monk'):
                Heroes.add(char(Image, monkStats, (random.randrange(1, 21)), coords[i], 'monk'));



    def createEnemys(self):
        coords = [(724, 320), (724, 520)];
        for i in range(2):
            Image = pygame.image.load(f'Skull.png').convert_alpha();
            imageRect = Image.get_rect();
            imageRect = imageRect.move(coords[i]);
            Enemys.add(char(Image, 50, 10, 5, 'AD', (random.randrange(1, 20)), coords[i]), 'skull');

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
    global turnDict;

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
                turnDict = sorted(turnDict.items(), key = lambda x:x[1]);
                print(turnDict);
            Pve.combatScreen();

        

        # RENDER YOUR GAME HERE
        
        pygame.display.set_caption(screenType)
        pygame.display.flip(); # Update game screen
        clock.tick(60);  # limits FPS to 60

    pygame.quit();


main();
