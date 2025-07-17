from typing import Optional, TypeVar, Type

from django.db import (
    DatabaseError,
    transaction,
    IntegrityError,
    OperationalError
)
from django.core.exceptions import ValidationError
from django.db.models import QuerySet, Model

Model_ = TypeVar("Model_", bound=Model)


class BaseRepository:
    def __init__(self, model: Type[Model_]) -> None:
        self.model = model

    def get_by_id(self, id_: int) -> Optional[Model_]:

        if not isinstance(id_, int) or id_ <= 0:
            raise ValueError(f"ID must be a positive integer, got: {id_}")

        try:
            obj = self.model.objects.get(id=id_)
            return obj
        except self.model.DoesNotExist:
            return None
        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} with ID {id_}") from e

    def get_all(self) -> QuerySet:

        try:
            queryset = self.model.objects.all()
            return queryset
        except DatabaseError as e:
            raise OperationalError(f"Failed to retrieve {self.model.__name__} objects") from e

    @transaction.atomic
    def create(self, **kwargs) -> Model_:

        try:
            obj = self.model.objects.create(**kwargs)
            return obj
        except ValidationError as e:
            raise ValidationError(f"Validation failed for {self.model.__name__}") from e
        except IntegrityError as e:
            raise IntegrityError(f"Integrity constraint violation for {self.model.__name__}") from e
        except DatabaseError as e:
            raise OperationalError(f"Failed to create {self.model.__name__}") from e

    @transaction.atomic
    def update(self, id_: int, **kwargs) -> Model_:

        try:
            obj = self.get_by_id(id_)

            if obj is None:
                raise ValueError(f"{self.model.__name__} with ID {id_} not found")

            for field, value in kwargs.items():
                setattr(obj, field, value)

            obj.save()

            return obj
        except ValidationError as e:
            raise ValidationError(f"Validation failed for {self.model.__name__}") from e
        except IntegrityError as e:
            raise IntegrityError(f"Integrity constraint violation for {self.model.__name__}") from e
        except DatabaseError as e:
            raise OperationalError(f"Failed to update {self.model.__name__}") from e

    @transaction.atomic
    def delete(self, id_: int) -> None:

        try:
            obj = self.get_by_id(id_)

            if obj is None:
                raise ValueError(f"{self.model.__name__} with ID {id_} not found")

            obj.delete()
        except DatabaseError as e:
            raise OperationalError(f"Failed to delete {self.model.__name__}") from e

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.model.__name__})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model.__name__})"
