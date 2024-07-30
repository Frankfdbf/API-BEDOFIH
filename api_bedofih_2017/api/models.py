# Native imports
import datetime as dt

# Third party imports
from pydantic import BaseModel

# Custom imports


class ErrorList(BaseModel):
    """ List of errors when posting bulk entries """
    index: int
    error: str
    

class Event(BaseModel):
    """ Events model """
    event_id: int # e_seq
    isin: str # e_isin
    event_type: str | None # e_act_m_state
    event_datetime: dt.datetime # e_dt_me
    next_update_date: dt.date # e_d_upd
    instrument_state: str # e_value_state
    code_trading_group: str # e_cd_gc
    delayed_opening_time: dt.time | None # e_t_op
    halt_origin: str | None # e_reservation
    
    class Config:
        orm_mode = True
        from_attributes=True


class Trade(BaseModel):
    """ Trade model """
    trade_id: int # t_id_tr
    trade_number: int # t_tr_nb
    isin: str # t_isin
    price: float # t_price
    quantity: int # t_q_exchanged
    capital: float # t_capital
    dtm_neg: dt.datetime # t_dtm_neg
    aggressive: str | None # t_agg
    application: str # t_app
    
    id_fd_buy_order: int # id_fd_buy_order
    id_fd_sell_order: int # id_fd_sell_order
    seq_nb_buy_order: int # t_b_sq_nb
    seq_nb_sell_order: int # t_s_sq_nb
    
    buyer_type: str # t_b_type
    seller_type: str # t_s_type
    buyer_account: str # t_b_account
    seller_account: str # t_s_account
    d_buy_order_entry: dt.date # t_d_b_en
    d_sell_order_entry: dt.date # t_d_s_en
    
    class Config:
        orm_mode = True
        from_attributes=True
        
        
class Order(BaseModel):
    """ Order model."""
    message_id: int # concat fundamental id and characteristic id, cast as int
    fd_id: int # o_id_fd
    cha_id: int # o_cha_id
    isin: str # o_isin
    sequence_number: int # o_sq_nb
    next_sequence_number: int # o_sq_nbm
    
    state: str # o_state
    is_buy: bool # o_bs
    type: str # o_type
    execution: str | None # o_execution
    validity: str # o_validity
    application: int # o_app
    origin: str | None # o_origin
    account: int # o_account
    nb_transactions: int # o_nb_tr
    hft_classification: str # o_member
    
    price: float # o_price
    stop_price: float # o_price_stop
    
    initial_qty: int # o_q_ini
    minimum_qty: int # o_q_min
    display_qty: int # o_q_dis
    negotiated_qty: int # o_q_neg
    remaining_qty: int # o_q_rem
    
    dtm_validity: dt.datetime # o_dtm_va
    dtm_book_entry: dt.datetime # o_dtm_be
    dtm_book_release: dt.datetime # o_dtm_br
    dtm_modification: dt.datetime | None # o_dtm_mo
    dtm_priority: dt.datetime | None # o_dtm_p
    dt_expiration: dt.datetime # o_dt_expiration
    dt_update: dt.datetime # o_dt_upd    
    
    class Config:
        orm_mode = True
        from_attributes=True
