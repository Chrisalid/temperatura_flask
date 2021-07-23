from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///weather.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class City(Base):
    ''' Table Columns List

    Notes:
        This class lists the columns that the table
        will have in addition to adding a name to it.
    '''
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        ''' Table Representation

        Notes:
            This method is how the table
            will be represented.
        '''
        return f'<Activities {self.activity}>'

    def save(self):
        ''' Save Object To The Table

        Notes:
            Here, objects are saved in the table.
        '''
        db_session.add(self)
        db_session.commit()

    def delete(self):
        ''' Delete Object To The Table

        Notes:
            This method is designed to
            delete objects from the table.
        '''
        db_session.delete(self)
        db_session.commit()


def init_db():
    ''' Initialize The Database

    Notes:
        This method initializes the database and
        if it has not been created it creates it.
    '''
    Base.metadata.create_all(bind=engine)


def insert_city(name):
    ''' Insert A City

    Args:
        name: String
    Notes:
        This method inserts a new city from its name.
    '''
    city = City(name=name)
    city.save()


def query_city():
    ''' Queries List

    Notes:
        This method lists the objects in the City table,
        showing their name and ID.
    '''
    cities = City.query.all()
    for city in cities:
        print(city.name, city.id)


if __name__ == '__main__':
    # insert_city(name='Fortaleza')
    # insert_city(name='Maracanaú')
    # city = City.query.filter_by(name='Seattle').first()
    # city.delete()
    # init_db()
    query_city()
