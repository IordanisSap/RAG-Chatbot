import os

def validate_path(base, input):
    user_path = os.path.normpath(os.path.join(base, input))
    if not os.path.commonpath([base, user_path]) == base:
        raise ValueError("Attempted directory traversal detected!")
    return user_path