import pygame
import math

screen = pygame.display.set_mode((1024, 768), pygame.NOFRAME);
screen.fill((0, 0, 0));

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

        self.drawButtons();
        self.drawTorches();
    
    # Update the entirely menu
    def updateMenu(self):
        screen.blit(self.bgimage, (0, 0));
        screen.blit(self.logo, (294, 0));

        self.drawButtons();

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