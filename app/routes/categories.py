import concurrent

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app import models
from app.services import search_google
from app.logger.logger import logger

router = APIRouter(prefix="/categories", tags=["Category"])


@router.post("/start")
def read_categories(
        cmd: models.CategoryParse
):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        try:
            executor.map(search_google, cmd.search_keys)
        except KeyboardInterrupt:
            logger.info("Finishing with KeyboardInterrupt")
        except Exception as e:
            logger.error("An error occurred", e)

    return Response(status_code=status.HTTP_200_OK)
