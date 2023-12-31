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

# Variável para som de clique, musicas e ações do jogo
selectSound = pygame.mixer.Sound('Sounds\\selectSound.mp3');
hitSound = pygame.mixer.Sound('Sounds\\hit.mp3');
defend = pygame.mixer.Sound('Sounds\\defend.mp3');
paladinBuff = pygame.mixer.Sound('Sounds\\paladinDefend.mp3');
battleMusic = pygame.mixer.music;
battleMusic.load('Sounds\\BattleTrack.mp3');


# Testar se o mixer foi inicializado com sucesso (erro existente em versões aneriores do pygame)
if (pygame.mixer.get_init() != True):
    pygame.mixer.init();

# Variável de fonte
font = pygame.font.Font('Fonts\\AGoblinAppears-o2aV.ttf', 18)

# Variáveis de grupos do jogador e inimigos
Heroes = pygame.sprite.Group();
Enemys = pygame.sprite.Group();

# Variáveis dos status dos personagens
# (HP: (8-25), MANA: (0-50), ATK: (8-25), FDEF: (5-20), MDEF: (5-20), 'AP/AD', MANACOST: (10 or 0)) # Valores para as configurações de personagens
mageStats = (9, 10, 24, 6, 6, 'AP', 10);
PaladinStats = (25, 30,  11, 15, 12, 'AD', 10);
monkStats = (19, 20, 16, 9, 8, 'AD', 10);
rangerStats = (14, 0, 13, 12, 8, 'AD', 0);
clericStats = (13, 30, 9, 11, 13, 'AP', 10);
skullStats = (100, 0, 4, 10, 20, 'AD', 0);

# Lista de variáveis de velocidade (no sistema de d&d, a velocidade não pode se repetir).
# Essa será uma versão simplificada do sistema de d&d
allSpeed = []

# Outras variáveis necessárias (não otimizadas)
enemyButtons = [];
turnDict = {};
listTurn = [];
indexTurn = 0;
selectedChar = '';
oneTime = 0;
winText = '';
action = '';
verifyStats = False;
winTeam = 1;

# Variáveis de configuração para seta de seleção do jogo
arrow = pygame.image.load('Images\\Assets\\arrow.png').convert_alpha();
arrowCoordsButton = [(65, 600), (93, 679), (402, 600), (402, 679)];
arrowCoordsChar = [(686, 220), (686, 420)];
indexButtonArrow = 0;
indexCharArrow = 0;

# Classe de criação de personagem
class char(pygame.sprite.Sprite):
    def __init__(self, image, hp, mana, atk, fdef, mdef, typeAtk, manaCost, speed, coords, name):
        pygame.sprite.Sprite.__init__(self)
        self.id = name;
        self.hp = hp;
        self.maxHp = hp;
        self.mana = mana;
        self.maxMana = mana;
        self.manaCost = manaCost;
        self.atk = atk;
        self.fisicalDef = fdef;
        self.magicalDef = mdef;
        self.speed = speed;
        self.type = typeAtk;
        self.image = image;
        self.indexDefense = 0;
        self.stateRounds = 0;
        self.state = 'Normal';
        self.image = pygame.transform.scale(self.image, (70, 70));
        self.rect = self.image.get_rect();
        self.rect = self.rect.move(coords);
        screen.blit(self.image, coords);

    # Função com utilidade apenas para visualização de estatísticas de todos os personagens
    def explain(self):
        print(f'Nome: {self.id}, Speed: {self.speed}, HP: {math.floor(self.hp)}, defF: {self.fisicalDef}, defM: {self.magicalDef}, atk: {self.atk} \n');

    # Funções get apenas para retorno de valores simples
    def getSpeed(self):
        return self.speed;

    def getId(self):
        return self.id;

    def getHp(self):
        return self.hp;

    def getMaxHp(self):
        return self.maxHp;

    # Função de ataque dos personagens. se baseia no tipo de dano e defesa dos participantes
    # Verifica se o personagem atacado foi morto ou não
    def attack(self, Char):
        hitSound.play();
        print(f'{self.id} esta atacando {Char.id}');
        if self.type == 'AD':
            Char.hp = Char.hp - ((self.atk) * (50/(50 + (Char.fisicalDef))));
        else:
            Char.hp = Char.hp - ((self.atk) * (50/(50 + (Char.magicalDef))));
        print(f'nome: {Char.id}, hp: {math.floor(Char.hp)}/{Char.maxHp}\n');
        if (math.floor(Char.hp) <= 0):
            death(Char);
        
    # Função de aumentar/dobrar a defesa do personagem ao escolher essa ação 
    def buffDefense(self):
        defend.play();
        self.indexDefense = 1;
        self.fisicalDef = self.fisicalDef * 2;
        self.magicalDef = self.magicalDef * 2;
        print(f'O personagem {self.id} foi fortificado!\n');

    # Função de habilidades inatas dos personagens, recebendo qual o personagem atual e o que será atacado
    # Varifica qual o personagem atual para saber qual é sua habilidade de classe para ativa-la
    def skill(self, selectedChar):
        # Skill do mago que aumenta seu ataque em 25% e da dano a todos os inimigos
        if (self.id == 'Mage'):
            self.atk = self.atk*1.25;
            for i in range(len(Enemys.sprites())):
                self.attack(Enemys.sprites()[i]);
            self.atk = self.atk/1.25;
            self.mana -= self.manaCost;
        # Skill do paladino que triplica sua defesa e aplica efeito 'Provocar' aos inimigos
        elif (self.id == 'Paladin'):
            paladinBuff.play();
            self.indexDefense = 2;
            self.fisicalDef = self.fisicalDef * 3;
            self.magicalDef = self.magicalDef * 3;
            print(f'O paladino provoca todos os inimigos!\n');
        # Skill do clérigo que cura todos os heróis aliados até seu maximo de HP possível 
        elif (self.id == 'Cleric'):
            for i in range(len(Heroes.sprites())):
                if (Heroes.sprites()[i].hp < Heroes.sprites()[i].maxHp):
                    Heroes.sprites()[i].hp += (Heroes.sprites()[i].maxHp * 0.25);
                if (Heroes.sprites()[i].hp > Heroes.sprites()[i].maxHp):
                    Heroes.sprites()[i].hp = Heroes.sprites()[i].maxHp;
            # Custa 5 de mana por aliado em campo
            self.mana -= ((self.manaCost/2)*len(Heroes.sprites()));
            print(f'O clérigo curou seus aliados até o limite!\n');
        # Skill do ranger que realiza um ataque normal com efeito de 'Envenenamento' a um inimigo
        elif (self.id == 'Ranger'):
            selectedChar.state = 'Poisoned';
            print(f'{selectedChar.id} foi envenenado!\n');
            self.attack(selectedChar);
        # Skill do monge que realiza um ataque simples com efeito de 'Atordoamento' a um inimigo
        elif (self.id == 'Monk'):
            selectedChar.state = 'Stunned';
            print(f'{selectedChar.id} foi stunnado!\n');
            self.attack(selectedChar);
            self.mana -= self.manaCost;

    # Função que verifica o estado de um personagem toda vez que seu turno se inicia
    def statsVerify(self):
        global verifyStats ;
        verifyStats = True;
        
        # Verifica se um Buff de defesa esta ativo no personagem. se sim, o cancelará 
        if (self.indexDefense == 1):
            self.indexDefense = 0;
            self.fisicalDef = self.fisicalDef / 2;
            self.magicalDef = self.magicalDef / 2;
            print(f'A defesa de {self.id} diminuiu');
        # Verifica a habilidade do paladino. se estiver ativa pelo tempo limite, a cancela
        if ((self.indexDefense == 2) and (self.stateRounds == 3)):
            self.stateRounds = 0;
            self.fisicalDef = self.fisicalDef / 3;
            self.magicalDef = self.magicalDef / 3;
            print(f'A provocação do paladino cessou!');
        elif ((self.indexDefense == 2) and (self.stateRounds < 2)):
            self.indexDefense += 1;
        # Se seu estado for 'Normal', Seu turno se iniciará
        if (self.state == 'Normal'):
            return True;
        # Se seu estado for 'Envenenado' (Skill ranger), tomará 15% de seu HP atual como dano
        # Caso o efeito de envenenamento esteja ativo a duas rodadas, o cancelará e iniciará sua vez
        elif (self.state == 'Poisoned'):
            if (self.stateRounds == 3):
                self.stateRounds = 0;
                self.state = 'Normal';
                print(f'{self.id} voltou ao normal!\n');
            else:
                poison = math.floor(self.hp * 0.15);
                self.hp -= poison;
                print(f'{self.id} tomou {poison} de dano de envenenamento\n');
                self.stateRounds += 1;
            return True;
        # Caso seu estado seja 'Atordoado', o inimigo não jogará nessa rodada.
        # Se o estado de 'Atordodado' estiver ativo a uma rodada, ele será cancelado
        elif (self.state == 'Stunned'):
            if (self.stateRounds == 2):
                self.stateRounds = 0;
                self.state = 'Normal';
                print(f'{self.id} voltou ao normal!\n');
                return True;
            self.stateRounds += 1;
            print(f'{self.id} está incapacitado.\n');
            return False;

    # Função que cria os heróis com base nos personagens escolhidos
    def createHeroes():
        coords = [(250, 220), (200, 320), (250, 420)];
        print();
        for i in range(len(Pve.listHeroes)):
            image = pygame.image.load(f'Images\\Players\\{Pve.listHeroes[i]}\\{Pve.listHeroesButtons[i]}').convert_alpha();
            image = pygame.transform.scale(image, (150, 150));
            name = str(Pve.listHeroes[i])
            speed = random.randrange(1, 20);
            # Verifica se a velocidade já existe pois não pode ser repetida
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
        global enemyButtons;
        coords = [(724, 220), (724, 420)];
        for i in range(2):
            image = pygame.image.load(f'Images\\Monsters\\Skull.png').convert_alpha();
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
                enemyButtons.append(Skull1);
            else:
                Skull2 = char(image, *skullStats, speed, coords[i], name)
                Enemys.add(Skull2); turnDict[Skull2] = char.getSpeed(Skull2);
                enemyButtons.append(Skull2);
        print();

# Classe do modo Pve exigido no PDF
class pve():
    def selectScreen(self):     
        # Carrega o plano de fundo com efeito fade
        self.bgimage = pygame.image.load('Images\\Backgrounds\\BackgroundPve.png').convert();
        self.bgimage.set_alpha(0);
        screen.blit(self.bgimage, (0, 0));
        menus.fade.backgroundFade(self.bgimage, 'out', 5);

        self.listHeroes = [];

        # Lista de botões no menu
        self.listHeroesTypes = ['Paladin', 'Monk', 'Ranger', 'Cleric', 'Mage']
        self.listButtonsImages = ['Paladin.png', 'Monk.png', 'Ranger.png', 'Cleric.png', 'Mage.png'];
        self.listButtonsCords = [(150, 150), (425, 150), (700, 150), (285, 415), (565, 415)]; self.dictButtons = {};

        self.midBlack = pygame.image.load('Images\\Backgrounds\\BackgroundOptions.png').convert_alpha();
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
        # Caso contrario, inicia o modo combate
        if (len(self.listHeroes) < 3):
            self.teamScreen();
        else:
            screenType = 'Combat';
            
    # Desenha na tela as fotos dos heróis, que serão botões clicáveis para adicioná-los ao seu time
    def drawButtons(self):
        # Coloca os botões na tela e os adiciona a um dicionário com o valor do rect
        for i in range(len(self.listHeroesTypes)):
            key = self.listHeroesTypes[i] + '.png';
            buttonImage = pygame.image.load(f'Images\\Players\\{self.listHeroesTypes[i]}\\{key}').convert_alpha();
            buttonImage = pygame.transform.scale(buttonImage, (150, 150))
            imageRect = buttonImage.get_rect();
            imageRect = imageRect.move(self.listButtonsCords[i]);
            if (key not in self.dictButtons):
                self.dictButtons[key] = imageRect;
            screen.blit(buttonImage, self.listButtonsCords[i]);

# Classe feita para a parte de combate do jogo
class combat():
    def combatScreen(self, indexTurn):
        self.actions = ['Attack', 'Skill', 'Defend', 'Analyze'];
        # Atualiza e redesenha os heróis e inimigos na tela
        self.bgimage = pygame.image.load('Images\\Backgrounds\\BackgroundPve.png').convert();
        screen.blit(self.bgimage, (0, 0));
        # Atualiza os personagens e os desenha na tela
        Heroes.update() ; Enemys.update();
        Heroes.draw(screen) ; Enemys.draw(screen);
        # Carrega a barra de menu e vida
        self.menuBar();
        # Escreve todo o texto nas barras de menu e vida
        self.drawText(indexTurn);

    # Desenha as barras de menu de ação e de informações vida
    def menuBar(self):
        coords = [(10, 508), (739, 508)];
        bar = ['menuBar', 'infoBar']
        for i in range(2):
            image = pygame.image.load(f'Images\\Assets\\{bar[i]}.png').convert_alpha();
            screen.blit(image, coords[i]);

    # Escreve todo o conteúdo requisitado no PDF
    def drawText(self, index):
        global listTurn;
        persona = listTurn[index];
        # Coordenadas para o texto de hp/maxHp
        coords = [550, 625, 700]

        attackText = font.render(f"Attack", True, (0, 0, 0));
        skillText = font.render(f"Skill", True, (0, 0, 0));
        defendText = font.render(f"Defend", True, (0, 0, 0));
        analyzeText = font.render(f"Analyze", True, (0, 0, 0));
        # Caso não seja um herói, escreve apenas inimigo
        textTurn = font.render(f"It's {persona.getId()} turn!", True, (0, 0, 0)); 
        # Textos para a barra de menu
        screen.blit(textTurn, (196, 528));
        screen.blit(attackText, (108, 604));
        screen.blit(defendText, (445, 604));
        screen.blit(skillText, (136, 683));
        screen.blit(analyzeText, (445, 683));
        # Textos para a barra de status
        for i in range(len(Heroes)):
                textHp = font.render(f'{Heroes.sprites()[i].getId()}:  {math.floor(Heroes.sprites()[i].getHp())}/{Heroes.sprites()[i].getMaxHp()}', True, (0, 0, 0));
                screen.blit(textHp, (760, coords[i]));

# Função que organiza o dicionário por ordem de velocidade decrescente e o transforma em lista para ordem de jogada
def sortDictTurn():
    global listTurn; global turnDict;
    turnDict = dict(sorted(turnDict.items(), key=operator.itemgetter(1), reverse=True))
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
    # Interface de configuração do jogo (não funcional)
    elif (typeButton == 'optionsButton.png'):
        return
    # Botão que fecha o jogo com efeito fade
    elif (typeButton == 'quitButton.png'):
        running = False;
        menus.fade.musicFade('out');
        menus.fade.backgroundFade(True, 'in', 3);
    # Botão de "voltar" muito comum em jogos
    # (Não sei qual o motivo de alguem usar no estado atual mas tá ai existindo)
    elif (typeButton == 'setaE.png'):
        screenType = lastScreenType
        if lastScreenType == 'Menu':
            menus.fade.backgroundFade(True, 'in', 25);
            menus.fade.backgroundFade(Menu.bgimage, 'out', 25);
            Menu.menuScreen;
    # Botão de Pvp (não funcional)
    elif (typeButton == 'pvpButton.png'):
        return;
    # Chama o modo Pve do jogo
    elif (typeButton == 'pveButton.png'):
        screenType = 'PVE'
        menus.fade.backgroundFade(True, 'in', 25);
        Pve.selectScreen();
    # Botão para reiniciar o jogo, indo para interface de escolha de modo e reiniciando variaveis
    elif (typeButton == ('restartButton.png')):
        resetVariables();
        Over.resetVariables();
        Menu.play();
        screenType = 'PlayMode';
        menus.fade.backgroundFade(True, 'in', 25);
        Play.playScreen();

# Função que verifica a morte de um personagem e quantidade de personagens nos times
# se essa quantidade for igual a 0, chamará a tela de 'GameOver' do jogo
def death(Char):
    global arrowCoordsChar ; global indexCharArrow ;
    global screenType; global winText ; global winTeam ;
    
    # Remove o personagem morto da lista de turnos
    listTurn.remove(Char);
    
    # Remove o char do grupo de sprites e/ou da lista em que ele era uma opção para ataque
    if ((Char.id == 'Skull0') or (Char.id == 'Skull1')):
        Enemys.remove(Char);
        arrowCoordsChar.remove(arrowCoordsChar[indexCharArrow]);
        enemyButtons.remove(enemyButtons[indexCharArrow]);
    else:
        Heroes.remove(Char);
    # Verifica se algum time perdeu
    if ((len(Heroes.sprites()) == 0)):
        winText = 'Vitória dos Inimigos';
        winTeam = 0;
        screenType = 'GameOver';
    elif ((len(Enemys.sprites()) == 0)):
        winText = 'Vitória dos Heróis';
        winTeam = 1;
        screenType = 'GameOver';

# Função para reinicialização de variaveis para início de uma nova partida PVE
def resetVariables():
    # Variaveis globais necessárias (não otimizado)
    global running;
    global arrowCoordsButton;
    global arrowCoordsChar;
    global indexCharArrow;
    global indexButtonArrow;
    global oneTime;
    global allSpeed;
    global listTurn;
    global action;
    global canPlay;
    global verifyStats;
    global turnDict;
    global indexTurn;


    Heroes.empty();
    Enemys.empty();
    arrowCoordsButton = [(65, 600), (93, 679), (402, 600), (402, 679)];
    arrowCoordsChar = [(686, 220), (686, 420)];
    indexButtonArrow = 0;
    indexCharArrow = 0;
    allSpeed = [];
    listTurn = [];
    action = '';
    canPlay = False;
    verifyStats = False;
    turnDict = {};
    indexTurn = 0;
    oneTime = 0;
 
# Variáveis/Objetos necessarios para acesso geral
Play = menus.play();
Over = menus.finish();
Pve = pve();
Combat = combat();

# Mostra o menu do jogo quando executado
Menu = menus.menu();


def main():
    # Variáveis globais necessárias (não otimizado)
    global running;
    global screenType;
    global lastScreenType;
    global selectSound;
    global turnDict;
    global indexTurn;
    global selectedChar;
    global arrow;
    global arrowCoordsButton;
    global arrowCoordsChar;
    global indexCharArrow;
    global indexButtonArrow;
    global oneTime;
    global winText;
    global verifyStats;
    global canPlay;
    global listTurn;

    # Variáveis de Idle (não otimizado)
    indexIdle1 = 0;
    indexIdle2 = 0;
    indexIdle3 = 0;
    contTime = 0;
    action = '';
    

    # Variável de delay
    lastTick = pygame.time.get_ticks();

    while running:
        # Eventos
        for event in pygame.event.get():
            # Fecha o jogo ao clicar no botão "quit", usar ALT + F4 ou clicar no 'X' do frame
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
                                # Verifica se o personagem clicado ja está no time e se o tamanho do time é menor que 3, e se possível, adiciona o personagem ao dicionario
                                if (key in Pve.dictButtons):
                                    if (Pve.listHeroesTypes[list(Pve.dictButtons).index(key)] not in Pve.listHeroes) and (len(Pve.listHeroes) < 3):
                                        Pve.listHeroes.append(Pve.listHeroesTypes[list(Pve.dictButtons).index(key)]);
            
                elif (screenType == 'GameOver'):
                    for (key, value) in Over.dictButtons.items():
                        if (value.collidepoint(mouse_pos)):
                            if (value == Over.dictButtons[key]):
                                selectSound.play();
                                if (key != screenType):
                                    screenType == key;
                                    updateScreenType(key);
                                    
            # Funções para quando o teclado for clicado
            if event.type == pygame.KEYDOWN:
                # Funções direcionadas aos personagens aliados
                if ((charTurn.getId() != 'Skull1') or (charTurn.getId() != 'Skull0') and (screenType == 'Combat')):
                    # Reseta a variável de turnos caso ela exceda o limite
                    if (indexTurn >= len(listTurn)):
                        indexTurn = 0;
                    if event.key == pygame.K_RIGHT:
                        
                        # Caso a ação seja uma string vazia
                        # Passa para proxima opção de ataque, skill ou defesa
                        if (action == ''):
                            indexButtonArrow += 1;
                            # Reseta a variável índice de ação para que não exceda o limite
                            if (indexButtonArrow >= len(Combat.actions)):
                                indexButtonArrow = 0;
                        # Se nenhum personagem for selecionado até o momento
                        # Passar para proxima opção de qual personagem atacar
                        elif (selectedChar == ''):
                            indexCharArrow += 1;
                            # Reseta o índice de qual personagem será selecionado
                            if (indexCharArrow >= len(Enemys.sprites())):
                                indexCharArrow = 0;
                    # Ao usar a tecla 'Return/ENTER', a ação ou perosnagem escolhida será lida
                    elif event.key == pygame.K_RETURN:
                        if (action == ''):
                            action = Combat.actions[indexButtonArrow];
                            # Se a ação for defender, nenhum personagem será lido
                            if (action == 'Defend'):
                                selectedChar = ' ';
                            if ((action == 'Skill') and (charTurn.getId() == ('Cleric') or charTurn.getId() == ('Paladin') or charTurn.getId() == ('Mage'))):
                                selectedChar = ' ';
                        elif (selectedChar == ''):
                            selectedChar = enemyButtons[indexCharArrow];
                        verifyStats = False;
                    # Caso a tecla Z seja clicada, voltará à opção de escolher uma ação 
                    elif event.key == pygame.K_z:
                        action = '';
        
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
                # Video citado no arquivo README
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
            # Reinicialização de variáveis para não excederem o limite
            if (indexTurn >= len(listTurn)):
                indexTurn = 0;
            if (indexCharArrow >= len(Enemys.sprites())):
                indexCharArrow = 0;
                
            # Cria os times de cada lado e inicializa musica de combate
            if oneTime == 0:
                Menu.stop();
                battleMusic.play();
                char.createHeroes();
                char.createEnemys();
                sortDictTurn();
                oneTime = 1;
            # Troca o personagem do turno atual
            charTurn = listTurn[indexTurn];
            Combat.combatScreen(indexTurn);
            ### VERIFICACAO DE STATUS E ESTADOS PARA JOGADA DOS ALIADOS
            # Se for a vez de um aliado e o estado dele nao for incapacitado, a função retornará True, permitindo jogada
            if ((charTurn.getId() != 'Skull1') and (charTurn.getId() != 'Skull0')):
                if verifyStats == False:
                    canPlay = charTurn.statsVerify();
                if (canPlay == True):
                    # Se a ação e alvo não forem escolhidos, menterá as setas na tela. se forem, dará inicio a escolha do jogador
                    if ((action != '') and (selectedChar != '')):
                        if (action == 'Attack'):
                            charTurn.attack(selectedChar);
                        elif (action == 'Skill'):
                            # Verifica se há mana suficiente para uso da habilidade. se não houver
                            # Voltará um turno (é adicionado novamente posteriormente) para refazer sua jogada
                            if (charTurn.mana < charTurn.manaCost):
                                print(f'Mana insuficiente! Impossível usar habilidade ({charTurn.mana}/{charTurn.manaCost})');
                                action = '';
                                indexTurn -= 1;
                            else:
                                charTurn.skill(selectedChar);
                        elif (action == 'Defend'):
                            charTurn.buffDefense();
                        # Chama uma função que verifica os dados do personagem selecionado
                        elif (action == 'Analyze'):
                            selectedChar.explain();
                            indexTurn -= 1;
                        selectedChar = '';
                        action = '';
                        indexTurn += 1;
                        
                    else:
                        # Move a seta de escolha usando indices organizados
                        if ((action == '') and (len(Heroes.sprites()) and len(Enemys.sprites()) != 0)):
                            screen.blit(arrow, arrowCoordsButton[indexButtonArrow]);
                        elif ((action != '') and (len(Heroes.sprites()) and len(Enemys.sprites()) != 0)):
                            screen.blit(arrow, arrowCoordsChar[indexCharArrow]);
                            
            # Verifica se o turno atual é de um inimigo e se ele pode jogar, assim como feito anteriormente com o aliado
            elif ((charTurn.getId() == 'Skull1') or (charTurn.getId() == 'Skull0')):
                canPlay = charTurn.statsVerify();
                indexCharArrow = 0;
                indexButtonArrow = 0;
                if (canPlay == True):
                    for tempChar in listTurn:
                        # Se o paladino possuir sua habilidade de 'Provocar' ativa, automaticamente o seleciona como alvo
                        if ((tempChar.id == 'Paladin') and (tempChar.indexDefense == 2)):
                            selectedChar = tempChar;
                            break;
                    if (selectedChar == ''):
                        selectedChar = random.choice(listTurn);
                        # Verifica se o personagem selecionado aleatoriamente nao é um inimigo (evita friendly fire). caso seja, seleciona um novo alvo
                        while ((selectedChar.id == 'Skull0') or (selectedChar.id == 'Skull1')):
                            selectedChar = random.choice(listTurn);
                    charTurn.attack(selectedChar);
                selectedChar = '';
                action = '';
                indexTurn += 1;
                
        # Muda a musica e abre a tela de fim de jogo (nao travalhada)
        elif (screenType == 'GameOver'):
            battleMusic.pause();
            Over.gameOver(winText, winTeam);

        # Game render 
        pygame.display.flip(); # game screen update
        clock.tick(60);  # 60fps limit

    pygame.quit();

main();
