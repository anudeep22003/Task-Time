from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Boolean, null
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, registry, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import date
from enum_factory import Status

engine = create_engine("sqlite:///src/alchemy_test/alchemic_activity.db")
Session = sessionmaker(bind=engine)
session = Session()

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Activity(Base):
    __tablename__ = "activity"
    id = Column(Integer, primary_key=True)
    created_by = Column(String)
    activity = Column(String)
    time_allocated = Column(Time)
    status = Column(String)
    date_created = Column(Date)
    parent_id = Column(Integer)
    alive = Column(Boolean, default=True)
    activity_details = relationship(
        "ActivityDetails", uselist=False, back_populates="activity"
    )

    def __init__(
        self,
        activity,
        time_allocated,
        parent_id = None,
        status: Status = Status.NOT_STARTED,
        date_created=date.today(),
        alive=True,
        created_by="Anudeep",
    ) -> None:

        self.created_by = created_by
        self.activity = activity
        self.time_allocated = time_allocated
        self.status = status
        self.date_created = date_created
        self.parent_id = parent_id
        self.alive = alive
    

        def add_details(self):
            pass


class ActivityDetails(Base):
    __tablename__ = "activity_details"

    activity_id = Column(Integer, ForeignKey("activity.id"), primary_key=True)
    context = Column(String)
    category = Column(String)
    notes = Column(String)
    time_used = Column(Time)
    time_difference = Column(Time)
    num_edits = Column(Integer)
    alive = Column(Boolean)
    alive = relationship("ActivityDetails",back_populates=)
    activity = relationship("Activity", back_populates="activity_details")

    def __init__(
        self,
        activity_id,
        context = None,
        category = None,
        notes =  None,
        time_used = 0,
        time_difference = None,
        num_edits = 0,
        # alive = ,
    ) -> None:
        
        self.activity_id = activity_id
        self.context = context
        self.category = category
        self.notes = notes
        self.time_used = time_used
        self.time_difference = time_difference
        self.num_edits = num_edits
        # self.alive = alive


Base.metadata.create_all(bind=engine)

# if __name__ == "__main__":
a = Activity("Hello", 20)
b = Activity("World", 45)
b_d = ActivityDetails(a.id, context="Big details")
session.add(a)
session.add(b)
session.add(b_d)
session.commit()
session.close()
    
#! learn how to implement a cascade relationship
#! learn how to create an entry in the details table if a value in main table is created.