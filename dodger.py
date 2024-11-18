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


# Ajoutez une variable globale pour les vies
LIVES = 3  # Nombre initial de vies # MODIFICATION

# Charger l'image des cœurs # MODIFICATION
HEART_SIZE = (50, 50)  # Taille des cœurs
heartImage = pygame.image.load('heart.png')  # Image de cœur
heartImage = pygame.transform.scale(heartImage, HEART_SIZE)  # Redimensionner l'image


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

#Fonction pour afficher les coeurs
def drawHearts(surface, lives, heartImage, start_x, start_y):
    """Affiche les cœurs en fonction des vies restantes à une position donnée."""
    for i in range(lives):
        surface.blit(heartImage, (start_x + i * (HEART_SIZE[0] + 5), start_y))

          
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
# Charger les images des joueurs et retirer le fond blanc
NEW_PLAYER_SIZE = (220, 220)  # Taille souhaitée pour le joueur
playerImages = []
for i in range(1, 5):
    image = pygame.image.load(f'player{i}.png').convert()  # Charger l'image
    image.set_colorkey((255, 255, 255))  # Rendre le blanc transparent
    image = pygame.transform.scale(image, NEW_PLAYER_SIZE)  # Redimensionner
    playerImages.append(image)

playerIndex = 0  # Index de l'image courante pour l'animation
playerRect = playerImages[0].get_rect() #CHANGEMENT
baddieImage = pygame.image.load('baddie.png')
backgroundImage = pygame.image.load('Wood.jpg').convert()
bgImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
Speed = 5 # vitesse de défilement de l'arrière-plan
bg_x = 0 # position de départ de l'arrière-plan

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

playerIndex = 0  # CHANGEMENT Index de l'image actuelle pour l'animation
animationCounter = 0  # CHANGEMENT Compteur pour contrôler la vitesse d'animation

topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    lives = LIVES  # Initialiser les vies pour chaque nouvelle partie # MODIFICATION
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

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        top_score_y = 40 + 50  # Position du "Top Score" (40 pixels en haut + taille du texte) #MODIFICATION Affichage des coeurs
        drawHearts(windowSurface, lives, heartImage, 10, top_score_y)

        # Draw the player's rectangle.
        windowSurface.blit(playerImages[playerIndex], playerRect) #CHANGEMENT

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        # Afficher les cœurs restants MODIFICATION
        top_score_y = 40 + 50  # Position du "Top Score" (40 pixels en haut + taille du texte)
        drawHearts(windowSurface, lives, heartImage, 10, top_score_y)


        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            lives -= 1  # Réduire les vies # MODIFICATION
            if lives <= 0:  # Si plus de vies, fin du jeu # MODIFICATION
                if score > topScore:
                    topScore = score  # set new top score
                break
            else:
                # Réinitialisez la position du joueur
                playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)  # MODIFICATION
                baddies = []  # Réinitialisez les baddies # MODIFICATION

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
