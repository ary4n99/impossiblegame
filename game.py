from tkinter import CENTER, Tk, Canvas, Label, Button, PhotoImage, Entry, messagebox
import sys, random

# RESOLUTION: 1920x1080
# CHEATKEY: hold c gor invincibility

def quitgame(): # configures quit popup to destroy window
    quitbox = messagebox.askquestion("Quit", "Are you sure you want to quit?", icon = "warning")
    
    if quitbox == 'yes':
        window.destroy()

def windowconfig(): # configures window and canvas geometry and attributes; initializes boss key photo
    global window, canvas, workphoto, workphotolabel
   
    window = Tk()
    window.geometry("1920x1080")
    window.attributes("-fullscreen", True)
    
    canvas = Canvas(window, width = 1920, height = 1080)
    canvas.pack()
    
    workphoto = PhotoImage(file="work.gif")
    workphotolabel = Label(image = workphoto)
    workphotolabel.image = workphoto
    
def level_static(): # creates black borders and end area for all the levels
    global obstacle, endarea
    
    bordercolour = "black"
    
    canvas.create_rectangle(0, 0, 1920, 150, fill = bordercolour, width = 0)
    canvas.create_rectangle(0, 930, 1920, 1080, fill = bordercolour, width = 0)
    canvas.create_rectangle(0, 0, 20, 1080, fill = bordercolour, width = 0)
    canvas.create_rectangle(1900, 0, 1920, 1080, fill = bordercolour, width = 0)
    
    endarea = canvas.create_rectangle(1760, 150, 1900, 930, fill = "palegreen1", width = 0)
    canvas.tag_lower(endarea)

def mainlevel(init = False): # creates obstacles and sets properties and movement based on current level
    global bossmode, cheaton, collision, currentlevel, initialrun, isgameover, is_level_over, obstacle, obstaclecoords, obstacledirection,obstaclecount, obstaclespeed, pause, playercoords, loadedfromsave, score
    
    if currentlevel == 1:
        speed = 8
        colour = "green"
    elif currentlevel == 2:
        speed = 10
        colour = "blue"
    elif currentlevel == 3:
        speed = 12
        colour = "black"
    elif currentlevel == 4:
        speed = 14
        colour = "red"


    if init == True: # sets score to true if a new game is played
        if loadedfromsave != True and currentlevel == 1:
            score = 200
        
        try: 
            gameoverbutton.destroy() # destroys and obstacles buttons after game over, as they are regenerated each time
            savegamebutton.destroy()
            canvas.delete(pausetext, player)
            for i in range(len(obstacle)):
                canvas.delete(obstacle[i])
        except:
            pass
        
        playerconfig(50, 540, 150, 640) # initializes player and obstacle attributes
        pause = False
        is_level_over = False
        obstacle = []
        obstacledirection = []
        obstaclespeed = []
        obstaclecoords = [(),(),(),(),()]
        obstaclecount = len(obstaclecoords)
        
        window.bind("p", lambda x: pausegame("Paused")) # binds pause key

        for i in range(obstaclecount):
            if currentlevel == 1 or currentlevel == 2: # creates circles for level 1 and 2 and squares for level 3 and 4
                obstacle.append(canvas.create_oval((i + 1) * 300, (i + 1) * 300, 400 + i * 300, 400 + i * 300, fill = colour, width = 5))
            else: 
                obstacle.append(canvas.create_rectangle((i + 1) * 300, (i + 1) * 300, 400 + i * 300, 400 + i * 300, fill = colour, width = 5))
            
            obstaclespeed.append(random.randint(speed - 1, speed + 1)) # selects random speed based on base speed value (depending on level)

    for j in range(obstaclecount): # gets coordinates from obstacle and sets values to list
        obstaclecoords[j] = canvas.coords(obstacle[j])
    
    if init == True and isgameover == False:
        for y in range(obstaclecount):
            obstacledirection.append(False) # sets initial direction for obstacles (false = down)
        
        initialrun = False
        collisiondetection() # starts collision detection, border detection, level complete and scoring mechanisms
        borderdetection()
        nextlevel()
        scorecounter()

    for k in range(len(obstacle)): # checks obstacles coordinates, changing direction so it bounces off the black borders
        if obstaclecoords[k][3] >= 930: 
            obstacledirection[k] = True
        elif obstaclecoords[k][3] <= 250: 
            obstacledirection[k] = False
        
        if obstacledirection[k] == True: 
            canvas.move(obstacle[k], 0, -obstaclespeed[k])
        else: 
            canvas.move(obstacle[k], 0, obstaclespeed[k])
    
    if pause == False and is_level_over == False: # reruns loop after 5ms if not paused and level isn't over
        window.after(5, mainlevel)

def scorecounter():
    global score, scoretext
    
    try:
        canvas.delete(scoretext) # deletes score
    except:
        pass
    
    if pause != True and is_level_over == False: # redraws score on top of screen
        scoretext = canvas.create_text(960, 75, text = "Score: " + str(score), font = ("Helvetica", 40), fill = "white")
        if score > 0:
            score -= 1
        
        window.after(1000, scorecounter) # score decreases by 1 every 1s

def playerconfig(x1 = 50, y1 = 540, x2 = 150, y2 = 640):
    global player
    
    player = canvas.create_rectangle(x1, y1, x2, y2, fill = "red", width = 5) # creates player shape
    window.bind(leftkey, lambda x: canvas.move(player, -10, 0)) # binds move keys to user selected choices
    window.bind(rightkey, lambda x: canvas.move(player, 10, 0))
    window.bind(upkey, lambda x: canvas.move(player, 0, -10))
    window.bind(downkey, lambda x: canvas.move(player, 0, 10))

def welcomepage():
    global startbutton, leaderbutton, welcometext, esctext, titletext, pausetext, savetext, loadbutton, smileyphotolabel, cheattext
    canvas.configure(bg = "black") # creates black background

    # creates buttons for homepage
    startbutton = Button(canvas, text="Start", font=("Helvetica", 20), command = startgame)
    startbutton.place(x = 960, y = 600, anchor = CENTER)
    
    leaderbutton = Button(canvas, text="View leaderboard", font=("Helvetica", 20), command = leaderboard)
    leaderbutton.place(x = 960, y = 700, anchor = CENTER)

    loadbutton = Button(canvas, text="Load save", font=("Helvetica", 20), command = loadsave)
    loadbutton.place(x = 960, y = 800, anchor = CENTER)
    
    # creates text for homepage
    titletext = canvas.create_text(960, 300, text = "The Impossible Game", font = ("Helvetica", 30), fill = "white")
    welcometext = canvas.create_text(960, 450, text = "Welcome!", font = ("Helvetica", 80), fill = "white")
    esctext = canvas.create_text(960, 900, text = "Press esc to quit", font = ("Helvetica", 10), fill = "white")
    pausetext = canvas.create_text(960, 950, text = "Press p to toggle pause, x to toggle work mode (boss key)", font = ("Helvetica", 10), fill = "white")
    savetext = canvas.create_text(960, 1000, text = "You can save progress at the end of each level", font = ("Helvetica", 10), fill="white")
    cheattext = canvas.create_text(960, 862, text = "Hold c to disable collisions", font = ("Helvetica", 6), fill="white")
    
    # creates photo for homepage
    smileyphoto = PhotoImage(file = "smiley.gif")
    smileyphotolabel = Label(image = smileyphoto, borderwidth = 0)
    smileyphotolabel.image = smileyphoto
    smileyphotolabel.place(x = 50, y = 50)

def startgame(): # starts the game initially
    screenclear()
    canvas.configure(bg = "white")
    level_static()
    mainlevel(True)

def screenclear(): # clears screen
    leaderbutton.destroy()
    startbutton.destroy()
    loadbutton.destroy()
    smileyphotolabel.destroy()
    try:
        savegamebutton.destroy()
        saveprogressbutton.destroy()
    except:
        pass
    
    canvas.delete(welcometext, titletext, esctext, pausetext, savetext, cheattext)

def leaderboard(): # displays leaderboard
    global gohomebutton, leadertext
    
    screenclear()
    leadertext = []
    
    try: # if leaderboard file exists, it is read and displayed
        with open("leaderboard.txt") as file:
            leaderboard = [line.strip() for line in file]
        
        if len(leaderboard) > 8:
            temp = 8
        else:
            temp = len(leaderboard)
        
        for i in range(temp):
            leadersplit = leaderboard[i].split(",")
            leadertext.append(canvas.create_text(660, i*100+100, text = str(i+1) + ". " + leadersplit[0], font = ("Helvetica", 30), fill = "white"))
            leadertext.append(canvas.create_text(1260, i*100+100, text = "Score: " + leadersplit[1], font = ("Helvetica", 30), fill = "white"))
    except: # if it doesn't exist, says the message leaderboard is empty
        leadertext.append(canvas.create_text(960, 100, text = "The leaderboard is empty!", font = ("Helvetica", 30), fill = "white"))
    
    gohomebutton = Button(canvas, text="Go home", font=("Helvetica", 20), command = deleteleaderpage)
    gohomebutton.place(x = 960, y = 1000, anchor = CENTER)

def deleteleaderpage(): # clears leaderboard page when user selects to go home
    for i in range(len(leadertext)):
        canvas.delete(leadertext[i])
    
    gohomebutton.destroy()
    welcomepage()

def displayfinaltext(inputtext): # displays text when you beat the game
    global pause, pausetext, initialrun, currentlevel, finalscore
    
    pausetext = canvas.create_text(960, 450, text = inputtext, font = ("Helvetica", 80), fill = "Black")
    finalscore = score

def pausegame(inputtext): # displays text when you pause, game over or move onto next level; delets said text when recalled
    global pause, pausetext, initialrun, currentlevel, finalscore
    
    if initialrun != True:
        pause = not pause
        if pause == True:
            pausetext = canvas.create_text(960, 450, text = inputtext, font = ("Helvetica", 80), fill = "Black")
            window.unbind(leftkey) # unbinds keys so player cant move when paused, game over or moving onto next level
            window.unbind(upkey)
            window.unbind(rightkey)
            window.unbind(downkey)
        else:
            canvas.delete(pausetext)
            window.bind(leftkey, lambda x: canvas.move(player, -10, 0)) # rebinds keys
            window.bind(upkey, lambda x: canvas.move(player, 0, -10))
            window.bind(rightkey, lambda x: canvas.move(player, 10, 0))
            window.bind(downkey, lambda x: canvas.move(player, 0, 10))
            scorecounter()
            mainlevel()

def restartgame(): # goes home when game over/win
    screenclear()
    gameoverbutton.destroy()
    canvas.delete(player, endarea)
   
    try: 
        saveprogressbutton.destroy()
        canvas.delete(scoretext)
        canvas.delete(finalscoretext)
    except: 
        pass
    
    for i in range(len(obstacle)):
        canvas.delete(obstacle[i])
    
    initialize()
    welcomepage()

def updateleaderboard(): #updates leaderboard file
    global statsbox, nameprompt, finalscore
    
    username = nameprompt.get()
    statsbox.destroy()
    saveprogressbutton.destroy()
    scorelist = []
    
    try: # tries to open leaderboard and add name to file
        with open("leaderboard.txt", "r") as file:
            leaderboard = [line.strip() for line in file]
        
        for i in range(len(leaderboard)):
            leadersplit = leaderboard[i].split(",")
            scorelist.append(leadersplit[1])
        
        insertindex = len(scorelist) + 1
        for i in range(len(scorelist)):
            if int(scorelist[i]) <= finalscore:
                insertindex = i
                break
            
        with open("leaderboard.txt", "w") as file:
            for i in range(len(leaderboard)):
                if i == insertindex:
                    file.write(username + "," + str(finalscore) + "\n")
                    file.write(leaderboard[i] + "\n")
                else:
                    file.write(leaderboard[i] + "\n")
    except: # if it doesn't exist, the file is created and user details are added 
        with open("leaderboard.txt", "w+") as file:
            file.write(username + "," + str(finalscore) + "\n")

def collisiondetection(): # checks for collisions between player and obstacles
    global gameoverbutton, isgameover, cheaton, collision, obstaclecoords, playercoords, is_level_over, scoretext, finalscore, score
    
    playercoords = canvas.coords(player)
    
    try:
        collision = canvas.find_overlapping(playercoords[0], playercoords[1], playercoords[2], playercoords[3]) # checks the overlapping coordinates for the player
    except:
        pass
    
    if len(collision) == 2 and cheaton == False and is_level_over == False and isgameover == False: # if user overlaps with more than one object (aka touches the obstacles), a game over message is displayed
        isgameover = True
        pausegame("Game Over!")
        gameoverbutton = Button(canvas, text = "Go home", font = ("Helvetica", 20), command = restartgame)
        gameoverbutton.place(x = 960, y = 600, anchor = CENTER)
        window.unbind("p")
        score = 200

    if isgameover == False: # repeats if game is not over
        window.after(5, collisiondetection)

def borderdetection(): # stops user going out of bounds
    global playercoords
    
    playercoords = canvas.coords(player)
    
    if pause == False:
        try: # checks coordinates and unbinds respective key to stop user going further; rebinds key if coordnates are not on the edge
            if playercoords[0] <= 20:
                window.unbind(leftkey)
            else:
                window.bind(leftkey, lambda x: canvas.move(player, -10, 0))
            
            if playercoords[1] <= 150:
                window.unbind(upkey)
            else:
                window.bind(upkey, lambda x: canvas.move(player, 0, -10))
            
            if playercoords[2] >= 1900:
                window.unbind(rightkey)
            else:
                window.bind(rightkey, lambda x: canvas.move(player, 10, 0))
            
            if playercoords[3] >= 930:
                window.unbind(downkey)
            else:
                window.bind(downkey, lambda x: canvas.move(player, 0, 10))
            
            window.after(5, borderdetection)
        except: 
            pass

def bosskey(): # toggles google docs image when "x" is pressed, making it look like work is being done
    global bossmode, workphotolabel, workphoto
    
    bossmode = not bossmode
    
    if bossmode == True:
        workphotolabel.place(x = -2, y = -2)
    else:
        workphotolabel.destroy()
        workphotolabel = Label(image = workphoto)
        workphotolabel.image = workphoto

def initialize(): # initializes variables before game is run/rerun
    global currentlevel, obstacle, obstacledirection, obstaclespeed, obstaclecoords, collision, initialrun, pause, bossmode, loadedfromsave, isgameover, is_level_over, cheaton
    
    currentlevel = 1
    initialrun = True
    cheaton = False
    loadedfromsave = False
    isgameover = False
    bossmode = False
    
    window.bind("<Escape>", lambda x: quitgame()) # binds keys for pause, boss mode, cheat mode, and quit
    window.bind("p", lambda x: pausegame("Paused"))
    window.bind("<KeyPress-c>", lambda x: cheatmodeon())
    window.bind("<KeyRelease-c>", lambda x: cheatmodeoff())
    window.bind("x", lambda x: bosskey())

def cheatmodeon(): # sets cheat mode on
    global cheaton
    cheaton = True

def cheatmodeoff(): # sets cheat mode off
    global cheaton
    cheaton = False

def savestats(): # displays prompt to save stats to leaderboard
    global statsbox, nameprompt
    
    statsbox = Tk()
    statsbox.title("Please enter your name:")
    
    nameprompt = Entry(statsbox, width = 50)
    nameprompt.pack()
    namebutton = Button(statsbox, text="Save stats to leaderboard", command = updateleaderboard)
    namebutton.pack()

def donothing(): # does nothing lol
    pass

def keyprompt(): # prompts user to enter key bindings to control player icon
    global keypromptbox, upprompt, downprompt, leftprompt, rightprompt
    
    keypromptbox = Tk()
    keypromptbox.title("Enter player control keys:")
    keypromptbox.attributes('-topmost', True) # makes sure prompt stays on top
    try:
        keypromptbox.protocol("WM_DELETE_WINDOW", donothing) # removes keybind for "X" so window can't be closed
    except:
        pass
    keypromptbox.geometry("+%d+%d" % (500, 500)) # sets location of prompt
    
    upprompt = Entry(keypromptbox, width = 50)
    upprompt.insert(0, "UP (remove this text)")
    upprompt.pack()
    
    leftprompt = Entry(keypromptbox, width = 50)
    leftprompt.insert(0, "LEFT (remove this text)")
    leftprompt.pack()
    
    downprompt = Entry(keypromptbox, width = 50)
    downprompt.insert(0, "DOWN (remove this text)")
    downprompt.pack()
    
    rightprompt = Entry(keypromptbox, width = 50)
    rightprompt.insert(0, "RIGHT (remove this text)")
    rightprompt.pack()
    
    submitkeybutton = Button(keypromptbox, text = "Submit", command = configureuserkeys)
    submitkeybutton.pack()

def configureuserkeys(): # verifies user entries for keyprompt popup
    global keypromptbox, upprompt, downprompt, leftprompt, rightprompt, upkey, downkey, leftkey, rightkey
    upkey = upprompt.get()
    downkey = downprompt.get()
    leftkey = leftprompt.get()
    rightkey = rightprompt.get()
    keypromptbox.destroy()

    if len(upkey) != 1 or len(downkey) != 1 or len(leftkey) != 1 or len(rightkey) != 1 or upkey.isalpha() == False or downkey.isalpha() == False or leftkey.isalpha() == False or rightkey.isalpha() == False: # checks if keys entered are alpha characters and 1 character long
        messagebox.showerror("Invalid input", "Please enter 1 alphabetical character for each prompt.", icon = "error")
        keyprompt()
    elif upkey == "p" or downkey == "p" or leftkey == "p" or rightkey == "p" or upkey == "x" or downkey == "x" or leftkey == "x" or rightkey == "x" or upkey == "c" or downkey == "c" or leftkey == "c" or rightkey == "c": # checks if keys entered are the same as pause, boss or cheat key
        messagebox.showerror("Invalid input", "These are protected keys, please choose others.", icon = "error")
        keyprompt()
    elif upkey == downkey or upkey == leftkey or upkey == rightkey or downkey == leftkey or downkey == rightkey or leftkey == rightkey: # checks if any of the keys are the same
        messagebox.showerror("Invalid input", "They can't be the same!", icon = "error")
        keyprompt()
    window.lift()

def nextlevel(): # checks if level is complete, redirecting player to next level
    global saveprogressbutton, gameoverbutton, currentlevel, is_level_over, pause, initialrun, savegamebutton, finalscore, score, finalscoretext
    
    playercoords = canvas.coords(player)
    
    try: 
        if playercoords[2] >= 1760: # checks if player coordinates are at the green area
            is_level_over = True

            # increments level and displays text and buttons to save/go to next level
            if currentlevel == 1:
                currentlevel += 1 
                pausegame("You completed level 1!")
                gameoverbutton = Button(canvas, text = "Level 2", font = ("Helvetica", 20), command = lambda: mainlevel(True))
                gameoverbutton.place(x = 960, y = 600, anchor = CENTER)
                savegamebutton = Button(canvas, text = "Save progress", font=("Helvetica", 20), command = savegame)
                savegamebutton.place(x = 960, y = 700, anchor = CENTER)
            elif currentlevel == 2:
                currentlevel +=1
                pausegame("You completed level 2!")
                gameoverbutton = Button(canvas, text = "Level 3", font = ("Helvetica", 20), command = lambda: mainlevel(True))
                gameoverbutton.place(x = 960, y = 600, anchor = CENTER)
                savegamebutton = Button(canvas, text = "Save progress", font = ("Helvetica", 20), command = savegame)
                savegamebutton.place(x = 960, y = 700, anchor = CENTER)
            elif currentlevel == 3:
                currentlevel +=1
                pausegame("You completed level 3!")
                gameoverbutton = Button(canvas, text = "Level 4", font = ("Helvetica", 20), command = lambda: mainlevel(True))
                gameoverbutton.place(x = 960, y = 600, anchor = CENTER)
                savegamebutton = Button(canvas, text = "Save progress", font = ("Helvetica", 20), command = savegame)
                savegamebutton.place(x = 960, y = 700, anchor = CENTER)
            elif currentlevel == 4:
                displayfinaltext("You beat the impossible game!")
                finalscoretext = canvas.create_text(960, 75, text = "Score: "+ str(score), font=("Helvetica", 40), fill="white")
                finalscore = score
                gameoverbutton = Button(canvas, text = "Go home", font = ("Helvetica", 20), command = restartgame)
                gameoverbutton.place(x = 960, y = 600, anchor = CENTER)
                saveprogressbutton = Button(canvas, text = "Save score", font = ("Helvetica", 20), command = savestats)
                saveprogressbutton.place(x = 960, y = 700, anchor = CENTER)
                
            window.unbind("p")

        if is_level_over == False: # repeats if level isn't over
            window.after(5, nextlevel)
    except:
        pass

def savegame(): # writes player level and score to file
    global playercoords, currentlevel, score
    
    playercoords = canvas.coords(player)
    
    with open("playerprogress.txt", "w+") as file:
        file.writelines(str(currentlevel) + "\n")
        file.writelines(str(score))
    
    savegamebutton.destroy()

def loadsave(): # loads save from file
    global playercoords, currentlevel, loadedfromsave, score
    
    loadedfromsave = True
    try: # if file exists, it is opened and read
        with open("playerprogress.txt") as file:
            currentlevel = int(file.readline())
            score = int(file.readline())
    except: # if it doesn't exist, it's created with the default start game values
        currentlevel = 1
        score = 200
        with open("playerprogress.txt", "w+") as file:
            file.writelines("1\n")
            file.writelines("200")

    loadbutton.destroy()

# starts the game initially
score = 200
windowconfig()
initialize()
welcomepage()
keyprompt()

window.mainloop()