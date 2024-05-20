from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from core.models import Profile


# noinspection PyMethodParameters
class ProfileRelationMixin:
    """
    Миксин для связи между профилями пользователя и профилями внешних систем.
    Использует 2 поля:
        - profile_id - идентификатор профиля;
        - profile - профиль привязанный к пользователю.
    Эти поля подмешиваются в модели, которые должны быть связаны с профилями пользователей.
    Связь может быть как один-к-одному, так и один-ко-многим.
    """

    _profile_id_nullable: bool = False
    _profile_id_unique: bool = False
    _profile_back_populates: str | None = None

    @declared_attr
    def profile_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("profiles.id"),
            unique=cls._profile_id_unique,
            nullable=cls._profile_id_nullable,
        )

    @declared_attr
    def profile(cls) -> Mapped[Profile]:
        return relationship(
            "Profile",
            back_populates=cls._profile_back_populates,
        )
