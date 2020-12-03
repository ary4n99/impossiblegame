from tkinter import CENTER, Tk, Canvas, Label, Button, PhotoImage, Entry, \
    messagebox
import sys
import random
import os

# RESOLUTION: 1920x1080 (YOU MUST SET THE OS SCREEN RESOLUTION TO THIS FOR THE
# GAME TO WORK PROPERLY)
#
# CHEATKEY: hold c for invincibility
#
# https://creazilla.com/nodes/55045-ok-hand-emoji-clipart (SOURCE FOR PHOTO)

def initializegame():
    global currentlevel, initialrun, pause, bossmode, \
        loadedfromsave, isgameover, islevelover, cheatmode, score, \
        workphoto, workphotolabel, player, canvas, window

    window = Tk()

    window.geometry("1920x1080")
    window.attributes("-fullscreen", True)

    canvas = Canvas(window, width=1920, height=1080)
    canvas.pack()

    workphoto = PhotoImage(file="work.gif")
    workphotolabel = Label(image=workphoto)
    workphotolabel.image = workphoto


    currentlevel = 1
    initialrun = True
    cheatmode = False
    pause = False
    bossmode = False
    loadedfromsave = False
    isgameover = False
    islevelover = False
    score = 200

    # binds keys for pause, boss mode, cheat mode, and quit
    window.bind("<Escape>", lambda x: quitgame())
    window.bind("p", lambda x: pausegame("Paused"))
    window.bind("<KeyPress-c>", lambda x: cheatmodeon())
    window.bind("<KeyRelease-c>", lambda x: cheatmodeoff())
    window.bind("x", lambda x: bosskey())





def welcomepage():

    global startbutton, leaderbutton, welcometext, esctext, titletext, \
        pausetext, savetext, loadbutton, smileyphotolabel, cheattext, \
        window, canvas


    # creates black background
    canvas.configure(bg="black")

    # creates buttons for homepage
    startbutton = Button(canvas, text="Start",
                         font=("Helvetica", 20),
                         command=startgame)
    startbutton.place(x=960, y=600, anchor=CENTER)

    leaderbutton = Button(canvas, text="View leaderboard",
                          font=("Helvetica", 20),
                          command=leaderboard)
    leaderbutton.place(x=960, y=700, anchor=CENTER)

    loadbutton = Button(canvas, text="Load save",
                        font=("Helvetica", 20),
                        command=loadsave)
    loadbutton.place(x=960, y=800, anchor=CENTER)

    # creates text for homepage
    titletext = canvas.create_text(960, 300, text="The Impossible Game",
                                   font=("Helvetica", 30),
                                   fill="white")
    welcometext = canvas.create_text(960, 450, text="Welcome!",
                                     font=("Helvetica", 80),
                                     fill="white")
    esctext = canvas.create_text(960, 900, text="Press esc to quit",
                                 font=("Helvetica", 10),
                                 fill="white")
    pausetext = canvas.create_text(960, 950,
                                   text="Press p to toggle pause, " +
                                   "x to toggle work mode (boss key)",
                                   font=("Helvetica", 10),
                                   fill="white")
    savetext = canvas.create_text(960, 1000,
                                  text="You can save progress at the end " +
                                  "of each level, and add to the " +
                                  "leaderboard if you win!",
                                  font=("Helvetica", 10),
                                  fill="white")
    cheattext = canvas.create_text(960, 862,
                                   text="Hold c to disable collisions",
                                   font=("Helvetica", 6),
                                   fill="white")

    # creates photo for homepage
    smileyphoto = PhotoImage(file="smiley.gif")
    smileyphotolabel = Label(image=smileyphoto, borderwidth=0)
    smileyphotolabel.image = smileyphoto
    smileyphotolabel.place(x=50, y=50)

def playerconfig(x1=50, y1=540, x2=150, y2=640):
    global player

    player = canvas.create_rectangle(x1, y1, x2, y2, fill="red", width=5)
    window.bind(leftkey, lambda x: canvas.move(player, -10, 0))
    window.bind(rightkey, lambda x: canvas.move(player, 10, 0))
    window.bind(upkey, lambda x: canvas.move(player, 0, -10))
    window.bind(downkey, lambda x: canvas.move(player, 0, 10))




def bosskey():
    global bossmode, workphotolabel, workphoto

    bossmode = not bossmode
    try:
        smileyphotolabel.destroy()
    except:
        pass

    if bossmode is True:
        workphotolabel.place(x=-2, y=-2)
    else:
        workphotolabel.destroy()
        workphotolabel = Label(image=workphoto)
        workphotolabel.image = workphoto


def cheatmodeon():
    global cheatmode
    cheatmode = True


def cheatmodeoff():
    global cheatmode
    cheatmode = False

def quitgame():
    global pause
    if pause is False:
        pausegame()
    quitbox = messagebox.askquestion("Quit", "Are you sure you want to quit?",
                                     icon="warning")
    if quitbox == 'yes':
        window.destroy()
        try:
            keypromptbox.destroy()
        except:
            pass
