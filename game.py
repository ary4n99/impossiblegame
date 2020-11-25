from tkinter import Tk, Canvas, Label, Button, messagebox, CENTER, PhotoImage
import sys

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

def level_one():
    global pause, obstaclecoords, obstacledirection, obstaclespeed, initialrun
    
    if initialrun == True:
        obstacle.append(canvas.create_oval(200, 200, 250, 250, fill="blue", width=5))
    
    obstaclecoords[0] = canvas.coords(obstacle[0])
    
    if initialrun == True:
        obstaclespeed.append(3)
        obstacledirection.append(False)
        collisiondetection()
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

def moveplayer(event):
    move_factor = 10
    if event.char == "a": canvas.move(player, -move_factor, 0)
    elif event.char == "d": canvas.move(player, move_factor, 0)
    elif event.char == "w": canvas.move(player, 0, -move_factor)
    elif event.char == "s": canvas.move(player, 0, move_factor)

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
    cheattext = canvas.create_text(960, 950, text="Press x to toggle work mode (boss key) anytime", font=("Helvetica", 10), fill="white")

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
    
def pausegame(input):
    global pause, pausetext, pausepopup, initialrun, currentlevel
    if initialrun != True:
        pause = not pause
        if pause == True:
            pausetext = canvas.create_text(960, 450, text=input, font=("Helvetica", 80), fill="Black")
            pausepopup = canvas.create_rectangle(0, 0, 1920,1080, fill="black", stipple="gray25")
            window.bind("<Key>", collisiondetection)
        else:
            canvas.delete(pausetext, pausepopup)
            window.bind("<Key>", moveplayer)
            if currentlevel == 1:
                level_one()

def restartgame():
     screenclear()
     gameoverbutton.destroy()
     canvas.delete(pausepopup, player, startarea, endarea)
     for i in range(len(obstacle)):
         canvas.delete(obstacle[i])
     initialize()
     welcomepage()

def collisiondetection():
    global gameoverbutton
    collision[0] = canvas.find_overlapping(obstaclecoords[0][0], obstaclecoords[0][1], obstaclecoords[0][2], obstaclecoords[0][3])
    for i in range(len(collision)):
        if len(collision[i]) == 2:
            pausegame("Game Over!")
            gameoverbutton = Button(canvas, text="Restart", font=("Helvetica", 20), command=restartgame)
            gameoverbutton.place(x=960, y=600, anchor=CENTER)
        else:
            window.after(2, collisiondetection)    

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
    global currentlevel, obstacle, obstacledirection, obstaclespeed, obstaclecoords, collision, initialrun, pause, bossmode
    currentlevel = 1
    obstacle = []
    obstacledirection = []
    obstaclespeed = []
    obstaclecoords = [()]
    collision= [()]
    initialrun = True
    pause = False
    bossmode = False
    window.bind('<Escape>', lambda x: quitgame())
    window.bind("p", lambda x: pausegame("Paused"))
    window.bind("x", lambda x: bosskey())
    window.bind("<Key>", moveplayer)

windowconfig()
initialize()
welcomepage()

window.mainloop()