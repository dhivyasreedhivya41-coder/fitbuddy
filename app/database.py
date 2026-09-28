from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)


class WorkoutPlan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    original_plan = Column(Text)
    updated_plan = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)


def save_user(user_id, name, age, weight, goal, intensity):
    db = SessionLocal()
    existing = db.query(User).filter_by(id=user_id).first()
    if existing:
        existing.name = name
        existing.age = age
        existing.weight = weight
        existing.goal = goal
        existing.intensity = intensity
    else:
        db.add(User(id=user_id, name=name, age=age, weight=weight,
                    goal=goal, intensity=intensity))
    db.commit()
    db.close()


def save_plan(user_id, plan):
    db = SessionLocal()
    db.add(WorkoutPlan(user_id=user_id, original_plan=plan))
    db.commit()
    db.close()


def update_plan(user_id, updated_text):
    db = SessionLocal()
    workout = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
    if workout:
        workout.updated_plan = updated_text
        db.commit()
    db.close()
def get_original_plan(user_id):
    db = SessionLocal()
    plan = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
    result = plan.original_plan if plan else None
    db.close()
    return result