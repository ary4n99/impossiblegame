from tkinter import Tk, Canvas, Label, Button, messagebox, CENTER, PhotoImage, NW
import sys
def quit():
    quitbox = messagebox.askquestion("Quit", "Are you sure you want to quit?", icon = "warning")
    if quitbox == 'yes':
        window.destroy()

def windowconfig():
    global window, canvas
    window = Tk()
    window.geometry("1920x1080")
    window.attributes("-fullscreen", True)
    window.bind('<Escape>', lambda x: quit())
    window.bind("<Key>", move)
    canvas = Canvas(window, width=1920, height=1080)
    canvas.pack()

def level_one_static():
    global box1
    box1 = canvas.create_rectangle(200, 200, 300, 300, fill="firebrick4")
    canvas.create_rectangle(200, 0, 1720, 150, fill="midnight blue")
    canvas.create_rectangle(200, 930, 1720, 1080, fill="midnight blue")
    # canvas.create_image(500, 500, image=PhotoImage(file="coin.gif"))

def level_one():
    global obstacle_one_direction, obstacle_one_speed
    coords = canvas.coords(box1)
    if coords[3] >= 930: obstacle_one_direction = True
    elif coords[3] <= 250: obstacle_one_direction = False
    if obstacle_one_direction == True: canvas.move(box1, 0, -obstacle_one_speed)
    else: canvas.move(box1, 0, obstacle_one_speed)
    window.after(2, level_one)

def playerconfig():
    global player
    player = canvas.create_oval(50, 540, 130, 620, fill="black")

def move(event):
    movefactor = 10
    if event.char == "a": canvas.move(player, -movefactor, 0)
    elif event.char == "d": canvas.move(player, movefactor, 0)
    elif event.char == "w": canvas.move(player, 0, -movefactor)
    elif event.char == "s": canvas.move(player, 0, movefactor)

def welcomepage():
    global startbutton, leaderbutton, welcometext, esctext, titletext
    canvas.configure(bg="black")
    
    startbutton = Button(canvas, text="Start", font=("Helvetica", 20), command=startgame)
    startbutton.place(x=960, y=600, anchor=CENTER)
    
    leaderbutton = Button(canvas, text="View leaderboard", font=("Helvetica", 20), command=leaderboard)
    leaderbutton.place(x=960, y=700, anchor=CENTER)
    
    titletext = canvas.create_text(960, 300, text="The Impossible Game", font=("Helvetica", 30), fill="white")
    welcometext = canvas.create_text(960, 450, text="Welcome!", font=("Helvetica", 80), fill="white")
    esctext = canvas.create_text(960, 800, text="Press esc to quit at anytime", font=("Helvetica", 10), fill="white")

def startgame():
    screenclear()
    canvas.configure(bg="white")
    playerconfig()
    level_one_static()
    level_one()

def screenclear():
    leaderbutton.destroy()
    startbutton.destroy()
    canvas.delete(welcometext, esctext, titletext)

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
    

obstacle_one_direction = False # False = down
obstacle_one_speed = 3

windowconfig()
welcomepage()

window.mainloop()