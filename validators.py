from typing import Any, Dict, List


def is_valid_email(email: str) -> bool:
    """
    Validate whether the provided email address is in the correct format.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_age(age: Any) -> bool:
    """
    Check if the provided age is a valid non-negative integer.

    Args:
        age (Any): The age to check.

    Returns:
        bool: True if valid, False otherwise.
    """
    if isinstance(age, int) and age >= 0:
        return True
    return False


def validate_user_data(user_data: Dict[str, Any]) -> List[str]:
    """
    Validate user data ensuring all fields meet specified criteria.

    Args:
        user_data (Dict[str, Any]): A dictionary containing user data.

    Returns:
        List[str]: A list of error messages or an empty list if valid.
    """
    errors = []
    if 'email' not in user_data or not is_valid_email(user_data['email']):
        errors.append('Invalid email address.')
    if 'age' in user_data and not is_valid_age(user_data['age']):
        errors.append('Age must be a non-negative integer.')
    return errors
