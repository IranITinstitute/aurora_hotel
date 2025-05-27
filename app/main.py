from typing import Union

from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database.dao import delete_review, get_reviews, delete_complaint, get_complaints, add_complaint, add_review, get_reviews, get_service_orders, delete_service, add_service, edit_service, get_available_services, check_promo, edit_promo, add_promo, delete_promo, get_promos, get_employee_by_email, get_clients, delete_client, add_client, edit_client, check_room_availability, get_available_rooms, get_bookings, get_rooms_with_bookings, add_booking, booking_cancel
import app.database.schemas as ps
from passlib.context import CryptContext
import secrets

app = FastAPI()

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SESSION_COOKIE_NAME = "session_token"
active_sessions = set()

app.mount("/web/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

async def get_current_user(request: Request):
    session_token = request.cookies.get(SESSION_COOKIE_NAME)
    if session_token not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Not authenticated",
            headers={"Location": "/login"}
        )
    return True

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def perform_login(request: Request):
    form_data = await request.form()
    email = form_data.get("email")
    password = form_data.get("password")
    
    employee = get_employee_by_email(email)
    
    # Прямое сравнение паролей без хэширования
    if not employee or password != employee.password:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Неверный email или пароль"
        })
    
    session_token = secrets.token_urlsafe(32)
    active_sessions.add(session_token)
    
    response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_token,
        httponly=True,
        max_age=852369
    )
    return response

@app.get("/logout")
async def logout(request: Request):
    session_token = request.cookies.get(SESSION_COOKIE_NAME)
    if session_token in active_sessions:
        active_sessions.remove(session_token)
    
    response = RedirectResponse(url="/login")
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response



"""
	MAIN ROUTER
"""

@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
	return templates.TemplateResponse(
		request=request, name="index.html", context={"reviews": get_reviews(2)}
	)

@app.get("/rooms", response_class=HTMLResponse)
async def rooms_page(request: Request):
	return templates.TemplateResponse(
		request=request, name="rooms.html", context={"hello": "world"}
	)


@app.get("/booking", response_class=HTMLResponse)
async def booking_page(request: Request, start_date: str, end_date:str):
	return templates.TemplateResponse(
		request=request, name="booking.html", context={"available_rooms": get_available_rooms(start_date, end_date)}
	)


@app.get("/reviews", response_class=HTMLResponse)
async def reviews_page(request: Request):
	return templates.TemplateResponse(
		request=request, name="reviews.html", context={"reviews": get_reviews(0)}
	)



@app.post("/reviews")
async def route_add_review(
        username: str = Form(...),
        email: str = Form(...),
        grade: int = Form(...),
        comment: str = Form(...)
    ):
    add_review(username, email, grade, comment)

    return RedirectResponse(url="/reviews", status_code=303)

@app.post("/complaint")
async def route_add_complaint(
    complaint_username: str = Form(..., alias="complaint-username"),
    complaint_description: str = Form(..., alias="complaint-description")
    ):
    add_complaint(complaint_username, complaint_description)
    return RedirectResponse(url="/", status_code=303)



"""
	API ROUTER
"""

@app.post("/api/booking")
async def route_add_booking(booking_data: ps.BookingCreateRequest):
    return add_booking(
        in_date = booking_data.in_date,
        name = booking_data.name,
        out_date = booking_data.out_date,
        phone = booking_data.phone,
        room = booking_data.room,
        day_price = booking_data.day_price,
        bornDate = booking_data.bornDate,
        mail = booking_data.mail,
        passNum = booking_data.passNum,
        paymentType = booking_data.paymentType,
        services = booking_data.services,
        countedPrice = booking_data.countedPrice
        )


@app.post("/api/booking_cancel")
async def route_booking_cancel(booking_id: int):
    return booking_cancel(booking_id)



@app.get("/api/clients")
async def route_get_client(request: Request):
	return get_clients()


@app.post("/api/deleteClient")
async def route_delete_client(user_id: int):
	return delete_client(user_id)

@app.post("/api/addClient")
async def route_addClient(request: Request):
	return add_client()

@app.post("/api/editClient")
async def route_editClient(client_data: ps.ClientUpdate):
	return edit_client(client_data)






@app.post("/api/deletePromo")
async def route_delete_promo(promo_id: int):
	return delete_promo(promo_id)



@app.post("/api/deleteComplaint")
async def route_delete_complaint(complaint_id: int):
	return delete_complaint(complaint_id)


@app.post("/api/addPromo")
async def route_addPromo(request: Request):
	return add_promo()

@app.post("/api/editPromo")
async def route_editPromo(promo_data: ps.PromoUpdate):
	return edit_promo(promo_data)

@app.post("/api/checkPromo")
async def route_check_client(promo_name: str):
	return check_promo(promo_name)





@app.get("/api/getAvailableServices")
async def route_get_available_services(request: Request):
    return get_available_services()

@app.post("/api/deleteService")
async def route_delete_Service(service_id: int):
	return delete_service(service_id)


@app.post("/api/deleteReview")
async def route_delete_Service(review_id: int):
	return delete_review(review_id)   


@app.post("/api/addService")
async def route_addService(request: Request):
	return add_service()

@app.post("/api/editService")
async def route_editService(service_data: ps.ServiceUpdate):
	return edit_service(service_data)






@app.get("/api/check_room_availability")
async def route_check_room_availability(room_id: int, start_date: str, end_date: str):
	return check_room_availability(room_id, start_date, end_date)


"""
	ADMIN ROUTER
"""

@app.get("/admin")
async def admin_index_page(request: Request, auth: bool = Depends(get_current_user)):
	return RedirectResponse(url="/admin/bookings", status_code=303)


@app.get("/admin/clients", response_class=HTMLResponse)
async def clients_page(request: Request, auth: bool = Depends(get_current_user)):
	return templates.TemplateResponse(
		request=request, name="admin_clients.html", context={"clients": get_clients()}
	)

@app.get("/admin/promo", response_class=HTMLResponse)
async def promos_page(request: Request, auth: bool = Depends(get_current_user)):
	return templates.TemplateResponse(
		request=request, name="admin_promo.html", context={"promos": get_promos()}
	)

@app.get("/admin/complaints", response_class=HTMLResponse)
async def promos_page(request: Request, auth: bool = Depends(get_current_user)):
	return templates.TemplateResponse(
		request=request, name="admin_complaints.html", context={"complaints": get_complaints(), "reviews": get_reviews(0)}
	)

@app.get("/admin/services", response_class=HTMLResponse)
async def promos_page(request: Request, auth: bool = Depends(get_current_user)):
	return templates.TemplateResponse(
		request=request, name="admin_services.html", context={"services": get_available_services(), "serviceOrders": get_service_orders()}
	)

@app.get("/admin/bookings", response_class=HTMLResponse)
async def clients_page(request: Request, auth: bool = Depends(get_current_user)):
	return templates.TemplateResponse(
		request=request, name="admin_bookings.html", context={"rooms": get_rooms_with_bookings()}
	)


