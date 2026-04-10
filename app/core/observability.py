
import time

def track_execution(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        duration = time.time() - start
        print(f"[METRIC] execution_time={duration}")
        return result
    return wrapper
