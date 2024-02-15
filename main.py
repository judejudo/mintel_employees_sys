from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"

    ssn = Column("ssn", Integer,primary_key=True )
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__ (self, ssn, first, last, gender, age):
        self.ssn = ssn
        self.firstname = first
        self.lastname = last
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender}, {self.age})"
    
class Thing(Base):
    __tablename__ = "things"

    tid = Column("tid", Integer, primary_key=True)
    description = Column("description", String)
    owner = Column(Integer, ForeignKey("people.ssn"))

    def __init__(self, tid, des, owner):
        self.tid = tid
        self.description = des
        self.owner = owner

    def __repr__(self):
        return f"({self.tid}) {self.description} owned by {self.owner}"
    
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)  

Session = sessionmaker(bind=engine)
session = Session()

person = Person(1234,"Mike","Smith", "m", 35)
session.add(person)
session.commit()

p1 = Person(2311, "Ann", "Smith", "f", 35)
p2 = Person(2312, "Bob", "Smith", "m", 25)
p3 = Person(2313, "Jude", "Judo", "m", 55)
session.add(p1)
session.add(p2)
session.add(p3)
session.commit()

t1 = Thing(1, "car", p1.ssn)
t2 = Thing(2, "laptop", p1.ssn)
t3 = Thing(3, "PS5", p2.ssn)
t4 = Thing(4, "Tool", p3.ssn)
t5 = Thing(5, "Book", p3.ssn)
session.add(t1)
session.add(t2)
session.add(t3)
session.add(t4)
session.add(t5)
session.commit()

# results = session.query(Person).filter(Person.lastname == "Smith")
# for result in results:
#     print(result)

results2 = session.query(Thing).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Anna").all()
for result in results2:
    print(result)