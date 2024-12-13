import pygame, random, sys
from pygame.locals import *

ANIMATION_SPEED = 5
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 50
BADDIEMAXSIZE = 50
BADDIEMINSPEED = 5
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 40
PLAYERMOVERATE = 5
INPUTBOXCOLOR = (255, 255, 255)
CORRECTANSWERS = ["31 october", "31st october", "31st of october", "october 31", "31 oct", "31 oct.", "31.10", "31 octobre", "10.31", "octobre 31st"]
FONTSIZE = 40
NEW_PLAYER_SIZE = (80, 80)
LIVES = 3
HEART_SIZE = (50, 50)
JUMPSPEED = 15
GRAVITY = 1
GROUND_LEVEL = WINDOWHEIGHT - 50

class Baddie:
    def __init__(self, images, min_size, max_size, min_speed, max_speed, level_baddie_types, crush_sprites=None, bounce_sound=None):
        #Defines the types of baddies and their specific images
        baddie_types = {
            'baddie1': images[0], 
            'baddie2': images[1], 
            'baddie3': images[2],  
            'baddie4': images[3], 
        }

        # Chooses a specific type of baddie
        self.baddie_type = random.choice(level_baddie_types)
        self.image = pygame.transform.scale(
            baddie_types[self.baddie_type],
            (random.randint(min_size, max_size), random.randint(min_size, max_size))
        )
        self.speed = random.randint(min_speed, max_speed)

        # Specific resources for pumpkins
        self.crush_sprites = crush_sprites if self.baddie_type == 'baddie1' else None
        self.bounce_sound = bounce_sound if self.baddie_type == 'baddie1' else None

        # Specific bat resources
        self.is_falling = False  # Indicates whether the bat is falling
        self.fall_speed = 2 

        # Initialises position according to type
        if self.baddie_type in ['baddie1', 'baddie2']:
            # Horizontal movement on the ground
            self.rect = pygame.Rect(
                WINDOWWIDTH, 
                GROUND_LEVEL,
                self.image.get_width(),
                self.image.get_height()
            )
        elif self.baddie_type == 'baddie3':
            # Flying movement
            start_y = GROUND_LEVEL - 120
            self.rect = pygame.Rect(
                WINDOWWIDTH, 
                start_y,
                self.image.get_width(),
                self.image.get_height()
            )
            # Vertical oscillation
            self.vertical_speed = 2
            self.amplitude_top = start_y - 200
            self.amplitude_bottom = start_y + 200
        elif self.baddie_type == 'baddie4':
            # Falling movement
            self.rect = pygame.Rect(
                random.randint(0, WINDOWWIDTH - self.image.get_width()), 
                -self.image.get_height(),
                self.image.get_width(),
                self.image.get_height()
            )

    def move(self):
        # Movement defined by type
        if self.baddie_type in ['baddie1', 'baddie2']:
            # Classic horizontal movement
            self.rect.move_ip(-self.speed, 0)
        elif self.baddie_type == 'baddie3':
            # Flying movement with vertical oscillation
            self.rect.move_ip(-self.speed, self.vertical_speed)
            # Reverse vertical direction if necessary
            if self.rect.top <= self.amplitude_top or self.rect.bottom >= self.amplitude_bottom:
                self.vertical_speed *= -1
        elif self.baddie_type == 'baddie4':
            # Vertical movement (fall)
            self.rect.move_ip(0, self.speed)

    def is_off_screen(self):
        # Checks whether the "baddie" is off the screen
        return (
            self.rect.right < 0 or
            (self.baddie_type == 'baddie4' and self.rect.top > WINDOWHEIGHT)
        ) 
    
    def play_crush_animation(self, surface):
        # Plays the destruction animation for a pumpkin
        if self.baddie_type == 'baddie1' and self.crush_sprites:
            for sprite in self.crush_sprites:
                surface.blit(sprite, self.rect)  # Displays each sprite at the baddie position
                pygame.display.update()
                pygame.time.delay(40)  # Pause between each image
            if self.bounce_sound:
                self.bounce_sound.play()  # Plays the bounce sound
    
    def fall_to_ground(self):
        # Drops the bat gently to the ground
        target_y = GROUND_LEVEL - self.rect.height  # Target height
        if self.is_falling and self.rect.y < target_y:
            self.rect.y += self.fall_speed
        elif self.rect.y >= target_y:
            self.is_falling = False  # Stops the fall when the target height is reached
   
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
        self.rect.x -= self.speed # Moves object to the left
        if self.rect.right < 0: # If the object leaves the screen, moves it back to the right
            self.rect.x = WINDOWWIDTH
        surface.blit(self.image, self.rect) # Displays the image of the object on the surface

    def check_collision(self, player_rect):
        if player_rect.colliderect(self.rect): # Checks collision with player
            self.rect.x = WINDOWWIDTH # Reset the position of the object to the right of the screen after the collision
            return self.points  # Returns points to add to the score
        return 0  # No collision, no points

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
    for baddie in baddies:
        if playerRect.colliderect(baddie.rect):  # Checks collision
            # Case 1: Collision from above
            if playerRect.bottom <= baddie.rect.top + 10:
                return baddie, True  # Collision from above

            # Case 2: Collision from below (baddie3 only)
            elif baddie.baddie_type == 'baddie3' and playerRect.top <= baddie.rect.bottom and playerRect.centery > baddie.rect.bottom:
                return baddie, "bas"  # Collision from under

            # Case 3: Classic collision (side or other)
            else:
                return baddie, False  # Classic collision 
    return None, None  # No collision

def get_baddie_types_by_level(level):
    # Returns the types of baddies available for a given level
    if level == 1:
        return ['baddie1', 'baddie2']
    elif level == 2:
        return ['baddie2', 'baddie3']
    elif level == 3:
        return ['baddie3', 'baddie4']
    else:
        return []  # No baddie for other levels

def play_crush_animation(surface, baddie_rect): # Pumpkin animation function
    for sprite in crush_sprites:
        surface.blit(sprite, baddie_rect)
        pygame.display.update()
        pygame.time.delay(40)  # 40 ms pause between each image

def displayGameOverScreen():
    # Displays the Game Over screen
    global score  # Adds this line to modify the global variable `score`.
    windowSurface.fill((0, 0, 0))  # Black background
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 2), (255, 0, 0))
    drawText('Press any key to restart.', font, windowSurface, (WINDOWWIDTH / 3.5), (WINDOWHEIGHT / 2) + 50, TEXTCOLOR)
    pygame.display.update()
    waitForPlayerToPressKey()
    score = 0  # Resets the score after the player has pressed a key.

def displayWinScreen():
    # Displays the victory sequence with three images in a loop and waits for a key
    pygame.mixer.music.stop()
    win_images = [pygame.image.load(f'win{i}.png') for i in range(1, 4)]
    scaled_images = [pygame.transform.scale(image, (WINDOWWIDTH, WINDOWHEIGHT)) for image in win_images]

    current_index = 0  # Index of the current image
    animation_counter = 0  # Counter for animation
    animation_speed = FPS // 12  # Animation speed (3 frames per second)

    while True:
        # Event management to detect a button
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return  # Exits the function if a key is pressed

        # Shows current image
        windowSurface.blit(scaled_images[current_index], (0, 0))
        drawText('Press any key to restart', font, windowSurface, WINDOWWIDTH // 3, WINDOWHEIGHT - 150, TEXTCOLOR)
        pygame.display.update()

        # Manages the animation of images
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

def drawHearts(surface, lives, heartImage, start_x, start_y):
    # Displays hearts according to lives remaining at a given position
    for i in range(lives):
        surface.blit(heartImage, (start_x + i * (HEART_SIZE[0] + 5), start_y))

def play_level_music(level):
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
font = pygame.font.SysFont(None, 48)

# Set up sounds.
collectObjectMagic = pygame.mixer.Sound('pickup.wav')
bounce_sound = pygame.mixer.Sound('bounce.wav')
bonk_sound = pygame.mixer.Sound('bonk.mp3')

# Set up sounds for levels.
level_sounds = { 
    1: 'sound_level1.mp3',
    2: 'sound_level2.mp3',
    3: 'sound_level3.mp3',
}

# Set up images.
playerImages = []
for i in range(1, 5):
    image = pygame.image.load(f'player{i}.png').convert()
    image.set_colorkey((0, 0, 0))
    image = pygame.transform.scale(image, NEW_PLAYER_SIZE)
    playerImages.append(image)
heartImage = pygame.image.load('heart.png')
heartImage = pygame.transform.scale(heartImage, HEART_SIZE)
backgroundImage_StartScreen = pygame.image.load('start.webp')
bgImage_StartScreen = pygame.transform.scale(backgroundImage_StartScreen, (WINDOWWIDTH, WINDOWHEIGHT))
# Baddies images
baddie_images = [
    pygame.image.load('baddie1.png'),
    pygame.image.load('baddie2.png'),
    pygame.image.load('baddie3.png'),
    pygame.image.load('baddie4.png'),
]
# Image for the pumpkin animation 
crush_sprites = [
    pygame.transform.scale(
        pygame.image.load(f'Pumpkin{i}.png').convert_alpha(),
        (BADDIEMAXSIZE, BADDIEMAXSIZE)  # Resizes images to the maximum size of the baddies
    )
    for i in range(1, 7)  # Charges Pumpkin1.png à Pumpkin6.png
]
# Resizes images to the maximum size of the baddies
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

# Set up the win page.
game_over = False 
win = False 

# Set up player.
playerIndex = 0  # Index of the current image for the animation
animationCounter = 0  # Counter to control animation speed
playerRect = playerImages[0].get_rect()

# Set up lives.
top_score_y = 40 + 50  # "Top Score" position on the screen

# Set up backgroundImage.
Speed = 5 
bg_x = 0 

# Set up ObjectMagic.
frog = ObjectMagic('Frog.png', (50,50), 100, GROUND_LEVEL, Speed)
bird = ObjectMagic('Bird.png', (50,50), 200, GROUND_LEVEL, Speed)
teapot = ObjectMagic('TeaPot.png', (50,50), 300, GROUND_LEVEL, Speed)
# Sets horizontal position for each object
frog.rect.x = WINDOWWIDTH
bird.rect.x = WINDOWWIDTH
teapot.rect.x = WINDOWWIDTH

# Bonus question
def questionScreen():
    # Displays a question with an answer box
    input_text = ""  
    question = "When is Halloween?" 
    score = 0 

    # Loop to display the question screen
    while True:
        windowSurface.blit(bgImage_StartScreen, (0, 0)) 

        # Places the question and text box
        question_x = (WINDOWWIDTH - font.size(question)[0]) / 2
        question_y = WINDOWHEIGHT / 3
        input_box_x = (WINDOWWIDTH - 400) / 2 
        input_box_y = question_y + 70

        # Show question
        drawText(question, font, windowSurface, question_x, question_y)

        # Draws the text box
        input_box = pygame.Rect(input_box_x, input_box_y, 400, 50)
        pygame.draw.rect(windowSurface, INPUTBOXCOLOR, input_box)
        pygame.draw.rect(windowSurface, TEXTCOLOR, input_box, 2)

        # Displays text entered
        drawText(input_text, font, windowSurface, input_box.x + 10, input_box.y + 10)

        # Updates display
        pygame.display.flip()

        # Event management
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if input_text.lower() in CORRECTANSWERS:
                        return 100 
                    else:
                        drawText("Wrong Answer!", font, windowSurface, input_box_x, input_box_y + 80, (255, 0, 0))
                        pygame.display.update()
                        pygame.time.wait(2000) 
                        return 0  
                elif event.key == K_BACKSPACE:  
                    input_text = input_text[:-1]
                else: 
                    input_text += event.unicode

score = questionScreen()

# Game start screen
windowSurface.blit(bgImage_StartScreen, (0, 0))
drawText('Spooky Sprint', font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 6))
drawText(f'Your starting score: {score}', font, windowSurface, (WINDOWWIDTH / 2.5) - 30, (WINDOWHEIGHT / 6) + 60)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2.5) - 30, (WINDOWHEIGHT / 6) + 120)
pygame.display.update()

# Waiting for a keypress to start
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Start the game after the key has been pressed
            break
    else:
        continue
    break


topScore = 0
while True:
    # Set up the start of the game.
    baddies = []
    level = 1
    playerRect.topleft = (WINDOWWIDTH / 2, GROUND_LEVEL - 30) 
    previous_level = None 
    moveLeft = moveRight = False
    reverseCheat = slowCheat = False
    isJumping = False
    canDoubleJump = False
    jumpSpeed = JUMPSPEED  
    baddieAddCounter = 0
    lives = LIVES 

    while True: # The game loop runs while the game part is playing.
        score += 1

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
                    # First jump 
                    isJumping = True 
                    canDoubleJump = True 
                    jumpSpeed = JUMPSPEED  
                elif canDoubleJump :
                    # Double jump 
                    canDoubleJump = False
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
            level_baddie_types = get_baddie_types_by_level(level)  # Gets the types of baddie for the level
            if level_baddie_types:  # If baddies types are available for this level
                baddies.append(Baddie(baddie_images, BADDIEMINSIZE, BADDIEMAXSIZE, BADDIEMINSPEED, BADDIEMAXSPEED, level_baddie_types, crush_sprites=crush_sprites, bounce_sound=bounce_sound))

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        
        # Handle jumping
        if isJumping:
            playerRect.move_ip(0, -jumpSpeed)
            jumpSpeed -= GRAVITY

            # If the player lands on the ground
            if playerRect.bottom >= GROUND_LEVEL + 50:
                playerRect.bottom = GROUND_LEVEL + 50 
                isJumping = False
                canDoubleJump = False
                jumpSpeed = JUMPSPEED  # Resets jump speed for next time

        
        # Update player animation
        animationCounter += 1
        if animationCounter >= ANIMATION_SPEED:
            animationCounter = 0
            playerIndex = (playerIndex + 1) % len(playerImages)  #Passes to the next image in a loop

        # Move the baddies
        for b in baddies:
            if b.is_falling:  # If the bat is falling
                b.fall_to_ground()  # Applies the fall
            else:
                # Normal movement
                if not reverseCheat and not slowCheat:
                    b.move() 
                elif reverseCheat:
                    b.rect.move_ip(5, 0)  # Reverse movement
                elif slowCheat:
                    b.rect.move_ip(-1, 0)  # Movement in slow 


        # Delete baddies that have gone off the left side of the screen.
        baddies = [b for b in baddies if not b.is_off_screen()]

        # Draw scrolling background
        bgImage = backgrounds[level] # Defines background according to level
        windowSurface.blit(bgImage, (bg_x, 0))
        windowSurface.blit(bgImage, (bg_x + WINDOWWIDTH, 0))
        bg_x -= Speed # Moves background to the left

        if bg_x <= -WINDOWWIDTH:
            bg_x = 0
        
        # Checks whether level has changed for the sound
        if level != previous_level:
            play_level_music(level)
            previous_level = level
        
        # Draw ObjectMagic with levels.
        if level == 1:
            # Moves the frog object
            windowSurface.blit(frog.image, (frog.rect.x, frog.rect.y))
            frog.rect.x -= frog.speed
            if frog.rect.x <= -frog.rect.width:
                frog.rect.x = WINDOWWIDTH
            # Checks the collision between the player and the magic object
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
        # Goes to next level
        if score >= 1000 * level:
            level += 1
            if level > 3:
                displayWinScreen()  # Displays victory images
                level = 1 
                score = 0 
                break 

        # Draw the score, top score, level, lives.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Level: %s' % (level), font, windowSurface, WINDOWWIDTH - 200, 10)
        drawHearts(windowSurface, lives, heartImage, 10, top_score_y)

        # Draw the player's rectangle.
        windowSurface.blit(playerImages[playerIndex], playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b.image, b.rect)

        pygame.display.update()
        
        # Check if any of the baddies have hit the player.
        hit_baddie, collision_type = playerHasHitBaddie(playerRect, baddies)

        if hit_baddie:
            # Case 1: Pumpkin (baddie1)
            if hit_baddie.baddie_type == 'baddie1':
                if collision_type == True:  
                    hit_baddie.play_crush_animation(windowSurface) 
                    baddies.remove(hit_baddie)
                    isJumping = True
                    jumpSpeed = JUMPSPEED 
                else:
                    # Classic collision with the pumpkin
                    lives -= 1
                    print(f"Vies restantes : {lives}")
                    baddies.remove(hit_baddie)

            # Case 2: Bat (baddie3)
            elif hit_baddie.baddie_type == 'baddie3':
                if hit_baddie.is_falling:
                    pass 
                elif collision_type == "bas": 
                    hit_baddie.is_falling = True 
                    bonk_sound.play()
                    jumpSpeed = 0 
                else:
                    # Classic collision with a bat
                    lives -= 1 
                    print(f"Vies restantes : {lives}")
                    baddies.remove(hit_baddie) 
           
            # Case 3: Other baddies
            else:
                lives -= 1 
                print(f"Vies restantes : {lives}")
                baddies.remove(hit_baddie) 

        if lives <= 0:
            if score > topScore:
                topScore = score
            displayGameOverScreen() 
            break
        
        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    if game_over:
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3), (255, 0, 0))
        drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()
    elif win:
        displayWinScreen()