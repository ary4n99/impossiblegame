from tkinter import Tk, Canvas, Label, Button, messagebox
import sys
def quit():
    quitbox = messagebox.askquestion("Quit", "Are you sure you want to quit?", icon = "warning")
    if quitbox == 'yes':
        window.destroy()

def windowconfig(): #1920x1080
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
    canvas.create_rectangle(200, 0, 1720, 150, fill="midnight blue")
    canvas.create_rectangle(200, 930, 1720, 1080, fill="midnight blue")
    box1 = canvas.create_rectangle(200, 200, 300, 300, fill="firebrick4")

def level_one():
    global obstacle_one_direction, obstacle_one_speed
    coords = canvas.coords(box1)
    print(coords)
    if coords[3] >= 930:
        obstacle_one_direction = True
    elif coords[3] <= 250:
        obstacle_one_direction = False

    if obstacle_one_direction == True:
        canvas.move(box1, 0, -obstacle_one_speed)
    else:
        canvas.move(box1, 0, obstacle_one_speed)
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

obstacle_one_direction = False #false = down
obstacle_one_speed = 3
windowconfig()
playerconfig()
level_one_static()
level_one()
window.mainloop()