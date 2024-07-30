# Native imports
from pathlib import Path
import datetime as dt
import requests

# Third party imports
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select, create_engine, and_, func
from sqlalchemy.sql import functions
import pandas as pd
pd.set_option('display.max_columns', None)

# Custom imports
# from api_bedofih_2017.database.connection.session import get_db_session
from api_bedofih_2017.database.models import Trade, Base, Event, Order
from api_bedofih_2017.config import settings


"""
# session: Session = get_db_session()
engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(engine)
SessionBuilder = sessionmaker(engine)
with SessionBuilder.begin() as session: 
    response = session.execute(
        select(Trade).where(and_(
            Trade.dtm_neg >= dt.datetime(2017, 12, 13, 9),
            Trade.dtm_neg <= dt.datetime(2017, 12, 13, 10)
        ))
        #     # Trade.dtm_neg == dt.datetime(2017, 12, 13, 9)
        #     Trade.trade_id == 2752657754
        # )
    ).scalars().all()
    for trade in response:
        print(trade.aggressive)
    
    
path_dir = Path("/Users/australien/Documents/PERSO/Studies/IESEG/Master 2/Data/trades/FR0000121014")
for file in path_dir.iterdir():
    # For each file:
    
    with SessionBuilder.begin() as session:
        print(file.name)
        df = pd.read_parquet(file)

        for row in df.to_dict("records"):
            # For each row in the dataframe
            
            trade = Trade(
                trade_id = row["t_id_tr"],
                trade_number = row["t_tr_nb"],
                isin = "FR0000121014",
                price = row["t_price"],
                quantity = row["t_q_exchanged"],
                capital = row["t_capital"],
                dtm_neg = row["t_dtm_neg"],
                aggressive = row["t_agg"] if not pd.isna(row["t_agg"]) else None,
                application = row["t_app"],
                
                id_fd_buy_order = row["t_id_b_fd"],
                id_fd_sell_order = row["t_id_s_fd"],
                seq_nb_buy_order = row["t_b_sq_nb"],
                seq_nb_sell_order = row["t_s_sq_nb"],
                
                buyer_type = row["t_b_type"],
                seller_type = row["t_s_type"],
                buyer_account = row["t_b_account"],
                seller_account = row["t_s_account"],
                d_buy_order_entry = row["t_d_b_en"],
                d_sell_order_entry = row["t_d_s_en"],
            )
            session.add(trade)
    #         break
    # break


      
# isin
# capital        t_capital               float64      x
# price        t_price                 float64        x
# d_buyer_entry        t_d_b_en         datetime64[ns]    x
# d_seller_entry        t_d_s_en         datetime64[ns]   x
# id_fd_buy_order        t_id_b_fd                 int64      x
# id_fd_sell_order        t_id_s_fd                 int64     x
# application        t_app                  category          x
# seq_nb_buy_order        t_b_sq_nb                 int32     x
# seq_nb_sell_order    t_s_sq_nb                 int32        x
# buyer_account        t_b_account            category        x
# seller_account        t_s_account            category       x
# quantity        t_q_exchanged             int32             x
# trade_number        t_tr_nb                   int32         x
# trade_id        t_id_tr                   int64             x
# aggressive        t_agg                  category           x
# buyer_type        t_b_type               category           x 
# seller_type        t_s_type               category          x
# dtm_neg        t_dtm_neg        datetime64[ns]              x

"""

engine = create_engine(settings.DATABASE_URL)
SessionBuilder = sessionmaker(engine)

# path_event = Path(r"/Users/australien/Documents/IESEG/Master 2/Data/events")

# for file in path_event.iterdir():
#     # For each file:
    
#     with SessionBuilder.begin() as session:
#         print(file.name)
#         df = pd.read_parquet(file)
        
#         for row in df.to_dict("records"):
        
#             event = Event(
#                 event_id = row["e_seq"],
#                 isin = row["e_isin"],
#                 event_type = row["e_act_m_state"] if not pd.isna(row["e_act_m_state"]) else None,
#                 event_datetime = row["e_dt_me"],
#                 next_update_date = row["e_d_upd"],
#                 instrument_state = row["e_value_state"],
#                 code_trading_group = row["e_cd_gc"],
#                 delayed_opening_time = row["e_t_op"],
#                 halt_origin = row["e_reservation"] if not pd.isna(row["e_reservation"]) else None,
#             )
#             session.add(event)

    
path_dir = Path("/Users/australien/Documents/IESEG/Master 2/Data/orders/FR0000121014")
for file in path_dir.iterdir():
    # For each file:
    
    #with SessionBuilder.begin() as session:
    print(file.name)
    df = pd.read_parquet(file)
    
    data = []

    for row in df.to_dict("records"):
        # For each row in the dataframe
        
        payload = {
            "message_id": int(str(row["o_id_fd"]) + str(row["o_cha_id"])), # concat fundamental id and characteristic id, cast as int
            "fd_id": row["o_id_fd"],
            "cha_id": row["o_cha_id"],
            "isin": "FR0000121014",
            "sequence_number": row["o_sq_nb"],
            "next_sequence_number": row["o_sq_nbm"],
            
            "state": row["o_state"],
            "is_buy": True if row["o_bs"] == "B" else False if row["o_bs"] == "S" else None,
            "type": row["o_type"],
            "execution": row["o_execution"] if not pd.isna(row["o_execution"]) else None,
            "validity": row["o_validity"],
            "application": row["o_app"],
            "origin": row["o_origin"] if not pd.isna(row["o_origin"]) else None,
            "account": row["o_account"],
            "nb_transactions": row["o_nb_tr"],
            "hft_classification": row["o_member"],
            
            "price": row["o_price"],
            "stop_price": row["o_price_stop"],
            
            "initial_qty": row["o_q_ini"],
            "minimum_qty": row["o_q_min"],
            "display_qty": row["o_q_dis"],
            "negotiated_qty": row["o_q_neg"],
            "remaining_qty": row["o_q_rem"],
            
            "dtm_validity": row["o_dtm_va"].isoformat(timespec="microseconds"),
            "dtm_book_entry": row["o_dtm_be"].isoformat(timespec="microseconds"),
            "dtm_book_release": row["o_dtm_br"].isoformat(timespec="microseconds"),
            "dtm_modification": row["o_dtm_mo"].isoformat(timespec="microseconds") if not pd.isna(row["o_dtm_mo"]) else None,
            "dtm_priority": row["o_dtm_p"].isoformat(timespec="microseconds") if not pd.isna(row["o_dtm_p"]) else None,
            "dt_expiration": row["o_dt_expiration"].isoformat(timespec="seconds"),
            "dt_update": row["o_dt_upd"].isoformat(timespec="seconds"),
        }
        data.append(payload)
        
    response = requests.post("http://0.0.0.0:8000/api/orders-bulk", json=data)
    # if response.status_code not in (201, 401, 500):
    #     print(response.status_code)
    #     print(response.text)
    #     print(payload)
    # print(response.status_code)
    print(response.json()["errors"])
    
    
    # break
        #print(x)
        #break
    #break
        
        # order = Order(
        #     message_id = int(str(row["o_id_fd"]) + str(row["o_cha_id"])), # concat fundamental id and characteristic id, cast as int
        #     fd_id = row["o_id_fd"],
        #     cha_id = row["o_cha_id"],
        #     isin = "FR0000121014",
        #     sequence_number = row["o_sq_nb"],
        #     next_sequence_number = row["o_sq_nbm"],
            
        #     state = row["o_state"],
        #     is_buy = True if row["o_bs"] == "B" else False if row["o_bs"] == "S" else None,
        #     type = row["o_type"],
        #     execution = row["o_execution"] if not pd.isna(row["o_execution"]) else None,
        #     validity = row["o_validity"],
        #     application = row["o_app"],
        #     origin = row["o_origin"] if not pd.isna(row["o_origin"]) else None,
        #     account = row["o_account"],
        #     nb_transactions = row["o_nb_tr"],
        #     hft_classification = row["o_member"],
            
        #     price = row["o_price"],
        #     stop_price = row["o_price_stop"],
            
        #     initial_qty = row["o_q_ini"],
        #     minimum_qty = row["o_q_min"],
        #     display_qty = row["o_q_dis"],
        #     negotiated_qty = row["o_q_neg"],
        #     remaining_qty = row["o_q_rem"],
            
        #     dtm_validity = row["o_dtm_va"],
        #     dtm_book_entry = row["o_dtm_be"],
        #     dtm_book_release = row["o_dtm_br"],
        #     dtm_modification = row["o_dtm_mo"],
        #     dtm_priority = row["o_dtm_p"] if not pd.isna(row["o_dtm_p"]) else None,
        #     dt_expiration = row["o_dt_expiration"],
        #     dt_update = row["o_dt_upd"],
        # )
        # #session.add(order)
        # print(order.__dict__)
        # break
    
    # break (stop after one file)