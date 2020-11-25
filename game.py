from tkinter import Tk, Canvas, Label, Button, messagebox, CENTER, PhotoImage
import sys

def quitgame():
    quitbox = messagebox.askquestion("Quit", "Are you sure you want to quit?", icon = "warning")
    if quitbox == 'yes':
        window.destroy()

def windowconfig():
    global window, canvas
    window = Tk()
    window.geometry("1920x1080")
    window.attributes("-fullscreen", True)
    window.bind('<Escape>', lambda x: quitgame())
    window.bind("p", lambda x: pausegame())
    window.bind("<Key>", moveplayer)
    canvas = Canvas(window, width=1920, height=1080)
    canvas.pack()

def level_static():
    global obstacle
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
        obstaclespeed.append(3)
        obstacledirection.append(False)
        initialrun = False
    
    obstaclecoords[0] = canvas.coords(obstacle[0])
    if obstaclecoords[0][3] >= 930: obstacledirection[0] = True
    elif obstaclecoords[0][3] <= 200: obstacledirection[0] = False
    if obstacledirection[0] == True: canvas.move(obstacle[0], 0, -obstaclespeed[0])
    else: canvas.move(obstacle[0], 0, obstaclespeed[0])
    if pause == False:
        window.after(2, lambda: level_one())

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
    global startbutton, leaderbutton, welcometext, esctext, titletext, pausetext
    canvas.configure(bg="black")
    
    startbutton = Button(canvas, text="Start", font=("Helvetica", 20), command=startgame)
    startbutton.place(x=960, y=600, anchor=CENTER)
    
    leaderbutton = Button(canvas, text="View leaderboard", font=("Helvetica", 20), command=leaderboard)
    leaderbutton.place(x=960, y=700, anchor=CENTER)
    
    titletext = canvas.create_text(960, 300, text="The Impossible Game", font=("Helvetica", 30), fill="white")
    welcometext = canvas.create_text(960, 450, text="Welcome!", font=("Helvetica", 80), fill="white")
    esctext = canvas.create_text(960, 800, text="Press esc to quit at anytime", font=("Helvetica", 10), fill="white")
    pausetext = canvas.create_text(960, 900, text="Press p to toggle pause at anytime", font=("Helvetica", 10), fill="white")

def startgame():
    screenclear()
    canvas.configure(bg="white")
    playerconfig()
    level_static()
    level_one()

def screenclear():
    leaderbutton.destroy()
    startbutton.destroy()
    canvas.delete(welcometext, titletext, esctext, pausetext)

def leaderboard():
    global gohomebutton, leadertext
    with open("leaderboard.txt") as file:
        leaderboard = [line.strip() for line in file]
    
    screenclear()
    leadertext = []
    for i in range(len(leaderboard)):
        leadertext.append(canvas.create_text(960, i*100+100, text=leaderboard[i], font=("Helvetica", 30), fill="white"))
    
    gohomebutton = Button(canvas, text="Go home", font=("Helvetica", 20), command=deleteleaderpage)
    gohomebutton.place(x=960, y=1000, anchor=CENTER)

def deleteleaderpage():
    for i in range(len(leadertext)):
        canvas.delete(leadertext[i])
    gohomebutton.destroy()
    welcomepage()
    
def pausegame():
    global pause, pausetext, pausepopup
    pause = not pause
    print(pause)
    if pause == True:
        pausetext = canvas.create_text(960, 450, text="Paused", font=("Helvetica", 80), fill="Black")
        pausepopup = canvas.create_rectangle(0, 0, 1920,1080, fill="black", stipple="gray75")
    else:
        canvas.delete(pausetext, pausepopup)
        restartgame()

def restartgame():
    global currentlevel
    if currentlevel == 1:
        level_one()
    # elif currentlevel == 2:


pause = False
currentlevel = 1
obstacle = []
obstacledirection = []
obstaclespeed = []
obstaclecoords = [()]
initialrun = True

windowconfig()
welcomepage()

window.mainloop()