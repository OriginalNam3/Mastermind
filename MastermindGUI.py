import tkinter as tk
from MastermindClass import Mastermind
import random


class MastermindGUI:

    def __init__(self):
        self.game = Mastermind()
        self.colours = ['red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'purple', 'brown']
        self.choice = 'red'
        self.game.gen_code()
        self.window = tk.Tk()
        self.window.title('MASTERMIND')
        self.displayfrm = tk.Frame(self.window, highlightbackground='black', highlightthickness=1)
        self.displayfrm.grid(row=0, column=0)
        self.h = 60
        self.r = 25
        self.w = self.h * (self.game.rn+1)
        self.display = tk.Canvas(self.displayfrm, height=self.h * 10, width=self.w)
        self.display.grid(row=1, column=0)
        self.triesdisplay = tk.Label(self.displayfrm, text='Tries: 0')
        self.triesdisplay.grid(row=0, column=0)
        self.message = tk.Label(self.window, text='MASTERMIND', font='Garamond, 15')
        self.message.grid(row=1, column=0)
        self.inputfrm = tk.Frame(self.window)
        self.inputfrm.grid(row=2, column=0)
        self.buttons = tk.Canvas(self.inputfrm, height=3.2 * self.h)
        self.buttons.grid(row=0, column=0)

        self.submitbtn = tk.Button(self.inputfrm, text='Submit Guess', command=self.submit)
        self.submitbtn.grid(row=1, column=0)

        self.guess = []
        for x in range(4):
            btn = self.buttons.create_oval(self.h / 2 + self.r / 2 + self.h * (x % 4), self.h * (x // 4) + (self.r / 2),
                                      self.h * (x % 4 + 1) - (self.r / 2) + (self.h / 2), self.h * ((x // 4) + 1) - (self.r / 2), fill=random.choice(self.colours))
            self.buttons.tag_bind(btn, '<Button-1>', self.select)
            self.guess.append(btn)

        self.pastguesses = []
        for y in range(10):
            self.display.create_rectangle(0, self.h * y, self.w, self.h * y + 1, fill='black')
            ng = []
            pegs = []
            for x in range(4):
                ng.append(self.display.create_oval(((self.h * ((2 * x) + 1)) / 2) - self.r, ((self.h * ((2 * y) + 1)) / 2) - self.r,
                                              ((self.h * ((2 * x) + 1)) / 2) + self.r, ((self.h * ((2 * y) + 1)) / 2) + self.r,
                                              fill='grey'))
                pegs.append(
                    self.display.create_oval((self.h * (4.25 + (x % 2) / 2)) - self.r / 4, (self.h * (y + 0.25 + (x // 2) / 2)) - self.r / 4,
                                        (self.h * (4.25 + (x % 2) / 2)) + (self.r / 4), (self.h * (y + 0.25 + (x // 2) / 2)) + (self.r / 4),
                                        fill='grey'))
            self.pastguesses.append([ng, pegs])

        for x in range(8):
            self.buttons.tag_bind(self.buttons.create_rectangle(self.h / 2 + self.h * (x % 4), self.h * ((x // 4) + 1), self.h / 2 + self.h * (x % 4 + 1),
                                     self.h * ((x // 4) + 2),
                                     fill=self.colours[x]), '<Button-1>', self.change)
        self.window.mainloop()

    def win(self, w):
        def again():
            self.game.reset()
            self.submitbtn.config(text='Submit Guess', command=self.submit)
            self.message.config(text='MASTERMIND', fg='black')
            self.triesdisplay.config(text='Tries: 0')
        if w:
            self.message.config(text='YOU WIN!!!', fg='gold')
        else:
            self.message.config(text='YOU LOSE :(', fg='red')
        self.submitbtn.config(text='Play Again', command=again)

    def submit(self):
        g = [self.colours.index(self.buttons.itemcget(self.guess[i], 'fill')) for i in range(4)]
        if self.game.valid(g): self.game.check(g)
        c = [self.colours[self.game.get_last_guess()[0][i]] for i in range(self.game.rn)]
        b, w = self.game.get_last_guess()[1]
        self.triesdisplay.config(text='Tries: ' + str(self.game.t))
        for x in range(4):
            self.display.itemconfig(self.pastguesses[self.game.t - 1][0][x], fill=c[x])
        for x in range(b + w):
            if b > 0:
                b -= 1
                self.display.itemconfig(self.pastguesses[self.game.t - 1][1][x], fill='black')
            else:
                self.display.itemconfig(self.pastguesses[self.game.t - 1][1][x], fill='white')
        if not self.game.state:
            self.resetguesses()
            self.win(self.game.get_last_guess()[1][0] == 4)


    def select(self, event):
        for x in range(4):
            if self.h / 2 + self.r / 2 + self.h * (x % 4) <= event.x <= self.h * (x % 4 + 1) - (self.r / 2) + (self.h / 2) and self.h * (x // 4) + (
                    self.r / 2) <= event.y <= self.h * ((x // 4) + 1) - (self.r / 2):
                self.buttons.itemconfig(self.guess[x], fill=self.choice)
                break

    def change(self, event):
        for x in range(8):
            if (self.h / 2) + self.h * (x % 4) <= event.x <= (self.h / 2) + self.h * (x % 4 + 1) and self.h * ((x // 4) + 1) <= event.y <= self.h * (
                    (x // 4) + 2):
                self.choice = self.colours[x]
                break

    def resetguesses(self):
        for ng, pegs in self.pastguesses:
            for x in range(4):
                self.display.itemconfig(ng[x], fill='grey')
                self.display.itemconfig(pegs[x], fill='grey')


    # def play(self):
    #     guess = [''] * self.game.rn
    #     self.window = tk.Tk()
    #     self.window.title('Mastermind')
    #     guessfrm = tk.Frame(self.window, highlightbackground='black', highlightthickness=1, padx=10, pady=10)
    #     guessfrm.grid(row=0)
    #     inputfrm = tk.Frame(self.window, highlightbackground='black', highlightthickness=1, padx=10, pady=10)
    #     inputfrm.grid(row=1)
    #     tk.Label(guessfrm, text='Guesses').grid(row=0, column=0, columnspan=4)
    #     tk.Label(guessfrm, text='White').grid(row=0, column=4)
    #     tk.Label(guessfrm, text='Black').grid(row=0, column=5)
    #
    #     for y in range(10):
    #         for x in range(4):
    #             tk.Label(guessfrm, bg='white', text='      ', highlightbackground='black', highlightthickness=1).grid(row=1+y, column=x)
    #
    #     lbl1 = tk.Label(inputfrm, bg=random.choice(self.colours), text='      ')
    #     lbl1.grid(row=0, column=1)
    #     lbl2 = tk.Label(inputfrm, bg=random.choice(self.colours), text='      ')
    #     lbl2.grid(row=0, column=2)
    #     lbl3 = tk.Label(inputfrm, bg=random.choice(self.colours), text='      ')
    #     lbl3.grid(row=0, column=3)
    #     lbl4 = tk.Label(inputfrm, bg=random.choice(self.colours), text='      ')
    #     lbl4.grid(row=0, column=4)
    #
    #     def changeone():
    #         lbl1.config(bg=self.colours[(self.colours.index(lbl1['bg']) + 1) % 8])
    #
    #     def changetwo():
    #         lbl2.config(bg=self.colours[(self.colours.index(lbl2['bg']) + 1) % 8])
    #
    #     def changethree():
    #         lbl3.config(bg=self.colours[(self.colours.index(lbl3['bg']) + 1) % 8])
    #
    #     def changefour():
    #         lbl4.config(bg=self.colours[(self.colours.index(lbl4['bg']) + 1) % 8])
    #
    #     def submit():
    #         guess = [self.game.c[self.colours.index(lbl1['bg'])], self.game.c[self.colours.index(lbl2['bg'])], self.game.c[self.colours.index(lbl3['bg'])], self.game.c[self.colours.index(lbl4['bg'])]]
    #         self.game.check(guess)
    #         guesses = self.game.g[-10:]
    #         for i in range(len(guesses)):
    #             for j in range(len(guesses[i][0])):
    #                 tk.Label(guessfrm, bg=self.colours[self.game.c.index(guesses[len(guesses)-i-1][0][j])],
    #                          text='      ', highlightbackground='black', highlightthickness=1).grid(row=10-i, column=j)
    #             tk.Label(guessfrm, text=guesses[len(guesses)-i-1][1][1]).grid(row=10 - i, column=4)
    #             tk.Label(guessfrm, text=guesses[len(guesses) - i - 1][1][0]).grid(row=10 - i, column=5)
    #         if not self.game.state or self.game.t >= 10:
    #             self.window.destroy()
    #             self.win(not self.game.state)
    #
    #     tk.Button(inputfrm, command=changeone, text='1').grid(row=1, column=1)
    #     tk.Button(inputfrm, command=changetwo, text='2').grid(row=1, column=2)
    #     tk.Button(inputfrm, command=changethree, text='3').grid(row=1, column=3)
    #     tk.Button(inputfrm, command=changefour, text='4').grid(row=1, column=4)
    #     tk.Button(inputfrm, text='Submit', bg='black', command=submit, fg='black', height=3).grid(row=0, rowspan=2, column=5, columnspan=2)
    #     self.window.mainloop()
