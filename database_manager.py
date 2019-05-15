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

	OnwerId = Column(Integer, ForeignKey("People.Id",
		ondelete='CASCADE'))
	Owner = relationship("Person")

	def get_weights_as_array(self, weight_count = 10):
		values = self.Weights.split(' ')
		temp = range(1, weight_count - 1)
		result = []

		result.append(float(values[0][1:]))
		for i in temp:
			result.append(float(values[i]))
		result.append(float(values[weight_count - 1][:-1]))		

		return result

def create_tables():
	Base.metadata.bind = engine	
	Base.metadata.create_all()

def renew_tables():
	SubspaceImage.__table__.drop(engine)
	Person.__table__.drop(engine)
	#SubspaceImages.__table__.drop(engine)

	create_tables()

def renew_subspaceimage_table():
	SubspaceImage.__table__.drop(engine)
	SubspaceImage.__table__.create(engine)

def get_people(*ids):
	session = Session()
	people = None
	
	if (len(ids) > 0):
		people = session.query(Person).filter(Person.Id.in_(ids))
	if (people.first() is None):
		maxid = session.query(func.max(Person.Id))[0][0]
		people = session.query(Person).filter(Person.Id == maxid)

	session.close()
	return people

def get_people_count():
	session = Session()
	result = session.query(func.count(Person.Id))
	session.close()
	return result[0][0]

def get_subspace_images(ids = None):
	session = Session()
	if (ids is None):
		result = session.query(SubspaceImage).all()
	session.close()
	return result

def create_people(*people):
	'''each person data will be saved in the form of name, age, occupation'''	
	session = Session()

	for personData in people:
		if (len(personData) >= 3):
			person = Person(Name = personData[0], Age = personData[1], Occupation = personData[2])

	session.add(person)
	session.commit()
	session.close()

def create_subspace_images(file_info, weights, remove = False):
	if (remove):
		delete_subspace_images(None)

	Images = []
	temp = range(0, len(file_info))

	for i in temp:
		Images.append(
			SubspaceImage(Path = file_info[i][1], OnwerId = file_info[i][0], Weights = str(weights[i])))

	session = Session()
	session.add_all(Images)
	session.commit()
	session.close()

def delete_subspace_images(ids):
	if (ids == None):
		session = Session()
		session.execute('''TRUNCATE TABLE SubspaceImages''')
		session.commit()
		session.close()
		return

def clean_up():
	engine.dispose()

if (__name__ == "__main__"):
	# renew_tables()
	# clean_up()
	pass
