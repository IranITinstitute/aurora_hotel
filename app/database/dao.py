from sqlalchemy import or_, desc, func, and_
from sqlalchemy.sql import column
from .models import engine, Client, Booking, Room, Employee, LoyaltyProgram, Service, ServiceOrder, Payment, Review, Complaint
from .schemas import ClientBase
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import json







def get_rooms_with_bookings():
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        booked_rooms = db.query(Room, Booking, Client)\
            .join(Booking, Room.id == Booking.room_id)\
            .join(Client, Booking.client_id == Client.id)\
            .filter(Room.status == 'booked')\
            .order_by(Room.id)\
            .all()
        
        for room, booking, client in booked_rooms:
            booking_dict = booking.to_dict()
            booking_dict["days"] = abs((datetime.strptime(booking_dict["out_date"], "%d-%m-%Y").date() - datetime.strptime(booking_dict["in_date"], "%d-%m-%Y").date()).days)
            
            # Получаем услуги клиента
            client_services = db.query(ServiceOrder, Service)\
                .join(Service, ServiceOrder.service_id == Service.id)\
                .filter(ServiceOrder.client_id == client.id)\
                .all()
            
            # Извлекаем названия услуг
            service_names = [service.name for service_order, service in client_services]
            
            # Получаем платежи по booking_id
            booking_payments = db.query(Payment)\
                .filter(Payment.booking_id == booking.id)\
                .all()
            
            # Преобразуем платежи в словари
            payments_list = [payment.to_dict() for payment in booking_payments]
            
            return_list.append({
                "room": room.to_dict(),
                "booking": booking_dict,
                "client": client.to_dict(),
                "services": service_names,
                "payments": payments_list
            })

        return [return_list, json.dumps(return_list)]


def get_promos():
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        promos = db.query(LoyaltyProgram).order_by(LoyaltyProgram.id).all()
        
        for promo in promos:
            
            return_list.append(promo.to_dict())

        return return_list


def get_rooms():
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        rooms = db.query(Room).order_by(Room.id).all()
        
        for room in rooms:
            
            return_list.append(room.to_dict())

        return return_list


def get_bookings():
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        bookings = db.query(Booking).order_by(Booking.id).all()
        
        for booking in bookings:
            
            return_list.append(booking.to_dict())

        return return_list


def get_available_rooms(start_date, end_date):
    with Session(autoflush=False, bind=engine) as db:
        dstart_date = datetime.strptime(start_date, "%d.%m.%Y").date()
        dend_date = datetime.strptime(end_date, "%d.%m.%Y").date()

        return_list = []
        rooms = db.query(Room).order_by(Room.id).all()
       
        for room in rooms:
            if check_room_availability(room.id, start_date, end_date)["available"] == True:
                return_list.append(room.to_dict())

        return [return_list, json.dumps(return_list)]

def check_room_availability(room_id, start_date, end_date):
    with Session(autoflush=False, bind=engine) as db:
        start_date = datetime.strptime(start_date, "%d.%m.%Y").date()
        end_date = datetime.strptime(end_date, "%d.%m.%Y").date()

        # Запрос для поиска пересечений с другими бронированиями
        bookings = db.query(Booking).filter(
            Booking.room_id == room_id,
            Booking.in_date <= end_date,
            Booking.out_date >= start_date
        ).all()

        if bookings:
            return {"room_id": room_id, "available": False}  # Номер занят
        return {"room_id": room_id, "available": True}  # Номер свободен


def add_booking(in_date, name, out_date, phone, room, day_price, bornDate, mail, passNum, paymentType, services, countedPrice):
    with Session(autoflush=False, bind=engine) as db:
        # Преобразуем строки в datetime
        try:
            check_in_date = datetime.strptime(in_date, "%d.%m.%Y").date()
            check_out_date = datetime.strptime(out_date, "%d.%m.%Y").date()
        except ValueError:
            print(123)
        
        # Проверяем, свободен ли номер в указанный период
        existing_booking = db.query(Booking).filter(
            Booking.room_id == room,
            Booking.in_date <= check_out_date,
            Booking.out_date >= check_in_date
        ).first()

        hotel_room = db.query(Room).filter(Room.id == room).first()
        hotel_room.status = 'booked'

        if existing_booking:
            raise HTTPException(status_code=400, detail="The room is already booked in the given dates.")

        try:
            # Пытаемся найти клиента
            client = db.query(Client).filter(Client.phone == str(phone)).first()
        except SQLAlchemyError as e:
            # Обрабатываем ошибки запроса к БД
            db.rollback()
            print(f"Ошибка при поиске клиента: {e}")
            client = None

        if not client:
            # Если клиент не найден, создаем нового
            try:
                new_client = Client(phone=phone, full_name=name, email=mail, pass_num=passNum, born_date=datetime.strptime(bornDate, "%d.%m.%Y").date())
                db.add(new_client)
                db.commit()  # Фиксируем транзакцию
                client = new_client  # Используем созданный объект
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Ошибка при создании клиента: {e}")
                # Можно выбросить исключение или вернуть ошибку
                
        print(services)
        if services:
            for i in range(0, len(services)):
                new_service_order = ServiceOrder(
                    client_id = client.id,
                    service_id = services[i],
                    order_date = check_in_date,
                    price = db.query(Service).filter(Service.id == services[i]).first().price
                )
                db.add(new_service_order)
                db.commit()
        

              
        
        new_booking = Booking(
            client_id=client.id,
            room_id=room,
            in_date=in_date,
            out_date=out_date,
            price=countedPrice,
            status="booked"
        )
        db.add(new_booking)
        db.commit()

        new_payment = Payment(
            booking_id = new_booking.id,
            price = countedPrice,
            payment_date = datetime.now(),
            pay_type = paymentType
        )
        db.add(new_payment)
        db.commit()

        return {"message": "Room successfully booked."}



def booking_cancel(booking_id):
    with Session(autoflush=False, bind=engine) as db:
        try:
            # Получаем бронирование
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                raise ValueError("Бронирование не найдено")

            # Получаем клиента из бронирования
            client_id = booking.client_id
            
            # Удаляем все услуги клиента
            db.query(ServiceOrder).filter(ServiceOrder.client_id == client_id).delete()

            # Обновляем статус комнаты
            room = db.query(Room).filter(Room.id == booking.room_id).first()
            if room:
                room.status = "available"

            # Удаляем само бронирование
            db.delete(booking)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise e

        

def add_client():
    with Session(autoflush=False, bind=engine) as db:
        client = Client(full_name="NewUser", 
                        phone=79)
        db.add(client)
        db.commit()
        client = db.query(Client).filter(Client.full_name == "NewUser").first()
        return {"userId": client.id}
        

def delete_client(user_id):
    with Session(autoflush=False, bind=engine) as db:
        client = db.query(Client).filter(Client.id == user_id).first()
        db.delete(client)
        db.commit()

def edit_client(client_dict):
    with Session(autoflush=False, bind=engine) as db:
        edit_data = client_dict.model_dump(exclude_none=True)
        client = db.query(Client).filter(Client.id == edit_data["userId"]).first()
        match list(edit_data.keys())[0]:
            case "full_name":
                client.full_name = edit_data[list(edit_data.keys())[0]]
                db.commit()

            case "phone":
                client.phone = edit_data[list(edit_data.keys())[0]]
                db.commit()

            case "email":
                client.email = edit_data[list(edit_data.keys())[0]]
                db.commit()
                
            case "pass_num":
                client.pass_num = edit_data[list(edit_data.keys())[0]]
                db.commit()

            case "born_date":
                client.born_date = edit_data[list(edit_data.keys())[0]]
                db.commit()

def get_clients():
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        clients = db.query(Client).order_by(Client.id).all()
        for client in clients:
            return_list.append(client.to_dict())

        return return_list



def add_promo():
    with Session(autoflush=False, bind=engine) as db:
        promo = LoyaltyProgram(name="Z00YH", discount=0)
        db.add(promo)
        db.commit()
        return {"promoId": True}


def delete_promo(promo_id):
    with Session(autoflush=False, bind=engine) as db:
        promo = db.query(LoyaltyProgram).filter(LoyaltyProgram.id == promo_id).first()
        db.delete(promo)
        db.commit()


def edit_promo(promo_dict):
    with Session(autoflush=False, bind=engine) as db:
        edit_data = promo_dict.model_dump(exclude_none=True)
        print(edit_data)
        promo = db.query(LoyaltyProgram).filter(LoyaltyProgram.id == edit_data["promoId"]).first()
        print(promo.id)
        match list(edit_data.keys())[1]:
            case "name":
                promo.name = edit_data[list(edit_data.keys())[1]]
                db.commit()

            case "discount":
                promo.discount = edit_data[list(edit_data.keys())[1]]
                db.commit()

def check_promo(promo_name):
    with Session(autoflush=False, bind=engine) as db:
        try:
            promo = db.query(LoyaltyProgram).filter(LoyaltyProgram.name == promo_name).first()
            return {"discount": promo.discount}
        except:
            return {"discount": "NotFound"}
        



def add_service():
    with Session(autoflush=False, bind=engine) as db:
        service = Service(name="None", description="None", price=0)
        db.add(service)
        db.commit()
        return {"serviceId": True}


def delete_service(promo_id):
    with Session(autoflush=False, bind=engine) as db:
        service = db.query(Service).filter(Service.id == service_id).first()
        db.delete(service)
        db.commit()


def edit_service(service_dict):
    with Session(autoflush=False, bind=engine) as db:
        edit_data = service_dict.model_dump(exclude_none=True)
        service = db.query(Service).filter(Service.id == edit_data["serviceId"]).first()
        print(edit_data)
        match list(edit_data.keys())[1]:
            case "name":
                service.name = edit_data[list(edit_data.keys())[1]]
                db.commit()

            case "description":
                service.description = edit_data[list(edit_data.keys())[1]]
                db.commit()

            case "price":
                service.price = edit_data[list(edit_data.keys())[1]]
                db.commit()


def add_complaint(username, description):
    with Session(autoflush=False, bind=engine) as db:
        # Поиск существующего клиента
        client = db.query(Client).filter(
            Client.full_name == username
        ).first()

        # Создание нового клиента если не найден
        if not client:
            client = Client(
                full_name=username,
                phone=79,
                pass_num="00 00 000000",
                born_date=None,
                email=None
            )
            db.add(client)
            try:
                db.commit()
                db.refresh(client)
            except Exception as e:
                db.rollback()
                raise ValueError("Ошибка при создании клиента")

        # Создание жалобы
        new_complaint = Complaint(
            client_id=client.id,
            description=description,
            status="новое",
            complain_date=datetime.now()
        )
        
        db.add(new_complaint)
        try:
            db.commit()
            db.refresh(new_complaint)
        except Exception as e:
            db.rollback()
            raise ValueError("Ошибка при создании жалобы")

        return new_complaint


def get_complaints():
    print(123)
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        complaints = db.query(Complaint).order_by(Complaint.id).all()
        for complaint in complaints:
            return_list.append(complaint.to_dict())
        print(return_list)
        return return_list


def get_service_orders():
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        # Делаем join с необходимыми таблицами
        query = db.query(
            ServiceOrder,
            Client.full_name,
            Service.name,
            Room.room_num
        ).join(
            Client, ServiceOrder.client_id == Client.id
        ).join(
            Service, ServiceOrder.service_id == Service.id
        ).join(
            Booking, Client.id == Booking.client_id
        ).join(
            Room, Booking.room_id == Room.id
        ).order_by(ServiceOrder.id)
        
        for service_order, client_name, service_name, room_num in query:
            order_dict = service_order.to_dict()
            order_dict.update({
                "client_name": client_name,
                "service_name": service_name,
                "room_number": room_num
            })
            return_list.append(order_dict)

        return return_list




def get_reviews(limit):
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        
        # Получаем отзывы
        if limit > 0:
            reviews = db.query(Review).order_by(Review.id).limit(limit).all()
        else:
            reviews = db.query(Review).order_by(Review.id).all()
        
        # Обрабатываем каждый отзыв
        for review in reviews:
            review_dict = review.to_dict()
            
            # Находим клиента
            client = db.query(Client).filter(Client.id == review.client_id).first()
            username = client.full_name if client else "Неизвестный пользователь"
            
            review_dict["username"] = username
            return_list.append(review_dict)

        return return_list






def add_review(username, email, grade, comment):
    with Session(autoflush=False, bind=engine) as db:
    
        # Ищем существующего клиента
        client = db.query(Client).filter(
            (Client.full_name == username) | 
            (Client.email == email)
        ).first()

        # Если клиент не найден - создаем нового
        if not client:
            client = Client(
                full_name=username,
                email=email,
                phone='НЕ УКАЗАН',  # Обязательное поле
                pass_num='НЕ УКАЗАН',  # Обязательное поле для примера
                born_date=datetime.now().date()  # Заглушка для обязательного поля
            )
            db.add(client)
            db.commit()
            db.refresh(client)

        # Получаем последнюю активную бронь клиента для room_id
        last_booking = db.query(Booking).filter(
            Booking.client_id == client.id,
            Booking.status == 'active'
        ).order_by(Booking.id.desc()).first()

        if not last_booking:
            # Создаем отзыв
            new_review = Review(
                client_id=client.id,
                room_id=None,
                grade=grade,
                comment=comment,
                created_at=func.now()
            )

        else:
            # Создаем отзыв
            new_review = Review(
                client_id=client.id,
                room_id=last_booking.room_id,
                grade=grade,
                comment=comment,
                created_at=func.now()
            )
        
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        
        return new_review.to_dict()

       
        






def get_available_services():
    with Session(autoflush=False, bind=engine) as db:
        return_list = []
        services = db.query(Service).order_by(Service.id).all()
        for service in services:
            return_list.append(service.to_dict())

        return return_list














def get_employee_by_email(email: str):
    with Session(autoflush=False, bind=engine) as db:
        employee = db.query(Employee)\
            .filter(Employee.email == email)\
            .first()
        return employee
        

