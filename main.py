#Alannnah Steck
#U1L2
#visualizing rat growth
from Rats import Rat


import random
import time
import matplotlib.pyplot as plt


GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what

def findBig(biggestRats):
  bigWeight = biggestRats[0].getWeight()
  bigRat = biggestRats[0]
  for rat in biggestRats:
    ratWeight = rat.getWeight()
    if ratWeight > bigWeight:
      bigWeight = ratWeight
      bigRat = rat
  return bigRat

def fitness(rats, pups):
  for index in range(2):
    for pup in pups[index]:
      rats[index].append(pup)
  totalWeight = 0
  timesAdded = 0
  for sex in rats:
    for rat in sex:
      weight = rat.getWeight()
      totalWeight += weight
      timesAdded += 1
  mean = int(totalWeight/timesAdded)
  return mean >= GOAL, mean

def select(rats):
  biggestRats = []
  smallestRats = []
  for index in range(2):
    for rat in rats[index]:
      status = rat.canBreed()
      if status == False:
        rats[index].remove(rat)
  for index in range(2): 
    smallest = rats[index][0]
    smallWeight = smallest.getWeight()
    for rat in rats[index]:
      ratWeight = rat.getWeight()
      if ratWeight < smallWeight:
         smallest = rat
    smallestRats.append(smallest)
    amount = len(rats[index])
    while amount > 10:
      smallest = rats[index][0]
      smallWeight = smallest.getWeight()
      for rat in rats[index]:
        ratWeight = rat.getWeight()
        if ratWeight < smallWeight:
         smallest = rat
         smallWeight = smallest.getWeight()
      rats[index].remove(smallest)
      amount -= 1
    biggest = rats[index][0]
    bigWeight = biggest.getWeight()
    for rat in rats[index]:
      ratWeight = rat.getWeight()
      if ratWeight > bigWeight:
         biggest = rat
    biggestRats.append(biggest)
  biggest = biggestRats[0]
  bigWeight = biggest.getWeight()
  for rat in biggestRats:
    ratWeight = rat.getWeight()
    if ratWeight > bigWeight:
      biggest = rat
  smallest = smallestRats[0]
  smallWeight = smallest.getWeight()
  for rat in smallestRats:
    ratWeight = rat.getWeight()
    if ratWeight < smallWeight:
      smallest = rat

  return rats, biggest, smallest

def breed(rats):
  pups = [[],[]]
  random.shuffle(rats[0])
  for time in range(10):
    sexes = ["M","F"]
    dad = rats[0][time]
    mom = rats[1][time]
    mom.litter += 1
    dad.litter += 1
    for baby in range(LITTER_SIZE):
      sex = random.choice(sexes)
      wt = calculate_weight(sex, mom, dad) 
      R = Rat(sex, wt)
      pupSex = R.getSex()
      if pupSex == "M":
        pups[0].append(R)
      else:
        pups[1].append(R)
  return pups 

def mutate(pups):
  for index in range(2):
    for pup in pups[index]:
      chance = random.random()
      if chance <= MUTATE_ODDS:
        scale = random.uniform(MUTATE_MIN, MUTATE_MAX)
        pup.mutate(scale)
  return pups


def calculate_weight(sex, mother, father):
  
  # Use the triangular function from the random library to skew the 
  #baby's weight based on its sex
  mWeight = father.getWeight()
  fWeight = mother.getWeight()
  if sex == "M":
    wt = int(random.triangular(mWeight, fWeight, fWeight))
  else:
    wt = int(random.triangular(mWeight, fWeight, mWeight)) 
  
  return wt

def initial_population():
  #Create the initial set of rats based on constants
  rats = [[],[]]
  mother = Rat("F", INITIAL_MIN_WT)
  father = Rat("M", INITIAL_MAX_WT) 
  
  for r in range(NUM_RATS):
    if r < 10:
      sex = "M"
      ind = 0
    else:
      sex = "F"
      ind = 1
  
    wt = calculate_weight(sex, mother, father) 
    R = Rat(sex, wt)
    rats[ind].append(R)
  
  return rats

def fileToList(files):
  newFiles = []
  for item in files:
    with open(item, 'r') as openFile:
      contents = openFile.read()
    contents = contents.split(",\t")
    for item in contents:
      try:
        ind = contents.index(item)
        item = int(item) 
        contents[ind] = item
      except:
        contents.remove(item)
    newFiles.append(contents)
  return newFiles

def makeGraph(files):
  avgSet = files[0]
  maxSet = files[1]
  minSet = files[2]

  for data in [avgSet,maxSet,minSet]:
    plt.plot(data)
  plt.title("Rat Weights")
  plt.xlabel("generation")
  plt.ylabel("weight (grams)")

  plt.legend(["averages","biggest","smallest"])
  plt.savefig("sample.png")

def main():
  start = time.time()
  generations = 0
  pups = [[],[]]
  finished = False
  means = []
  meansStr =""
  biggestList = []
  smallestList = []
  bigStr =""
  smallStr =""
  #code n stuff :)
  rats = initial_population()
  while finished == False and generations < GENERATION_LIMIT:
    
    finished, mean = fitness(rats, pups) #kids join parents, add groups
    means.append(mean)
    rats, biggest, smallest = select(rats)
    biggestList.append(biggest)
    smallestList.append(smallest)
    pups = breed(rats) 
    pups = mutate(pups)
    generations += 1

  #print things below
  stop = time.time()
  timeRun = round(stop - start, 3)
  print("…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ".center(50," "))
  print("RESULTS".center(32," "))
  print("…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁠⁐̤⁠ᕐ⁠ᐷ…⁠ᘛ⁐̤ᕐᐷ".center(50," ") + "\n")
  print(f"Generations: {generations}")
  years = int(generations/GENERATIONS_PER_YEAR)
  print(f"Experiment Duration: ~{years} years")
  print(f"Simulation Duration : {timeRun}\n\n")
  print("The Largest Rat")
  biggestRat = findBig(biggestList)
  print(biggestRat) 
  for bigRat in biggestList:
    bigRat = bigRat.getWeight()
    bigRat = str(bigRat)
    bigStr += f"{bigRat},\t"
    with open("maximums.txt", 'w') as openFile:
      openFile.write(bigStr) 
  for smallRat in smallestList:
    smallRat = smallRat.getWeight()
    smallRat = str(smallRat)
    smallStr += f"{smallRat},\t"
    with open("minimums.txt", 'w') as openFile:
      openFile.write(smallStr) 
  print("\n\nGeneration Weight Averages (grams)\n")
  for mean in means:
    mean = str(mean)
    meansStr += f"{mean},\t"
    with open("averages.txt", 'w') as openFile:
      openFile.write(meansStr) 

  print(meansStr)
  files = ["averages.txt","maximums.txt","minimums.txt"]
  files = fileToList(files)
  makeGraph(files)

  
  

if __name__ == "__main__":
  main()