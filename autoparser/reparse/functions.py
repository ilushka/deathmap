import sys
import itertools

DO_DEBUG = False

class TitleMatch:
  def __init__(self, match, weight):
    self.match = match
    self.weight = weight

  def __repr__(self):
    return "<TitleMatch: \"%s\", %d>" % (self.match, self.weight)

def __debug(*args):
  if DO_DEBUG:
    print sys._getframe(1).f_code.co_name + ": " + str(args)
  
def certain_victim(Victim):
  __debug(Victim)
  if Victim[0] is not None:
    return TitleMatch(match=Victim[0][0], weight=10)
  return None

def ambiguous_victim(Victim):
  __debug(Victim)
  if Victim[0] is not None:
    return TitleMatch(match=Victim[0][0], weight=2)
  return None

def certain_victim_state(State):
  __debug(State)
  if State[0] is not None:
    return TitleMatch(match=State[0][0], weight=10)
  return None

def ambiguous_victim_state(State):
  __debug(State)
  if State[0] is not None:
    return TitleMatch(match=State[0][0], weight=5)
  return None

def wrong_victim_state(State):
  __debug(State)
  if State[0] is not None:
    return TitleMatch(match=State[0][0], weight=-5)
  return None

def any_crash(Crash):
  __debug(Crash)
  if Crash[0] is not None:
    return TitleMatch(match=Crash[0][0], weight=10)
  return None

def any_vehicle(Vehicle):
  __debug(Vehicle)
  if Vehicle[0] is not None:
    return TitleMatch(match=Vehicle[0][0], weight=10)
  return None

def crash_match(args):
  __debug(args)
  # remove all None elements
  args = filter(lambda a: a is not None, args)
  # flatten 2d array into 1d
  flattened = list(itertools.chain.from_iterable(args))
  # remove all None elemets again
  return filter(lambda a: a is not None, flattened)

functions = {
  'CertainVictim': certain_victim,
  'AmbiguousVictim': ambiguous_victim,
  'CertainVictimState': certain_victim_state,
  'AmbiguousVictimState': ambiguous_victim_state,
  'WrongVictimState': wrong_victim_state,
  'AnyCrash': any_crash,
  'AnyVehicle': any_vehicle,
  'CrashType1': crash_match,
  'CrashType2': crash_match,
  'CrashType3': crash_match,
  'CrashType4': crash_match,
  'CrashType5': crash_match,
  'CrashType6': crash_match,
}

