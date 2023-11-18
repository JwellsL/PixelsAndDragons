# Todas as bibliotecas necessárias 
import pygame ; import math ; import random ; import operator
# Todos arquivos .py necessários 
import menus ;

# Variáveis necessárias para inicialização do pygame
pygame.init();
screen = pygame.display.set_mode((1024, 768)); #pygame.NOFRAME
screen.fill((0, 0, 0));
screenType = 'Menu'; lastScreenType = screenType;
clock = pygame.time.Clock();

# Variável prioridade para rodar o código 
running = True;

# Inicialização e simples configuracao do pygame.mixer
pygame.mixer.init();
pygame.mixer.music.set_volume(0);
# Necessary sound variables
selectSound = pygame.mixer.Sound('selectSound.mp3');

# Testar se o mixer foi inicializado
if (pygame.mixer.get_init() != True):
    pygame.mixer.init();

# Variável de fonte
font = pygame.font.Font('goblin.ttf', 18)

# Variáveis de grupos
Heroes = pygame.sprite.Group();
Enemys = pygame.sprite.Group();

# Variáveis dos status dos personagens
# ((8-25), (8-25), (5-20), 'AP/AD') # Valores para as configurações 
mageStats = (9, 24, 6, 6, 'AP');
PaladinStats = (25, 11, 15, 12, 'AD');
monkStats = (19, 16, 9, 8, 'AD');
rangerStats = (14, 13, 12, 8, 'AD');
clericStats = (11, 9, 11, 13, 'AP');
skullStats = (30, 2, 10, 20, 'AD');

# Lista de variáveis de velocidade (no sistema de d&d, a velocidade não pode se repetir)
allSpeed = []

# Outras variáveis 
dictButtons = {};
turnDict = {};
listTurn = [];
indexTurn = 0;
selectedChar = '';

# Classe de criação de personagem
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

    # Função com utilidade apenas para visualização de estatísticas 
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

    # Função de ataque dos personagens. se baseia no tipo de dano e defesa dos participantes
    def attack(self, Char):
        print(f'{self.id} esta atacando {Char.getId()}');

        if (self.IndexDefense == 1):
            self.setDefense();
        if self.type == 'AD':
            Char.hp = Char.hp - ((self.atk) * (50/(50 + (Char.fisicalDef))));
        else:
            Char.hp = Char.hp - ((self.atk) * (50/(50 + (Char.magicalDef))));
    
        if (Char.hp <= 0):
            death(Char)
        print(f'nome: {Char.id}, hp: {Char.hp}/{Char.maxHp}')

    # Função de aumentar a defesa do personagem ao escolher essa ação 
    def setDefense(self):
        if self.IndexDefense == 0:
            self.IndexDefense = 1;
            self.fisicalDef = self.fisicalDef * 2;
            self.magicalDef = self.magicalDef * 2;
        else:
            self.IndexDefense = 0;
            self.fisicalDef = self.fisicalDef / 2;
            self.magicalDef = self.magicalDef / 2;
        return; 
            

# Classe do modo Pve exigido no PDF
class pve():
    def selectScreen(self):     
        # Carrega o plano de fundo com efeito fade
        self.bgimage = pygame.image.load('BackgroundPve1.png').convert();
        self.bgimage.set_alpha(0);
        screen.blit(self.bgimage, (0, 0));
        menus.fade.backgroundFade(self.bgimage, 'out', 5);

        self.listHeroes = [];

        # Lista de botões no menu
        self.listHeroesTypes = ['Paladin', 'Monk', 'Ranger', 'Cleric', 'Mage']
        self.listButtonsImages = ['Paladin.png', 'Monk.png', 'Ranger.png', 'Cleric.png', 'Mage.png'];
        self.listButtonsCords = [(150, 150), (425, 150), (700, 150), (285, 415), (565, 415)]; self.dictButtons = {};

        self.midBlack = pygame.image.load('BackgroundOptions.png').convert_alpha();
        self.midBlack.set_alpha(255);
        self.teamScreen();

    # Função que cria um quadro na tela e chama outra função de criação de botões 
    def teamScreen(self):
        screen.blit(self.midBlack, (75, 75));
        self.drawButtons();

    # Atualiza o modo Pve
    def updatePveMode(self, index):
        global screenType;

        screen.blit(self.bgimage, (0, 0));
        # Se o número de personagens escolhidos for menor que 3, continua com os botões na tela
        if (len(self.listHeroes) < 3):
            self.teamScreen();
        else:
            screenType = 'Combat';
            

    def drawButtons(self):
        # Coloca os botões na tela e os adiciona a um dicionário com o valor do rect
        for i in range(len(self.listHeroesTypes)):
            key = self.listHeroesTypes[i] + '.png';
            buttonImage = pygame.image.load(f'{(key)}').convert_alpha();
            buttonImage = pygame.transform.scale(buttonImage, (150, 150))
            imageRect = buttonImage.get_rect();
            imageRect = imageRect.move(self.listButtonsCords[i]);
            if (key not in self.dictButtons):
                self.dictButtons[key] = imageRect;
            screen.blit(buttonImage, self.listButtonsCords[i]);

# Classe feita para a parte de combate do jogo
class combat():
    def combatScreen(self, indexTurn):
        self.dictButtons = {};
        # Atualiza e redesenha os heróis e inimigos na tela
        self.bgimage = pygame.image.load('BackgroundPve1.png').convert();
        screen.blit(self.bgimage, (0, 0));

        Heroes.update() ; Enemys.update();
        Heroes.draw(screen) ; Enemys.draw(screen);
        # Carrega a barra de menu e vida
        self.menuBar();
        # Escreve todo o texto nas barras de menu e vida
        self.drawText(indexTurn);

    # Desenha as barraa de menu e vida
    def menuBar(self):
        coords = [(10, 508), (739, 508)];
        bar = ['menuBar', 'infoBar']
        for i in range(2):
            image = pygame.image.load(f'{bar[i]}.png').convert_alpha();
            screen.blit(image, coords[i]);

    # Escreve todo o conteúdo requisitado no PDF
    def drawText(self, index):
        global listTurn;
        persona = listTurn[index];
        # Coordinates for HP/MAXHP text
        coords = [550, 625, 700]

        attackText = font.render(f"Attack", True, (0, 0, 0));
        attackRect = attackText.get_rect(); attackRect.move((445, 604));
        self.dictButtons['Attack'] = attackRect;
        skillText = font.render(f"Skill", True, (0, 0, 0));
        skillRect = skillText.get_rect(); skillRect.move((445, 604));
        self.dictButtons['Skill'] = skillRect;
        defendText = font.render(f"Defend", True, (0, 0, 0));
        defendRect = defendText.get_rect(); defendRect.move((445, 604));
        self.dictButtons['Defend'] = defendRect;
        # Caso nao seja um herói, escreve apenas inimigo
        text = font.render(f"It's {persona.getId()} turn!", True, (0, 0, 0)); 
        # Textos para a barra de menu
        screen.blit(text, (196, 528));
        screen.blit(attackText, (108, 604));
        screen.blit(defendText, (445, 604));
        screen.blit(skillText, (136, 683));
        # Textos para a barra de status
        for i in range(len(Heroes)):
                textHp = font.render(f'{Heroes.sprites()[i].getId()}:  {Heroes.sprites()[i].getHp()}/{Heroes.sprites()[i].getMaxHp()}', True, (0, 0, 0));
                screen.blit(textHp, (760, coords[i]));

        
# Função que cria os heróis com base nos personagens escolhidos
def createHeroes():
    coords = [(250, 220), (200, 320), (250, 420)];
    for i in range(len(Pve.listHeroes)):
        key = Pve.listHeroes[i] + '.png';
        image = pygame.image.load(f'{(key)}').convert_alpha();
        image = pygame.transform.scale(image, (150, 150));
        name = str(Pve.listHeroes[i])
        speed = random.randrange(1, 20);
        # Verifica se a velocidade ja existe pois nao pode ser repetida
        while speed in allSpeed:
            speed = random.randrange(1, 20);
        allSpeed.append(speed)
        # Verifica qual personagem escolhido e o cria com sua respectativa estatística alem de adicioná-lo a um dicionário 
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

# Função de criação de inimigos
def createEnemys():
    coords = [(724, 220), (724, 420)];
    for i in range(2):
        image = pygame.image.load(f'Skull.png').convert_alpha();
        image = pygame.transform.scale(image, (200, 200));
        name = 'Skull' + str(i);
        speed = random.randrange(1, 20); 

        # Verifica repetição de velocidade
        while speed in allSpeed:
            speed = random.randrange(1, 20);
        allSpeed.append(speed);
        if (i == 0):
            Skull1 = char(image, *skullStats, speed, coords[i], name)
            Enemys.add(Skull1); turnDict[Skull1] = char.getSpeed(Skull1);
            dictButtons[Skull1] = Skull1.rect;
        else:
            Skull2 = char(image, *skullStats, speed, coords[i], name)
            Enemys.add(Skull2); turnDict[Skull2] = char.getSpeed(Skull2);
            dictButtons[Skull2] = Skull2.rect;

# Função que organiza o dicionário por ordem de velocidade decrescente e o transforma em lista
def sortDictTurn():
    global listTurn; global turnDict;
    turnDict = dict(sorted(turnDict.items(), key=operator.itemgetter(1),reverse=True))
    for i in turnDict.keys():
        listTurn.append(i);


# Chama a tela que sera carregada de acordo com o tipo de botão clicado
def updateScreenType(typeButton):
    global running;
    global screenType;
    global lastScreenType;

    # Modos de jogo
    if (typeButton == 'playButton.png'):
        screenType = 'PlayMode';
        menus.fade.backgroundFade(True, 'in', 25);
        Play.playScreen();
    # Loja do jogo (não funcional)
    elif (typeButton == 'shopButton.png'):
        return
        # Shop.interface();
    # Ainda sem configuração
    elif (typeButton == 'MenuButtons.png'):
        return
    # Ainda sem configuração 
    elif (typeButton == 'optionsButton.png'):
        return
    # Botão que fecha o jogo com efeito fade
    elif (typeButton == 'quitButton.png'):
        running = False;
        menus.fade.musicFade('out');
        menus.fade.backgroundFade(True, 'in', 3);
    # Botão de "voltar" muito comum em jogos
    elif (typeButton == 'setaE.png'):
        screenType = lastScreenType
        if lastScreenType == 'Menu':
            menus.fade.backgroundFade(True, 'in', 25);
            menus.fade.backgroundFade(Menu.bgimage, 'out', 25);
            Menu.menuScreen;
    # Botão de Pvp ainda nao funcional
    elif (typeButton == 'pvpButton.png'):
        return
    # Chama o modo Pve do jogo
    elif (typeButton == 'pveButton.png'):
        screenType = 'PVE'
        menus.fade.backgroundFade(True, 'in', 25);
        Pve.selectScreen();

# Função que define qual o personagem clicado (no momento atual do jogo, a jogabilidade é apenas no mouse)
def action(typeButton, charTurn, selectedChar):
    global listTurn;
    if (typeButton == 'Attack'):
        charTurn.attack(selectedChar);
    elif (typeButton == 'Skill'):
        # charTurn.skill(selectedChar);
        pass
    elif (typeButton == 'Defend'):
        charTurn.setDefense();

def death(Char):
    listTurn.remove(listTurn.index(selectedChar.getId()));
    if ((Char.id == 'Skull0') or (Char.id == 'Skull1')):
        Enemys.remove(Char);
    else:
        Heroes.remove(Char);
    
# Variáveis necessarias para acesso geral
Play = menus.play();
Menu = menus.menu();
Pve = pve();
Combat = combat();

def main():
    # Variáveis globais 
    global running;
    global screenType;
    global lastScreenType;
    global selectSound;
    global turnDict;
    global indexTurn;
    global selectedChar;

    # Mostra o menu do jogo quando executado
    Menu.menuScreen();

    # Variáveis de Idle que serão otimizadas futuramente
    indexIdle1 = 0;
    indexIdle2 = 0;
    indexIdle3 = 0;
    contTime = 0;
    oneTime = 0;

    # Variável de delay
    lastTick = pygame.time.get_ticks();

    while running:
    
        # Eventos
        # Fecha o jogo ao clicar no botão "quit" ou usar ALT + F4
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;
                menus.fade.musicFade('out');
                menus.fade.backgroundFade(True, 'in', 3);

            # Eventos para o botão do mouse ser clicado
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos(); # Coordenadas do mouse
                # Terá funções diferentes baseadas no tipo de tela do jogo
                # Os comentarios serão reduzidos a partir daqui para evitar repetição 
                if (screenType == 'Menu'):
                    # Roda todo o dicionario de botões para verificar o rect de qual botão foi clicado
                    for (key, value) in Menu.dictButtons.items():
                        if (value.collidepoint(mouse_pos)):
                            # Se algum botão for clicado, toca o som de seleção/click
                            selectSound.play();
                            if (value == Menu.dictButtons[key]):
                                # Se a chave for diferente do tipo de tela, atualiza o tipo de tela
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
                                # Verifica se o personagem clicado ja está no time e se o tamanho do time é menor que 3, se sim, adiciona o personagem ao dicionario
                                if (key in Pve.dictButtons):
                                    if (Pve.listHeroesTypes[list(Pve.dictButtons).index(key)] not in Pve.listHeroes) and (len(Pve.listHeroes) < 3):
                                        Pve.listHeroes.append(Pve.listHeroesTypes[list(Pve.dictButtons).index(key)]);
                elif (screenType == 'Combat'):
                    selectedChar = '';
                    if (indexTurn >= len(listTurn)):
                        indexTurn = 0;
                    if ((listTurn[indexTurn].getId() != 'Skull1') or (listTurn[indexTurn].getId() != 'Skull0')):
                        for (key, value) in dictButtons.items(): # inimigos
                            if ((value.collidepoint(mouse_pos)) and (selectedChar == '')):
                            # essa parte em diante do código de verificação não esta funcionando
                                if key in listTurn:
                                    selectedChar = key;
                        for (key, value) in Combat.dictButtons.items():
                            if (value == Combat.dictButtons[key]): # botoes
                                if (key == 'Attack'):
                                    action(key, listTurn[indexTurn], selectedChar);
                                elif (key == 'Skill'):
                                    action(key, listTurn[indexTurn], selectedChar);
                                else:
                                    action(key, listTurn[indexTurn], '');
                    indexTurn += 1;
                                    
        # Faz diferentes ações baseado no tipo de tela                                            
        if (screenType == 'Menu'):
            # Atualiza o menu com delay
            if ((pygame.time.get_ticks() - lastTick)  >=  180):
                lastTick = pygame.time.get_ticks();
                Menu.updateMenu();
        elif (screenType == 'PlayMode'):
            # Scrolla e tela para fazer animacao de caminhada
            Play.scroll -= 5;
            if (contTime == 5):
                for i in range(0, Play.tiles):
                    screen.blit(Play.bgimage, (i * Play.bgimage.get_width() + Play.scroll, 0));
                # Codigo encontrado em vídeo no youtube explicando clmo fazer uma animacao infinita de plano de fundo
                if (abs(Play.scroll) > Play.bgimage.get_width()):
                    Play.scroll = 0;
                contTime = 0;
            Play.drawButtons();
            if ((pygame.time.get_ticks() - lastTick)  >=  60):
                lastTick = pygame.time.get_ticks();
                # Atualiza os idles de caminhada
                Play.updatePlayMode(indexIdle1, indexIdle2);
                if (indexIdle1 >= 3):
                    indexIdle1 = 0;
                if (indexIdle2 >= 9):
                    indexIdle2 = 0;
                indexIdle1 += 1;
                indexIdle2 += 1;
            contTime += 1;
        elif (screenType == 'PVE'):
            # Animação de personagens na escolha de time, retirada até término dos sprites
            if ((pygame.time.get_ticks() - lastTick)  >=  240):
                lastTick = pygame.time.get_ticks();
                if (indexIdle3 >= 4):
                    indexIdle3 = 0;
                Pve.updatePveMode(indexIdle3);
                indexIdle3 += 1;
        elif (screenType == 'Combat'):
            if (indexTurn >= len(listTurn)):
                    indexTurn = 0;
            # Cria os times de cada lado
            if oneTime == 0:
                createHeroes();
                createEnemys();
                oneTime = 1;
                sortDictTurn();
                print(turnDict);
            
            if (listTurn[indexTurn].getId() == 'Skull1') or (listTurn[indexTurn].getId() == 'Skull0'):
                selectedChar = '';
                selectedChar = random.choice(listTurn);
                while ((selectedChar.id == 'Skull0') or (selectedChar.id == 'Skull1')):
                    selectedChar = random.choice(listTurn);
                action('Attack', listTurn[indexTurn], selectedChar);
                indexTurn += 1;
            Combat.combatScreen(indexTurn);

        # Renderização do jogo
        pygame.display.flip(); # Atualiza a tela do jogo
        clock.tick(60);  # Limita o fps a 60

    pygame.quit();


main();
