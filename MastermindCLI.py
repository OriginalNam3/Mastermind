from MastermindClass import Mastermind


class MastermindCLI:
    def __init__(self):
        self.game = Mastermind()

    def help(self):
        print('This game requires you to guess a code comprised of', self.game.c, '. \n\n\nHere are some helpful commands:')
        print('"/guesses" for a list of past guesses.\n"/code" to reinput the code. \n"/restart" to restart the entire game. '
              '\n"/tries" to see how many guesses you have made. \n"/parameters" to see game parameters\n"/exit" to exit the game. \n\n')

    def commands(self, c):
        if c == 'guesses':
            print('Guesses: ')
            for g in self.game.get_guesses():
                print(g)
            print('\n\n')
        if c == 'code':
            print('Code was ', self.game.code)
            s = ''
            while not s or len(s) != self.game.rn or not self.game.valid(s): s = input()
            self.game.code = s
            self.game.reset()
        if c == 'restart':
            self.play()
        if c == 'turn':
            print('Tries: ', self.game.t)
        if c == 'parameters':
            print('Lmao u thought. ')
        if c == 'exit':
            exit(0)

    def play(self):
        while True:
            self.help()
            print('First input the code! (input /randomcode to generate a random code)')
            s = ''
            while (not s or len(s) != self.game.rn or not self.game.valid(s)) and s != '/randomcode': s = input('Code: ')
            if s == '/randomcode': self.game.gen_code()
            else: self.game.code = list(s)
            print('\n\n')
            while self.game.state:
                guess = ''
                while not guess or len(guess) != self.game.rn or not self.game.valid(guess): guess = input('Guess: ')
                guess = list(guess)
                if guess[0] == '/':
                    self.commands(guess[1:])
                    continue
                self.game.check(guess)
                if not self.game.state: print('You Win!\n\n\n')
                else: print('You got', self.game.check(guess)[1], 'colours correct with their positions wrong and', self.game.check(guess)[0], 'colours AND positions correct!')
