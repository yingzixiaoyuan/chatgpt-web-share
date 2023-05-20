import asyncio

import api.globals as g
from api.database import get_async_session_context, get_user_db_context
from api.exceptions import InvalidParamsException
from api.schema import UserCreate, UserRead
from api.users import get_by_username, get_user_manager_context
from fastapi import APIRouter
from starlette.requests import Request
from utils.logger import get_logger

config = g.config

logger = get_logger(__name__)

router = APIRouter()

# @router.get("/user/me", response_model=UserRead, tags=["user"])
# async def get_me(user: User = Depends(current_active_user)):
#     return UserRead.from_orm(user)


@router.post("/register", tags=["register"],response_model=UserRead)
async def register_user(request: Request,user:UserCreate):   
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.create(user, safe=True, request=request)
                return UserRead.from_orm(user)

    # check_result = await get_by_username(username=user.username)
    # if check_result:
    #     raise InvalidParamsException("errors.userAlreadyExist")   
    # try: 
    #     async with get_async_session_context() as session:
    #         async with get_user_db_context(session) as user_db:
    #             async with get_user_manager_context(user_db) as user_manager:   
    #                 user.available_ask_count = 30         
    #                 result = await user_manager.create(
    #                     UserCreate(
    #                         **user.dict(),
    #                     )
    #                 )
    #                 return result
    # except Exception as e:
    #     logger.error(e)
    #     return None
