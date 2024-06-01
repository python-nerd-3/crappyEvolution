import random
import copy
from matplotlib import pyplot as plt
import numpy as np
# i am aware that there is no disadvantage in just increasing your stats and lowering your gullibility
# this is just to test the emergent behavior and watch number go up bc number up = dopamine

γ = 1 # mutation factor; determines how volatile mutations are
spawnAmt = 200 # how many goobers are created in the first generation

goobers = []
ids = 0
stats = ("power", "charm", "wisdom")
run = True
gen = 0
heritages = []
cont = True
autorun = 0
popHistory = []
matplotlibIsCringe = []

def splitList(lst, chunk_size):
    return list(zip(*[iter(lst)] * chunk_size))
# fun fact i stole this code

def mean(lst):
    return sum(lst) / len(lst)
    

def mutate(goober):
    newGoober = Goober()
    newGoober.power = goober.power + random.randint(γ * -1, γ)
    newGoober.charm = goober.charm +  random.randint(γ * -1, γ)
    newGoober.wisdom = goober.wisdom + random.randint(γ * -1, γ)
    newGoober.stats = {"power": newGoober.power, "charm": newGoober.charm, "wisdom": newGoober.wisdom} 
    newGoober.stats = list(newGoober.stats.items())
    random.shuffle(newGoober.stats)
    newGoober.topStat = sorted(newGoober.stats, key=lambda item: item[1])[0][0]
    newGoober.gullibility = goober.gullibility + random.randint(γ * -1, γ)
    newGoober.gullibility = max(min(newGoober.gullibility, 100), 0)
    newGoober.heritage = goober.heritage


class Goober:
    def __init__(self):
        global ids
        self.power = random.randint(8, 12)
        self.charm = random.randint(8, 12)
        self.wisdom = random.randint(8, 12)
        
        self.stats = {"power": self.power, "charm": self.charm, "wisdom": self.wisdom} 
        self.stats = list(self.stats.items())
        random.shuffle(self.stats)
        self.topStat = sorted(self.stats, key=lambda item: item[1])[0][0]

        self.weakAppearance = random.choice(("power", "charm", "wisdom"))
        self.gullibility = random.randint(45, 55)
        self.id = ids + 1
        self.heritage = self.id

        goobers.append(self)
        ids += 1

for i in range(spawnAmt):
    Goober() # this is the most threatening line of code known to man

print(f"{spawnAmt} goobers have emerged from the depths.")
print("Each and every one is mediocre for now but shall rise soon.")
while run:
    gen += 1
    random.shuffle(goobers)
    battlers1 = goobers[int(len(goobers)/2):]
    battlers2 = goobers[:int(len(goobers)/2)]
    ind = -1
    for i in battlers1:
        ind += 1
        j = battlers2[ind]
        stat = j.weakAppearance if i.gullibility < random.randint(1, 100) else i.topStat
        if (getattr(i, stat) > getattr(j, stat)):
            print(f"Goober #{i.id} wins against #{j.id}! [{stat}]")
            goobers = [k for k in goobers if k.id != j.id]
        elif (getattr(i, stat) < getattr(j, stat)):
            print(f"Goober #{j.id} wins against #{i.id}! [{stat}]")
            goobers = [k for k in goobers if k.id != i.id]
        else:
            print(f"It's a tie between #{i.id} and #{j.id}!", end=" ")
            if (random.getrandbits(1) if len(goobers) > spawnAmt / 4 else random.getrandbits(2)):
                print("Both goobers survive!")
            else:
                print("Both goobers die.")
                goobers = [k for k in goobers if k.id != j.id and k.id != i.id]
    print(f"Generation {gen}: {len(goobers)} goobers remain.")
    currentGen = copy.copy(goobers)
    for i in currentGen: 
        mutate(i)
    if len(goobers) == 0:
        print("Goobers have gone extinct.")
        run == False
        continue
    print(f"They all clone and there are now {len(goobers)} goobers.")
    cont = True
    popHistory.append(len(goobers))
    if autorun:
        autorun -= 1
        continue
    while cont:
        inp = input("Input to continue, \"exit\" to exit > ")
        cont = False
        if (inp == "exit"):
            run = False
        if (inp == "stats"):
            print("Mean power: " + str(mean(list(map(lambda i: i.power, goobers)))))
            print("Mean charm: " + str(mean(list(map(lambda i: i.charm, goobers)))))
            print("Mean wisdom: " + str(mean(list(map(lambda i: i.wisdom, goobers)))))
            print("Mean gullibility: " + str(mean(list(map(lambda i: i.gullibility, goobers)))))
            cont = True
        if (inp == "heritage"):
            heritages = {}
            for i in goobers:
                if str(i.heritage) in heritages:
                    heritages[str(i.heritage)] += 1
                else:
                    heritages[str(i.heritage)] = 1
            heritages = dict(sorted(heritages.items(), key= lambda i: i[1]))
            print(heritages)
            cont = True
        if (inp.isdigit()):
            inp = int(inp)
            autorun = inp
        if (inp == "pop"):
            plt.plot(np.array(popHistory))
            plt.show()
            cont = True