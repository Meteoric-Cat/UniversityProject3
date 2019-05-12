from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql+pymysql://root:caothanhhuyen123@localhost:3306/face_recognition")


Base = declarative_base()

class Person(Base):
	__tablename__ = "People"

	Id = Column(Integer, primary_key = True)
	Name = Column(String(250))
	Age = Column(Integer)
	Occupation = Column(String(250))

	SubspaceImages = relationship("SubspaceImage")

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

def stop_database_connections():
	engine.dispose()

if (__name__ == "__main__"):
	# create_tables()
