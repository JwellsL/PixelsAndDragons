# All the necessary library imports for the game
import pygame ; import math ; import random ; import operator
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
selectSound = pygame.mixer.Sound('Sounds\\selectSound.mp3');

# Test if mixer was initialized
if (pygame.mixer.get_init() != True):
    pygame.mixer.init();

#Font variable
font = pygame.font.Font('Fonts\\AGoblinAppears-o2aV.ttf', 18)

# Group variable
Heroes = pygame.sprite.Group();
Enemys = pygame.sprite.Group();

# Char stats variable
# ((8-25), (8-25), (5-20), 'AP/AD')
mageStats = (9, 24, 6, 6, 'AP');
PaladinStats = (25, 11, 15, 12, 'AD');
monkStats = (19, 16, 9, 8, 'AD');
rangerStats = (14, 13, 12, 8, 'AD');
clericStats = (11, 9, 11, 13, 'AP');
skullStats = (40, 15, 10, 20, 'AD');

# Variable list for speed (can't be repeated in d&d)
allSpeed = []

# Another variables
dictButtons = {};
turnDict = {};
listTurn = [];
indexTurn = 0;


class char(pygame.sprite.Sprite):
    def __init__(self, image, hp, atk, fdef, mdef, typeAtk, speed, coords, name):
        pygame.sprite.Sprite.__init__(self)
        self.id = name;
        self.hp = hp;
        self.maxHp = hp;
        self.atk = atk;
        self.fisicalDef = fdef;
        self.magicalDef = mdef;
        self.speed = speed;
        self.type = typeAtk;
        self.image = image;
        self.IndexDefense = 0;
        self.state = ''; #Idle, defense
        self.image = pygame.transform.scale(self.image, (70, 70));
        self.rect = self.image.get_rect() ;
        self.rect = self.rect.move(coords);
        screen.blit(self.image, coords);
        self.explain();

    def explain(self):
        print(f'Nome: {self.id}, Speed: {self.speed}, HP: {self.hp}, defT: {self.fisicalDef + self.magicalDef}, atk: {self.atk}');

    def getSpeed(self):
        return self.speed;

    def getId(self):
        return self.id;

    def getHp(self):
        return self.hp;

    def getMaxHp(self):
        return self.hp;

    def attack(self, Char):
        if self.type == 'AD':
            Char.hp = Char.hp - ((self.atk) * (50/(50 + (Char.fisicalDef))));
        else:
            Char.hp = Char.hp - ((self.atk) * (50/(50 + (Char.magicalDef))));
        print(f'hp: {Char.hp}/{Char.maxHp}')
    
    def setDefense(self):
        self.IndexDefense = 1;
        self.fisicalDef = self.fisicalDef * 2;
        self.magicalDef = self.magicalDef * 2;
        return; 
            

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

class combat():
    def combatScreen(self, indexTurn):
        global dictButtons;
        Heroes.update() ; Enemys.update();
        Heroes.draw(screen) ; Enemys.draw(screen);
        self.menuBar();
        self.drawText(indexTurn);

    def menuBar(self):
        coords = [(10, 508), (739, 508)];
        bar = ['menuBar', 'infoBar']
        for i in range(2):
            image = pygame.image.load(f'Images\\Assets\\{bar[i]}.png').convert_alpha();
            screen.blit(image, coords[i]);

    def drawText(self, index):
        persona = listTurn[index];
        # Coordinates for HP/MAXHP text
        coords = [550, 625, 700]

        attackText = font.render(f"Attack", True, (0, 0, 0));
        attackRect = attackText.get_rect(); attackRect.move((445, 604));
        dictButtons['Attack'] = attackRect;
        skillText = font.render(f"Skill", True, (0, 0, 0));
        skillRect = skillText.get_rect(); skillRect.move((445, 604));
        dictButtons['Skill'] = skillRect;
        defendText = font.render(f"Defend", True, (0, 0, 0));
        defendRect = defendText.get_rect(); defendRect.move((445, 604));
        dictButtons['Defend'] = defendRect;

        if (persona.getId() == 'Skull0' or persona.getId() == 'Skull1'):
            text = font.render(f"It's enemy's turn!", True, (0, 0, 0));
        else:
            text = font.render(f"It's {persona.getId()} turn!", True, (0, 0, 0)); 
        # Codes for the menu bar text
        screen.blit(text, (196, 528));
        screen.blit(attackText, (108, 604));
        screen.blit(defendText, (445, 604));
        screen.blit(skillText, (136, 683));
        # Codes for the stats bar text
        for i in range(3):
                textHp = font.render(f'{Heroes.sprites()[i].getId()}:  {Heroes.sprites()[i].getHp()}/{Heroes.sprites()[i].getMaxHp()}', True, (0, 0, 0));
                screen.blit(textHp, (760, coords[i]));

        

def createHeroes():
    coords = [(250, 220), (200, 320), (250, 420)];
    for i in range(len(Pve.listHeroes)):
        image = pygame.image.load(f'Images\\Players\\{Pve.listHeroes[i]}\\{(Pve.listHeroes[i] + '.png')}').convert_alpha();
        image = pygame.transform.scale(image, (150, 150));
        name = str(Pve.listHeroes[i])
        speed = random.randrange(1, 20);
        while speed in allSpeed:
            speed = random.randrange(1, 20);
        allSpeed.append(speed)
        if (Pve.listHeroes[i] == 'Paladin'):
            Paladin = char(image, *PaladinStats, speed, coords[i], name)
            Heroes.add(Paladin); turnDict[Paladin] = Paladin.getSpeed();
        elif (Pve.listHeroes[i] == 'Mage'):
            Mage = char(image, *mageStats, speed, coords[i], name)
            Heroes.add(Mage); turnDict[Mage] = Mage.getSpeed();
        elif (Pve.listHeroes[i] == 'Cleric'):
            Cleric = char(image, *clericStats, speed, coords[i], name)
            Heroes.add(Cleric); turnDict[Cleric] = Cleric.getSpeed();
        elif (Pve.listHeroes[i] == 'Ranger'):
            Ranger = char(image, *rangerStats, speed, coords[i], name)
            Heroes.add(Ranger); turnDict[Ranger] = Ranger.getSpeed();
        elif (Pve.listHeroes[i] == 'Monk'):
            Monk = char(image, *monkStats, speed, coords[i], name)
            Heroes.add(Monk); turnDict[Monk] = Monk.getSpeed();

def createEnemys():
    coords = [(724, 220), (724, 420)];
    for i in range(2):
        image = pygame.image.load(f'Images\\Monsters\\Skull.png').convert_alpha();
        image = pygame.transform.scale(image, (200, 200));
        name = 'Skull' + str(i);
        speed = random.randrange(1, 20); 
        
        while speed in allSpeed:
            speed = random.randrange(1, 20);
        allSpeed.append(speed)
        if (i == 0):
            Skull1 = char(image, *skullStats, speed, coords[i], name)
            Enemys.add(Skull1); turnDict[Skull1] = char.getSpeed(Skull1);
            dictButtons[Skull1] = Skull1.rect;
        else:
            Skull2 = char(image, *skullStats, speed, coords[i], name)
            Enemys.add(Skull2); turnDict[Skull2] = char.getSpeed(Skull2);
            dictButtons[Skull2] = Skull2.rect;

def sortDictTurn():
    global listTurn; global turnDict;
    turnDict = dict(sorted(turnDict.items(), key=operator.itemgetter(1),reverse=True))
    for i in turnDict.keys():
        listTurn.append(i);


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

def action(typeButton, indexTurn, selectedChar):
    if (typeButton == 'Attack'):
        listTurn[indexTurn].attack(selectedChar)
    
# Necessary class variables for general access
Play = menus.play();
Menu = menus.menu();
Pve = pve();
Combat = combat();

def main():
    # Global variables
    global running;
    global screenType;
    global lastScreenType;
    global selectSound;
    global turnDict;
    global indexTurn;

    # Shows the game menu when execute
    Menu.menuScreen();
    
    indexIdle1 = 0;
    indexIdle2 = 0;
    indexIdle3 = 0;
    contTime = 0;
    oneTime = 0;
    selectedChar = '';

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
                elif (screenType == 'Combat'):
                    for (key, value) in dictButtons.items():
                        if selectedChar != '':
                            print('aqui')
                            print(selectedChar);
                            if (value.collidepoint(mouse_pos)):
                                if (value == dictButtons[key]): 
                                    print('aqui2')  
                                    action(key, indexTurn, selectedChar);
                        elif key in listTurn:
                            selectedChar = key;
                            print(selectedChar);
                                
                                                       
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
                createHeroes();
                createEnemys();
                oneTime = 1;
                sortDictTurn();
                print(turnDict);
            Combat.combatScreen(indexTurn);

        # Game render
        pygame.display.flip(); # Update game screen
        clock.tick(60);  # limits FPS to 60

    pygame.quit();


main();
