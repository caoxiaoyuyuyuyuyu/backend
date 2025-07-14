from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class UserCreateDTO(BaseModel):
    """用户创建DTO"""
    openid: str = Field(..., min_length=1, max_length=64, description="微信openid")
    unionid: Optional[str] = Field(None, max_length=64, description="微信unionid")
    nickname: Optional[str] = Field(None, max_length=64, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[int] = Field(0, ge=0, le=2, description="0未知 1男 2女")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")

    @validator('phone')
    def validate_phone(cls, v):
        if v and not v.isdigit():
            raise ValueError('手机号必须为数字')
        return v

class UserUpdateDTO(BaseModel):
    """用户更新DTO"""
    nickname: Optional[str] = Field(None, max_length=64, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    status: Optional[int] = Field(None, ge=0, le=1, description="0禁用 1正常")

class UserResponseDTO(BaseModel):
    """用户响应DTO"""
    id: int
    nickname: Optional[str]
    avatar: Optional[str]
    gender: Optional[int]
    country: Optional[str]
    province: Optional[str]
    city: Optional[str]
    status: int
    created_at: datetime
    last_login: Optional[datetime]
    login_count: int

    class Config:
        orm_mode = True