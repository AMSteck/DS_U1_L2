class Rat:
   def __init__(self, sex, weight):
    self.sex = sex
    self.weight = weight
    self.litter = []

  def __str__(self):
    return f"{self.sex}, {self.weight}