from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import authenticate_user
from app.core.security import create_access_token
from app.api.deps import get_db
from app.core.logger import logger

router = APIRouter()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    logger.info("Login attempt for username=%s", form_data.username)

    try:
        user = authenticate_user(db, form_data.username, form_data.password)

        if not user:
            logger.warning(
                "Authentication failed for username=%s",
                form_data.username
            )
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.username})

        logger.info(
            "Authentication successful for username=%s",
            user.username
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            "Unexpected error during login for username=%s : %s",
            form_data.username,
            str(e),
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal server error")
