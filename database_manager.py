from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql+pymysql://root:caothanhhuyen123@localhost:3306/face_recognition")
Session = sessionmaker(bind =  engine)

Base = declarative_base()

class Person(Base):
	__tablename__ = "People"

	Id = Column(Integer, primary_key = True)
	Name = Column(String(250))
	Age = Column(Integer)
	Occupation = Column(String(250))

	SubspaceImages = relationship("SubspaceImage",
		cascade = "all, delete, delete-orphan")

class SubspaceImage(Base):
	__tablename__ = "SubspaceImages"

	Id = Column(Integer, primary_key = True)
	Path = Column(String(250))
	Weights = Column(String(1000))

	OnwerId = Column(Integer, ForeignKey("People.Id"))
	Owner = relationship("Person")

def create_tables():
	Base.metadata.bind = engine	
	Base.metadata.create_all()

def renew_tables()
	Person.__table__.drop()
	SubspaceImages.__table__.drop()

	create_tables()

def get_people(*ids):
	session = Session()
	
	if (len(ids) > 0):
		people = session.query(Person).filter(Person.Id.in_(ids))
	
	session.close()
	return people

def get_people_count():
	session = Session()
	count = session.query(func.count(Person.Id))
	session.close()
	return count

def create_people(*people):
	'''each person data will be saved in the form of name, age, occupation'''	
	session = Session()

	for personData in people:
		if (len(personData) >= 3):
			person = Person(Name = personData[0], Age = personData[1], Occupation = personData[2])

	session.add(person)
	session.commit()
	session.close()

def clean_up():
	engine.dispose()

if (__name__ == "__main__"):
	# create_tables()
