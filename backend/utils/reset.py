
from api.database import get_async_session_context, get_user_db_context
from api.users import get_user_manager_context

from utils.logger import get_logger

logger = get_logger(__name__)

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
