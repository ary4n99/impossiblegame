from tkinter import Tk, Canvas, Label, Button, messagebox, CENTER, PhotoImage, Entry
import sys

#RESOLUTION: 1920x1080
#CHEATKEY: c

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
    global obstacle, startarea, endarea
    bordercolour = "black"
    canvas.create_rectangle(0, 0, 1920, 150, fill=bordercolour, width=0)
    canvas.create_rectangle(0, 930, 1920, 1080, fill=bordercolour, width=0)
    canvas.create_rectangle(0, 0, 20, 1080, fill=bordercolour, width=0)
    canvas.create_rectangle(1900, 0, 1920, 1080, fill=bordercolour, width=0)
    startarea = canvas.create_rectangle(20, 150, 160, 930, fill="palegreen1", width=0)
    endarea = canvas.create_rectangle(1760, 150, 1900, 930, fill="palegreen1", width=0)
    canvas.tag_lower(startarea)
    canvas.tag_lower(endarea)

def level_one():
    global pause, obstaclecoords, obstacledirection, obstaclespeed, initialrun
    
    if initialrun == True:
        obstacle.append(canvas.create_oval(200, 200, 250, 250, fill="blue", width=5))
    
    obstaclecoords[0] = canvas.coords(obstacle[0])
    
    if initialrun == True:
        obstaclespeed.append(3)
        obstacledirection.append(False)
        collisiondetection()
        borderdetection()
        initialrun = False
    
    if obstaclecoords[0][3] >= 920: obstacledirection[0] = True
    elif obstaclecoords[0][3] <= 210: obstacledirection[0] = False
    if obstacledirection[0] == True: canvas.move(obstacle[0], 0, -obstaclespeed[0])
    else: canvas.move(obstacle[0], 0, obstaclespeed[0])
    if pause == False:
        window.after(2, level_one)

def playerconfig():
    global player
    player = canvas.create_rectangle(50, 540, 130, 620, fill="red", width=5)
    window.bind(leftkey, lambda x: canvas.move(player, -10, 0))
    window.bind(rightkey, lambda x: canvas.move(player, 10, 0))
    window.bind(upkey, lambda x: canvas.move(player, 0, -10))
    window.bind(downkey, lambda x: canvas.move(player, 0, 10))

def welcomepage():
    global startbutton, leaderbutton, welcometext, esctext, titletext, pausetext, cheattext
    canvas.configure(bg="black")

    startbutton = Button(canvas, text="Start", font=("Helvetica", 20), command=startgame)
    startbutton.place(x=960, y=600, anchor=CENTER)
    
    leaderbutton = Button(canvas, text="View leaderboard", font=("Helvetica", 20), command=leaderboard)
    leaderbutton.place(x=960, y=700, anchor=CENTER)
    
    titletext = canvas.create_text(960, 300, text="The Impossible Game", font=("Helvetica", 30), fill="white")
    welcometext = canvas.create_text(960, 450, text="Welcome!", font=("Helvetica", 80), fill="white")
    esctext = canvas.create_text(960, 800, text="Press esc to quit at anytime", font=("Helvetica", 10), fill="white")
    pausetext = canvas.create_text(960, 850, text="Press p to toggle pause at anytime", font=("Helvetica", 10), fill="white")
    cheattext = canvas.create_text(960, 900, text="Press x to toggle work mode (boss key) anytime", font=("Helvetica", 10), fill="white")

def startgame():
    screenclear()
    canvas.configure(bg="white")
    playerconfig()
    level_static()
    level_one()

def screenclear():
    leaderbutton.destroy()
    startbutton.destroy()
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
    global pause, pausetext, initialrun, currentlevel
    if initialrun != True:
        pause = not pause
        if pause == True:
            pausetext = canvas.create_text(960, 450, text=inputtext, font=("Helvetica", 80), fill="Black")
            window.unbind("<Key>")
        else:
            canvas.delete(pausetext)
            window.bind("<Key>", moveplayer)
            if currentlevel == 1:
                level_one()

def restartgame():
     screenclear()
     gameoverbutton.destroy()
     savestatsbutton.destroy()
     canvas.delete(player, startarea, endarea)
     for i in range(len(obstacle)):
         canvas.delete(obstacle[i])
     initialize()
     welcomepage()

def updateleaderboard():
    global statsbox, nameprompt, score
    savestatsbutton.destroy()
    username = nameprompt.get()
    statsbox.destroy()
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
        if int(scorelist[i]) <= score:
            insertindex = i
    
    with open("leaderboard.txt", "w+") as file:
        for i, line in enumerate(leaderboardlines):     
            if i == insertindex:      
                file.writelines(line + "\n")               
                file.writelines(username + "," + str(score))
            else:
                file.writelines(line)
    
    with open("leaderboard.txt", "w") as file:
        for i, line in enumerate(leaderboardlines):     
            if i >=8:      
                file.write() 
            else:
                file.writelines(line)

def collisiondetection():
    global gameoverbutton, savestatsbutton, isgameover, cheaton
    collision[0] = canvas.find_overlapping(obstaclecoords[0][0], obstaclecoords[0][1], obstaclecoords[0][2], obstaclecoords[0][3])
    for i in range(len(collision)):
        if len(collision[i]) == 2 and cheaton == False:
            isgameover = True
            pausegame("Game Over!")
            gameoverbutton = Button(canvas, text="Go home", font=("Helvetica", 20), command=restartgame)
            gameoverbutton.place(x=960, y=600, anchor=CENTER)
            savestatsbutton = Button(canvas, text="Save stats", font=("Helvetica", 20), command=savestats)
            savestatsbutton.place(x=960, y=700, anchor=CENTER)
            window.unbind("p")
            window.unbind(downkey)  
            window.unbind(upkey)
            window.unbind(leftkey)
            window.unbind(rightkey)      
        else:
            window.after(2, collisiondetection)    

def borderdetection():
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
    global currentlevel, obstacle, obstacledirection, obstaclespeed, obstaclecoords, collision, initialrun, pause, bossmode, score, isgameover, cheaton
    currentlevel = 1
    score = 0
    obstacle = []
    obstacledirection = []
    obstaclespeed = []
    obstaclecoords = [()]
    collision= [()]
    initialrun = True
    pause = False
    cheaton = False
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
    if upkey == "p" or downkey == "p" or leftkey == "p" or rightkey == "p" or upkey == "x" or downkey == "x" or leftkey == "x" or rightkey == "x" or upkey == "c" or downkey == "c" or leftkey == "c" or rightkey == "c":
        messagebox.showerror("Invalid input", "These are protected keys, please choose others.", icon = "error")
        keyprompt()
    if upkey == downkey or upkey == leftkey or upkey == rightkey or downkey == leftkey or downkey == rightkey or leftkey == rightkey:
        messagebox.showerror("Invalid input", "They can't be the same!", icon = "error")
        keyprompt()
    window.lift()

windowconfig()
initialize()
welcomepage()
keyprompt()

window.mainloop()