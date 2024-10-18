from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base

DB_NAME = "weather_db.sqlite"

engine = create_engine(f'sqlite:///{DB_NAME}', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    temperature = Column(Integer)
    precipitation = Column(Integer)
    pressure = Column(Integer)
    wind_speed = Column(Integer)
    wind_direction = Column(String)

    @classmethod
    def get_data(cls):
        session = Session()
        data = session.query(cls).order_by(cls.id.desc()).limit(10)
        session.close()
        result = [(item.temperature, item.precipitation, item.pressure, item.wind_speed, item.wind_direction) for item
                  in data[::-1]]
        return result


Base.metadata.create_all(bind=engine)
