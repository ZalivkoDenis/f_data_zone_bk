from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from core.mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    """
    Модель профиля пользователя.
    Используется связь между пользователем и профилем один-к-одному.
    """

    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None]
