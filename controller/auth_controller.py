from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from model.exception_handler_model.seller_exception import SellerException
from model.seller import Seller, SellerStatus
from security.auth import (
    Principal,
    ROLE_ADMIN,
    ROLE_SELLER,
    create_access_token,
    get_current_principal,
    is_admin,
)
from service import seller_service

router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    seller_id: int
    email: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    seller_id: int
    seller_name: str
    role: str


class RegisterRequest(BaseModel):
    seller_name: str
    email: str
    status: Optional[str] = "active"


class MeResponse(BaseModel):
    principal_id: int
    role: str


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(login_request: LoginRequest) -> LoginResponse:
    result: Union[Seller, SellerException] = await seller_service.get_seller_by_id(login_request.seller_id)

    if isinstance(result, SellerException):
        raise HTTPException(status_code=401, detail="Invalid seller id or email")

    if result.email.strip().lower() != login_request.email.strip().lower():
        raise HTTPException(status_code=401, detail="Invalid seller id or email")

    role = ROLE_ADMIN if is_admin(result.seller_id, result.email) else ROLE_SELLER

    token = create_access_token(result.seller_id, role)

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        seller_id=result.seller_id,
        seller_name=result.seller_name,
        role=role,
    )


@router.get("/me", response_model=MeResponse, status_code=200)
async def me(principal: Principal = Depends(get_current_principal)) -> MeResponse:
    return MeResponse(principal_id=principal.principal_id, role=principal.role)


@router.post("/register", response_model=LoginResponse, status_code=201)
async def register(register_request: RegisterRequest) -> LoginResponse:
    existing: Union[Seller, SellerException] = await seller_service.get_seller_by_email(register_request.email)
    if not isinstance(existing, SellerException):
        raise HTTPException(status_code=409, detail="A seller with this email already exists")

    try:
        status = SellerStatus(register_request.status or "active")
    except ValueError:
        status = SellerStatus.ACTIVE

    new_seller = Seller(
        seller_name=register_request.seller_name,
        email=register_request.email,
        status=status,
    )

    await seller_service.create_seller(new_seller)

    created: Union[Seller, SellerException] = await seller_service.get_seller_by_email(register_request.email)
    if isinstance(created, SellerException):
        raise HTTPException(status_code=500, detail="Registration failed")

    role = ROLE_ADMIN if is_admin(created.seller_id, created.email) else ROLE_SELLER
    token = create_access_token(created.seller_id, role)

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        seller_id=created.seller_id,
        seller_name=created.seller_name,
        role=role,
    )
