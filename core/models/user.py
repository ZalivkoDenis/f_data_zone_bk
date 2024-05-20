from __future__ import annotations
from typing import TYPE_CHECKING

from . import Base

from core.mixins import UlEmailPasswordMixin

from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .profile import Profile


class User(UlEmailPasswordMixin, Base):
    """
    User model

    Аттрибуты, устанавливаемые UlEmailPasswordMixin:
        user_email
        (X) password - не используется, т.к. используется авторизация по JWT-токену
        password_hash

    """

    _user_email_as_login = True

    active: Mapped[bool] = mapped_column(default=False, server_default=None)
    superuser: Mapped[bool] = mapped_column(default=False, server_default=None)

    # profile
    profile: Mapped[Profile] = relationship(back_populates="user")
