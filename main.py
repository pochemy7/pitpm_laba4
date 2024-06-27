from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Создание объекта FastAPI
app = FastAPI()

# Настройка базы данных MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_p_Shilov:12345@77.91.86.135/isp_p_Shilov"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели SQLAlchemy для пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True) 
    email = Column(String(100), unique=True, index=True) 

class Doctor(Base):
    __tablename__ = "Doctor"

    id = Column(Integer, primary_key=True, index=True)
    doctorId = Column(int(100), unique=True, index=True)#код врача
    name = Column(String(50), index=True) 
    numberLicense = Column(int(100), unique=True, index=True)  
    dateOfBirth = Column(int(12), index=True)
    phoneNumber = Column(int(13), index=True, unique=True)

class Specialization(Base):
    __tablename__ = "Specialization"

    id = Column(Integer, primary_key=True, index=True)
    SpecializationID = Column(int(100), unique=True, index=True)
    nameSpecialization = Column(String(50), index=True)  

class ConsultationTimeTable(Base):
    __tablename__ = "ConsultationTimeTable"

    id = Column(Integer, primary_key=True, index=True)
    doctorId = Column(String(50), index=True)  
    specializationID = Column(int(10), index=True)
    patientID = Column(int(100), index=True)
    dateOfConsultation = Column(int(12), index=True)

class AppointmentTimeTable(Base):
    __tablename__ = "AppointmentTimeTableTimeTable"

    id = Column(Integer, primary_key=True, index=True)
    doctorId = Column(String(50), index=True)
    dateOfAppointment = Column(int(12), index=True)
    timeOfAppointment = Column(int(1), index=True)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Определение Pydantic модели для пользователя
class UserCreate(BaseModel):
    name: str
    email: str

class DoctorCreate(BaseModel):
    doctorId: int
    name: str
    numberLicense: int
    dateOfBirth: int
    phoneNumber: int

class Specialization(BaseModel):
    SpecializationID: int
    nameSpecialization: str

class AppointmentTimeTableCreate(BaseModel):
    doctorId: int
    dateOfAppointment: int
    timeOfAppointment: int

class ConsultationTimeTableCreate(BaseModel):
    doctorId: str
    specializationID: int
    patientID: int
    dateOfConsultation: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Маршрут для получения пользователя по ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Маршрут для создания нового пользователя
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
