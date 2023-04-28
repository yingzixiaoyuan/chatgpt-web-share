from api.database import get_async_session_context, get_user_db_context
from api.schema import UserCreate
from api.users import get_user_manager_context

from utils.logger import get_logger

logger = get_logger(__name__)


async def create_user(username, nickname: str, email: str, password: str, is_superuser: bool = False, **kwargs):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            username=username, nickname=nickname,
                            email=email, password=password, is_superuser=is_superuser,is_active=True,
                            **kwargs
                        )
                    )
                    logger.info(f"User created: {user}")
                    return user
    except Exception as e:
        logger.info(f"Create User {username} Error: {e}")
        return None

async def reset_user_count():
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as db:
                async with get_user_manager_context(db) as user_manager:
                    await user_manager.reset_user_count()
                    await user_manager.reset_test_count()
                    logger.info(f"Reset User count")
                    return True
    except Exception as e:
        logger.info(f"Reset User count Error: {e}")
        return None
