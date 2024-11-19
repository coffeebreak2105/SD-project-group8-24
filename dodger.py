import pygame, random, sys
from pygame.locals import *

ANIMATION_SPEED = 5  # CHANGEMENT Vitesse d'animation (nombre de frames avant de changer d'image)
WINDOWWIDTH = 1500
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

class ObjectMagic:
    def __init__(self, image_path, scale_size, points, y_position, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale_size)
        self.rect = self.image.get_rect()
        self.rect.y = y_position
        self.rect.x = WINDOWWIDTH
        self.points = points
        self.speed = speed

    def move_and_draw(self, surface):
        self.rect.x -= self.speed # Déplacer l'objet vers la gauche
        if self.rect.right < 0: # Si l'objet sort de l'écran, le remettre à droite
            self.rect.x = WINDOWWIDTH
        surface.blit(self.image, self.rect) # Afficher l'image de l'objet sur la surface

    def check_collision(self, player_rect):
        if player_rect.colliderect(self.rect): # Vérifier la collision avec le joueur
            self.rect.x = WINDOWWIDTH # Réinitialiser la position de l'objet à droite de l'écran après la collision
            return self.points  # Retourne les points pour ajouter au score
        return 0  # Pas de collision, pas de points

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images. CHANGEMENT
NEW_PLAYER_SIZE = (80, 80)  # Remplacez par la taille souhaitée pour le personnage
playerImages = [pygame.transform.scale(pygame.image.load(f'player{i}.png'), NEW_PLAYER_SIZE) for i in range(1, 5)]
playerIndex = 0  # Index de l'image courante pour l'animation
playerRect = playerImages[0].get_rect() #CHANGEMENT
baddieImage = pygame.image.load('baddie.png')
backgroundImage = pygame.image.load('Wood.jpg').convert()
bgImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
#birdImage = pygame.image.load('Bird.png').convert_alpha() 
#frogImage = pygame.image.load('Frog.png').convert_alpha()
#frogImage = pygame.transform.scale(frogImage, (100, 100))
#teapotImage = pygame.image.load('TeaPot.png').convert_alpha()

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

# Set up player.
playerIndex = 0  # CHANGEMENT Index de l'image actuelle pour l'animation
animationCounter = 0  # CHANGEMENT Compteur pour contrôler la vitesse d'animation

# Set up backgroundImage.
Speed = 5 # vitesse de défilement de l'arrière-plan
bg_x = 0 # position de départ de l'arrière-plan

# Set up ObjectMagic.
#frogRect = frogImage.get_rect() # obtenir dimension image
#frogRect.bottom = WINDOWHEIGHT # positionner en bas de la fenêtre
#frog_x = 0 # position initiale en x de frogImage alignée à gauche
#frogMagic = ObjectMagic(10)
frog = ObjectMagic('Frog.png', (50,50), 1000, WINDOWHEIGHT-50, Speed)
bird = ObjectMagic('Bird.png', (50,50), 15, WINDOWHEIGHT-100, Speed)
teapot = ObjectMagic('TeaPot.png', (50,50), 20, WINDOWHEIGHT-150, Speed)

topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
        # Update player animation CHANGEMENT
        animationCounter += 1
        if animationCounter >= ANIMATION_SPEED:
            animationCounter = 0
            playerIndex = (playerIndex + 1) % len(playerImages)  # Passer à l'image suivante en boucle

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw scrolling background
        windowSurface.blit(bgImage, (bg_x, 0))
        windowSurface.blit(bgImage, (bg_x + WINDOWWIDTH, 0))
        bg_x -= Speed # déplacer arrière-plan vers la gauche

        if bg_x <= -WINDOWWIDTH:
            bg_x = 0

        # Draw ObjectMagic.
        #windowSurface.blit(frogImage, (frog_x, frogRect.y))
        #frog_x -= Speed # déplacement frog vers la gauche avec le fond

        #if frog_x <= -frogRect.width:
            #frog_x = WINDOWWIDTH
        # Mettre a jour position de frogRect en fonction de frog_x.
        #frogRect.x = frog_x
        #frogRect.y = WINDOWHEIGHT - frogRect.height
        
        # Check if player has hit ObjectMagic.
        #if playerRect.colliderect(frogRect):
            #score += frogMagic.points
            #frog_x = WINDOWWIDTH
        
        # Draw ObjectMagic v2.
        score += frog.check_collision(playerRect)
        frog.move_and_draw(windowSurface)

        score += bird.check_collision(playerRect)
        bird.move_and_draw(windowSurface)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImages[playerIndex], playerRect) #CHANGEMENT

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
