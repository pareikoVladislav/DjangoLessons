from enum import Enum


class Gender(str, Enum):
    male = "Male"
    female = "Female"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class Role(str, Enum):
    admin = "Admin"
    employee = "Employee"
    reader = "Reader"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class Language(str, Enum):
    en = "English"
    be = "Belarusian"
    ru = "Russian"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]

    @classmethod
    def get_attr_by_value(cls, value: str):
        for attr in cls:
            if attr.value == value:
                return attr.name

    @classmethod
    def get_available_values(cls):
        return [attr.value for attr in cls]


class Genre(str, Enum):
    N_A = 'N/A'
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    SCIENCE_FICTION = 'Science Fiction'
    FANTASY = 'Fantasy'
    MYSTERY = 'Mystery'
    BIOGRAPHY = 'Biography'

    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls]

    @classmethod
    def get_attr_by_value(cls, value: str):
        for attr in cls:
            if attr.value == value:
                return attr.name

    @classmethod
    def get_available_values(cls):
        return [attr.value for attr in cls]
