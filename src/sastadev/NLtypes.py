from dataclasses import dataclass

@dataclass
class Top:
    name: str = "Top"

@dataclass
class Object(Top):
    name: str = "Object"


@dataclass
class Temporal:
    name: str = "Temporal"

@dataclass
class Time(Temporal):
    name: str = "Time"


@dataclass
class Period(Temporal):
    name: str = "Period"
    source: Time = None
    dest: Time = None


@dataclass
class Event(Top):
    name: str = "Event"
    period: Period = Period()


@dataclass
class Locational(Top):
    name: str = "Temporal"

@dataclass
class Location(Locational):
    name: str = "Locational"

@dataclass
class Path(Locational):
    name: str = "Path"
    source : Location = None
    dest : Location = None

@dataclass
class Animate(Object):
    name: str = "Animate"


@dataclass
class NonAnimate(Object):
    name: str = "NoneAnimate"

@dataclass
class Human(Animate):
    name: str = "Human"

@dataclass
class NonHuman(Animate):
    name: str = "NonHuman"

@dataclass
class Role(Top):
    name: str = "Role"
    period: Period = Period()

@dataclass
class Activity(Event):
    name: str = "Activity"

# accomplishment, achievement

@dataclass
class State(Event):
    name: str = "State"

@dataclass
class Property(Event):
    name: str = "property"




def tryhierarchy():
    person = Human()
    r = isinstance(person, Human)
    print(r)
    r = isinstance(person, Animate)
    print(r)
    r = isinstance(person, Object)
    print(r)
    r = isinstance(person, Top)
    print(r)
    christmas = Event()
    r = isinstance(christmas, Object)
    print(r)
    r = isinstance(christmas, Human)
    print(r)


if __name__ == '__main__':
    tryhierarchy()