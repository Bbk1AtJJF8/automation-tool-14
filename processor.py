import typing

class Validator:
    def __init__(self, check_fn: typing.Callable[[typing.Any], bool], error_msg: str):
        self.check_fn = check_fn
        self.error_msg = error_msg

    def __and__(self, other: 'Validator') -> 'Validator':
        return Validator(
            lambda x: self.check_fn(x) and other.check_fn(x),
            f'{self.error_msg} and {other.error_msg}'
        )

    def __call__(self, val: typing.Any) -> bool:
        try:
            return self.check_fn(val)
        except (KeyError, TypeError