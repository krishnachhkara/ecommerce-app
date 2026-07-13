from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Text,Integer,DateTime,func,ForeignKey
from app.db.base import Base
from app.models.user import User
from datetime import datetime


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),index=True,nullable=False)
    hashed_token:Mapped[str] = mapped_column(Text,nullable=False,unique=True,index=True)
    expires_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())

    #relation ship
    user:Mapped["User"] = relationship(back_populates="refresh_tokens")