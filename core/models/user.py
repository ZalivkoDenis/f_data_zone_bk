from __future__ import annotations
from typing import TYPE_CHECKING

from . import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .profile import Profile


class User(Base):

    username: Mapped[str] = mapped_column(String(32), unique=True)

    profile: Mapped[Profile] = relationship(back_populates="user")
