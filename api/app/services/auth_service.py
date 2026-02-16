from passlib.context import CryptContext
from app.repositories.auth_repository import get_user_by_username
from app.core.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db, username: str, password: str):
    logger.info("Authenticating user username=%s", username)

    try:
        user = get_user_by_username(db, username)

        if not user:
            logger.warning("User not found username=%s", username)
            return None

        if not pwd_context.verify(password, user.hashed_password):
            logger.warning("Invalid password for username=%s", username)
            return None

        logger.info("User authenticated successfully username=%s", username)
        return user

    except Exception as e:
        logger.error(
            "Authentication error for username=%s : %s",
            username,
            str(e),
            exc_info=True
        )
        return None
