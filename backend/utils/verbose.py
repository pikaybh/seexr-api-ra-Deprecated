import functools

def print_return(func):
    """함수의 반환 값을 출력하는 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"🔹 {func.__name__}: {result}")
        return result
    return wrapper

__all__ = ["print_return"]