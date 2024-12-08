# services/user_services.py
import os
import logging
import bcrypt  # type: ignore
import jwt
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from model.user_model import User
from pydantic import BaseModel
from model.utils_model import get_db_connection
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "Android@123")
JWT_EXPIRATION_TIME = 60

router = APIRouter()

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signin")
def sign_in(sign_in_request: SignInRequest):
    email = sign_in_request.email
    password = sign_in_request.password

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT id, employeeId, username, email, birthday, password, created_at, updated_at, deleted_at 
            FROM aslan_users 
            WHERE email = %s
        ''', (email,))
        user_row = cursor.fetchone()

        if not user_row:
            return JSONResponse(status_code=401, content={"statusCode": 401, "body": "Unauthorized"})

        stored_password_hash = user_row[5]
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            return JSONResponse(status_code=401, content={"statusCode": 401, "body": "Unauthorized"})

        payload = {
            "sub": user_row[0],  # User ID
            "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        user_info = {
            "id": user_row[0],
            "employeeId": user_row[1],
            "username": user_row[2],
            "email": user_row[3],
            "birthday": user_row[4].strftime('%Y-%m-%d') if user_row[4] else None,
            "created_at": user_row[6].strftime('%Y-%m-%d %H:%M:%S') if user_row[6] else None,
            "updated_at": user_row[7].strftime('%Y-%m-%d %H:%M:%S') if user_row[7] else None,
            "deleted_at": user_row[8].strftime('%Y-%m-%d %H:%M:%S') if user_row[8] else None,
            "token": token
        }

        return JSONResponse(status_code=200, content={"statusCode": 200, "body": user_info})

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    finally:
        cursor.close()
        conn.close()


@router.post("/signout")
def sign_out():
    return JSONResponse(status_code=200, content={"statusCode": 200, "body": "Signed out successfully"})


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    birthday: str

@router.post("/register")
def register(register_request: RegisterRequest):
    email = register_request.email
    username = register_request.username
    password = register_request.password
    birthday = register_request.birthday

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO aslan_users (email, username, password, birthday) 
            VALUES (%s, %s, %s, %s) RETURNING id, employeeId, username, email, birthday, created_at, updated_at, deleted_at
        ''', (email, username, hashed_password, birthday))

        user = cursor.fetchone()
        conn.commit()

        user_info = {
            "id": user[0],
            "employeeId": user[1],
            "username": user[2],
            "email": user[3],
            "birthday": user[4].strftime('%Y-%m-%d') if user[4] else None,
            "created_at": user[5].strftime('%Y-%m-%d %H:%M:%S') if user[5] else None,
            "updated_at": user[6].strftime('%Y-%m-%d %H:%M:%S') if user[6] else None,
            "deleted_at": user[7].strftime('%Y-%m-%d %H:%M:%S') if user[7] else None,
        }

        return JSONResponse(status_code=200, content={
            "statusCode": 200,
            "body": "Registered successfully",
            "user": user_info
        })

    except Exception as e:
        conn.rollback()
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Something went wrong")

    finally:
        cursor.close()
        conn.close()
