import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 2
BADDIEMAXSPEED = 5
ADDNEWBADDIERATE = 40 # Fréquence d'apparition des ennemis
PLAYERMOVERATE = 5
JUMPSPEED = 15
GRAVITY = 1
GROUND_LEVEL = WINDOWHEIGHT - 70  # Niveau du sol pour le personnage et les ennemis

# Classe Baddie
class Baddie:
    def __init__(self, images, min_size, max_size, min_speed, max_speed):
        self.size = random.randint(min_size, max_size)
        self.image = pygame.transform.scale(
            random.choice(images), (self.size, self.size)
        )
        self.speed = random.randint(min_speed, max_speed)
        self.rect = pygame.Rect(WINDOWWIDTH, GROUND_LEVEL - self.size, self.size, self.size)

    def move(self):
        self.rect.move_ip(-self.speed, 0)

    def is_off_screen(self):
        return self.rect.right < 0
    
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

# Set up images.
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()

# Images pour les ennemis
baddie_images = [
    pygame.image.load('baddie1.png'),
    pygame.image.load('baddie2.png'),
    pygame.image.load('baddie3.png'),
    pygame.image.load('baddie4.png'),
]

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, GROUND_LEVEL -playerRect.height)
    moveLeft = moveRight = False
    reverseCheat = slowCheat = False
    isJumping = False
    jumpSpeed = JUMPSPEED  # Initial jump speed
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
                if event.key == K_SPACE and not isJumping:
                    isJumping = True  # Start the jump
                    jumpSpeed = JUMPSPEED  # Reset jump speed for the jump

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
            baddies.append(Baddie(baddie_images, BADDIEMINSIZE, BADDIEMAXSIZE, BADDIEMINSPEED, BADDIEMAXSPEED))

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
            if playerRect.bottom >= GROUND_LEVEL:
                playerRect.bottom = GROUND_LEVEL
                isJumping = False
                jumpSpeed = JUMPSPEED  # Réinitialise la vitesse de saut pour la prochaine fois

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

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b.image, b.rect)

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
