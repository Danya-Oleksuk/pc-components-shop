from collections import namedtuple
from typing import Any, TypeVar

from django.db import models

ModelType = TypeVar("ModelType", bound=models.Model)

FieldDiff = namedtuple("FieldDiff", ["field_name", "old_value", "new_value"])


def model_update(
    *,
    model: ModelType,
    **fields: Any,
) -> tuple[ModelType, list[FieldDiff]]:
    available_fields = {f.name for f in model._meta.get_fields()}
    updates: list[FieldDiff] = []
    for field, new_value in fields.items():
        if field not in available_fields:
            model_name = model.__class__.__name__
            raise ValueError(f"Field {field} not found in model {model_name}")

        old_value = getattr(model, field)
        if old_value == new_value:
            continue

        updates.append(FieldDiff(field, old_value, new_value))
        setattr(model, field, new_value)

    if updates:
        model.full_clean()
        model.save(update_fields=fields.keys())
    return model, updates
