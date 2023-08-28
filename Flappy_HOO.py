#Vaneeza Shoaib, ZHW9ZC, Oleg Glushkov, BSU5ZU

#Game Name: Flappy HOO

#Game description:
# Similar to the game flappy bird, we will doing a remake with Flappy Hoo. The icon will attempt to pass through a given gap through platforms.
# The goal is to pass through as many gaps you can,and  collect as many collectable items to obtain the highest score

#3 Basic Features:
#USER INPUT: space bar to control movement up an down
#GAME OVER: when player touches platform/boxes either from top or bottom
#GRAPHIC/IMAGES: Cav man/Wahoo fish = player icon, boxes/platforms to create gap for icon to go through

#4 additional features:
#Scrolling Level: moving background similar to falldown PA idea -ENEMY HOKIE CHANGED TO SCROLLING LEVEL
#restart from Game Over: Game will restart upon pressing the space bar by player, it will asl recenter icon to start in the middle of the left end, reset score to 0
#collectable basketballs: icon can collect basketballs while attempting to pass through gap, increasing score by 2
#hi-score sheet: recording high score sheet, shown at the end of each game after game over with top three plays score and names

# --- GAME INSTRUCTIONS---
#Game immediately begins with asking the player to enter a name for the hi-score sheet, then it will open Game with Icon falling to the ground,
# either player can immeditely begin playing game by pressing space, or can start with a game over and press space to restart a new game
#game over occurs if HOO touches either top or bottom columns, or touches ground
import uvage

# --- GRAPHIC/IMAGES ---
name = input("Enter player name:")
camera = uvage.Camera(800, 600)

camera_width = 800
camera_height = 600
HOO_speed = 15
score = 0
game_on = True

ticker = 0

HOO = uvage.from_image(10, 350, "icon.png")

walls = [
    uvage.from_color(400, 600, "white", 1000, 20),
    uvage.from_color(400, 0, "white", 1000, 20),
]

Columns = [
    uvage.from_color(200, 50, "blue", 30, 400),
    uvage.from_color(200, 650, 'blue', 30, 300),
    uvage.from_color(400, 50, 'orange', 30, 300),
    uvage.from_color(400, 600, 'orange', 30, 275),
    uvage.from_color(600, 10, "blue", 30, 50),
    uvage.from_color(600, 450, 'blue', 30, 500),
    uvage.from_color(800, 100, 'orange', 30, 350),
    uvage.from_color(800, 650, 'orange', 30, 300),
]
# ---- COLLECTABLES ----
basketball = [
    uvage.from_image(300, 200, "bball.png"),
    uvage.from_image(500, 475, "bball.png"),
    uvage.from_image(670, 350, "bball.png"),
    uvage.from_image(850, 350, "bball.png"),
]
# ---- HI-SCORE FUNCTION----
def hi_score(new_score, new_player): # Hi-score can affect the playing of the game, to ensure hi-score is recorded Hi-score sheet must have no empty lines on file
    # displays top three scores and players name after each gameover
    filename = 'Flappy_HOO_HISCORE'
    in_file = open(filename, 'r')
    scores_d = {}
    for line in in_file:
        if line != "":
            row = line.strip().split(",")
            final_score = int(row[0])
            name = row[1]
            if final_score not in scores_d:
                scores_d[final_score] = [name]
            else:
                scores_d[final_score].append(name)
    out_file = open(filename, 'w')
    scores_d[new_score]= new_player
    scores_list = list(scores_d.keys())
    scores_list.sort(reverse=True)
    for k,v in scores_d.items():
        if type(v)==list:
            for name in v:
                out_file.write(str(k) + ','+ name+'\n')
        else:
            out_file.write(str(k) + ',' + str(v) + '\n')
    return scores_list[0], scores_d[scores_list[0]], scores_list[1], scores_d[scores_list[1]], scores_list[2], scores_d[scores_list[2]]
    out_file.close()
    filename.close()
score1 = 0
player1 = ''
score2 = 0
player2 = ''
score3 = 0
times = 0
player3 = ''
# ---- GAME FUNCTION ----
def tick():
# Player must repetedly tap space to control HOO location on screeen and get it through gap. On top of this movenement,
# player must aim to collect as many basketballs to increase score, avoid touhcing columns or ground

    global game_on
    global name
    global score
    global ticker, times
    global score1, player1, score2, player2, score3, player3
    global HOO
    # ------- USER INPUT ---------
    camera.clear("black")
    if game_on == True:
        HOO.speedy = HOO_speed  # gravity
        HOO.move_speed()
        for ball in basketball:
            if ball.x <= 0:
                ball.x = 800
            ball.x -= 4 #scrolling level for basketball collectables
            camera.draw(ball)
        for column in Columns:
            if column.x <= 0:
                column.x = 800
            column.x -= 4 #scrolling level for columns
            camera.draw(column)
            if HOO.touches(column):
                HOO.yspeed = 0
                game_on = False
                #times += 1
                #if times == 1:
                score1, player1, score2, player2, score3, player3 = hi_score(score, name)
                score = 0

        # ---- GAME OVER/ HI-SCORE ----
        if HOO.y > 600:
            HOO.yspeed = 0
            game_on = False
            #times += 1
            #if times == 1:
            score1, player1, score2, player2, score3, player3 = hi_score(score, name)
            score = 0
    # --- HOO MOVEMENT ---
    if uvage.is_pressing("space"):
        game_on = True
        HOO.y -= HOO_speed * 2
    camera.draw(HOO)

    # ----- SCORING ------
# score increases by ticker, by passing through gap you increase score by 1, collecting basketballs adds 2 points
    camera.draw(uvage.from_text(750, 50, str(int(score)), 50, "Yellow", bold=True))
    camera.draw(HOO)
    ticker += 1
    if ticker % 45 == 0:
        score += 1

    # ---- SCROLLING LEVEL ----
    for wall in walls:
        camera.draw(wall)

    for ball in basketball:
        if HOO.touches(ball):
            score = score + 2
            basketball.remove(ball)

    if game_on == False:
        ticker = 0
        HOO = uvage.from_image(10, 350, "icon.png")
        camera.draw(uvage.from_text(400, 50, "WELCOME TO FLAPPY HOO", 40, "orange", bold=False))
        camera.draw(uvage.from_text(400, 150, "GAME OVER", 40, "blue", bold=False))
        camera.draw(uvage.from_text(400, 200, "Press Space to play again", 40, "blue"))
        camera.draw(uvage.from_text(400, 250, "HI-SCORE", 40, "blue"))
        first_place = str(score1) + player1[0]
        second_place = str(score2) + player2[0]
        third_place = str(score3) + player3[0]
        camera.draw(uvage.from_text(400, 300, "first place-" + first_place, 40, "yellow"))
        camera.draw(uvage.from_text(400, 400, "second place-" + second_place, 40, "yellow"))
        camera.draw(uvage.from_text(400, 500, "third place-" + third_place, 40, "yellow"))
    camera.display()


uvage.timer_loop(30, tick)