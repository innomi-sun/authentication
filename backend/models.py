from sqlalchemy import Column, Integer, BigInteger, String, DateTime, CHAR, JSON
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import datetime
from postgresql_db import db
    
class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }

class MST_USER(db.Model, DictMixIn):
    __tablename__ = "mst_user"
    user_id = Column(Integer, primary_key=True, index=True)
    resource_key = Column(String(20), nullable=False, index=True, comment='LOTO, RACING')
    user_name = Column(String(20), index=True, unique=True)
    password = Column(String(200), comment='Save register password when user_role is 0.')
    email = Column(String(200), index=True)
    role_cd = Column(Integer, index=True, nullable=False, comment='0:To be verified, 1:Verified and free membership, 2:Paid membership level 1, 3:Paid membership level 2')
    created_datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    update_datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class TRN_REFRESH_TOKEN(db.Model, DictMixIn):
    __tablename__ = "trn_refresh_token"
    token_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    resource_key = Column(String(20), nullable=False, index=True, comment='LOTO, RACING')
    remote_info = Column(JSON)
    # access_token = Column(String(2000), unique=True)
    refresh_token = Column(String(100), index=True, unique=True)
    expiration_datetime = Column(DateTime(timezone=True))    
    created_datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    update_datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())