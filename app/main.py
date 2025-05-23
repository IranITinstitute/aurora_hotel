from typing import Union

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database.dao import check_promo, edit_promo, add_promo, delete_promo, get_promos, get_employee_by_email, get_clients, delete_client, add_client, edit_client, check_room_availability, get_available_rooms, get_bookings, get_rooms_with_bookings, add_booking, booking_cancel
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
		request=request, name="index.html", context={"hello": "world"}
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
async def route_delete_client(promo_id: int):
	return delete_promo(promo_id)

@app.post("/api/addPromo")
async def route_addPromo(request: Request):
	return add_promo()

@app.post("/api/editPromo")
async def route_editPromo(promo_data: ps.PromoUpdate):
	return edit_promo(promo_data)

@app.post("/api/checkPromo")
async def route_check_client(promo_name: str):
	return check_promo(promo_name)






@app.get("/api/check_room_availability")
async def route_check_room_availability(room_id: int, start_date: str, end_date: str):
	return check_room_availability(room_id, start_date, end_date)


"""
	ADMIN ROUTER
"""

@app.get("/admin", response_class=HTMLResponse)
async def admin_index_page(request: Request, auth: bool = Depends(get_current_user)):
	return templates.TemplateResponse(
		request=request, name="admin_index.html", context={"hello": "world"}
	)


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

@app.get("/admin/bookings", response_class=HTMLResponse)
async def clients_page(request: Request, auth: bool = Depends(get_current_user)):
	return templates.TemplateResponse(
		request=request, name="admin_bookings.html", context={"rooms": get_rooms_with_bookings()}
	)


