from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, LargeBinary
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship


# noinspection PyMethodParameters
class UlEmailPasswordMixin:
    """
    Mixin for model, which has login as email and password.
    User login: email and password.

    Аттрибуты класса:
        user_email: str - email пользователя.
        password: bytes | None - пароль в зашифрованном виде.
        password_hash: bytes | None - хэш пароля.

    """

    _user_email_as_login: bool = True
    _user_email_unique: bool = _user_email_as_login

    # Имя пользователя системы - должен быть e-mail @ferico.by
    @declared_attr
    def user_email(cls) -> Mapped[str]:
        return mapped_column(
            String(128),
            nullable=False,
            unique=cls._user_email_unique,
        )

    # Пароль пользователя, зашифрованный c использованием RSA-ключей AES-алгоритмом
    @declared_attr
    def password(cls) -> Mapped[bytes | None]:
        return mapped_column(
            LargeBinary(512),
            nullable=True,
            default=None,
            server_default=None,
        )

    # hash-пароль пользователя
    @declared_attr
    def password_hash(cls) -> Mapped[bytes | None]:
        return mapped_column(
            LargeBinary(128),
            nullable=True,
            default=None,
            server_default=None,
        )
