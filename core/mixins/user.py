from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import User


# noinspection PyMethodParameters
class UserRelationMixin:
    """
    Миксин для связи между пользователями и профилями.
    Использует 2 поля:
        - user_id - идентификатор пользователя;
        - user - профиль пользователя.
    Эти поля подмешиваются в модели, которые должны быть связаны с пользователями.
    Связь может быть как один-к-одному, так и один-ко-многим.
    """

    _user_id_nullable: bool = False
    _user_id_unique: bool = False
    _user_back_populates: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id"),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped[User]:
        return relationship(
            "User",
            back_populates=cls._user_back_populates,
        )
