
round_bet = 20
small_blind = 50
big_blind = 100
pot = 0

class Player:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.contribution = 0
    
    global big_blind

    def __repr__(self):
      return f'{self.name}, A:{self.amount}, C:{self.contribution}'
    
    def fold(self):
        global turn
        self.push()
        print(f'{self.name} has folded')
        players.remove(self)
        turn -= 1

    def check(self):
        print(f'{self.name} has checked')

    def call(self):
        if self.amount>= (round_bet - self.contribution):
            self.amount -= (round_bet - self.contribution)
            self.contribution = round_bet
            print(f"{self.name} has called on ${round_bet}")
        else:
            self.contribution = self.amount
            self.amount = 0
            print(f'{self.name} is ALL IN!')
    
    def raiser(self, x = big_blind):
        global round_bet
        round_bet = x
        print(f'{self.name} raised bet to ${round_bet}/', end='')
        self.call()
    
    def push(self):
        global pot
        pot += self.contribution
        self.contribution = 0

Arun = Player("Arun", 1000)
Neal = Player("Neal", 1000)
Ethan = Player("Ethan", 1000)
Bob = Player("Bob", 1000)

totalPlayer = [Arun, Neal, Ethan, Bob]

for player in totalPlayer:
    print(player)

players = [x for x in totalPlayer]
turn = 0

def current():
    global turn
    return players[turn % len(players)]

def n():
    global turn
    turn += 1

def menu():
    print(f"Actions for Player {current().name}")
    print("1: Call")
    print("2: Raise")
    print("3: Fold")
    print("4: Check" if round_bet == 0 else "")
    op = int(input("Select Action: "))
    
    
    valid = 4 if round_bet == 0 else 3

    while int(op) < 1 or int(op) > valid:
        print("Invalid choice pick again")
        print(f"Actions for Player {current().name}")
        print("1: Call")
        print("2: Raise")
        print("3: Fold")
        print("4: Check" if round_bet == 0 else "")
        op = int(input("Select Action: "))


    error = False
    if op == 2:
        raiseAmount = int(input("Total Raise amount (including current table bet): "))
        if raiseAmount <= big_blind:
            print(f"Error: Bet must be at least the value of big blind ({big_blind}.")
            error = True
        elif raiseAmount <= round_bet:
            print("Error: Raise must be larger than current table bet")
            error = True
        elif current().amount + current().contribution < raiseAmount:
            print("Error: Insufficient funds to raise")
            error = True

    while error:
        error = False
        # Raise validation
        if op == 2:
            raiseAmount = int(input("Total Raise amount (including current table bet): "))
            if raiseAmount <= big_blind:
                print(f"Error: Bet must be at least the value of big blind ({big_blind}.")
                error = True
            elif raiseAmount <= round_bet:
                print("Error: Raise must be larger than current table bet")
                error = True
            elif current().amount + current().contribution < raiseAmount:
                print("Error: Insufficient funds to raise")
                error = True
    
    if op == 1:
        current().call()
    elif op == 2:
        current().raiser(raiseAmount)
    elif op == 3:
        current().fold()
    elif op == 4:
        current().check()


def matcher():
    def checkIt():
        for player in players:
            if player.contribution != round_bet:
                print(player.contribution, round_bet)
                return False
        return True
    global matched
    matched = checkIt()

def status():
    for player in players:
        print(player)
        print(f'{pot =}\t{round_bet =}')


# Preflop round
matched = False
dealer = turn
n()
small = current()
small.raiser(small_blind)
n()
big = current()
big.raiser(big_blind)
n()

while matched == False:
    menu()
    status()
    n()
    matcher()
for player in players:
    player.push()

round_bet = 0
status()

print("\n\nITS DA FLOP \n\n")
# Flop
turn = (dealer + 1) % len(players)
pCount = 0
while matched == False or pCount < len(players):
    menu()
    status()
    n()
    while current().contribution != round_bet and round_bet == 0:
      n()
    matcher()
    pCount += 1
  
for player in players:
    player.push()
status()