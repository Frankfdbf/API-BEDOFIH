# Native imports
import datetime as dt
from typing import Annotated

# Third party imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_, or_
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

# Custom imports
from api_bedofih_2017.api import models
from api_bedofih_2017.database import models as db_models
from api_bedofih_2017.database.connection.session import get_db_session
from api_bedofih_2017.database.repository import DatabaseRepository
from api_bedofih_2017.api.dependencies import get_repository


router = APIRouter()

# Dependencies

TradeRepository = Annotated[
    DatabaseRepository[db_models.Trade],
    Depends(get_repository(db_models.Trade))
]

OrderRepository = Annotated[
    DatabaseRepository[db_models.Order],
    Depends(get_repository(db_models.Order))
]

# TRADES
# ******

@router.post("/trades", status_code=status.HTTP_201_CREATED)
async def create_trade(
    data: models.Trade,
    repository: TradeRepository
) -> models.Trade:
    """
    Create an trade entry.
    """
    data_dict = data.model_dump()
    trade = await repository.create(data_dict)
    return models.Trade.model_validate(trade)


@router.get("/trades/{trade_id}", status_code=status.HTTP_200_OK)
async def get_trade(
    trade_id: int,
    repository: TradeRepository
) -> models.Trade:
    """ 
    Retrieve trade based on id.
    """
    trade = await repository.get(trade_id)
    
    if trade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade id does not exist",
        )
    return models.Trade.model_validate(trade)

# ORDERS
# ******

@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(
    data: models.Order,
    repository: OrderRepository
) -> models.Order:
    """
    Create a single order entry.
    """
    data_dict = data.model_dump()
    order = await repository.create(data_dict)
    return models.Order.model_validate(order)


@router.post("/orders-bulk", status_code=status.HTTP_201_CREATED)
async def create_orders(
    data: list[models.Order],
    repository: OrderRepository
) -> dict[str, list[models.Order] | list[models.ErrorList]]:
    """
    Create multiple order entries.
    """
    created_orders = []
    errors = []
    
    for index, order_data in enumerate(data):
        try:
            data_dict = order_data.model_dump()
            order = await repository.create(data_dict)
            created_order = models.Order.model_validate(order)
            created_orders.append(created_order)
        except ValidationError as e:
            await repository.session.rollback()
            error_message = f"Validation error: {e.errors()}"
            errors.append(models.ErrorList(index=index, error=error_message))
        except Exception as e:
            await repository.session.rollback()
            error_message = f"Error creating order: {str(e)}"
            errors.append(models.ErrorList(index=index, error=error_message))
    return {
        "created_orders": created_orders,
        "errors": errors,
    }


@router.get("/orders/{message_id}", status_code=status.HTTP_200_OK)
async def get_message(
    message_id: int,
    repository: OrderRepository
) -> models.Order:
    """ 
    Retrieve message based on id.
    """
    message = await repository.get(message_id)
    
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message id does not exist",
        )
    return models.Order.model_validate(message)
    

@router.get("/orders/{order_id}/trades",response_model=list[models.Trade], status_code=status.HTTP_200_OK)
async def get_trades_by_order_id(
    order_id: int,
    session: AsyncSession = Depends(get_db_session)
) -> list[models.Trade]:
    """
    Retrieve trades based on order id. 
    """
    result = await session.execute(
        select(db_models.Trade).where(
            or_(
                db_models.Trade.id_fd_buy_order == order_id,
                db_models.Trade.id_fd_sell_order == order_id,
            )
        )
    )
    trades = result.scalars().all()
    
    if not trades:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No trades found for this order_id",
        )
    #return models.Trade.model_validate(trades)
    return [models.Trade.model_validate(trade) for trade in trades]


# DATES
# *****


@router.get("/dates/{date}/trades",response_model=list[models.Trade], status_code=status.HTTP_200_OK)
async def get_trades_from_date(
    date: str,
    session: AsyncSession = Depends(get_db_session)
) -> list[models.Trade]:
    """
    Retrieve trades based on a trade date. 
    """
    result = await session.execute(
        select(db_models.Trade).where(and_(
            #db_models.Trade.dtm_neg < dt.date(2017, 1, 4),
            #db_models.Trade.dtm_neg > dt.date(2017, 1, 3)
            func.date(db_models.Trade.dtm_neg) == dt.date(2017, 1, 2)
        ))
    )
    trades = result.scalars().all()
    
    if not trades:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No trades found for this date",
        )
        
    return [models.Trade.model_validate(trade) for trade in trades]