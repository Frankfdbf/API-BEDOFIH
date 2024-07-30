# Native imports
from collections.abc import Callable

# Third party imports
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Custom imports
from api_bedofih_2017.database import models, repository
from api_bedofih_2017.database.connection import session


def get_repository(
    model: type[models.Base],
) -> Callable[[AsyncSession], repository.DatabaseRepository]:
    def func(session: AsyncSession = Depends(session.get_db_session)):
        return repository.DatabaseRepository(model, session)

    return func