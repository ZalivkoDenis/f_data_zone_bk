from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from core.mixins import UserRelationMixin, ProfileRelationMixin, UlEmailPasswordMixin


if TYPE_CHECKING:
    pass


class Profile(UserRelationMixin, Base):
    """
    Модель профиля пользователя.
    Используется связь между пользователем и профилем один-к-одному.

    Аттрибуты, устанавливаемые UserRelationMixin - связь с User
        user_id
        user

    """

    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    middle_name: Mapped[str | None] = mapped_column(String(40))

    b24profile: Mapped[B24Profile] = relationship(back_populates="profile")
    email_svc_profiles: Mapped[list[EmailServiceProfile]] = relationship(
        back_populates="profile"
    )


class EmailServiceProfile(ProfileRelationMixin, UlEmailPasswordMixin, Base):
    """
    Обслуживаемые профили почтовых сервисов
    Модель внешнего профиля для текущего пользователя

    Аттрибуты, устанавливаемые ProfileRelationMixin - связь с Profile
        profile_id
        profile

    Аттрибуты, устанавливаемые UlEmailPasswordMixin
        user_email
        password
        (X) password_hash - не используется

    """

    __tablename__ = "email_svc_profiles"

    _profile_id_unique = False  # one-to-many
    _profile_back_populates = "email_svc_profiles"

    imap_server: Mapped[str] = mapped_column(String(64), nullable=False)


class B24Profile(ProfileRelationMixin, UlEmailPasswordMixin, Base):
    """
    Корпоративный Битрикс24: ferico.bitrix24.by (one-to-one)
    Модель внешнего профиля для текущего пользователя

    Аттрибуты, устанавливаемые ProfileRelationMixin - связь с Profile
        profile_id
        profile

    Аттрибуты, устанавливаемые UlEmailPasswordMixin
        user_email
        password
        (X) password_hash - не используется

    """

    _profile_id_unique = True  # one-to_one
    _profile_back_populates = "b24profile"
