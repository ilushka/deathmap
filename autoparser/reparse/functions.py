class Age:
  def __init__(self, age):
    self.age = age

  def get_age(self):
    return self.age
    
def basic_age(age):
  return Age(age[0][0])

def victim_age(a):
  return a[0]

def age_year_old(a):
  return a

functions = {
  'Basic Age': basic_age,
  'Victim Age': victim_age,
  'Age Year Old': age_year_old
}

