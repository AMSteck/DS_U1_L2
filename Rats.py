#git@github.com:AMSteck/DS_U1_L1.git

class Rat:
   def __init__(self, sex, weight):
    self.sex = sex
    self.weight = weight
    self.litter = 0

   def __str__(self):
    string = f"<·^__)~~ |{self.sex}| ~ {self.weight} grams"
    return string

   def __repr__(self):
    string = f"<·^__)~~ |{self.sex}| ~ {self.weight} grams"
    return string

   def mutate(self, scale):
      self.weight *= scale
      self.weight = int(self.weight)

   def getSex(self):
      return self.sex

   def getWeight(self):
      return self.weight

   def canBreed(self):
      if self.litter < 5:
         return True
      else:
         return False

   def __lt__(self, other):
    return self.weight < other.weight

   def __le__(self, other):
    return self.weight <= other.weight

   def __gt__(self, other):
    return self.weight > other.weight

   def __ge__(self, other):
    return self.weight >= other.weight

   def __eq__(self, other):
    return self.weight == other.weight
