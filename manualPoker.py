# Imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
from tkcalendar import *
import xlsxwriter as xw

#region Window Config
# Define colors
mainColor = "#70A0A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 24)
inputFont = ("Verdana", 20)
usernameFont = ("Verdana", 16)
aFont = ("Times New Roman", 20)


def showFrame(frame):
    frame.tkraise()

# Creating window
root=Tk()
root.state("zoomed")  #Fullscreen
sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")

# Configurations
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

pokerFrame = Frame(root, background = mainColor)
pokerFrame.grid(row = 0, column = 0, sticky = "nsew")
#endregion

nameFont = ("Verdana", 22)
amtFont = ("Verdana", 16)
betFont = ("Verdana", 18)


potAmount = 0
pCount = 0
currentPlayer = None


class Player:

  def __init__(self, name, amt):
    self.name = name
    self.amt = amt
    self.bet = 0
    
    
    def sel():
      global currentPlayer
      currentPlayer = self


    self.nLabel = Label(pokerFrame, text = self.name)
    self.aLabel = Label(pokerFrame, text = f'$A: {self.amt}')
    self.bLabel = Label(pokerFrame, text = f'$B: {self.bet}')
    self.sbutton = Button(pokerFrame, text = "Select", command = sel)
  
Arun = Player("Arun", 1000)
Tauheed = Player("Tauheed", 1000)
Ethan = Player("Ethan", 1000)

players = [Arun, Tauheed, Ethan]
padxer = 100
for player in players:
  player.nLabel.grid(row = 1, column = pCount, padx = padxer, columnspan = 1)
  player.nLabel.config(font = nameFont)

  player.aLabel.grid(row = 2, column = pCount, padx = padxer, columnspan = 1)
  player.aLabel.config(font = amtFont)

  player.bLabel.grid(row = 3, column = pCount, padx = padxer, columnspan = 1)
  player.bLabel.config(font = betFont)

  player.sbutton.grid(row = 4, column = pCount, padx = padxer, columnspan = 1)
  pCount += 1

potNameLabel = Label(pokerFrame, text = "POT")
potNameLabel.grid(row = 5, column = 0, pady =(200, 0))
potNameLabel.config(font = nameFont)

potAmtLabel = Label(pokerFrame, text = f"${potAmount}")
potAmtLabel.grid(row = 6, column = 0)
potAmtLabel.config(font = betFont)

bnLabel = Label(pokerFrame, text = "Set bet")
bnLabel.grid(row = 5, column = 2, columnspan = 2, padx = 200)
bnLabel.config(font = betFont)

bEntry = Entry(pokerFrame)
bEntry.grid(row = 6, column = 2, columnspan = 2, padx = 200)
bEntry.config(font = betFont)

def update():
  for player in players:


def better():
  bet = bEntry.get()
  t = bet - currentPlayer.bet
  currentPlayer.amt -= t
  currentPlayer.bet = bet
  update()
bButton = Button(pokerFrame, text = "Set", command = lambda: print("HI"))
bButton.grid(row = 7, column = 2, columnspan = 1)
bButton.config(font = amtFont)

pButton = Button(pokerFrame, text = "Push", command = lambda: print("PUSH"))
pButton.grid(row = 7, column = 3, columnspan = 1)
pButton.config(font = amtFont)

cpLabel = Label(pokerFrame, text = f"Current Player: {Arun.name}")
cpLabel.grid(row = 7, column = 1, padx = 0)
cpLabel.config(font = amtFont)





root.mainloop()