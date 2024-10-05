def str_to_bool(value: str) -> bool:
    return value.lower() in ("yes", "true", "t", "1", "True")