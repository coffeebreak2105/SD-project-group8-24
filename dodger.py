import pygame, random, sys
from pygame.locals import *

ANIMATION_SPEED = 5  # CHANGEMENT Vitesse d'animation (nombre de frames avant de changer d'image)
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 50 # changement (lara): avant 30
BADDIEMAXSIZE = 50
BADDIEMINSPEED = 5 # changement (lara): avant 2
BADDIEMAXSPEED = 8 # changement (lara): avant 5
ADDNEWBADDIERATE = 40 # Fréquence d'apparition des ennemis
PLAYERMOVERATE = 5
INPUTBOXCOLOR = (255, 255, 255) # Zone de texte blanche
CORRECTANSWERS = ["31 october", "31st october", "october 31", "31 oct", "31 oct.", "31.10", "31 octobre", "10.31", "octobre 31st"] # Réponses acceptées
FONTSIZE = 40
NEW_PLAYER_SIZE = (250, 250)  # Remplacez par la taille souhaitée pour le personnage
LIVES = 3  # Nombre initial de vies # MODIFICATION
HEART_SIZE = (50, 50)  # Taille des cœurs
JUMPSPEED = 15
GRAVITY = 1
GROUND_LEVEL = WINDOWHEIGHT - 50  # Changement (lara)/ Niveau du sol pour le personnage et les ennemis
game_over = False  # Ajout : Indique si le joueur a perdu
win = False  # Ajout : Indique si le joueur a gagné

# Images pour les ennemis
baddie_images = [
    pygame.image.load('baddie1.png'),
    pygame.image.load('baddie2.png'),
    pygame.image.load('baddie3.png'),
    pygame.image.load('baddie4.png'),
]

def get_baddie_types_by_level(level):
    """Retourne les types de baddies disponibles pour un niveau donné."""
    if level == 1:
        return ['baddie1', 'baddie2']
    elif level == 2:
        return ['baddie2', 'baddie3']
    elif level == 3:
        return ['baddie3', 'baddie4']
    else:
        return []  # Aucun baddie pour les autres niveaux

class Baddie:
    def __init__(self, images, min_size, max_size, min_speed, max_speed, level_baddie_types):
        baddie_types = {
            'baddie1': images[0],
            'baddie2': images[1],
            'baddie3': images[2],
            'baddie4': images[3],
        }

        # Choisir un type de baddie spécifique
        self.baddie_type = random.choice(level_baddie_types)

        self.image = pygame.transform.scale(
            baddie_types[self.baddie_type],
            (random.randint(min_size, max_size), random.randint(min_size, max_size))
        )
        self.speed = random.randint(min_speed, max_speed)

        # Initialiser la position selon le type
        if self.baddie_type in ['baddie1', 'baddie2']:
            # Mouvement horizontal au sol
            self.rect = pygame.Rect(
                WINDOWWIDTH, 
                GROUND_LEVEL, # changement (lara)
                self.image.get_width(),
                self.image.get_height()
            )
        elif self.baddie_type == 'baddie3':
            # Mouvement volant
            start_y = GROUND_LEVEL - 150 # changement (lara)
            self.rect = pygame.Rect(
                WINDOWWIDTH, 
                start_y, # changement (lara)
                self.image.get_width(),
                self.image.get_height()
            )
            # Oscillation verticale, changement (lara)
            self.vertical_speed = 2
            self.amplitude_top = start_y - 200
            self.amplitude_bottom = start_y + 200
        elif self.baddie_type == 'baddie4':
            # Mouvement tombant
            self.rect = pygame.Rect(
                random.randint(0, WINDOWWIDTH - self.image.get_width()), 
                -self.image.get_height(),
                self.image.get_width(),
                self.image.get_height()
            )

    def move(self):
        # Mouvement défini par le type
        if self.baddie_type in ['baddie1', 'baddie2']:
            # Mouvement horizontal classique (droite → gauche au sol)
            self.rect.move_ip(-self.speed, 0)
        elif self.baddie_type == 'baddie3':
            # Mouvement volant avec oscillation verticale
            self.rect.move_ip(-self.speed, self.vertical_speed)
            # Inverser la direction verticale si nécessaire
            if self.rect.top <= self.amplitude_top or self.rect.bottom >= self.amplitude_bottom: # cahngement (lara)
                self.vertical_speed *= -1
        elif self.baddie_type == 'baddie4':
            # Mouvement vertical (chute)
            self.rect.move_ip(0, self.speed)

    def is_off_screen(self):
        # Vérifier si le *baddie* est hors de l'écran
        return (
            self.rect.right < 0 or
            (self.baddie_type == 'baddie4' and self.rect.top > WINDOWHEIGHT)
        ) 
    

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
        if playerRect.colliderect(b.rect):
            return True
    return False

def displayGameOverScreen():
    """Affiche l'écran de Game Over."""
    global score  # Ajoutez cette ligne pour modifier la variable globale `score`.
    windowSurface.fill((0, 0, 0))  # Fond noir
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 2), (255, 0, 0))
    drawText('Press any key to restart.', font, windowSurface, (WINDOWWIDTH / 3.5), (WINDOWHEIGHT / 2) + 50, TEXTCOLOR)
    pygame.display.update()
    waitForPlayerToPressKey()
    score = 0  # Réinitialise le score après que le joueur a appuyé sur une touche.


def displayWinScreen():
    """Affiche la séquence de victoire avec trois images en boucle et attend une touche."""
    win_images = [pygame.image.load(f'win{i}.png') for i in range(1, 4)]
    scaled_images = [pygame.transform.scale(image, (WINDOWWIDTH, WINDOWHEIGHT)) for image in win_images]

    current_index = 0  # Index de l'image actuelle
    animation_counter = 0  # Compteur pour l'animation
    animation_speed = FPS // 12  # Vitesse d'animation (3 images par seconde)

    while True:
        # Gestion des événements pour détecter une touche
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return  # Quitte la fonction si une touche est pressée

        # Afficher l'image actuelle
        windowSurface.blit(scaled_images[current_index], (0, 0))
        drawText('Press any key to restart', font, windowSurface, WINDOWWIDTH // 3, WINDOWHEIGHT - 150, TEXTCOLOR)
        pygame.display.update()

        # Gérer l'animation des images
        animation_counter += 1
        if animation_counter >= animation_speed:
            animation_counter = 0
            current_index = (current_index + 1) % len(scaled_images)

        mainClock.tick(FPS)


def drawText(text, font, surface, x, y, color=None):
    if color is None:
        color = TEXTCOLOR
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawHearts(surface, lives, heartImage, start_x, start_y): # Fonction pour afficher les coeurs
    # Affiche les cœurs en fonction des vies restantes à une position donnée
    for i in range(lives):
        surface.blit(heartImage, (start_x + i * (HEART_SIZE[0] + 5), start_y))

def play_level_music(level): # Fonction pour changer sound des levels
    if level in level_sounds:
        pygame.mixer.music.load(level_sounds[level])
        pygame.mixer.music.play(-1, 0.0)

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
collectObjectMagic = pygame.mixer.Sound('pickup.wav')
# Sounds for levels
level_sounds = { 
    1: 'sound_level1.mp3',
    2: 'sound_level2.mp3',
    3: 'sound_level3.mp3',
}

# Set up images. CHANGEMENT
# Charger les images des joueurs et retirer le fond blanc
playerImages = []
for i in range(1, 7):
    image = pygame.image.load(f'player{i}.png').convert_alpha()
    image.set_colorkey((0, 0, 0))  # Rendre le fond noir transparent
    image = pygame.transform.smoothscale(image, NEW_PLAYER_SIZE)
    playerImages.append(image)
heartImage = pygame.image.load('heart.png')  # Image de cœur
heartImage = pygame.transform.scale(heartImage, HEART_SIZE)  # Redimensionner l'image
backgroundImage_StartScreen = pygame.image.load('start.webp')
bgImage_StartScreen = pygame.transform.scale(backgroundImage_StartScreen, (WINDOWWIDTH, WINDOWHEIGHT))

# Images pour les backgrounds
backgrounds = { 
    1: pygame.transform.scale(pygame.image.load('Wood.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
    2: pygame.transform.scale(pygame.image.load('Wood2.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
    3: pygame.transform.scale(pygame.image.load('Wood3.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
}

# Show the "Start" screen.
windowSurface.blit(bgImage_StartScreen, (0,0))
drawText('Spooky Sprint', font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 6))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2.5) - 30, (WINDOWHEIGHT / 6) + 60)
pygame.display.update()
waitForPlayerToPressKey()

# Set up player.
playerIndex = 0  # CHANGEMENT Index de l'image actuelle pour l'animation
animationCounter = 0  # CHANGEMENT Compteur pour contrôler la vitesse d'animation
playerRect = playerImages[0].get_rect()

# Set up lives.
top_score_y = 40 + 50  # Position du "Top Score" (40 pixels en haut + taille du texte)

# Set up backgroundImage.
Speed = 5 # vitesse de défilement de l'arrière-plan
bg_x = 0 # position de départ de l'arrière-plan

# Set up ObjectMagic.
frog = ObjectMagic('Frog.png', (50,50), 200, GROUND_LEVEL, Speed) #changement lara
bird = ObjectMagic('Bird.png', (50,50), 300, GROUND_LEVEL, Speed)
teapot = ObjectMagic('TeaPot.png', (50,50), 500, GROUND_LEVEL, Speed)
# Initialiser position horizontale pour chaque objet
frog.rect.x = WINDOWWIDTH
bird.rect.x = WINDOWWIDTH
teapot.rect.x = WINDOWWIDTH

#Question bonus
def questionScreen():
    # Affiche une question avec une zone de réponse
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

score = questionScreen()

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
    level = 1
    playerRect.topleft = (WINDOWWIDTH / 2, GROUND_LEVEL - 30) # changement lara
    previous_level = None # Pour son dans level
    moveLeft = moveRight = False
    reverseCheat = slowCheat = False
    isJumping = False
    canDoubleJump = False
    jumpSpeed = JUMPSPEED  # Initial jump speed
    baddieAddCounter = 0
    lives = LIVES  # Initialiser les vies pour chaque nouvelle partie # MODIFICATION
    score = 0
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
                if event.key == K_SPACE and not isJumping:
                    # Premier saut
                    isJumping = True  # Start the jump
                    canDoubleJump = True # Activer le double saut
                    jumpSpeed = JUMPSPEED  # Reset jump speed for the jump
                elif canDoubleJump :
                    # Double saut 
                    canDoubleJump = False # désactiver le double saut
                    jumpSpeed = JUMPSPEED


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


        # Add new baddies from the right side at the bottom of the screen.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            level_baddie_types = get_baddie_types_by_level(level)  # Obtenez les types pour le niveau
            if level_baddie_types:  # Si des types sont disponibles pour ce niveau
                baddies.append(Baddie(baddie_images, BADDIEMINSIZE, BADDIEMAXSIZE, BADDIEMINSPEED, BADDIEMAXSPEED, level_baddie_types))


        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        
        # Handle jumping
        if isJumping:
            playerRect.move_ip(0, -jumpSpeed)  # Move up initially
            jumpSpeed -= GRAVITY  # Gravity effect

            # If the player lands on the ground
            if playerRect.bottom >= GROUND_LEVEL + 50: # changement lara
                playerRect.bottom = GROUND_LEVEL + 50  # changement lara
                isJumping = False
                canDoubleJump = False
                jumpSpeed = JUMPSPEED  # Réinitialise la vitesse de saut pour la prochaine fois

        
        # Update player animation CHANGEMENT # changer ça de place
        animationCounter += 1
        if animationCounter >= ANIMATION_SPEED:
            animationCounter = 0
            playerIndex = (playerIndex + 1) % len(playerImages)  # Passer à l'image suivante en boucle

        # Move the baddies to the left across the bottom of the screen.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b.move()  # Move left
            elif reverseCheat:
                b.rect.move_ip(5, 0) # Move right if reverse cheat is active
            elif slowCheat:
                b.rect.move_ip(-1, 0) # Move left slowly if slow cheat is active

        # Delete baddies that have gone off the left side of the screen.
        baddies = [b for b in baddies if not b.is_off_screen()]

        # Draw scrolling background
        bgImage = backgrounds[level] # définir background selon level
        windowSurface.blit(bgImage, (bg_x, 0))
        windowSurface.blit(bgImage, (bg_x + WINDOWWIDTH, 0))
        bg_x -= Speed # déplacer arrière-plan vers la gauche

        if bg_x <= -WINDOWWIDTH:
            bg_x = 0
        
        # Vérification si level a changé pour le sound
        if level != previous_level:
            play_level_music(level)
            previous_level = level
        
        # Draw ObjectMagic with levels.
        if level == 1:
            # Déplacement de l'objet frog
            windowSurface.blit(frog.image, (frog.rect.x, frog.rect.y))
            frog.rect.x -= frog.speed
            if frog.rect.x <= -frog.rect.width:
                frog.rect.x = WINDOWWIDTH
            # Vérification collision player et objet magique
            if playerRect.colliderect(frog.rect):
                score += frog.points
                frog.rect.x = WINDOWWIDTH
                collectObjectMagic.play()
        elif level == 2:
            windowSurface.blit(bird.image, (bird.rect.x, bird.rect.y))
            bird.rect.x -= bird.speed
            if bird.rect.x <= -bird.rect.width:
                bird.rect.x = WINDOWWIDTH
            if playerRect.colliderect(bird.rect):
                score += bird.points
                bird.rect.x = WINDOWWIDTH
                collectObjectMagic.play()
        elif level == 3:
            windowSurface.blit(teapot.image, (teapot.rect.x, teapot.rect.y))
            teapot.rect.x -= teapot.speed
            if teapot.rect.x <= -teapot.rect.width:
                teapot.rect.x = WINDOWWIDTH
            if playerRect.colliderect(teapot.rect):
                score += teapot.points
                teapot.rect.x = WINDOWWIDTH
                collectObjectMagic.play()
        # Passage au level suivant
        if score >= 1000 * level:
            level += 1
            if level > 3:
                displayWinScreen()  # Affiche les images de victoire 
                level = 1  # Réinitialise le niveau
                score = 0  # Réinitialise le score
                break  # Quitte la boucle pour redémarrer une nouvelle partie


        # Draw the score, top score, level, lives.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Level: %s' % (level), font, windowSurface, WINDOWWIDTH - 200, 10)
        drawHearts(windowSurface, lives, heartImage, 10, top_score_y)

        # Draw the player's rectangle.
        windowSurface.blit(playerImages[playerIndex], playerRect) #CHANGEMENT

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b.image, b.rect)


        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            lives -= 1  # Réduire les vies # MODIFICATION
            if lives <= 0:  # Si plus de vies, fin du jeu # MODIFICATION
                if score > topScore:
                    topScore = score  # set new top score
                    displayGameOverScreen()  # Afficher l'écran Game Over
                break
            else:
                # Réinitialisez la position du joueur
                playerRect.topleft = (WINDOWWIDTH / 2, GROUND_LEVEL - 30)  # MODIFICATION # Changement lara
                baddies = []  # Réinitialisez les baddies # MODIFICATION

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
if game_over:
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3), (255, 0, 0))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
elif win:
    displayWinScreen()  # Affiche l'écran de victoire
    gameOverSound.stop()