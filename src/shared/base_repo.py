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
            raise self.model.DoesNotExist(f"Object with ID {id_} not found")
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
        many_to_many_fields = {}

        try:
            for field in self.model._meta.many_to_many:
                if field.name in kwargs:
                    many_to_many_fields[field.name] = kwargs.pop(field.name)

            obj = self.model.objects.create(**kwargs)

            for field_name, value in many_to_many_fields.items():
                field = getattr(obj, field_name)

                if value:
                    field.set(value)

            return obj
        except ValidationError as e:
            raise ValidationError(f"Validation failed for {self.model.__name__}") from e
        except IntegrityError as e:
            raise IntegrityError(f"Integrity constraint violation for {self.model.__name__}") from e
        except DatabaseError as e:
            raise OperationalError(f"Failed to create {self.model.__name__}") from e

    @transaction.atomic
    def update(self, book, **kwargs) -> Model_:

        try:

            for field, value in kwargs.items():
                setattr(book, field, value)

            book.save()

            return book
        except ValidationError as e:
            raise ValidationError(f"Validation failed for {self.model.__name__}") from e
        except IntegrityError as e:
            raise IntegrityError(f"Integrity constraint violation for {self.model.__name__}") from e
        except DatabaseError as e:
            raise OperationalError(f"Failed to update {self.model.__name__}") from e

    def delete(self, book) -> None:
        try:
            book.delete()
        except DatabaseError as e:
            raise OperationalError(f"Failed to delete {self.model.__name__}") from e

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.model.__name__})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model.__name__})"
