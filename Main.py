# Centaurian Fleet
#
# A Space Invader like game
# Crappy Art and Novice Programming by the Mighty Buda / https://www.mightybuda.com
#
# Sounds downloaded from https://freesound.org/
# Background sounds from https://freesound.org/people/klankbeeld/
#   Available at https://freesound.org/people/klankbeeld/sounds/133100/
#
# Laser sound from https://freesound.org/people/Leszek_Szary/
#   Available at https://freesound.org/people/Leszek_Szary/sounds/146725/
#
# Explsion sounds from https://freesound.org/people/Prof.Mudkip/
#   Available at https://freesound.org/people/Prof.Mudkip/sounds/386862/
#


import pygame, random, time
from pygame import mixer

running = True

## Initiate PyGame
pygame.init()

# Load Graphics
icon = pygame.image.load("favicon_16x16.png")
PlayerImg = pygame.image.load("PlayerShip.png")
PlayerImg_Size = 64
EnemyImg = pygame.image.load("enemy1.png")
EnemyImg_Size = 64
BackgroundImg = pygame.image.load("background_800x600.png")
Laser = pygame.image.load("laserblast.png")
LaserImg_Size = 32
# IntroImg = pygame.image.load("intro_256x144.png")

Title_Font = pygame.font.Font("Pixeled.ttf", 30)
Game_Font = pygame.font.Font("Pixeled.ttf", 16)

Game_Title = Title_Font.render("CENTAURIAN FLEET", 1, (255, 255, 255))

# Generate Window for Game
Window_X_Size = 800
Window_Y_Size = 600
screen = pygame.display.set_mode((Window_X_Size, Window_Y_Size))
pygame.display.set_caption("Centaurian Fleet")
pygame.display.set_icon(icon)

# Background Music
mixer.music.load('background.mp3')
mixer.music.play(-1)


def Player(x, y):
    screen.blit(PlayerImg, (int(x - (PlayerImg_Size / 2)), int(y - (PlayerImg_Size / 2))))


def Enemy(x, y):
    screen.blit(EnemyImg, (int(x - (EnemyImg_Size / 2)), int(y - (EnemyImg_Size / 2))))


def LaserBlast(x, y):
    screen.blit(Laser, (int(x - (LaserImg_Size / 2)), int(y - (LaserImg_Size / 2))))


# global variables
running = True
HighScore = 0
ScoreCounter = 0


def intro():
    global running
    global HighScore
    global ScoreCounter

    BG_offset = 0
    running = True
    print("Current High Score = " + str(HighScore))
    while running:

        # Scrolling Background
        screen.blit(BackgroundImg, (0, 0 + BG_offset))
        screen.blit(BackgroundImg, (0, -600 + BG_offset))
        BG_offset += 1
        if BG_offset == 601:
            BG_offset = 0

        screen.blit(Game_Title, (int((Window_X_Size - Game_Title.get_width()) / 2), int(Window_Y_Size / 2 - 100)))

        Instruct_1 = Game_Font.render("Press ENTER to start", 1, (255, 255, 255))
        Instruct_2 = Game_Font.render("Press Q to quit", 1, (255, 255, 255))
        High_Score_Text = Game_Font.render("High Score: " + str(HighScore), 1, (255, 255, 255))

        screen.blit(Instruct_1, (int((Window_X_Size - Instruct_1.get_width()) / 2), int(Window_Y_Size / 2)))
        screen.blit(Instruct_2, (int((Window_X_Size - Instruct_2.get_width()) / 2), int(Window_Y_Size / 2 + 50)))
        screen.blit(High_Score_Text, (int((Window_X_Size - Instruct_2.get_width()) / 2), int(Window_Y_Size - 50)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Make quit button work
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Ends Game with single button
                    running = False
                    print("Quitting")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Ends Game with single button
                    print("Let's Play")
                    return
        pygame.display.update()
    return


def GamePlay():
    global running
    global HighScore
    global ScoreCounter

    if running == False:
        return

    BG_offset = 0

    # Initiate Variables
    PlayerPosition = [(Window_X_Size / 2), (Window_Y_Size - 50)]
    PlayerX_Change = 0
    EnemyPosX = []
    EnemyPosY = []
    EnemySpeed = []
    Laser_State = "Charged"
    Laser_Y = 650
    Laser_X = 850
    Laser_Speed = int(10)
    ScoreCounter = 0
    laser_sound = pygame.mixer.Sound("laser2.wav")
    enemy_sound = pygame.mixer.Sound("enemy.wav")

    # Initiate Enemies
    EnemyNum = 5  # How many enemies on screen
    for i in range(EnemyNum):
        EnemyPosX.append(random.randint(EnemyImg_Size, Window_X_Size - EnemyImg_Size))
        EnemyPosY.append(random.randint(EnemyImg_Size, 3 * EnemyImg_Size))
        EnemySpeed.append(random.randint(-3, 3))

    while running:
        screen.fill((50, 50, 50))  # redraw background for each tick

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Make quit button work
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Ends Game with single button
                    return
                if event.key == pygame.K_LEFT:
                    PlayerX_Change = -5
                if event.key == pygame.K_RIGHT:
                    PlayerX_Change = 5
                if event.key == pygame.K_SPACE and Laser_State == "Charged":
                    Laser_X = PlayerPosition[0]
                    Laser_Y = PlayerPosition[1]
                    Laser_State = "Fire"
                    laser_sound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    PlayerX_Change = 0
                if event.key == pygame.K_RIGHT:
                    PlayerX_Change = 0

        # Enemy Movement
        for i in range(EnemyNum):
            EnemyPosX[i] += EnemySpeed[i]
            if EnemyPosX[i] > (Window_X_Size - EnemyImg_Size):
                EnemySpeed[i] *= -1
                EnemyPosY[i] += abs(4 * EnemySpeed[i])
            elif EnemyPosX[i] < EnemyImg_Size:
                EnemySpeed[i] *= -1
                EnemyPosY[i] += abs(10 * EnemySpeed[i])

        # Player Movement
        PlayerPosition[0] += PlayerX_Change  # change in position from last cycle
        if PlayerPosition[0] >= Window_X_Size - (PlayerImg_Size / 2):
            PlayerPosition[0] = Window_X_Size - (PlayerImg_Size / 2)
        elif PlayerPosition[0] <= (PlayerImg_Size / 2):
            PlayerPosition[0] = (PlayerImg_Size / 2)

        # Hit Detection
        for i in range(EnemyNum):
            if (EnemyPosX[i] - (EnemyImg_Size / 2)) <= (Laser_X) <= (EnemyPosX[i] + (EnemyImg_Size / 2)) and (
                    EnemyPosY[i] - (EnemyImg_Size / 2)) <= (Laser_Y) <= (EnemyPosY[i] + (EnemyImg_Size / 2)):
                enemy_sound.play()
                Laser_Y = 650
                Laser_X = 850
                ScoreCounter += 1
                Laser_State = "Charged"
                EnemyPosX[i] = random.randint(EnemyImg_Size, Window_X_Size - EnemyImg_Size)
                EnemyPosY[i] = random.randint(EnemyImg_Size, 3 * EnemyImg_Size)
                EnemySpeed[i] = random.randint((-3 - int(ScoreCounter / 5)), (3 + int(ScoreCounter / 5)))
            if EnemyPosY[i] >= (PlayerPosition[1]):
                Game_Over = Title_Font.render("Game Over", 1, (255, 255, 255))
                screen.blit(Game_Over,
                            (int((Window_X_Size - Game_Over.get_width()) / 2), int(Window_Y_Size / 2 - 100)))
                pygame.display.update()
                time.sleep(2)
                return

        # Scrolling Background
        screen.blit(BackgroundImg, (0, 0 + BG_offset))
        screen.blit(BackgroundImg, (0, -600 + BG_offset))
        BG_offset += 2
        if BG_offset == 602:
            BG_offset = 0

        # Paint Items on Screen

        # Paint player
        Player(PlayerPosition[0], PlayerPosition[1])
        # Paint enemies
        for i in range(EnemyNum):
            Enemy(EnemyPosX[i], EnemyPosY[i])
        # Paint Laser Blast
        if Laser_State == "Fire" and Laser_Y > 10:
            Laser_Y -= Laser_Speed
            LaserBlast(Laser_X, Laser_Y)
        elif Laser_State == "Fire" and Laser_Y <= 10:
            Laser_State = "Charged"
            Laser_Y = PlayerPosition[1]

        Score_Text = Game_Font.render("Score: " + str(ScoreCounter), 1, (255, 255, 255))
        screen.blit(Score_Text, (5,5))

        if ScoreCounter > HighScore:
            HighScore = ScoreCounter
        pygame.display.update()  # Update Screen

        ############# End of GamePlay Function


def Game_Over():
    global running
    global HighScore
    global ScoreCounter

    BG_offset = 0

    while running:

        # Scrolling Background
        screen.blit(BackgroundImg, (0, 0 + BG_offset))
        screen.blit(BackgroundImg, (0, -600 + BG_offset))
        BG_offset += 1

        if BG_offset == 601:
            BG_offset = 0

        High_Score_Text = Game_Font.render("High Score: " + str(HighScore), 1, (255, 255, 255))
        Score_Text = Game_Font.render("Your Score: " + str(ScoreCounter), 1, (255, 255, 255))
        Press_Enter = Game_Font.render("Press ENTER to Continue", 1, (255, 255, 255))

        screen.blit(Score_Text, (int((Window_X_Size - Score_Text.get_width()) / 2), int(Window_Y_Size / 2 + 50)))
        screen.blit(Press_Enter, (int((Window_X_Size - Press_Enter.get_width()) / 2), int(Window_Y_Size / 2 + 150)))
        screen.blit(High_Score_Text, (int((Window_X_Size - High_Score_Text.get_width()) / 2), int(Window_Y_Size - 50)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Make quit button work
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Ends Game with single button
                    print("Back to Intro")
                    return
        pygame.display.update()
    return


########  Primary Program Loop ###############
while running:
    intro()
    GamePlay()
    Game_Over()
