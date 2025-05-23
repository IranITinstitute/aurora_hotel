from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP, create_engine, SmallInteger, DateTime, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:root@localhost:5432/aurora_db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()
Base.metadata.create_all(engine)


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    full_name = Column(Text, nullable=False)
    phone = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    pass_num = Column(String(255), nullable=True)
    born_date = Column(Date, nullable=True)
    reg_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    bookings = relationship("Booking", back_populates="client")

    def to_dict(self):
        """Сериализация клиента в словарь с нужными форматами дат"""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "phone": self.phone,
            "email": self.email,
            "pass_num": self.pass_num,
            "born_date": self.born_date.strftime('%d-%m-%Y') if self.born_date else None,
            "reg_date": self.reg_date.strftime('%m-%d-%Y %H:%M') if self.reg_date else None
        }

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_num = Column(Integer, nullable=False)
    room_type = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    square = Column(Integer, nullable=False)
    descr = Column(Text, nullable=False)
    room_name = Column(Text, nullable=False)
    bookings = relationship("Booking", back_populates="room")

    def to_dict(self):
        return {
            "ID": self.id,
            "room_num": self.room_num,
            "room_type": self.room_type,
            "price": self.price,
            "capacity": self.capacity,
            "status": self.status,
            "square": self.square,
            "descr": self.descr,
            "room_name": self.room_name
        }

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    phone_num = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    salary = Column(Integer, nullable=False)
    password = Column(String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "job_title": self.job_title,
            "phone_num": self.phone_num,
            "email": self.email,
            "salary": self.salary,
            "password": self.password
        }

class LoyaltyProgram(Base):
    __tablename__ = 'loyalty_program'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    discount = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "discount": self.discount
        }

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }

class Booking(Base):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    in_date = Column(Date, nullable=False)
    out_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    room = relationship("Room", back_populates="bookings")
    client = relationship("Client", back_populates="bookings")

    def to_dict(self):
        return {
            "ID": self.id,
            "client_id": self.client_id,
            "room": self.room_id,
            "in_date": self.in_date.strftime('%d-%m-%Y') if self.in_date else None,
            "out_date": self.out_date.strftime('%d-%m-%Y') if self.out_date else None,
            "price": self.price,
            "status": self.status
        }

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.id', ondelete='CASCADE'), nullable=False)
    price = Column(Integer, nullable=False)
    payment_date = Column(TIMESTAMP(timezone=True), nullable=False)
    pay_type = Column(String(50))

    def to_dict(self):
        return {
            "ID": self.ID,
            "booking": self.booking,
            "price": self.price,
            "payment_date": self.payment_date.strftime('%m-%d-%Y %H:%M') if self.payment_date else None,
            "pay_type": self.pay_type
        }

class LoginHistory(Base):
    __tablename__ = 'login_history'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    login_time = Column(TIMESTAMP(timezone=True), nullable=False)

    def to_dict(self):
        return {
            "ID": self.ID,
            "client_id": self.client_id,
            "login_time": self.login_time.strftime('%m-%d-%Y %H:%M') if self.login_time else None
        }

class Complaint(Base):
    __tablename__ = 'complaints'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    complain_date = Column(TIMESTAMP(timezone=True), nullable=False)

    def to_dict(self):
        return {
            "ID": self.ID,
            "client_id": self.client_id,
            "description": self.description,
            "status": self.status,
            "complain_date": self.complain_date.strftime('%m-%d-%Y %H:%M') if self.complain_date else None
        }

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    grade = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    def to_dict(self):
        return {
            "ID": self.ID,
            "client_id": self.client_id,
            "room": self.room,
            "grade": self.grade,
            "comment": self.comment,
            "date": self.date.strftime('%d-%m-%Y') if self.date else None
        }

class RoomService(Base):
    __tablename__ = 'room_service'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    service_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=False)

    def to_dict(self):
        return {
            "ID": self.ID,
            "room": self.room,
            "employee": self.employee,
            "service_date": self.service_date.strftime('%d-%m-%Y') if self.service_date else None,
            "notes": self.notes
        }

class ServiceOrder(Base):
    __tablename__ = 'services_orders'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE'), nullable=False)
    order_date = Column(TIMESTAMP(timezone=True), nullable=False)
    price = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "ID": self.ID,
            "client_id": self.client_id,
            "service": self.service,
            "order_date": self.order_date.strftime('%m-%d-%Y %H:%M') if self.order_date else None,
            "price": self.price
        }

class UserInLP(Base):
    __tablename__ = 'user_in_lp'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    loyalty_program_id = Column(Integer, ForeignKey('loyalty_program.id', ondelete='CASCADE'), nullable=False)
    start_date = Column(Date, nullable=False)

    def to_dict(self):
        return {
            "ID": self.ID,
            "client_id": self.client_id,
            "loyality_program": self.loyality_program,
            "start_date": self.start_date.strftime('%d-%m-%Y') if self.start_date else None
        }