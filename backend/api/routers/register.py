import api.chatgpt
from api import globals as g
from api.database import get_async_session_context, get_user_db_context
from api.exceptions import InvalidParamsException
from api.models import User
from api.routers.system import check_users
from api.schema import UserCreate
from api.users import (current_active_user, get_by_username,
                       get_user_manager_context)
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/register", tags=["register"])
async def register_user(user:UserCreate):   
    check_result = await get_by_username(username=user.username)
    if check_result:
        raise InvalidParamsException("errors.userAlreadyExist")   
    try: 
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:              
                    user = await user_manager.create(
                        UserCreate(
                            **user.dict(),
                        )
                    )
                    return user
    except Exception as e:
        logger.error(e)
        return None
