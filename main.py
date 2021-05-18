#Test klasy Player
import math, pygame, random, sys

pygame.init()

WINDOWWIDTH = 720
WINDOWHEIGHT = 480
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (7, 118, 215)
LIGHT_BLUE = (7, 180, 215)

COLOR1 = WHITE
COLOR2 = WHITE

basicFont = "impact"

screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)

#Dźwięki
shot = pygame.mixer.Sound("shot.wav")
explosion = pygame.mixer.Sound("Explosion.wav")

def play():
    player1 = Player(100, 100, 15, 30, COLOR1, 1)
    player2 = Player(WINDOWWIDTH - 100, WINDOWHEIGHT - 100, 15, 30, COLOR2, 2)
    players = [player1, player2]
    blackhole = Blackhole()
    animations = []
    backgroundAnimation = BackgroundAnimation()
    backgroundAnimation.prepare()
    animations.append(backgroundAnimation)

    win = False

    pointsText1 = createFont("Score:{0}".format(player1.points), 24, player1.color)
    pointsText2 = createFont("Score:{0}".format(player2.points), 24, player2.color)
    winText = None
    informationText = None
    
    running = True
    pygame.mixer.music.load("backgroundMusic.wav")
    pygame.mixer.music.play(-1)
    screen.fill(BLACK)
    startText = createFont("GET 10 POINTS TO WIN", 30, WHITE)
    screen.blit(startText, (WINDOWWIDTH/2 - startText.get_rect()[2]/2, WINDOWHEIGHT/2 - startText.get_rect()[3]/2))
    pygame.display.update()
    clock.tick(FPS)
    pygame.time.wait(3000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                #pygame.event.post(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shot.play()
                    players[0].shot()
                if event.key == pygame.K_RCTRL:
                    shot.play()
                    players[1].shot()
                    
                        
        screen.fill(BLACK)
        for animation in animations:
            animation.update()
        if not players[0].isDestroy and not players[1].isDestroy:
            if polyPoly(players[0].vertices, players[1].vertices):
                players[0].destroy()
                players[1].destroy()
                destroyAnimation1 = DestroyAnimation()
                destroyAnimation2 = DestroyAnimation()
                destroyAnimation1.prepare(players[0])
                destroyAnimation2.prepare(players[1])
                animations.append(destroyAnimation1)
                animations.append(destroyAnimation2)
                explosion.play()
                players[0].reset()
                players[1].reset()
                
        if not players[1].isDestroy:
            if players[0].checkMissileCollision(players[1]):
                players[1].destroy()
                players[0].addPoint()
                pointsText1 = createFont("Score:{0}".format(players[0].points), 24, players[0].color)
                destroyAnimation = DestroyAnimation()
                destroyAnimation.prepare(players[1])
                animations.append(destroyAnimation)
                explosion.play()
                players[1].reset()
                

        if not players[0].isDestroy:
            if players[1].checkMissileCollision(players[0]):
                players[0].destroy()
                players[1].addPoint()
                pointsText2 = createFont("Score:{0}".format(players[1].points), 24, players[1].color)
                destroyAnimation = DestroyAnimation()
                destroyAnimation.prepare(players[0])
                animations.append(destroyAnimation)
                explosion.play()
                players[0].reset()
       
        if not player1.isDestroy:
            if blackhole.checkCollision(player1):
                player1.destroy()
                destroyAnimation = DestroyAnimation()
                destroyAnimation.prepare(player1)
                animations.append(destroyAnimation)
                explosion.play()
                player1.reset()
                
        if not player2.isDestroy:
            if blackhole.checkCollision(player2):
                player2.destroy()
                destroyAnimation = DestroyAnimation()
                destroyAnimation.prepare(player2)
                animations.append(destroyAnimation)
                explosion.play()
                player2.reset()
                    

        

        if win == False:
            for player in players:
                if player.points >= 10:
                    win = True
                    winText = createFont("YOU WIN", 30, player.color)
                    informationText = createFont("continue - ENTER, menu - BACKSPACE", 30, player.color)
                    
        

        
        screen.blit(pointsText1, (0, 0))
        screen.blit(pointsText2, (WINDOWWIDTH - pointsText2.get_rect()[2], 0))
        if win:
            screen.blit(winText, (WINDOWWIDTH/2 - winText.get_rect()[2]/2, WINDOWHEIGHT/2 - winText.get_rect()[3]/2))
            screen.blit(informationText, (WINDOWWIDTH/2 - informationText.get_rect()[2]/2, WINDOWHEIGHT/2 + 50 - winText.get_rect()[3]/2))
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RETURN]:
                player1.points = 0
                player2.points = 0
                pointsText1 = createFont("Score:{0}".format(players[0].points), 24, players[0].color)
                pointsText2 = createFont("Score:{0}".format(players[1].points), 24, players[1].color)
                win = False
            elif pressed[pygame.K_BACKSPACE]:
                pygame.mixer.music.stop()
                mainMenu()
        else:
            blackhole.draw()
            for player in players:
                if not player.isDestroy:
                    player.update()
                    blackhole.update(player.vertices, player.direction)
        pygame.display.update()
        clock.tick(FPS)

def prePlay():
    global COLOR1, COLOR2
    pygame.font.init()
    currentColor = WHITE

    pickColorText = createFont("PICK A COLOR", 24, WHITE)

    player1Button = Button(WINDOWWIDTH/2 + 50, 50, "PLAYER 1", WHITE, LIGHT_BLUE, 20)
    player2Button = Button(WINDOWWIDTH/2 + 200, 50, "PLAYER 2", WHITE, LIGHT_BLUE, 20)
    playButton = Button(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, "PLAY", WHITE, LIGHT_BLUE, 20)
    backButton = Button(WINDOWWIDTH - 200, WINDOWHEIGHT - 50, "BACK", WHITE, LIGHT_BLUE, 20)

    player1 = Player(WINDOWWIDTH/2 + 80, 200, 30, 60, WHITE, 1)
    player2 = Player(WINDOWWIDTH/2 + 230, 200, 30, 60, WHITE, 2)

    isActivePlayer1 = True
    isActicePLayer2 = False

    
    class Rect():
        def __init__(self,name, color, x, y):
            self.rect = pygame.Rect(10,10,10,10)
            self.rect.x = x
            self.rect.y = y
            self.name = name
            self.color = color
            all_rects.append(self)
        def Draw(self):
            pygame.draw.rect(screen, (self.color), self.rect)


    class ColorPicker():
        def __init__(self):
            self.colors = RGBA_TO_NAME
            self.gridX = 25
            self.MakeGrid()
        def MakeGrid(self):
            x, y = 75, 100
            i = 0
            for col, name in self.colors.items():

                rect = Rect(name, col, x, y)
                x += 10
                i += 1
                if i == 25:
                    i = 0
                    y += 10
                    x = 75
                    
    running = True 
    all_rects = []

    NAME_TO_RGBA = pygame.color.THECOLORS
    RGBA_TO_NAME = {}
    for name, rgb in NAME_TO_RGBA.items():
        if rgb in RGBA_TO_NAME:
            RGBA_TO_NAME[rgb].append(name)
        else:
            RGBA_TO_NAME[rgb] = [name]

    ColorPicker()
    while running:
        mx, my = pygame.mouse.get_pos()
        click = False
        clock.tick(60)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for rect in all_rects:
                        if rect.rect.collidepoint(pos):
                            currentColor = rect.color
                            if isActivePlayer1:
                                player1.color = currentColor
                                COLOR1 = currentColor
                            elif isActivePlayer2:
                                player2.color = currentColor
                                COLOR2 = currentColor
        if player1Button.getRect().collidepoint(mx, my):
            if click:  
                isActivePlayer1 = True
                isActivePlayer2 = False
        if player2Button.getRect().collidepoint(mx, my):
            if click:  
                isActivePlayer1 = False
                isActivePlayer2 = True
        if playButton.getRect().collidepoint(mx, my):
            if click:
                play()
        if backButton.getRect().collidepoint(mx, my):
            if click:
                mainMenu()
        screen.fill(BLACK)
        if isActivePlayer1:
            pygame.draw.rect(screen, WHITE, (WINDOWWIDTH/2 + 60, 135, 40, 75), 1)
        elif isActivePlayer2:
            pygame.draw.rect(screen, WHITE, (WINDOWWIDTH/2 + 210, 135, 40, 75), 1)
                            
        screen.blit(pickColorText, (100, 50))
        player1Button.update()
        player2Button.update()
        playButton.update()
        backButton.update()
        player1.draw()
        player2.draw()
        for rect in all_rects:
            rect.Draw()
        pygame.display.update()
        clock.tick(FPS)

    
    
def mainMenu():
    mainmenuText = createFont("SPACE WAR", 24, WHITE)
    buttons = []
    #(x, y, text, mainColor, secondColor, fontSize)
    playButton = Button(mainmenuText.get_rect()[2]/2, 0 + mainmenuText.get_rect()[3] * 5, "PLAY", WHITE, LIGHT_BLUE, 20)
    optionsButton = Button(mainmenuText.get_rect()[2]/2, 0 + mainmenuText.get_rect()[3] * 7, "OPTIONS", WHITE, LIGHT_BLUE, 20)
    quitButton = Button(mainmenuText.get_rect()[2]/2, 0 + mainmenuText.get_rect()[3] * 9, "QUIT", WHITE, LIGHT_BLUE, 20)
    buttons.append(playButton)
    buttons.append(optionsButton)
    buttons.append(quitButton)

    background_image = pygame.image.load("background.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WINDOWWIDTH, WINDOWHEIGHT))
    
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if playButton.getRect().collidepoint(mx, my):
            if click:  
                prePlay()
        if optionsButton.getRect().collidepoint(mx, my):
            if click:
                options()
        if quitButton.getRect().collidepoint(mx, my):
            if click:
                pygame.quit()
                sys.exit()

        screen.blit(background_image, [0, 0])
        screen.blit(mainmenuText, (mainmenuText.get_rect()[2]/2, 0 + mainmenuText.get_rect()[3]))
        for button in buttons:
            button.update()
        pygame.display.update()
        clock.tick(FPS)

def options():
    global screen, WINDOWWIDTH, WINDOWHEIGHT
    
    optionsText = createFont("OPTIONS", 20, WHITE)
    resolutionList = pygame.display.list_modes()
    
    numResolution = 0
    fullscreen = False
    
    fullscreenOptions = Button(50, 100, "FULLSCREEN: OFF", WHITE, LIGHT_BLUE, 20)
    resolutionOptions = Button(50, 150, "RESOLUTION: {0} - {1}".format(resolutionList[numResolution][0], resolutionList[numResolution][1]), WHITE, LIGHT_BLUE, 20)
    acceptOptions = Button(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, "ACCEPT", WHITE, LIGHT_BLUE, 20)
    backOptions = Button(WINDOWWIDTH - 200, WINDOWHEIGHT - 50, "BACK", WHITE, LIGHT_BLUE, 20)

    background_image = pygame.image.load("background.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WINDOWWIDTH, WINDOWHEIGHT))
    
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        if fullscreenOptions.getRect().collidepoint(mx, my):
            if click:
                if fullscreenOptions.textForm == "FULLSCREEN: OFF":
                    fullscreenOptions.changeText("FULLSCREEN: ON")
                    fullscreen = True
                elif fullscreenOptions.textForm == "FULLSCREEN: ON":
                    fullscreenOptions.changeText("FULLSCREEN: OFF")
                    fullscreen = False
                
        if resolutionOptions.getRect().collidepoint(mx, my):
            if click:
                numResolution += 1
                if numResolution >= len(resolutionList):
                    numResolution = 0
                resolutionOptions.changeText("RESOLUTION: {0} - {1}".format(resolutionList[numResolution][0], resolutionList[numResolution][1]))

        if acceptOptions.getRect().collidepoint(mx, my):
            if click:
                background_image = pygame.transform.scale(background_image, (resolutionList[numResolution]))
                WINDOWWIDTH, WINDOWHEIGHT = resolutionList[numResolution][0], resolutionList[numResolution][1]
                acceptOptions = Button(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, "ACCEPT", WHITE, LIGHT_BLUE, 20)
                backOptions = Button(WINDOWWIDTH - 200, WINDOWHEIGHT - 50, "BACK", WHITE, LIGHT_BLUE, 20)
                if fullscreen: 
                    screen = pygame.display.set_mode(resolutionList[numResolution], pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(resolutionList[numResolution])

        if backOptions.getRect().collidepoint(mx, my):
            if click:
                mainMenu()
                

        screen.blit(background_image, [0, 0])
        screen.blit(optionsText, (WINDOWWIDTH/2 - optionsText.get_rect()[2]/2, 0 + optionsText.get_rect()[3]))
        fullscreenOptions.update()
        resolutionOptions.update()
        acceptOptions.update()
        backOptions.update()
        pygame.display.update()
        clock.tick(FPS)

class Button:
    def __init__(self, x, y, text, mainColor, secondColor, fontSize):
        self.textForm = text
        self.mainColor = mainColor
        self.secondColor = secondColor
        self.fontSize = fontSize
        self.text = createFont(text, fontSize, mainColor)
        self.surface = pygame.Surface((self.text.get_rect()[2], self.text.get_rect()[3]))
        self.surface.set_alpha(0)
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            self.text = createFont(self.textForm, self.fontSize, self.secondColor)
        else:
            self.text = createFont(self.textForm, self.fontSize, self.mainColor)
        screen.blit(self.surface, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.rect.x, self.rect.y))

    def getRect(self):
        return self.rect

    def changeText(self, newText):
        self.textForm = newText
            
class Player:
    def __init__(self, x, y, width, height, color, playerNum):
        self.vertices = [[x, y - height], [x - width/2, y], [x + width/2, y]]
        self.verticesCopy = [[x, y - height], [x - width/2, y], [x + width/2, y]]
        self.direction = [0, 0]
        self.missiles = []
        self.playerNum = playerNum
        self.isDestroy = False
        self.color = color
        self.points = 0

    def update(self):
        pressed = pygame.key.get_pressed()
        if self.playerNum == 1:
            if pressed[pygame.K_d]:
                self.rotate(10)
            elif pressed[pygame.K_a]:
                self.rotate(-10)
            elif pressed[pygame.K_w]:
                x, y = self.updateVelocityVector()
                self.direction[0] += x * 0.5
                self.direction[1] += y * 0.5

            self.checkBoundaryCollision()
            self.updateMissiles()
            self.move()
            pygame.draw.polygon(screen, self.color, self.vertices, 3)
        if self.playerNum == 2:
            if pressed[pygame.K_RIGHT]:
                self.rotate(10)
            elif pressed[pygame.K_LEFT]:
                self.rotate(-10)
            elif pressed[pygame.K_UP]:
                x, y = self.updateVelocityVector()
                self.direction[0] += x * 0.5
                self.direction[1] += y * 0.5

            self.checkBoundaryCollision()
            self.updateMissiles()
            self.move()
            self.draw()

    def draw(self):
        pygame.draw.polygon(screen, self.color, self.vertices, 3)

    def rotate(self, rotation):
        center = [int((self.vertices[0][0] + self.vertices[1][0] + self.vertices[2][0]) / 3), int((self.vertices[0][1] + self.vertices[1][1] + self.vertices[2][1]) / 3)]
        angle = (rotation) * (math.pi/180)
        for t in self.vertices:
            x = t[0]
            y = t[1]
            t[0] = (x - center[0]) * math.cos(angle) - (y - center[1]) * math.sin(angle) + center[0]
            t[1] = (x - center[0]) * math.sin(angle) + (y - center[1]) * math.cos(angle) + center[1]

    def move(self):
        for t in self.vertices:
            t[0] += self.direction[0] * 0.1
            t[1] += self.direction[1] * 0.1

    def updateVelocityVector(self):
        center = [int((self.vertices[0][0] + self.vertices[1][0] + self.vertices[2][0]) / 3), int((self.vertices[0][1] + self.vertices[1][1] + self.vertices[2][1]) / 3)]
        normal = math.sqrt(math.pow(self.vertices[0][0] - center[0], 2) + math.pow(self.vertices[0][1] - center[1], 2))
        x = (self.vertices[0][0] - center[0]) / normal
        y = (self.vertices[0][1] - center[1]) / normal
        return x, y

    def shot(self):
        x, y = self.updateVelocityVector()
        self.missiles.append([[self.vertices[0][0], self.vertices[0][1]], [x, y]])

    def updateMissiles(self):
        if self.missiles:
            for missile in self.missiles:
                pygame.draw.circle(screen, WHITE,(int(missile[0][0]), int(missile[0][1])), 2)
                missile[0][0] += missile[1][0] * 4
                missile[0][1] += missile[1][1] * 4
                if missile[0][0] >= WINDOWWIDTH or missile[0][0] <= 0 or missile[0][1] >= WINDOWHEIGHT or missile[0][1] <= 0:
                    self.missiles.remove(missile)
                    
    def checkBoundaryCollision(self):
        if self.vertices[0][0] >= WINDOWWIDTH and self.vertices[1][0] >= WINDOWWIDTH and self.vertices[2][0] >= WINDOWWIDTH:
            for vertex in self.vertices:
                vertex[0] -= (WINDOWWIDTH + 30)
        if self.vertices[0][0] <= 0 and self.vertices[1][0] <= 0 and self.vertices[2][0] <= 0:
            for vertex in self.vertices:
                vertex[0] += (WINDOWWIDTH + 30)
        if self.vertices[0][1] >= WINDOWHEIGHT and self.vertices[1][1] >= WINDOWHEIGHT and self.vertices[2][1] >= WINDOWHEIGHT:
            for vertex in self.vertices:
                vertex[1] -= (WINDOWHEIGHT + 30)
        if self.vertices[0][1] <= 0 and self.vertices[1][1] <= 0 and self.vertices[2][1] <= 0:
            for vertex in self.vertices:
                vertex[1] += (WINDOWHEIGHT + 30)

    def checkMissileCollision(self, player):
        if self.missiles:
            for missile in self.missiles:
                if polyCircle(player.vertices, missile[0][0], missile[0][1], 2):
                    return True
        return False

    def destroy(self):
        self.isDestroy = True

    def addPoint(self):
        self.points += 1

    def reset(self):
        self.isDestroy = False
        for num in range(len(self.vertices)):
            for num2 in range(len(self.vertices[num])):
                self.vertices[num][num2] = self.verticesCopy[num][num2]
            
        self.direction = [0, 0]

class Blackhole:
    def __init__(self):
        self.r = 15
        self.center = [int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)]
        self.gravity = 0.2

    def update(self, vertices, direction):
        vertexCenter = [int((vertices[0][0] + vertices[1][0] + vertices[2][0]) / 3), int((vertices[0][1] + vertices[1][1] + vertices[2][1]) / 3)]
        normal = math.sqrt(math.pow(vertexCenter[0] - self.center[0], 2) + math.pow(vertexCenter[1] - self.center[1], 2))
        x = -((vertexCenter[0] - self.center[0]) / normal)
        y = -((vertexCenter[1] - self.center[1]) / normal)
        direction[0] += x * self.gravity
        direction[1] += y * self.gravity
        
    def draw(self):
        pygame.draw.circle(screen, WHITE, self.center, self.r, 1)

    def checkCollision(self, player):
        if polyCircle(player.vertices, self.center[0], self.center[1], self.r):
            return True
        return False
        

class Animation:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.duration = 0

    def update(self):
        pass

    def prepare(self):
        pass

class BackgroundAnimation(Animation):
    
    def __init__(self):
        super().__init__()
        self.objectsList = []

    def update(self):
        for i in range(len(self.objectsList)):
 
            # Draw the snow flake
            pygame.draw.circle(screen, WHITE, self.objectsList[i], 2)
 
            # Move the snow flake down one pixel
            self.objectsList[i][1] += 1
 
            # If the snow flake has moved off the bottom of the screen
            if self.objectsList[i][1] > WINDOWHEIGHT:
                # Reset it just above the top
                y = random.randrange(-50, -10)
                self.objectsList[i][1] = y
                # Give it a new x position
                x = random.randrange(0, WINDOWWIDTH)
                self.objectsList[i][0] = x

    def prepare(self):
        for i in range(50):
            x = random.randrange(0, WINDOWWIDTH)
            y = random.randrange(0, WINDOWHEIGHT)
            self.objectsList.append([x, y])

class DestroyAnimation(Animation):

    def __init__(self):
        self.objectsList = []

    def update(self):
        for circle in self.objectsList:
            circle[0] += circle[2]
            circle[1] += circle[3]
            pygame.draw.circle(screen, WHITE, (int(circle[0]), int(circle[1])), circle[4])

    def prepare(self, player):
        center = [int((player.vertices[0][0] + player.vertices[1][0] + player.vertices[2][0]) / 3), int((player.vertices[0][1] + player.vertices[1][1] + player.vertices[2][1]) / 3)]
        for i in range(40):
            randomDirectionX = random.randrange(-20, 20)
            randomDirectionY = random.randrange(-20, 20)
            while(randomDirectionX == 0 or randomDirectionY == 0):
                randomDirectionX = random.randrange(-20, 20)
                randomDirectionY = random.randrange(-20, 20)
            self.objectsList.append([center[0], center[1], randomDirectionX/10, randomDirectionY/10, random.randrange(2, 6)])


def createFont(t, s = 72,c = (255,255,0), b = False, i = False):
    font = pygame.font.SysFont(basicFont, s, bold = b, italic = i)
    text = font.render(t, True, c)
    return text



#Sekcja funkcji poświęcona detekcji kolizji, mianowicie potrzebna jest detekcja okrąg(pocisk oraz pole grawitacyjne) - wielokąt(statek) oraz wielokąt(statek) - wielokąt(statek)
def pointCircle(px, py, cx, cy, r):
    
    distX = px - cx
    distY = py - cy
    distance = math.sqrt( (distX*distX) + (distY*distY) ) #Obliczenie dystansu między punktem a okręgiem

    #Jeżeli dystans jest mniejszy bądź równy promieniu okręgu 
    #wtedy punkt jest w środku okręgu
    if(distance <= r):
       return True
    return False

def linePoint(x1, y1, x2, y2, px, py):
    #Oblicz dystans między punktem a krańcami odcinka
    d1 = math.sqrt((px-x1)**2 + (py-y1)**2)
    d2 = math.sqrt((px-x2)**2 + (py-y2)**2)

    #Oblicz długość odcinka
    lineLen = math.sqrt((x1-x2)**2 + (y1-y2)**2)

    #Bufor zastosowany w celu zwiększenia czułości detekcji
    buffer = 0.1

    #Jeżeli suma dystansów punktu do odcinka jest równa długości odcinka
    #to punkt jest na odcinku
    if(d1 + d2 >= lineLen - buffer and d1 + d2 <= lineLen + buffer):
        return True
    return False

def lineCircle(x1, y1, x2, y2, cx, cy, r):
    inside1 = pointCircle(x1, y1, cx, cy, r)
    inside2 = pointCircle(x2, y2, cx, cy, r)
    if(inside1 or inside2):
        return True

    #Oblicz długość odcinka
    lineLen = math.sqrt((x1-x2)**2 + (y1-y2)**2)

    #Oblicz iloczyn skalarny odcinka i okręgu
    dot = ( ((cx - x1) * (x2 - x1)) + ((cy - y1) * (y2 - y1)) ) / (lineLen**2)

    #Znajdź najbliższy punkt do odcinka
    closestX = x1 + (dot * (x2 - x1))
    closestY = y1 + (dot * (y2 - y1))

    onSegment = linePoint(x1, y1, x2, y2, closestX, closestY)
    if (not onSegment):
        return False

    #Oblicz dystans do najbliższego punktu
    distance = math.sqrt((closestX-cx)**2 + (closestY-cy)**2)

    if(distance <= r):
        return True
    return False

def polyCircle(vertices, cx, cy, r):
    #Przejdź przez wszystkie wierzchołki plus
    #następne na liście (Tak by można było uwzględnić boki wielokąta)
    nextone = 0;
    for current in range(len(vertices)):
        nextone = current + 1
        if(nextone == len(vertices)):
            nextone = 0

        vc = vertices[current]
        vn = vertices[nextone]

        collision = lineCircle(vc[0], vc[1], vn[0], vn[1], cx, cy, r)
        if(collision):
            return True
    return False

def lineLine(x1, y1, x2, y2, x3, y3, x4, y4):

    if (((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)) != 0 and ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)) != 0):
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        
        if(uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
            return True
    return False

def polyLine(vertices, x1, y1, x2, y2):
    nextone = 0
    for current in range(len(vertices)):
        nextone = current + 1
        if(nextone == len(vertices)):
            nextone = 0

        x3 = vertices[current][0]
        y3 = vertices[current][1]
        x4 = vertices[nextone][0]
        y4 = vertices[nextone][1]

        hit = lineLine(x1, y1, x2, y2, x3, y3, x4, y4)
        if(hit):
            return True
    return False

def polyPoly(p1, p2):
    nextone = 0
    for current in range(len(p1)):
        nextone = current + 1
        if(nextone == len(p1)):
            nextone = 0

        vc = p1[current]
        vn = p1[nextone]

        collision = polyLine(p2, vc[0], vc[1], vn[0], vn[1])
        if(collision):
            return True
    return False


mainMenu()
