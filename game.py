from tkinter import Tk, Canvas, Label, Button, messagebox, CENTER, PhotoImage, Entry
import sys, random

#RESOLUTION: 1920x1080
#CHEATKEY: hold c gor invincibility

def quitgame():
    quitbox = messagebox.askquestion("Quit", "Are you sure you want to quit?", icon = "warning")
    if quitbox == 'yes':
        window.destroy()

def windowconfig():
    global window, canvas, workphoto, workphotolabel
    window = Tk()
    canvas = Canvas(window, width=1920, height=1080)
    canvas.pack()
    window.geometry("1920x1080")
    window.attributes("-fullscreen", True)
    
    workphoto = PhotoImage(file="ss.gif")
    workphotolabel = Label(image = workphoto)
    workphotolabel.image = workphoto

def level_static():
    global obstacle, endarea
    bordercolour = "black"
    canvas.create_rectangle(0, 0, 1920, 150, fill=bordercolour, width=0)
    canvas.create_rectangle(0, 930, 1920, 1080, fill=bordercolour, width=0)
    canvas.create_rectangle(0, 0, 20, 1080, fill=bordercolour, width=0)
    canvas.create_rectangle(1900, 0, 1920, 1080, fill=bordercolour, width=0)
    endarea = canvas.create_rectangle(1760, 150, 1900, 930, fill="palegreen1", width=0)
    canvas.tag_lower(endarea)

def mainlevel(init = False):
    global bossmode, cheaton, collision, currentlevel, initialrun, isgameover, islevelover, obstacle, obstaclecoords, obstacledirection,obstaclecount, obstaclespeed, pause, playercoords
    if currentlevel == 1:
        speed = 1
        colour = "blue"
    elif currentlevel == 2:
        speed = 2
        colour = "green"
    elif currentlevel == 3:
        speed = 3
        colour = "black"


    if init == True:
        try:
            gameoverbutton.destroy()
            savegamebutton.destroy()
            canvas.delete(pausetext, player)
            for i in range(len(obstacle)):
                canvas.delete(obstacle[i])
        except:
            pass
        playerconfig(50, 540, 130, 630)
        obstacle = []
        obstacledirection = []
        obstaclespeed = []
        obstaclecoords = [(),(),(),(),()]
        pause = False
        islevelover = False

        x = 300
        y = 300
        obstaclecount = len(obstaclecoords)
        for i in range(obstaclecount):
            obstacle.append(canvas.create_oval(x+i*y, x+i*y, x+100+i*y, x+100+i*y, fill=colour, width=5))
            obstaclespeed.append(random.randint(speed,speed+1))

    for j in range(obstaclecount):
        obstaclecoords[j] = canvas.coords(obstacle[j])
    
    if init == True and isgameover == False:
        for y in range(obstaclecount):
            obstacledirection.append(False)
        initialrun = False
        collisiondetection()
        borderdetection()
        nextlevel()
        scorecounter()

    for k in range(len(obstacle)):
        if obstaclecoords[k][3] >= 930: obstacledirection[k] = True
        elif obstaclecoords[k][3] <= 250: obstacledirection[k] = False
        if obstacledirection[k] == True: canvas.move(obstacle[k], 0, -obstaclespeed[k])
        else: canvas.move(obstacle[k], 0, obstaclespeed[k])
    
    if pause == False and islevelover ==False:
        window.after(2, lambda: mainlevel())

def scorecounter():
    global score, scoretext
    try:
        canvas.delete(scoretext)
    except:
        pass
    if pause != True:
        scoretext = canvas.create_text(960, 50, text="Score: "+ str(score), font=("Helvetica", 40), fill="white")
        score -=1
        window.after(1000, scorecounter)

def playerconfig(x1 = 50, y1 = 540, x2 = 130, y2 = 630):
    global player
    player = canvas.create_rectangle(x1, y1, x2, y2, fill="red", width=5)
    window.bind(leftkey, lambda x: canvas.move(player, -10, 0))
    window.bind(rightkey, lambda x: canvas.move(player, 10, 0))
    window.bind(upkey, lambda x: canvas.move(player, 0, -10))
    window.bind(downkey, lambda x: canvas.move(player, 0, 10))

def welcomepage():
    global startbutton, leaderbutton, welcometext, esctext, titletext, pausetext, cheattext, loadbutton
    canvas.configure(bg="black")

    startbutton = Button(canvas, text="Start", font=("Helvetica", 20), command=startgame)
    startbutton.place(x=960, y=600, anchor=CENTER)
    
    leaderbutton = Button(canvas, text="View leaderboard", font=("Helvetica", 20), command=leaderboard)
    leaderbutton.place(x=960, y=700, anchor=CENTER)

    loadbutton = Button(canvas, text="Load save", font=("Helvetica", 20), command=loadsave)
    loadbutton.place(x=960, y=800, anchor=CENTER)
    
    titletext = canvas.create_text(960, 300, text="The Impossible Game", font=("Helvetica", 30), fill="white")
    welcometext = canvas.create_text(960, 450, text="Welcome!", font=("Helvetica", 80), fill="white")
    esctext = canvas.create_text(960, 850, text="Press esc to quit at anytime", font=("Helvetica", 10), fill="white")
    pausetext = canvas.create_text(960, 900, text="Press p to toggle pause at anytime", font=("Helvetica", 10), fill="white")
    cheattext = canvas.create_text(960, 950, text="Press x to toggle work mode (boss key) anytime", font=("Helvetica", 10), fill="white")

def startgame():
    screenclear()
    canvas.configure(bg="white")
    level_static()
    mainlevel(True)

def screenclear():
    leaderbutton.destroy()
    startbutton.destroy()
    loadbutton.destroy()
    try:
        savegamebutton.destroy()
        saveprogressbutton.destroy()
    except:
        pass
    canvas.delete(welcometext, titletext, esctext, pausetext, cheattext)

def leaderboard():
    global gohomebutton, leadertext
    with open("leaderboard.txt") as file:
        leaderboard = [line.strip() for line in file]
    screenclear()
    leadertext = []
    for i in range(len(leaderboard)):
        leadersplit = leaderboard[i].split(",")
        leadertext.append(canvas.create_text(660, i*100+100, text = str(i+1) + ". "+ leadersplit[0], font=("Helvetica", 30), fill="white"))
        leadertext.append(canvas.create_text(1260, i*100+100, text = "Score: "+ leadersplit[1], font=("Helvetica", 30), fill="white"))
    
    gohomebutton = Button(canvas, text="Go home", font=("Helvetica", 20), command=deleteleaderpage)
    gohomebutton.place(x=960, y=1000, anchor=CENTER)

def deleteleaderpage():
    for i in range(len(leadertext)):
        canvas.delete(leadertext[i])
    gohomebutton.destroy()
    welcomepage()
    
def pausegame(inputtext):
    global pause, pausetext, initialrun, currentlevel, finalscore
    if initialrun != True:
        pause = not pause
        if pause == True:
            pausetext = canvas.create_text(960, 450, text=inputtext, font=("Helvetica", 80), fill="Black")
            window.unbind(leftkey)
            window.unbind(upkey)
            window.unbind(rightkey)
            window.unbind(downkey)
            if "beat" in inputtext:
                finalscore = score
        else:
            canvas.delete(pausetext)
            window.bind(leftkey, lambda x: canvas.move(player, -10, 0))
            window.bind(upkey, lambda x: canvas.move(player, 0, -10))
            window.bind(rightkey, lambda x: canvas.move(player, 10, 0))
            window.bind(downkey, lambda x: canvas.move(player, 0, 10))
            scorecounter()
            mainlevel()

def restartgame():
     screenclear()
     gameoverbutton.destroy()
     canvas.delete(player, endarea, scoretext)
     for i in range(len(obstacle)):
         canvas.delete(obstacle[i])
     initialize()
     welcomepage()

def updateleaderboard():
    global statsbox, nameprompt, finalscore
    username = nameprompt.get()
    statsbox.destroy()
    saveprogressbutton.destroy()
    scorelist = []
    with open("leaderboard.txt") as file:
        leaderboardlines = file.readlines()
    with open("leaderboard.txt") as file:
        leaderboard = [line.strip() for line in file]
    
    for i in range(len(leaderboard)):
        leadersplit = leaderboard[i].split(",")
        scorelist.append(leadersplit[1])

    insertindex = len(scorelist) + 1
    for i in range(len(scorelist)):
        if int(scorelist[i]) <= finalscore:
            insertindex = i
    
    with open("leaderboard.txt", "w+") as file:
        for i, line in enumerate(leaderboardlines):     
            if i == insertindex:      
                file.writelines(line + "\n")               
                file.writelines(username + "," + str(finalscore))
            else:
                file.writelines(line)
    
    with open("leaderboard.txt", "w") as file:
        for i, line in enumerate(leaderboardlines):     
            if i >=8:      
                file.write() 
            else:
                file.writelines(line)

def collisiondetection():
    global gameoverbutton, isgameover, cheaton, collision, obstaclecoords, playercoords, islevelover, scoretext, finalscore, score
    playercoords = canvas.coords(player)
    collision = canvas.find_overlapping(playercoords[0], playercoords[1], playercoords[2], playercoords[3])
    if len(collision) == 2 and cheaton == False and islevelover == False and isgameover == False:
        isgameover = True
        pausegame("Game Over!")
        gameoverbutton = Button(canvas, text="Go home", font=("Helvetica", 20), command=restartgame)
        gameoverbutton.place(x=960, y=600, anchor=CENTER)
        window.unbind("p")
        scoretext = canvas.create_text(960, 50, text="Score: "+ str(score), font=("Helvetica", 40), fill="white")
        score = 200

    if isgameover == False:
        window.after(2, collisiondetection)    

def borderdetection():
    global playercoords
    playercoords = canvas.coords(player)
    if pause == False:
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
        window.after(2, borderdetection)  
    
def bosskey():
    global bossmode, workphotolabel, workphoto
    bossmode = not bossmode
    if bossmode == True:
        workphotolabel.place(x=-2, y=-2)
    else:
        workphotolabel.destroy()
        workphotolabel = Label(image = workphoto)
        workphotolabel.image = workphoto

def initialize():
    global currentlevel, obstacle, obstacledirection, obstaclespeed, obstaclecoords, collision, initialrun, pause, bossmode, loadedfromsave, isgameover, islevelover, cheaton
    currentlevel = 1
    initialrun = True
    cheaton = False
    loadedfromsave = False
    isgameover = False
    bossmode = False
    window.bind("<Escape>", lambda x: quitgame())
    window.bind("p", lambda x: pausegame("Paused"))
    window.bind("<KeyPress-c>", lambda x: cheatmodeon())
    window.bind("<KeyRelease-c>", lambda x: cheatmodeoff())
    window.bind("x", lambda x: bosskey())

def cheatmodeon():
    global cheaton
    cheaton = True

def cheatmodeoff():
    global cheaton
    cheaton = False

def savestats():
    global statsbox, nameprompt
    statsbox = Tk()
    statsbox.title("Please enter your name:")
    nameprompt = Entry(statsbox, width=50)
    nameprompt.pack()
    namebutton = Button(statsbox, text="Save stats to leaderboard", command=updateleaderboard)
    namebutton.pack()

def donothing():
    pass

def keyprompt():
    global keypromptbox, upprompt, downprompt, leftprompt, rightprompt
    keypromptbox = Tk()
    keypromptbox.title("Enter player control keys:")
    keypromptbox.attributes('-topmost', True)
    keypromptbox.protocol("WM_DELETE_WINDOW", donothing)
    keypromptbox.geometry("+%d+%d" % (500, 500))
    upprompt = Entry(keypromptbox, width=75)
    upprompt.insert(0, "UP (remove this text)")
    upprompt.pack()
    leftprompt = Entry(keypromptbox, width=75)
    leftprompt.insert(0, "LEFT (remove this text)")
    leftprompt.pack()
    downprompt = Entry(keypromptbox, width=75)
    downprompt.insert(0, "DOWN (remove this text)")
    downprompt.pack()
    rightprompt = Entry(keypromptbox, width=75)
    rightprompt.insert(0, "RIGHT (remove this text)")
    rightprompt.pack()
    
    submitkeybutton = Button(keypromptbox, text="Submit", command=configureuserkeys)
    submitkeybutton.pack()

def configureuserkeys():
    global keypromptbox, upprompt, downprompt, leftprompt, rightprompt, upkey, downkey, leftkey, rightkey
    upkey = upprompt.get()
    downkey = downprompt.get()
    leftkey = leftprompt.get()
    rightkey = rightprompt.get()
    keypromptbox.destroy()

    if len(upkey) != 1 or len(downkey) != 1 or len(leftkey) != 1 or len(rightkey) != 1 or upkey.isalpha() == False or downkey.isalpha() == False or leftkey.isalpha() == False or rightkey.isalpha() == False:
        messagebox.showerror("Invalid input", "Please enter 1 alphabetical character for each prompt.", icon = "error")
        keyprompt()
    elif upkey == "p" or downkey == "p" or leftkey == "p" or rightkey == "p" or upkey == "x" or downkey == "x" or leftkey == "x" or rightkey == "x" or upkey == "c" or downkey == "c" or leftkey == "c" or rightkey == "c":
        messagebox.showerror("Invalid input", "These are protected keys, please choose others.", icon = "error")
        keyprompt()
    elif upkey == downkey or upkey == leftkey or upkey == rightkey or downkey == leftkey or downkey == rightkey or leftkey == rightkey:
        messagebox.showerror("Invalid input", "They can't be the same!", icon = "error")
        keyprompt()
    window.lift()

def nextlevel():
    global saveprogressbutton, gameoverbutton, currentlevel, islevelover, pause, initialrun, savegamebutton
    playercoords = canvas.coords(player)
    if playercoords[2] >= 1760:
        islevelover = True
        if currentlevel == 1:
            currentlevel +=1
            pausegame("You completed level 1!")
            gameoverbutton = Button(canvas, text="Level 2", font=("Helvetica", 20), command=lambda: mainlevel(True))
            gameoverbutton.place(x=960, y=600, anchor=CENTER)
            savegamebutton = Button(canvas, text="Save game", font=("Helvetica", 20), command=savegame)
            savegamebutton.place(x=960, y=700, anchor=CENTER)
        elif currentlevel == 2:
            currentlevel +=1
            pausegame("You completed level 2!")
            gameoverbutton = Button(canvas, text="Level 3", font=("Helvetica", 20), command=lambda: mainlevel(True))
            gameoverbutton.place(x=960, y=600, anchor=CENTER)
            savegamebutton = Button(canvas, text="Save game", font=("Helvetica", 20), command=savegame)
            savegamebutton.place(x=960, y=700, anchor=CENTER)
        else:
            pausegame("You beat the impossible game!")
            gameoverbutton = Button(canvas, text="Go home", font=("Helvetica", 20), command=restartgame)
            gameoverbutton.place(x=960, y=600, anchor=CENTER)
            saveprogressbutton = Button(canvas, text="Save score", font=("Helvetica", 20), command=savestats)
            saveprogressbutton.place(x=960, y=700, anchor=CENTER)
            
        window.unbind("p")

    if islevelover == False:
        window.after(2, nextlevel)   

def savegame():
    global playercoords, currentlevel, score
    playercoords = canvas.coords(player)
    with open("playerprogress.txt", "w+") as file:
        file.writelines(str(currentlevel)+"\n")
        file.writelines(str(score))
    savegamebutton.destroy()

def loadsave():
    global playercoords, currentlevel, loadedfromsave, score
    loadedfromsave = True
    with open("playerprogress.txt") as file:
        currentlevel = int(file.readline()) + 1
        score = int(file.readline())
        

global score
score = 200

windowconfig()
initialize()
welcomepage()
keyprompt()

window.mainloop()