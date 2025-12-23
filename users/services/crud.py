from typing import Any

from django.db import transaction
from django_rest_passwordreset.views import ValidationError

from pc_components_shop.services.crud import model_update
from users.models.users import User


@transaction.atomic
def user_create(
    *,
    email: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
) -> User:
    if not email:
        raise ValidationError("User must have an email")

    user = User.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()
    user.refresh_from_db()
    return user


def user_update(
    *,
    user: User,
    **fields: Any,
) -> User:
    password: str = fields.pop("password", "")
    user, updates = model_update(model=user, **fields)

    if password:
        user.set_password(password)
        user.save(update_fields=["password"])

    return user


def user_delete(*, user: User, by_user: User | None = None) -> None:
    user.delete()
