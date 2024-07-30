# Native imports
import datetime as dt
from typing import Optional

# Third party imports
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Custom imports


class Base(DeclarativeBase):
    """Base database model."""
    pass


class Event(Base):
    """ Event database model """
    __tablename__ = "event"
    
    event_id: Mapped[int] = mapped_column(primary_key=True) # e_seq
    isin: Mapped[str] # e_isin
    event_type: Mapped[Optional[str]] # e_act_m_state
    event_datetime: Mapped[dt.datetime] # e_dt_me
    next_update_date: Mapped[dt.date] # e_d_upd
    instrument_state: Mapped[str] # e_value_state
    code_trading_group: Mapped[str] # e_cd_gc
    delayed_opening_time: Mapped[Optional[dt.time]] # e_t_op
    halt_origin: Mapped[Optional[str]] # e_reservation
    

class Trade(Base):
    """ Trade database model """
    __tablename__ = "trade"
    
    trade_id: Mapped[int] = mapped_column(primary_key=True) # t_id_tr
    trade_number: Mapped[int] # t_tr_nb
    isin: Mapped[str] # t_isin
    price: Mapped[float] # t_price
    quantity: Mapped[int] # t_q_exchanged
    capital: Mapped[float] # t_capital
    dtm_neg: Mapped[dt.datetime] = Column(DateTime(timezone=False)) # t_dtm_neg
    aggressive: Mapped[Optional[str]] = mapped_column(nullable=True) # t_agg
    application: Mapped[str] # t_app
    
    id_fd_buy_order: Mapped[int] # id_fd_buy_order
    id_fd_sell_order: Mapped[int] # id_fd_sell_order
    seq_nb_buy_order: Mapped[int] # t_b_sq_nb
    seq_nb_sell_order: Mapped[int] # t_s_sq_nb
    
    buyer_type: Mapped[str] # t_b_type
    seller_type: Mapped[str] # t_s_type
    buyer_account: Mapped[str] # t_b_account
    seller_account: Mapped[str] # t_s_account
    d_buy_order_entry: Mapped[dt.date] # t_d_b_en
    d_sell_order_entry: Mapped[dt.date] # t_d_s_en
    
    
class Order(Base):
    """ Order database model """
    __tablename__ = "order"

    message_id: Mapped[int] = mapped_column(primary_key=True) # concat fundamental id and characteristic id, cast as int
    fd_id: Mapped[int] # o_id_fd
    cha_id: Mapped[int] # o_cha_id
    isin: Mapped[str] # o_isin
    sequence_number: Mapped[int] # o_sq_nb
    next_sequence_number: Mapped[int] # o_sq_nbm
    
    state: Mapped[str] # o_state
    is_buy: Mapped[bool] # o_bs
    type: Mapped[str] # o_type
    execution: Mapped[Optional[str]] # o_execution
    validity: Mapped[str] # o_validity
    application: Mapped[int] # o_app
    origin: Mapped[Optional[str]] # o_origin
    account: Mapped[int] # o_account
    nb_transactions: Mapped[int] # o_nb_tr
    hft_classification: Mapped[str] # o_member
    
    price: Mapped[float] # o_price
    stop_price: Mapped[float] # o_price_stop
    
    initial_qty: Mapped[int] # o_q_ini
    minimum_qty: Mapped[int] # o_q_min
    display_qty: Mapped[int] # o_q_dis
    negotiated_qty: Mapped[int] # o_q_neg
    remaining_qty: Mapped[int] # o_q_rem
    
    dtm_validity: Mapped[dt.datetime] = Column(DateTime(timezone=False)) # o_dtm_va
    dtm_book_entry: Mapped[dt.datetime] = Column(DateTime(timezone=False)) # o_dtm_be
    dtm_book_release: Mapped[dt.datetime] = Column(DateTime(timezone=False)) # o_dtm_br
    dtm_modification: Mapped[Optional[dt.datetime]] = Column(DateTime(timezone=False)) # o_dtm_mo
    dtm_priority: Mapped[Optional[dt.datetime]] = Column(DateTime(timezone=False)) # o_dtm_p
    dt_expiration: Mapped[dt.datetime] = Column(DateTime(timezone=False)) # o_dt_expiration
    dt_update: Mapped[dt.datetime] = Column(DateTime(timezone=False)) # o_dt_upd    