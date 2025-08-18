from src.choices.base import Genre, Language


def validate_and_convert_choices(data: dict) -> dict:
    errors = {}

    def process_choice(field_name, enum_cls):
        raw = data.get(field_name)
        if raw is None or not isinstance(raw, str):
            return

        try:
            if raw in enum_cls.__members__:
                return
        except Exception:
            pass

        if hasattr(enum_cls, "get_available_values") and raw in enum_cls.get_available_values():
            if hasattr(enum_cls, "get_attr_by_value"):
                key = enum_cls.get_attr_by_value(raw)
                if key:
                    data[field_name] = key
                    return

        errors[field_name] = {
            'message': f"Invalid {field_name} value: '{raw}'",
            'available_values': getattr(enum_cls, "get_available_values", lambda: [])(),
        }

    process_choice('genre', Genre)
    process_choice('language', Language)

    return errors



def normalize_choice(field, enum_cls, data):
    raw = data.get(field)
    if raw is None:
        return
    if hasattr(enum_cls, "get_available_values") and raw in enum_cls.get_available_values():
        if hasattr(enum_cls, "get_attr_by_value"):
            key = enum_cls.get_attr_by_value(raw)
            if key:
                data[field] = key
