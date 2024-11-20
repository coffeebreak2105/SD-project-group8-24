import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 1200
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
TEXTCOLOR = (0, 0, 0)             # Texte noir
INPUTBOXCOLOR = (255, 255, 255)   # Zone de texte blanche
CORRECTANSWERS = ["31 october", "31st october", "october 31", "31 oct", "31 oct.", "31.10", "31 octobre"]  # Réponses acceptées
FONTSIZE = 40

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
pygame.display.set_caption('Spooky Sprint')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48) # taille 48 pour le texte

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
pygame.mixer.music.load('soundstart.mp3') # musique page accueil
pygame.mixer.music.play(-1, 0.0) # -1 pour que la musique soit à l'infini

# Set up images.
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')
backgroundImage_StartScreen = pygame.image.load('start.webp')
bgImage_StartScreen = pygame.transform.scale(backgroundImage_StartScreen, (WINDOWWIDTH, WINDOWHEIGHT))

# Show the "Start" screen.
windowSurface.blit(bgImage_StartScreen, (0,0))
#windowSurface.fill(BACKGROUNDCOLOR)
drawText('Spooky Sprint', font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 6))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2.5) - 30, (WINDOWHEIGHT / 6) + 60)
pygame.display.update()
waitForPlayerToPressKey()

#Question bonus
# Initialisation de Pygame
pygame.init()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Spooky Sprint")
font = pygame.font.SysFont(None, FONTSIZE)

# Chargement de l'image de fond
backgroundImage_StartScreen = pygame.image.load('start.webp')
bgImage_StartScreen = pygame.transform.scale(backgroundImage_StartScreen, (WINDOWWIDTH, WINDOWHEIGHT))

def drawText(text, font, surface, x, y, color=TEXTCOLOR):
    """Affiche du texte à une position donnée."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def questionScreen():
    """Affiche une question avec une zone de réponse."""
    input_text = ""  # Texte saisi par le joueur
    question = "When is Halloween?"  # La question
    score = 0  # Score initial

    # Boucle pour afficher l'écran de question
    while True:
        windowSurface.blit(bgImage_StartScreen, (0, 0))  # Affiche l'image de fond

        # Positionnement de la question et de la zone de texte
        question_x = (WINDOWWIDTH - font.size(question)[0]) / 2
        question_y = WINDOWHEIGHT / 3
        input_box_x = (WINDOWWIDTH - 400) / 2  # Zone de saisie centrée (largeur 400)
        input_box_y = question_y + 70

        # Afficher la question
        drawText(question, font, windowSurface, question_x, question_y)

        # Dessiner la zone de texte
        input_box = pygame.Rect(input_box_x, input_box_y, 400, 50)
        pygame.draw.rect(windowSurface, INPUTBOXCOLOR, input_box)  # Fond blanc
        pygame.draw.rect(windowSurface, TEXTCOLOR, input_box, 2)  # Bordure noire

        # Afficher le texte saisi
        drawText(input_text, font, windowSurface, input_box.x + 10, input_box.y + 10)

        # Mettre à jour l'affichage
        pygame.display.update()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # Appui sur Entrée
                    if input_text.lower() in CORRECTANSWERS:  # Vérifie la réponse
                        score = 100
                        return score
                    else:
                        drawText("Wrong Answer!", font, windowSurface, input_box_x, input_box_y + 80, (255, 0, 0))
                        pygame.display.update()
                        pygame.time.wait(2000)  # Pause pour afficher l'erreur
                        return score  # Score reste à 0
                elif event.key == K_BACKSPACE:  # Supprime un caractère
                    input_text = input_text[:-1]
                else:  # Ajoute du texte tapé
                    input_text += event.unicode

# Exemple d'utilisation
score = questionScreen()
print("Score du joueur:", score)

# Écran de démarrage du jeu
windowSurface.blit(bgImage_StartScreen, (0, 0))
drawText('Spooky Sprint', font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 6))
drawText(f'Your starting score: {score}', font, windowSurface, (WINDOWWIDTH / 2.5) - 30, (WINDOWHEIGHT / 6) + 60)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2.5) - 30, (WINDOWHEIGHT / 6) + 120)
pygame.display.update()

# Attente d'une touche pour commencer
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Débuter la partie après la touche pressée
            break
    else:
        continue
    break

topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
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

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

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
