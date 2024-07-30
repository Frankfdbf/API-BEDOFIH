# Native imports
from typing import Generic, TypeVar

# Third party imports 
from sqlalchemy import select, BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession

# Custom imports
from api_bedofih_2017.database import models as db_models 


Model = TypeVar("Model", bound=db_models.Base)


class DatabaseRepository(Generic[Model]):
    """ Generic repository class to perform database queries. """
    
    
    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session
        
    
    async def get(self, id) -> Model | None: 
        return await self.session.get(self.model, id)
    
    
    async def create(self, data: dict) -> Model:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    
    async def filter(self, *expressions: BinaryExpression) -> list[Model]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(await self.session.scalars(query))