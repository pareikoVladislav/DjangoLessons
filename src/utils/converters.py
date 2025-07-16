from src.choices.base import Genre, Language


def validate_and_convert_choices(data: dict) -> dict:
    errors = {}

    if 'genre' in data and isinstance(data['genre'], str):
        genre_attr = Genre.get_attr_by_value(data['genre'])
        if genre_attr is None:
            errors['genre'] = {
                'message': f"Invalid genre value: '{data['genre']}'",
                'available_values': Genre.get_available_values()
            }
        else:
            data['genre'] = genre_attr

    if 'language' in data and isinstance(data['language'], str):
        language_attr = Language.get_attr_by_value(data['language'])
        if language_attr is None:
            errors['language'] = {
                'message': f"Invalid language value: '{data['language']}'",
                'available_values': Language.get_available_values()
            }
        else:
            data['language'] = language_attr

    return errors
